"""Stand-ins for the programs the launcher calls (docker, colima, tailscale, openssl, security, osascript, pbcopy, caffeinate),
a fake server on a free port, and a runner for deploy/scat-chat.sh. No real docker, colima or tailscale runs."""

import http.server
import os
import subprocess
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

REPO = Path(__file__).parents[2]
# The launcher under test; SCAT_CHAT_TEST_LAUNCHER names a scratch copy (a mutation check), never used otherwise.
SCRIPT = Path(os.environ.get("SCAT_CHAT_TEST_LAUNCHER") or REPO / "deploy" / "scat-chat.sh")

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
run) case "$*" in *"--env-file /dev/stdin"*) cat > "$S/env-in" ;; esac
     if [ -n "${STUB_FAIL_RUN:-}" ]; then echo "port in use" >&2; exit 125; fi; touch "$S/container"; echo abc123 ;;
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
    # The keychain: items are files in $STUB_STATE/keychain (outside the launcher's state folder). Only argv is
    # logged, as the real tool shows it; a command read from stdin (-i) is logged by verb and service, never by value.
    "security": r"""#!/bin/sh
echo "security $*" >> "$CALLS"
D="$STUB_STATE/keychain"
mkdir -p "$D"
run() { # verb then its flags; -w takes a value for add, is a bare flag for find
    verb=$1; shift
    svc=""; val=""
    while [ $# -gt 0 ]; do
        case "$1" in
        -s) svc=$2; shift ;;
        -a) shift ;;
        -w) if [ "$verb" = add-generic-password ]; then val=$2; shift; fi ;;
        esac
        shift
    done
    [ -n "$svc" ] || return 2
    [ -z "${FROM_STDIN:-}" ] || echo "security(stdin) $verb -s $svc" >> "$CALLS"
    case "$verb" in
    add-generic-password) [ -z "${STUB_FAIL_KEYCHAIN:-}" ] || return 36
        printf '%s' "$val" > "$D/$svc"; printf '%s\n' "$val" >> "$STUB_STATE/keys-seen" ;;
    find-generic-password) [ -f "$D/$svc" ] || return 44; if [ "$WANT_W" = 1 ]; then cat "$D/$svc"; fi ;;
    delete-generic-password) [ -f "$D/$svc" ] || return 44; rm -f "$D/$svc" ;;
    *) return 2 ;;
    esac
}
WANT_W=0
case "$*" in *" -w") WANT_W=1 ;; esac
if [ "$1" = "-i" ]; then
    FROM_STDIN=1
    while IFS= read -r line; do
        eval "set -- $line"
        run "$@" || exit $?
    done
else
    run "$@"
fi
""",
    # the dialogs and notifications of dialog mode: recorded, never answered (no answer is "closed")
    "osascript": '#!/bin/sh\necho "osascript $*" >> "$CALLS"\n',
    # curl is the real one (it talks to the fake server); the stand-in only records its arguments
    "curl": '#!/bin/sh\necho "curl $*" >> "$CALLS"\nexec /usr/bin/curl "$@"\n',
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
    """Answers 401 to a POST to /mcp without the key in the stand-in keychain, 200 with it."""

    def __init__(self, keyfile: Path):
        self.keyfile = keyfile
        outer = self

        class H(http.server.BaseHTTPRequestHandler):
            def do_POST(self):
                self.rfile.read(int(self.headers.get("Content-Length", 0)))
                key = outer.keyfile.read_text() if outer.keyfile.exists() else ""
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
        self.keyfile = self.stub / "keychain" / "scat-chat"  # the stand-in keychain's one item
        self.state.mkdir(parents=True)
        self.server = FakeServer(self.keyfile)
        self.procs: list[subprocess.Popen] = []
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
            ("CAFFEINATE", "caffeinate"), ("OPEN", "open"), ("SECURITY", "security"),
            ("OSASCRIPT", "osascript"), ("CURL", "curl"),
        ]:  # fmt: skip
            self.env[f"SCAT_CHAT_{var}"] = str(self.bin / name)

    def _env(self, env):
        e = {**self.env, **{k: v for k, v in env.items() if v is not None}}
        for k, v in env.items():
            if v is None:
                e.pop(k, None)
        return e

    def run(self, *args, input="", **env):
        return subprocess.run(
            ["/bin/sh", str(SCRIPT), *args],
            check=False,
            env=self._env(env),
            input=input,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=60,
        )

    def start_bg(self, **env):
        """`start` in dialog mode (the app's mode), which waits to be stopped: returns the process once the
        state file says running. Its output goes to a file, so no stray child can hold a pipe open."""
        out = self.tmp / f"bg{len(self.procs)}.out"
        proc = subprocess.Popen(
            ["/bin/sh", str(SCRIPT), "start"],
            env=self._env({"SCAT_CHAT_UI": "dialog", **env}),
            stdin=subprocess.DEVNULL,
            stdout=out.open("w"),
            stderr=subprocess.STDOUT,
        )
        proc.out = out
        self.procs.append(proc)
        deadline = time.monotonic() + 30
        while time.monotonic() < deadline:
            if proc.poll() is not None:
                raise AssertionError(
                    f"start ended before it ran: {proc.returncode} {out.read_text()}"
                )
            if self.ui_lines()[:1] == ["running"]:
                return proc
            time.sleep(0.05)
        raise AssertionError("start never reached running: " + out.read_text())

    def stop_bg(self, proc):
        """The Stop verb while `proc` waits; returns the verb's result. The process is waited for meanwhile, so
        it is reaped as soon as it ends (the launcher waits for it to be gone)."""
        with ThreadPoolExecutor(1) as ex:
            verb = ex.submit(self.run, "stop")
            proc.wait(timeout=30)
            return verb.result()

    def ui_lines(self) -> list[str]:
        """The state file the app reads: state, vault, address, then a problem line when there is one."""
        p = self.state / "ui"
        return p.read_text().splitlines() if p.exists() else []

    def calls_list(self) -> list[str]:
        return self.calls.read_text().splitlines()

    def called(self, prefix: str) -> list[int]:
        return [i for i, c in enumerate(self.calls_list()) if c.startswith(prefix)]

    def item(self) -> bool:
        """The session key is in the stand-in keychain."""
        return self.keyfile.exists()

    def key(self) -> str:
        return self.keyfile.read_text()

    def keys_seen(self) -> list[str]:
        p = self.stub / "keys-seen"
        return p.read_text().split() if p.exists() else []

    def clip(self) -> str:
        p = self.stub / "clip"
        return p.read_text() if p.exists() else ""

    def nothing_left(self):
        assert not (self.stub / "container").exists(), "container left"
        assert not (self.stub / "funnel-on").exists(), "tunnel left on"
        assert not self.item(), "key left in the keychain"
        assert not (self.state / "session").exists()
        assert not (self.state / "caffeinate.pid").exists()

    def close(self):
        for proc in self.procs:
            if proc.poll() is None:  # a failed test must not leave a waiting launcher behind
                proc.kill()
                proc.wait()
        self.server.close()
        pid = self.state / "caffeinate.pid"
        if pid.exists():  # a failed test must not leave the stand-in running
            subprocess.run(["kill", pid.read_text().strip()], check=False, capture_output=True)


@pytest.fixture
def rig(tmp_path):
    r = Rig(tmp_path)
    yield r
    r.close()
