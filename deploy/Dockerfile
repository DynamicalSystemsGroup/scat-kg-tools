# The SCAT MCP server (M8) as a read-only container. Build context: the repository root.
#   docker build -f deploy/Dockerfile -t scatlab-mcp .
# Run (the launcher does this): --user <host uid>:<host gid>, --read-only --tmpfs /tmp, vault mounted read-write at /vault (the server writes
# views/ through the tool's operations), key from --env-file (SCAT_MCP_KEY), port published on 127.0.0.1 only.
FROM python:3.12-slim

COPY pyproject.toml /src/pyproject.toml
COPY src /src/src
COPY ontology/scat.ttl /src/ontology/scat.ttl
COPY contracts/lifecycle.md /src/contracts/lifecycle.md
RUN pip install --no-cache-dir "/src[mcp,draw]" && rm -rf /src /root/.cache

# Nothing writes outside /tmp (a tmpfs at run time) and /vault.
ENV HOME=/tmp \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# The published image cannot carry the host's uid, so the launcher sets the user at run time (--user uid:gid), which
# keeps the vault files the server writes owned by the coder. This unprivileged user is the default if none is set.
USER 65534:65534
EXPOSE 8765
ENTRYPOINT ["scat-mcp", "--vault", "/vault", "--host", "0.0.0.0", "--port", "8765"]
