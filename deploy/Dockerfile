# The SCAT MCP server (M8) as a read-only container. Build context: the repository root.
#   docker build -f deploy/Dockerfile --build-arg UID=$(id -u) -t scat-chat-mcp .
# Run (the launcher does this): --read-only --tmpfs /tmp, vault mounted read-write at /vault (the server writes
# views/ through the tool's operations), key from --env-file (SCAT_MCP_KEY), port published on 127.0.0.1 only.
FROM python:3.12-slim

# The host user's uid, so files the server writes into the mounted vault belong to the coder.
ARG UID=501

COPY pyproject.toml /src/pyproject.toml
COPY src /src/src
COPY ontology/scat.ttl /src/ontology/scat.ttl
RUN pip install --no-cache-dir "/src[mcp]" && rm -rf /src /root/.cache

RUN useradd --system --no-create-home --uid "${UID}" --shell /usr/sbin/nologin scat

# Nothing writes outside /tmp (a tmpfs at run time) and /vault.
ENV HOME=/tmp \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

USER scat
EXPOSE 8765
ENTRYPOINT ["scat-mcp", "--vault", "/vault", "--host", "0.0.0.0", "--port", "8765"]
