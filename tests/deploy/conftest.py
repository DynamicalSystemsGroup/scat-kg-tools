"""Stand-ins for the programs the launcher calls (docker, colima, tailscale, openssl, pbcopy, caffeinate),
a fake server on a free port, and a runner for deploy/scat-chat.sh. No real docker, colima or tailscale runs."""

import http.server
import subprocess
import threading
from pathlib import Path

import pytest

REPO = Path(__file__).parents[2]
SCRIPT = REPO / "deploy" / "scat-chat.sh"

STANDINS = {
    "docker": r"""#!/bin/sh
echo "docker $*" >> "$CALLS"
S="$STUB_STATE"
case "$1" in
info) [ -f "$S/colima-up" ] ;;
image) [ -f "$S/image" ] ;;
pull) if [ -n "${STUB_PUBLISHED:-}" ]; then touch "$S/image"; else echo "manifest unknown" >&2; exit 1; fi ;;
build) if [ -n "${STUB_FAIL_BUILD:-}" ]; then echo "no network"; exit 1; fi; touch "$S/image" ;;
rm) rm -f "$S/container" ;;
run) if [ -n "${STUB_FAIL_RUN:-}" ]; then echo "port in use" >&2; exit 125; fi; touch "$S/container"; echo abc123 ;;
ps) [ -f "$S/container" ] && echo abc123 ;;
logs) echo "log line" ;;
esac
""",
    "colima": r"""#!/bin/sh
echo "colima $*" >> "$CALLS"
case "$1" in
status) [ -f "$STUB_STATE/colima-up" ] ;;
start) touch "$STUB_STATE/colima-up" ;;
esac
""",
    "tailscale": r"""#!/bin/sh
echo "tailscale $*" >> "$CALLS"
S="$STUB_STATE"
case "$1 $2" in
"status --json") cat "$S/ts-status.json" ;;
"funnel --bg") [ -n "${STUB_FUNNEL_BLOCKED:-}" ] || touch "$S/funnel-on" ;;
"funnel status") if [ -f "$S/funnel-on" ]; then echo "https://fake-mac.tail1234.ts.net (Funnel on):"; echo "|-- / proxy http://127.0.0.1:8765"; else echo "No serve config"; fi ;;
"funnel --https=443") rm -f "$S/funnel-on" ;;
"funnel reset") rm -f "$S/funnel-on" ;;
esac
""",
    "openssl": r"""#!/bin/sh
n=$(cat "$STUB_STATE/openssl-n" 2>/dev/null || echo 0)
n=$((n + 1))
echo $n > "$STUB_STATE/openssl-n"
printf '%064d\n' "$n"
""",
    "pbcopy": '#!/bin/sh\ncat > "$STUB_STATE/clip"\n',
    "pbpaste": '#!/bin/sh\ncat "$STUB_STATE/clip" 2>/dev/null\n',
    "caffeinate": "#!/bin/sh\n# caffeinate stand-in\nwhile :; do sleep 1; done\n",
    "open": '#!/bin/sh\necho "open $*" >> "$CALLS"\n',
}

STATUS_OK = """{
  "BackendState": "Running",
  "Self": {
    "ID": "nTEST123CNTRL",
    "HostName": "fake-mac",
    "DNSName": "fake-mac.tail1234.ts.net."
  },
  "CertDomains": [
    "fake-mac.tail1234.ts.net"
  ],
  "Peer": {
    "x": {"HostName": "other", "Addrs": [
      "1"
    ]}
  }
}
"""
STATUS_NO_HTTPS = STATUS_OK.replace(
    '"CertDomains": [\n    "fake-mac.tail1234.ts.net"\n  ]', '"CertDomains": null'
)
STATUS_STOPPED = '{"BackendState": "NeedsLogin"}\n'


class FakeServer:
    """Answers 401 to a POST to /mcp without the key in the key file, 200 with it."""

    def __init__(self, keyfile: Path):
        self.keyfile = keyfile
        outer = self

        class H(http.server.BaseHTTPRequestHandler):
            def do_POST(self):
                self.rfile.read(int(self.headers.get("Content-Length", 0)))
                key = ""
                for line in outer.keyfile.read_text().splitlines():
                    if line.startswith("SCAT_MCP_KEY="):
                        key = line.split("=", 1)[1]
                ok = self.headers.get("Authorization") == f"Bearer {key}" and key
                self.send_response(200 if ok and self.path == "/mcp" else 401)
                self.send_header("Content-Length", "0")
                self.end_headers()

            def log_message(self, *a):
                pass

        self.httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H)
        self.port = self.httpd.server_address[1]
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()

    def close(self):
        self.httpd.shutdown()
        self.httpd.server_close()


class Rig:
    def __init__(self, tmp: Path):
        self.tmp = tmp
        self.home = tmp / "home"
        self.home.mkdir()
        self.stub = tmp / "stub"
        self.stub.mkdir()
        self.bin = tmp / "bin"
        self.bin.mkdir()
        self.calls = tmp / "calls.log"
        self.calls.touch()
        for name, body in STANDINS.items():
            p = self.bin / name
            p.write_text(body)
            p.chmod(0o755)
        (self.stub / "ts-status.json").write_text(STATUS_OK)
        self.state = self.home / "Library" / "Application Support" / "SCAT Chat"
        self.keyfile = self.state / "key.env"
        self.state.mkdir(parents=True)
        self.server = FakeServer(self.keyfile)
        self.vault = tmp / "vault"
        self.vault.mkdir()
        (self.vault / "scat.toml").write_text("x = 1\n")
        self.env = {
            "PATH": "/usr/bin:/bin",
            "HOME": str(self.home),
            "CALLS": str(self.calls),
            "STUB_STATE": str(self.stub),
            "SCAT_CHAT_UI": "plain",
            "SCAT_CHAT_CONTEXT": str(REPO),
            "SCAT_CHAT_PORT": str(self.server.port),
            "SCAT_CHAT_WAIT": "3",
            "SCAT_CHAT_TUNNEL_WAIT": "3",
            "SCAT_CHAT_VAULT": str(self.vault),
        }
        for var, name in [
            ("DOCKER", "docker"), ("COLIMA", "colima"), ("TAILSCALE", "tailscale"),
            ("OPENSSL", "openssl"), ("PBCOPY", "pbcopy"), ("PBPASTE", "pbpaste"),
            ("CAFFEINATE", "caffeinate"), ("OPEN", "open"),
        ]:  # fmt: skip
            self.env[f"SCAT_CHAT_{var}"] = str(self.bin / name)

    def run(self, *args, input="", **env):
        e = {**self.env, **{k: v for k, v in env.items() if v is not None}}
        for k, v in env.items():
            if v is None:
                e.pop(k, None)
        return subprocess.run(
            ["/bin/sh", str(SCRIPT), *args],
            check=False,
            env=e,
            input=input,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=60,
        )

    def calls_list(self) -> list[str]:
        return self.calls.read_text().splitlines()

    def called(self, prefix: str) -> list[int]:
        return [i for i, c in enumerate(self.calls_list()) if c.startswith(prefix)]

    def key(self) -> str:
        return self.keyfile.read_text().strip().split("=", 1)[1]

    def clip(self) -> str:
        p = self.stub / "clip"
        return p.read_text() if p.exists() else ""

    def nothing_left(self):
        assert not (self.stub / "container").exists(), "container left"
        assert not (self.stub / "funnel-on").exists(), "tunnel left on"
        assert not (self.state / "session").exists()
        assert not (self.state / "caffeinate.pid").exists()

    def close(self):
        self.server.close()
        pid = self.state / "caffeinate.pid"
        if pid.exists():  # a failed test must not leave the stand-in running
            subprocess.run(["kill", pid.read_text().strip()], check=False, capture_output=True)


@pytest.fixture
def rig(tmp_path):
    r = Rig(tmp_path)
    yield r
    r.close()
