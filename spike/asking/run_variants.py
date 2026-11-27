"""RS7-U3: run every variant against every client and print one table. One command, from this folder:

    uv run --project <rs5 checkout> --frozen --extra mcp python run_variants.py [--only B1,B4]

Raw wire logs go to logs/<id>.txt, the table to logs/table.txt. Everything is on 127.0.0.1.
"""

from __future__ import annotations

import re
import sys
from importlib.metadata import version
from pathlib import Path

import anyio
from harness import Row, run

LOGS = Path(__file__).parent / "logs"
ALL = ["A1 sdk-answers", "A2 sdk-silent", "A3 sdk-nocap", "A4 raw-postonly", "A4s sdk-postonly"]
POST_ONLY = ["A1 sdk-answers", "A4 raw-postonly"]  # one reader of GET, one POST-only
STATELESS = {"stateless": True}
JSON = {"json_response": True}
NOCHECK = {"check": False}

# (variant, tool, clients, server config, run kwargs)
PLAN: list[tuple[str, str, list[str], dict, dict]] = [
    ("B1", "b1_session", ALL, {}, {}),
    ("B2", "b2_related", ALL + ["A4q raw-silent"], {}, {}),
    ("B3", "b3_ctx", ALL + ["A4q raw-silent"], {}, {}),
    (
        "B4",
        "b1_session",
        POST_ONLY,
        STATELESS,
        {},
    ),  # capability check on: stateless has no initialize
    ("B4", "b1_session", POST_ONLY, STATELESS | NOCHECK, {}),
    ("B4", "b2_related", POST_ONLY, STATELESS | NOCHECK, {}),
    ("B4", "b3_ctx", POST_ONLY, STATELESS | NOCHECK, {}),
    ("B5", "b1_session", POST_ONLY, JSON, {}),
    ("B5", "b2_related", POST_ONLY, JSON, {}),
    ("B5", "b3_ctx", POST_ONLY, JSON, {}),
    ("B6", "b6_url", ["A1 sdk-answers", "A3 sdk-nocap", "A4 raw-postonly"], {}, {}),
    ("B7", "b7_after_ctx", POST_ONLY, {}, {}),
    ("B7", "b7_after_session", POST_ONLY, {}, {}),
    (
        "B8",
        "b8_caps",
        [
            "A1 sdk-answers",
            "A3 sdk-nocap",
            "R none",
            "R {elicitation:{}}",
            "R {form:{}}",
            "R {url:{}}",
        ],
        {},
        {},
    ),
    ("B8", "b8_nocheck", ["A3 sdk-nocap", "A1 sdk-answers", "A4 raw-postonly"], {}, {}),
    ("B9", "b9_timeout_session", ["A1 sdk-answers", "A4q raw-silent"], {}, {"hang": 6}),
    ("B9", "b9_timeout_ctx", ["A1 sdk-answers", "A4q raw-silent"], {}, {"hang": 6}),
    ("B10", "b10_flow", ["A3 sdk-nocap"], {}, {}),
    ("B11", "tools/list", ["A3 sdk-nocap", "A4 raw-postonly"], {}, {}),
]


def slug(r: Row, tool: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", f"{r.variant}-{tool}-{r.client}-{r.config}".lower()).strip(
        "-"
    )


def table(rows: list[Row]) -> str:
    head = "| variant | tool | server config | client | what the client saw | stream the request used | outcome | wall s |"
    out = [head, "|" + "---|" * 8]
    for r, tool in rows:
        out.append(
            f"| {r.variant} | {tool} | {r.config} | {r.client} | {r.saw} | {r.stream} | {r.outcome} ({r.server}) | {r.wall:.1f} |"
        )
    return "\n".join(out)


async def main(only: set[str]) -> None:
    LOGS.mkdir(exist_ok=True)
    done: list[tuple[Row, str]] = []
    for variant, tool, clients, cfg, kw in PLAN:
        if only and variant not in only:
            continue
        for c in clients:
            r = await run(variant, tool, c, **kw, **cfg)
            (LOGS / f"{slug(r, tool)}.txt").write_text(
                f"{variant} {tool} client={c} config={r.config}\nclient saw: {r.saw}\nstream: {r.stream}\n"
                f"outcome: {r.outcome}; server: {r.server}; wall {r.wall:.2f}s\n\n"
                + "\n".join(r.log)
                + "\n"
            )
            done.append((r, tool))
            print(f"  ran {variant} {tool} {c}: {r.outcome}", file=sys.stderr, flush=True)
    text = f"mcp SDK {version('mcp')}\n\n" + table(done)
    (LOGS / "table.txt").write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    only = {a for arg in sys.argv[2:] for a in arg.split(",")} if "--only" in sys.argv else set()
    anyio.run(main, only)
