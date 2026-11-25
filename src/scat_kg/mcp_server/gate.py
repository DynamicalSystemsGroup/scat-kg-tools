"""The key gate and the start rules of the HTTP transport. The gate is a front door, not authority."""

import hmac

LOOPBACK = ("127.0.0.1", "::1", "localhost")


def key_given(headers: list[tuple[bytes, bytes]]) -> str:
    """The key a request carries: `X-API-Key`, else `Authorization: Bearer <key>`; empty when none."""
    h = {k.decode("latin-1").lower(): v.decode("latin-1") for k, v in headers}
    if h.get("x-api-key"):
        return h["x-api-key"].strip()
    auth = h.get("authorization", "")
    return auth[7:].strip() if auth[:7].lower() == "bearer " else ""


def key_ok(given: str, key: str) -> bool:
    """Constant-time compare (bytes, so a non-ASCII header cannot raise)."""
    return hmac.compare_digest(given.encode("utf-8"), key.encode("utf-8"))


def gated(inner, key: str):
    """An ASGI app that answers 401 to every HTTP request without the key and passes the rest to `inner`."""

    async def app(scope, receive, send):
        if scope["type"] == "http" and not key_ok(key_given(scope.get("headers", [])), key):
            body = b"unauthorised: send the key as `Authorization: Bearer <key>` or `X-API-Key`"
            await send(
                {
                    "type": "http.response.start",
                    "status": 401,
                    "headers": [
                        (b"content-type", b"text/plain; charset=utf-8"),
                        (b"www-authenticate", b"Bearer"),
                        (b"content-length", str(len(body)).encode()),
                    ],
                }
            )
            await send({"type": "http.response.body", "body": body})
            return
        await inner(scope, receive, send)

    return app


def start_refusal(key: str | None, host: str) -> str | None:
    """Why the server may not start over HTTP, or None: no key is allowed on the loopback address only."""
    if key or host in LOOPBACK:
        return None
    return (
        f"refusing to serve HTTP on {host} without a key: set SCAT_MCP_KEY, "
        "or serve on 127.0.0.1 (or use --stdio)"
    )
