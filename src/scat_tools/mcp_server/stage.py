"""The stage layer of the MCP server (contracts/lifecycle.md, section 3): one stage per vault, kept in `lifecycle.toml`.

`apply(mcp, root)` wraps every registered tool so a call is first checked against the vault's stage, names each
tool's and prompt's stages in its description, adds `which_stage` and `set_stage`, adds the guide resources and
sets the server's instructions. The lists of tools, prompts and resources never change with the stage: the stage
is enforced by refusal, as a normal result (never `isError`). The stage is the file, read afresh on every call;
`set_stage` is the only writer of it. A detect predicate only advises: a person's `set_stage(to, by)` makes every move.
"""

import json
import os
import tempfile
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pydantic_core
from mcp.server.fastmcp import FastMCP
from mcp.types import CallToolResult, TextContent

from scat_tools import guides
from scat_tools.contract import SCHEMA_VERSION
from scat_tools.mcp_server import detects, prompts
from scat_tools.ops.result import refused, stamp
from scat_tools.vault import read_mode

FILE = "lifecycle.toml"
UNKNOWN = "unknown"
STAGE_TOOLS = ("which_stage", "set_stage")
_OWN = (
    "The tool owns conformance, the coder owns interpretation, the assistant holds no authority "
    f"({prompts.CITE}). "
)


@dataclass(frozen=True)
class State:
    """What `lifecycle.toml` says. `stage` is None when unknown; `problem` says why when the file was no help."""

    stage: str | None = None
    set_by: str | None = None
    problem: str | None = None  # why the stage is unknown, when there is a file


def read_state(root: Path) -> State:
    """The state in `<root>/lifecycle.toml`: unknown for no file, no `stage`, an unknown stage name or a bad file."""
    path = Path(root) / FILE
    if not path.exists():
        return State()
    try:
        data = tomllib.loads(path.read_bytes().decode("utf-8"))
    except (tomllib.TOMLDecodeError, UnicodeDecodeError) as e:
        return State(problem=f"`{FILE}` is not valid TOML ({e})")
    except OSError as e:
        return State(problem=f"`{FILE}` could not be read ({e})")

    def text(key: str) -> str | None:
        v = data.get(key)
        return v if isinstance(v, str) else None

    names = ", ".join(guides.STAGES)
    if "stage" not in data:
        return State(problem=f"`{FILE}` has no `stage`")
    stage = data["stage"]
    if not isinstance(stage, str) or stage not in guides.STAGES:
        return State(problem=f"`{FILE}` names the stage {stage!r}, which is not one of {names}")
    return State(stage, text("set_by"))


def _q(s: str) -> str:
    """A TOML basic string."""
    return json.dumps(s, ensure_ascii=False).replace("\x7f", "\\u007f")


def write_state(root: Path, stage: str | None, set_by: str | None) -> None:
    """Write `lifecycle.toml` atomically: a temp file in the same folder, then a replace."""
    lines = []
    if stage is not None:
        lines.append(f"stage = {_q(stage)}")
        if set_by is not None:
            lines.append(f"set_by = {_q(set_by)}")
    body = "\n".join(lines).strip("\n") + "\n"
    fd, tmp = tempfile.mkstemp(dir=root, prefix=".lifecycle-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(body)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, Path(root) / FILE)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


# ---- the instance, read per call (it is cached and copied by `guides`)


def _stages_of(inst: dict, tool: str) -> list[str]:
    return [n for n, s in inst["stages"].items() if tool in s["tools"]]


def _stages_phrase(names: list[str], inst: dict) -> str:
    if not names:
        return "none"
    return "all" if len(names) == len(inst["stages"]) else ", ".join(names)


def _transitions_out(inst: dict, stage: str) -> list[dict]:
    return [t for t in inst["transitions"] if t["from"] == stage]


def _exit_line(t: dict) -> str:
    to = "any stage" if t["to"] == "any" else t["to"]
    return f"{t['id']} to {to} ({t['decides']} decides: {t['trigger']})"


def _exits_text(inst: dict, stage: str) -> str:
    out = _transitions_out(inst, stage)
    return "; ".join(_exit_line(t) for t in out) if out else "none"


def _five_lines(inst: dict) -> str:
    return "\n".join(f"  {n}: {s['work']}" for n, s in inst["stages"].items())


def _exit_doc(t: dict, root: Path) -> dict:
    p = t["predicate"]
    if p["kind"] == "detect":
        holds, detail = detects.evaluate(p["check"], root)
        predicate = {"kind": "detect", "check": p["check"], "holds": holds, "detail": detail}
    else:
        predicate = {"kind": "person", "says": p["says"]}
    return {
        "id": t["id"],
        "to": t["to"],
        "dir": t["dir"],
        "trigger": t["trigger"],
        "decides": t["decides"],
        "predicate": predicate,
    }


# ---- refusals (normal results: kind operation, ok false, nothing written)


def _refusal(root: Path, operation: str, subject: str, why: str, fix: str) -> dict:
    return stamp(refused(operation.replace("_", "-"), subject, why, fix), root).to_dict()


def _unknown_refusal(root: Path, tool: str, inst: dict, state: State) -> dict:
    reason = f" ({state.problem})" if state.problem else ""
    return _refusal(
        root,
        tool,
        f"tool `{tool}`",
        f"the project's stage is not recorded{reason}, so `{tool}` did not run and nothing was changed",
        "the person decides which stage the project is in; ask them, one of:\n"
        + _five_lines(inst)
        + "\nthen, after the person says so, call `set_stage(to, by)` with the stage and the name the person gives.",
    )


def _out_of_stage_refusal(root: Path, tool: str, inst: dict, stage: str) -> dict:
    offered = _stages_of(inst, tool)
    where = ", ".join(offered) if offered else "no stage"
    return _refusal(
        root,
        tool,
        f"tool `{tool}`",
        f"`{tool}` is not offered in the {stage} stage, so it did not run and nothing was changed",
        f"`{tool}` is offered in: {where}. A move is the person's say-so; from {stage} the exits are: "
        f"{_exits_text(inst, stage)}. Ask the person, then call `set_stage(to, by)` after they say so.",
    )


def _as_result(doc: dict) -> CallToolResult:
    text = pydantic_core.to_json(doc, fallback=str, indent=2).decode()
    return CallToolResult(content=[TextContent(type="text", text=text)], structuredContent=doc)


def check_call(root: Path, tool: str) -> dict | None:
    """The refusal document for a call to `tool` in the vault's stage now, or None when it may run."""
    inst = guides.instance()
    state = read_state(root)
    if state.stage is None:
        return _unknown_refusal(root, tool, inst, state)
    spec = inst["stages"][state.stage]
    if tool not in spec["tools"]:
        return _out_of_stage_refusal(root, tool, inst, state.stage)
    return None


def _guarded(root: Path, tool: str, inner):
    def run(**kwargs):
        doc = check_call(root, tool)
        return _as_result(doc) if doc is not None else inner(**kwargs)

    return run


# ---- the stage tools


def _base(root: Path, operation: str) -> dict:
    return {
        "schema_version": SCHEMA_VERSION,
        "kind": "stage",
        "operation": operation,
        "ok": True,
        "mode": read_mode(root),
    }


def which_stage_doc(root: Path) -> dict:
    inst = guides.instance()
    state = read_state(root)
    doc = _base(root, "which-stage")
    if state.stage is None:
        names = ", ".join(inst["stages"])
        text = (
            f"The project's stage is not recorded; the person decides it (one of {names}).\n"
            + _five_lines(inst)
        )
        if state.problem:
            text += f"\nWhy: {state.problem}."
        text += "\nAfter the person says which, call `set_stage(to, by)`."
        doc |= {
            "stage": UNKNOWN,
            "set_by": None,
            "work": "No stage is recorded; a person names one.",
            "required_inputs": [],
            "tools": list(inst["stage_tools"]),
            "prompts": [],
            "stages": [{"name": n, "work": s["work"]} for n, s in inst["stages"].items()],
            "exits": [_exit_doc(t, root) for t in _transitions_out(inst, UNKNOWN)],
            "text": text,
            "guide": "scat://guide/index",
        }
        if state.problem:
            doc["problem"] = state.problem
        return doc
    spec = inst["stages"][state.stage]
    exits = [_exit_doc(t, root) for t in _transitions_out(inst, state.stage)]
    lines = [f"Stage: {state.stage}. {spec['work']}"]
    if state.set_by:
        lines.append(f"Set by {state.set_by}.")
    lines.append("Tools: " + ", ".join(spec["tools"] + list(inst["stage_tools"])) + ".")
    for e in exits:
        p = e["predicate"]
        how = (
            f"detect, {'holds' if p['holds'] else 'does not hold'} now ({p['detail']})"
            if p["kind"] == "detect"
            else f"person: {p['says']}"
        )
        lines.append(
            f"Exit {e['id']} to {e['to']} ({e['decides']} decides): {e['trigger']}; {how}."
        )
    doc |= {
        "stage": state.stage,
        "set_by": state.set_by,
        "work": spec["work"],
        "required_inputs": list(spec["required_inputs"]),
        "tools": list(spec["tools"]),
        "prompts": list(spec["prompts"]),
        "exits": exits,
        "text": "\n".join(lines),
        "guide": f"scat://guide/{state.stage}",
    }
    return doc


def _pick_transition(inst: dict, frm: str, to: str) -> dict | None:
    """The listed transition for a move: a move has one."""
    found = [t for t in _transitions_out(inst, frm) if t["to"] in (to, "any")]
    return found[0] if found else None


def set_stage_doc(root: Path, to: str, by: str | None) -> dict:
    inst = guides.instance()
    names = ", ".join(inst["stages"])
    state = read_state(root)
    frm = state.stage or UNKNOWN
    if to not in inst["stages"]:
        return _refusal(
            root,
            "set_stage",
            f"stage {to!r}",
            f"{to!r} is not a stage; the stages are {names}",
            f"call `set_stage` with one of {names}, once the person has said which",
        )
    if to == state.stage:
        return _refusal(
            root,
            "set_stage",
            f"stage `{to}`",
            f"the project is already in the {to} stage",
            f"from {frm} the exits are: {_exits_text(inst, frm)}",
        )
    t = _pick_transition(inst, frm, to)
    if t is None:
        return _refusal(
            root,
            "set_stage",
            f"move {frm} to {to}",
            f"no transition from {frm} to {to} is listed, so nothing moved",
            f"from {frm} the exits are: {_exits_text(inst, frm)}",
        )
    by = (by or "").strip()
    if not by:
        return _refusal(
            root,
            "set_stage",
            f"move {frm} to {to}",
            "`by` is needed: a move is signed with the name of the person who said so, and none was given, "
            "so nothing moved and nothing was written",
            f"the person says the move and gives the name to sign with; then call `set_stage(to={to!r}, by)` "
            "with that name",
        )
    advisory = []
    p = t["predicate"]
    if p["kind"] == "detect":
        holds, detail = detects.evaluate(p["check"], root)
        if not holds:
            advisory.append(
                f'{t["id"]}: "{p["check"]}" does not hold now ({detail}); the move was made anyway, '
                "because a detect predicate only advises"
            )
    try:
        write_state(root, to, by)
    except OSError as e:
        return _refusal(
            root,
            "set_stage",
            f"`{FILE}`",
            f"could not write: {e}",
            "check the folder's permissions",
        )
    exits = [_exit_doc(x, root) for x in _transitions_out(inst, to)]
    text = f"Moved from {frm} to {to} ({t['id']}, {t['decides']} decides), set by {by}."
    if advisory:
        text += " " + " ".join(advisory) + "."
    return _base(root, "set-stage") | {
        "stage": to,
        "set_by": by,
        "moved": True,
        "from": frm,
        "to": to,
        "transition": t["id"],
        "decides": t["decides"],
        "advisory": advisory,
        "exits": exits,
        "text": text,
        "guide": f"scat://guide/{to}",
    }


# ---- the hook

_SIGNATURE = (
    "`by` is a signature slot: the name the person gave, written by the assistant. It is not proof of "
    "consent (D-179), so call this only after the person says so."
)


def apply(mcp: FastMCP, root: Path) -> None:
    """Add the stage layer to the server `mcp` of the vault `root`."""
    root = Path(root)
    inst = guides.instance()
    tools = mcp._tool_manager._tools
    for name, tool in list(tools.items()):
        tool.fn = _guarded(root, name, tool.fn)
        offered = _stages_phrase(_stages_of(inst, name), inst)
        tool.description = f"{tool.description.rstrip()} Stages: {offered}."
    for name, prompt in mcp._prompt_manager._prompts.items():
        offered = _stages_phrase(
            [n for n, s in inst["stages"].items() if name in s["prompts"]], inst
        )
        prompt.description = f"{(prompt.description or '').rstrip()} Stages: {offered}."

    @mcp.tool(
        name="which_stage",
        description=(
            _OWN
            + "Say the project's stage (or unknown), who set it, the stage's work, tools and exits; for "
            "each exit its predicate, and for a detect predicate whether it holds now. Writes nothing. Works in "
            "every stage. Returns the stage document. Stages: all."
        ),
    )
    def which_stage() -> dict[str, Any]:
        return which_stage_doc(root)

    @mcp.tool(
        name="set_stage",
        description=(
            _OWN
            + "Move the project to stage `to`, only a move the stage's exits list. `by` is required: the move "
            "is made and written to `lifecycle.toml`; without `by` the call is refused and nothing is written. "
            "A detect predicate that does not hold is reported and does not block. "
            + _SIGNATURE
            + " Returns the stage document. Stages: all."
        ),
    )
    def set_stage(to: str, by: str | None = None) -> dict[str, Any]:
        return set_stage_doc(root, to, by)

    def _guide_resource(name: str) -> None:
        @mcp.resource(
            f"scat://guide/{name}",
            name=f"guide-{name}",
            description=f"The guide of the {name} stage."
            if name != "index"
            else "The index of the stages.",
            mime_type="text/markdown",
        )
        def guide() -> str:
            return guides.guide_text(name)

    for name in ("index", *guides.STAGES):
        _guide_resource(name)
    mcp._mcp_server.instructions = guides.guide_text("index")


__all__ = ["apply", "check_call", "read_state", "write_state"]
