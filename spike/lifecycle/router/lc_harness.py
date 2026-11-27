"""Test helpers: free ports, subprocess servers on 127.0.0.1, readiness polling, ps, measurements."""

import asyncio
import json
import socket
import statistics
import subprocess
import sys
import time
from pathlib import Path

from lc_router import _http_session

HERE = Path(__file__).parent
HOSTING = str(HERE / "lc_hosting.py")
MEAS = HERE / "measurements.json"


def record(key: str, value) -> None:
    """Write one measurement into measurements.json (cleared at the start of a test run)."""
    data = json.loads(MEAS.read_text()) if MEAS.exists() else {}
    data[key] = value
    MEAS.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def spawn(*args: str) -> subprocess.Popen:
    return subprocess.Popen(
        [sys.executable, HOSTING, *args],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        cwd=str(HERE),
    )


def stop(proc: subprocess.Popen) -> None:
    if proc.poll() is None:
        proc.terminate()
        try:
            proc.wait(5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(5)


async def _ready(
    url: str, deadline: float, router: bool = False, allow_down: bool = False
) -> float:
    """Seconds until `url` answers initialize (a router: and has every stage server connected)."""
    t0 = time.perf_counter()
    while time.perf_counter() < deadline:
        try:
            async with asyncio.timeout(4):
                async with _http_session(url) as s:
                    if router and not allow_down:
                        r = await s.call_tool("stage", {})
                        if r.structuredContent["down"]:
                            raise RuntimeError("upstream not ready")
            return time.perf_counter() - t0
        except BaseException as e:
            if isinstance(e, asyncio.CancelledError | KeyboardInterrupt):
                raise
            await asyncio.sleep(0.05)
    raise TimeoutError(url)


def wait_ready(
    url: str, router: bool = False, allow_down: bool = False, timeout: float = 30.0
) -> None:
    asyncio.run(_ready(url, time.perf_counter() + timeout, router, allow_down))


def rss_kb(pid: int) -> int:
    out = subprocess.run(
        ["ps", "-o", "rss=", "-p", str(pid)], check=False, capture_output=True, text=True
    ).stdout.strip()
    return int(out) if out else 0


def median_ms(samples: list[float]) -> float:
    return round(statistics.median(samples) * 1000, 3)


async def time_calls(session, tool: str, args: dict, n: int = 200, warm: int = 10) -> list[float]:
    for _ in range(warm):
        await session.call_tool(tool, args)
    out = []
    for _ in range(n):
        t = time.perf_counter()
        await session.call_tool(tool, args)
        out.append(time.perf_counter() - t)
    return out


class Topology:
    """(i) three stage processes plus a router process, or (ii) one process; all on 127.0.0.1."""

    def __init__(self, kind: str, mode: str = "dynamic"):
        self.kind, self.mode = kind, mode
        self.procs: dict[str, subprocess.Popen] = {}
        self.ports: dict[str, int] = {}
        self.startup_s = 0.0

    @property
    def router_url(self) -> str:
        return f"http://127.0.0.1:{self.ports['router']}/mcp"

    def stage_url(self, name: str) -> str:
        if self.kind == "i":
            return f"http://127.0.0.1:{self.ports[name]}/mcp"
        return f"http://127.0.0.1:{self.ports['router']}/stage/{name}/mcp"

    def start(self, stages=("plan", "code", "analyse")) -> "Topology":
        t0 = time.perf_counter()
        if self.kind == "i":
            for n in stages:
                self.ports[n] = free_port()
                self.procs[n] = spawn("stage", n, str(self.ports[n]))
            self.ports["router"] = free_port()
            urls = [f"{n}={self.stage_url(n)}" for n in ("plan", "code", "analyse")]
            self.procs["router"] = spawn("router", str(self.ports["router"]), self.mode, *urls)
        else:
            self.ports["router"] = free_port()
            self.procs["router"] = spawn("single", str(self.ports["router"]), self.mode)
        wait_ready(self.router_url, router=True, allow_down=len(stages) < 3)
        self.startup_s = time.perf_counter() - t0
        return self

    def stop(self) -> None:
        for p in self.procs.values():
            stop(p)

    def rss(self) -> dict[str, int]:
        return {n: rss_kb(p.pid) for n, p in self.procs.items()}
