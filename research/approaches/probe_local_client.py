"""Spike probe (WP25-U1): a minimal MCP client for a local Ollama model.

It does what a local chat client does: lists the SCAT MCP server's tools over streamable HTTP with the bearer key,
offers them to an Ollama model, runs the tool calls the model asks for, and prints the timings.
Usage: SCAT_MCP_KEY=... python probe_local_client.py MODEL "question" [--ollama http://127.0.0.1:11434]
"""

import asyncio
import json
import os
import sys
import time
import urllib.request

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

URL = os.environ.get("SCAT_MCP_URL", "http://127.0.0.1:8765/mcp")
OLLAMA = os.environ.get("OLLAMA", "http://127.0.0.1:11434")


def chat(model, messages, tools):
    body = json.dumps(
        {
            "model": model,
            "messages": messages,
            "tools": tools,
            "stream": False,
            "options": {"num_ctx": 8192},
        }
    ).encode()
    req = urllib.request.Request(OLLAMA + "/api/chat", body, {"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=1800))


async def main(model, question):
    hdr = {"Authorization": "Bearer " + os.environ["SCAT_MCP_KEY"]}
    async with streamablehttp_client(URL, headers=hdr) as (r, w, _), ClientSession(r, w) as s:
        await s.initialize()
        listed = (await s.list_tools()).tools
        tools = [
            {
                "type": "function",
                "function": {
                    "name": t.name,
                    "description": t.description or "",
                    "parameters": t.inputSchema,
                },
            }
            for t in listed
        ]
        print(f"tools offered: {len(tools)}")
        msgs = [{"role": "user", "content": question}]
        t0 = time.time()
        for turn in range(4):
            t = time.time()
            out = chat(model, msgs, tools)
            m = out["message"]
            print(
                f"turn {turn}: {time.time() - t:.0f}s, prompt_tokens={out.get('prompt_eval_count')}, "
                f"out_tokens={out.get('eval_count')}"
            )
            msgs.append(m)
            calls = m.get("tool_calls") or []
            if not calls:
                print("ANSWER:", (m.get("content") or "")[:600])
                break
            for c in calls:
                f = c["function"]
                print("CALL:", f["name"], json.dumps(f.get("arguments")))
                res = await s.call_tool(f["name"], f.get("arguments") or {})
                txt = "".join(x.text for x in res.content if hasattr(x, "text"))
                print("  result bytes:", len(txt), "isError:", res.isError)
                msgs.append({"role": "tool", "content": txt[:6000], "tool_name": f["name"]})
        print(f"total {time.time() - t0:.0f}s")


asyncio.run(main(sys.argv[1], sys.argv[2]))
