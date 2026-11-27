"""Hosting the router and the stage servers, 127.0.0.1 only.

(i)  python lc_hosting.py stage NAME PORT                      one stage server per process
     python lc_hosting.py router PORT MODE plan=URL code=URL .. the router, reaching stages over HTTP
(ii) python lc_hosting.py single PORT MODE                      one ASGI app: /stage/<name>/mcp and /mcp
"""

import sys
from contextlib import AsyncExitStack, asynccontextmanager

import uvicorn
from lc_router import Router, http_connector
from lc_stages import STAGES, build_stage
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from starlette.applications import Starlette
from starlette.routing import Mount, Route

HOST = "127.0.0.1"


class _Asgi:
    """A raw ASGI endpoint for Route (Starlette uses an object that is not a function as an ASGI app)."""

    def __init__(self, manager: StreamableHTTPSessionManager):
        self.manager = manager

    async def __call__(self, scope, receive, send):
        await self.manager.handle_request(scope, receive, send)


def router_routes(router: Router, path: str = "/mcp"):
    """The routes and the session manager of `router` on streamable HTTP."""
    manager = StreamableHTTPSessionManager(app=router.server)
    return [Route(path, _Asgi(manager))], manager


def stage_process(name: str, port: int) -> None:
    """(i) a stage server as its own process."""
    build_stage(name, host=HOST, port=port, log_level="WARNING").run("streamable-http")


def router_process(port: int, mode: str, urls: dict[str, str]) -> None:
    """(i) the router as its own process, reaching the stage servers over HTTP on their ports."""
    routes, manager = router_routes(Router(http_connector(urls), mode))

    @asynccontextmanager
    async def lifespan(_app):
        async with manager.run():
            yield

    uvicorn.run(
        Starlette(routes=routes, lifespan=lifespan), host=HOST, port=port, log_level="warning"
    )


def single_app(port: int, mode: str) -> Starlette:
    """(ii) one ASGI app: each stage server mounted at /stage/<name>/mcp, the router at /mcp, on one port."""
    stages = {n: build_stage(n, host=HOST, port=port) for n in STAGES}
    subapps = {n: s.streamable_http_app() for n, s in stages.items()}
    urls = {n: f"http://{HOST}:{port}/stage/{n}/mcp" for n in STAGES}
    routes, manager = router_routes(Router(http_connector(urls), mode))

    @asynccontextmanager
    async def lifespan(_app):
        async with AsyncExitStack() as stack:
            for s in stages.values():
                await stack.enter_async_context(s.session_manager.run())
            await stack.enter_async_context(manager.run())
            yield

    mounts = [Mount(f"/stage/{n}", app=a) for n, a in subapps.items()]
    return Starlette(routes=mounts + routes, lifespan=lifespan)


def single_process(port: int, mode: str) -> None:
    uvicorn.run(single_app(port, mode), host=HOST, port=port, log_level="warning")


if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == "stage":
        stage_process(args[0], int(args[1]))
    elif cmd == "router":
        router_process(int(args[0]), args[1], dict(a.split("=", 1) for a in args[2:]))
    elif cmd == "single":
        single_process(int(args[0]), args[1])
    else:
        raise SystemExit(__doc__)
