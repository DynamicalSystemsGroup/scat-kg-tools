"""The manuals of the lifecycle: one guide per stage and an index, read from the lifecycle instance.

    scat_kg.guides.instance()        # the parsed `yaml lifecycle` block of contracts/lifecycle.md (a fresh copy)
    scat_kg.guides.STAGES            # the stages, in the instance's order
    scat_kg.guides.guide_text(name)  # a stage's guide, or "index"; the text every path gives
    scat_kg.guide(stage)             # the API twin: its `str()` is `guide_text`

Nothing about stages is written twice. Tools, prompts, outputs, review loops, inputs and exits come from the
instance; only how to recognise a stage and the coder's acts are hand-written (`<stage>.md` beside this file),
and they name a tool, a prompt or an exit only through a placeholder (`{tool:x}`, `{prompt:x}`, `{exit:stage}`)
that must exist in the instance. No MCP code is imported here: the CLI and the API use it too.
"""

import copy
import functools
import re
from pathlib import Path

import yaml

from scat_kg.contract import SCHEMA_VERSION
from scat_kg.ops.result import Result, refused

_HERE = Path(__file__).resolve().parent
# Installed: the wheel ships the lifecycle document here. Source tree: it is in the repository's contracts/.
_PACKAGED = _HERE / "lifecycle.md"
_SOURCE = _HERE.parents[2] / "contracts" / "lifecycle.md"

INDEX = "index"

MODE = (
    "`mode` is the vault's attribution mode (`required`, `optional` or `disallowed`, from `scat.toml`), in "
    "every result: in required mode a narrative SHALL name its contributors, in disallowed mode it SHALL NOT, "
    "in optional mode it MAY."
)


def _instance_path() -> Path:
    for path in (_PACKAGED, _SOURCE):
        if path.is_file():
            return path
    raise FileNotFoundError(
        f"the lifecycle document is in neither {_PACKAGED} (installed) nor {_SOURCE} (source tree)"
    )


@functools.cache
def _parse(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = re.search(r"```yaml lifecycle\n(.*?)```", text, re.DOTALL)
    if not m:
        raise ValueError(f"{path} has no `yaml lifecycle` block")
    return yaml.safe_load(m.group(1))


def instance() -> dict:
    """The parsed `yaml lifecycle` block, a fresh deep copy each call."""
    return copy.deepcopy(_parse(_instance_path()))


def __getattr__(name: str):
    if name == "STAGES":  # read on first use, so importing scat_kg never needs the file
        return tuple(instance()["stages"])
    raise AttributeError(name)


def _words(text: str) -> str:
    return " ".join(text.split())


def _predicate(t: dict) -> str:
    p = t["predicate"]
    return f"detect: {p['check']}" if p["kind"] == "detect" else f"person: {p['says']}"


def _exits(inst: dict, stage: str) -> list[dict]:
    return [t for t in inst["transitions"] if t["from"] == stage]


def _hand(stage: str, inst: dict) -> tuple[str, dict[str, str]]:
    """The hand-written file of a stage: its docs page and its sections, placeholders filled from the instance."""
    raw = (_HERE / f"{stage}.md").read_text(encoding="utf-8")
    docs = re.match(r"docs: (\S+)\n", raw)
    if not docs:
        raise ValueError(f"{stage}.md must open with a `docs: <page>` line")
    sections = {
        m.group(1): m.group(2).strip()
        for m in re.finditer(r"^## ([^\n]+)\n(.*?)(?=^## |\Z)", raw, re.DOTALL | re.MULTILINE)
    }
    spec = inst["stages"][stage]
    own = {t["to"]: t["id"] for t in _exits(inst, stage)}

    def fill(m: re.Match) -> str:
        kind, name = m.group(1), m.group(2)
        pool = {"tool": spec["tools"], "prompt": spec["prompts"]}.get(kind)
        if kind == "exit":
            if name not in own:
                raise KeyError(f"{stage}.md: no transition from {stage} to {name}")
            return own[name]
        if name not in pool:
            raise KeyError(f"{stage}.md: {kind} {name} is not offered in the {stage} stage")
        return f"`{name}`"

    return docs.group(1), {
        k: re.sub(r"\{(tool|prompt|exit):([\w>-]+)\}", fill, v) for k, v in sections.items()
    }


def _stage_text(stage: str, inst: dict) -> tuple[str, str]:
    spec = inst["stages"][stage]
    docs, hand = _hand(stage, inst)
    lines = [f"# {stage}", spec["work"], "", f"Docs: {docs}", ""]
    lines += [f"Recognise: {hand['Recognise']}", ""]
    lines += ["Needs: " + "; ".join(spec["required_inputs"]) + ".", "", "Makes:"]
    lines += [
        f"- {o['output']}: {o['produced_by']}. Review: {o['review']}."
        for o in spec["allowed_outputs"]
    ]
    limits = spec.get("tool_limits") or {}
    tools = ", ".join(f"`{t}`" + (f" ({limits[t]})" if t in limits else "") for t in spec["tools"])
    lines += [
        "",
        f"Tools: {tools}.",
        "Prompts: " + ", ".join(f"`{p}`" for p in spec["prompts"]) + ".",
        "",
    ]
    lines += [f"The coder's acts: {hand['Acts']}", "", "Exits:"]
    for t in _exits(inst, stage):
        lines.append(
            f"- {t['id']} to {t['to']} ({t['decides']} decides): {t['trigger']}; {_predicate(t)}."
        )
    lines += ["", MODE]
    return "\n".join(lines), docs


def _index_text(inst: dict) -> str:
    which, setter = inst["stage_tools"]
    lines = [
        "# SCAT stages",
        "A project is in one stage at a time; each stage offers the tools its work needs.",
        "",
    ]
    lines += [f"- {name}: {spec['work']}" for name, spec in inst["stages"].items()]
    lines += ["", "Moves (id, from to, who decides, how it opens):"]
    for t in inst["transitions"]:
        to = "any stage" if t["to"] == "any" else t["to"]
        lines.append(f"- {t['id']} {t['from']} to {to} ({t['decides']}): {_predicate(t)}.")
    lines += [
        "",
        (
            f"`{which}` says the stage; `{setter}` moves it, only when a person says so. A detect "
            "predicate only advises; the person decides every move. `scat guide <stage>` gives a "
            "stage's guide."
        ),
        "",
        MODE,
    ]
    return "\n".join(lines)


def _build(name: str, inst: dict) -> dict:
    """The guide named `name` (a stage or "index") from `inst`: its text, docs page, tools and exit ids."""
    if name == INDEX:
        return {
            "text": _index_text(inst),
            "docs": None,
            "tools": list(inst["stage_tools"]),
            "exits": [t["id"] for t in inst["transitions"]],
        }
    if name not in inst["stages"]:
        raise KeyError(name)
    text, docs = _stage_text(name, inst)
    return {
        "text": text,
        "docs": docs,
        "tools": list(inst["stages"][name]["tools"]),
        "exits": [t["id"] for t in _exits(inst, name)],
    }


def guide_text(name: str) -> str:
    """A stage's guide, or the index (`name` "index"): the one text the CLI, the API and the server give."""
    return _build(name, instance())["text"]


class Guide:
    """What `scat_kg.guide` returns for a stage or the index: `str()` is the text `scat guide` prints."""

    ok = True
    mode = None  # guides are vault-free

    def __init__(self, stage: str, parts: dict):
        self.stage = stage
        self.text = parts["text"]
        self.docs = parts["docs"]
        self.tools = parts["tools"]
        self.exits = parts["exits"]

    def to_dict(self) -> dict:
        return {
            "schema_version": SCHEMA_VERSION,
            "kind": "guide",
            "operation": "guide",
            "ok": True,
            "mode": None,
            "stage": self.stage,
            "text": self.text,
            "docs": self.docs,
            "tools": self.tools,
            "exits": self.exits,
        }

    def __str__(self) -> str:
        return self.text

    __repr__ = __str__


def guide(stage: str | None = None) -> Guide | Result:
    """The guide of a stage; without `stage`, or "index", the index. An unknown name is a refusal."""
    name = INDEX if stage is None else stage
    inst = instance()
    if name != INDEX and name not in inst["stages"]:
        names = ", ".join(inst["stages"])
        return refused(
            "guide",
            f"stage `{name}`",
            f"`{name}` is not a stage; the stages are {names}",
            f"run `scat guide` for the index, or `scat guide <stage>` with one of {names}",
        )
    return Guide(name, _build(name, inst))
