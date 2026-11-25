# RS3: lab run, 25 November (early morning)

One light session, human-paced, two messages, synthetic lab vault only. Driven by the ACE with the chief engineer's
permission (Tailscale install, Funnel for this run, HTTPS and the Funnel policy on his tailnet).

## Set-up
- **Container.** The spike MCP server (`spike/chat-path-server/`, two read-only checks) runs in Docker under Colima, from
  `Dockerfile` here: read-only root filesystem, a non-root user (the host's uid), the lab vault mounted read-only at
  `/vault`, the port published on `127.0.0.1` only. An API key gate (`SCAT_MCP_KEY`, Bearer or `X-API-Key`) refuses
  anything without the key (401).
- **Tunnel.** Tailscale Funnel publishes `127.0.0.1:8765` at a public `https://<machine>.<tailnet>.ts.net/mcp`. The
  machine was renamed to a neutral name first, because enabling HTTPS publishes the machine name in a public
  certificate ledger permanently.
- **Chat.** In inference.coop's chat (LibreChat), MCP Settings > Add MCP: the URL, Streamable HTTPS, API Key auth; the
  key was pasted by the chief engineer, not by the agent.

## Result
- The co-op's chat server connected (Connected), listed the tools, and the model (`tinfoil/gpt-oss-120b`) called
  `check_vault` through MCP. Its answer, "7 errors, 0 warnings; most common rule SCAT-DONE-FIELD", matches the tool
  run directly in the container. **The route works end to end.**
- After a container restart the chat server's session got 404s, then re-initialised by itself.

## Findings for WP18 and the launcher
1. **macOS privacy blocks Colima's mount of `~/Documents`**: a readable file there gave "permission denied" inside the
   container. A vault under `~/Documents` needs a different mount or a copy; the launcher must handle this.
2. **The Tailscale CLI's `funnel` failed silently** until the tailnet had the Funnel policy; the console page
   `login.tailscale.com/f/funnel?node=<id>` adds it in one click. A first-run guide must include that step and the
   HTTPS step, and the rename before HTTPS.
3. **Keys go in by the coder's hand**, in LibreChat's form.
4. **No terminal was needed by the coder** except to install Tailscale (an admin password prompt); everything else
   can be a launcher's job.

## Clean-up
Funnel off (`No serve config`; the URL no longer answers), the container removed, the MCP entry deleted from the
chat's settings. HTTPS and the Funnel policy stay enabled on the tailnet; the machine keeps its neutral name.
