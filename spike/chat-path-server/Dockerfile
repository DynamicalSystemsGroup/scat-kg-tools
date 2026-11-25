# Throwaway spike image: the RS3 MCP server, read-only checks over a mounted vault.
FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml README.md /src/
COPY src /src/src
COPY ontology /src/ontology
RUN pip install --no-cache-dir /src "mcp>=1.2,<2" uvicorn
COPY spike/chat-path-server/server.py /app/server.py
RUN useradd -r -u 10001 scat
USER scat
EXPOSE 8765
# The vault is mounted read-only at /vault; the API key comes from the environment (SCAT_MCP_KEY).
ENTRYPOINT ["python", "server.py", "--vault", "/vault", "--host", "0.0.0.0", "--port", "8765"]
