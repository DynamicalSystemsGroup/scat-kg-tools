"""Kit for the independent suite (WP16-U8).

Everything here is written from the contracts (`contracts/rule-catalogue.md`, `contracts/page-contracts.md`,
`contracts/machine-interface.md`), not from the checker: it builds vaults, runs the CLI entry point (`scat_kg.cli.main`,
the function the `scat` command runs), and applies the fixes the tool gives as data, with an applier of its own.
"""

from __future__ import annotations

import contextlib
import io
import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path

from scat_kg import cli

STATUSES = ("stub", "draft", "done")


# --------------------------------------------------------------------------------------------- running the CLI
def scat_main(*args: str) -> tuple[int, str]:
    """Run `scat <args>` in this process; return (exit status, stdout)."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            code = cli.main([str(a) for a in args])
        except SystemExit as stop:  # argparse exits this way
            code = stop.code if isinstance(stop.code, int) else 1
    return int(code or 0), out.getvalue()


@dataclass
class Problem:
    raw: dict

    def __getattr__(self, name):
        try:
            return self.raw[name]
        except KeyError as miss:
            raise AttributeError(name) from miss

    @property
    def fix_text(self) -> str:
        """The lines under the first line of the message as `scat check` prints it."""
        return "\n".join(self.raw["text"].split("\n")[1:])

    def brief(self) -> str:
        return self.raw["text"].split("\n")[0]


class Vault:
    def __init__(self, root: Path):
        self.root = Path(root)

    # files ------------------------------------------------------------------------------------------------
    def path(self, rel: str) -> Path:
        return self.root / rel

    def write(self, rel: str, text: str, crlf: bool = False) -> None:
        p = self.path(rel)
        p.parent.mkdir(parents=True, exist_ok=True)
        data = text.replace("\r\n", "\n")
        if crlf:
            data = data.replace("\n", "\r\n")
        p.write_bytes(data.encode("utf-8"))

    def read(self, rel: str) -> str:
        return self.path(rel).read_bytes().decode("utf-8")

    def exists(self, rel: str) -> bool:
        return self.path(rel).exists()

    def edit(self, rel: str, old: str, new: str) -> None:
        text = self.read(rel)
        assert old in text, f"fixture error: {old!r} not in {rel}"
        self.write(rel, text.replace(old, new, 1), crlf="\r\n" in text)

    def line(self, rel: str, n: int) -> str:
        return self.read(rel).replace("\r\n", "\n").split("\n")[n - 1]

    def snapshot(self) -> dict[str, bytes]:
        return {
            str(p.relative_to(self.root)): p.read_bytes()
            for p in sorted(self.root.rglob("*"))
            if p.is_file()
        }

    def copy_to(self, dest: Path) -> Vault:
        shutil.copytree(self.root, dest)
        return Vault(dest)

    # the tool ---------------------------------------------------------------------------------------------
    def scat(self, *args: str) -> tuple[int, dict]:
        code, out = scat_main(*args, "--root", str(self.root), "--json")
        return code, json.loads(out)

    def check(self, page: str | None = None, neighborhood: bool = False) -> list[Problem]:
        args = ["check"]
        if neighborhood:
            args.append("--neighborhood")
        if page:
            args.append(page)
        _, doc = self.scat(*args)
        assert doc["kind"] == "check", doc
        return [Problem(p) for p in doc["problems"]]

    def status_of(self, name: str) -> str:
        m = re.search(r"^status:\s*(\S+)", self.read(self.find(name)), re.MULTILINE)
        return m.group(1) if m else ""

    def find(self, name: str) -> str:
        hits = [str(p.relative_to(self.root)) for p in self.root.rglob(f"{name}.md")]
        assert len(hits) == 1, (name, hits)
        return hits[0]


# --------------------------------------------------------------------------------------------- building pages
def page_text(
    type_: str,
    title: str,
    status: str = "done",
    description: str | None = "A page.",
    extra: str = "",
    body: str = "",
) -> str:
    lines = ["---", f"type: {type_}", f"status: {status}", f'title: "{title}"']
    if description is not None:
        lines.append(f'description: "{description}"')
    if extra:
        lines.append(extra)
    lines.append("---")
    return "\n".join(lines) + "\n" + (("\n" + body + "\n") if body else "")


NODES = {
    "group": [("borrowers", "Borrowers"), ("volunteers", "Volunteers")],
    "concern": [("quick-checkout", "Quick checkout"), ("safe-handling", "Safe handling")],
    "affordance": [("self-checkout", "Self checkout")],
    "technology": [("booking-app", "Booking app")],
}

# The base narrative. Row n is on line 14 + n. Nothing in the body names a node title in plain text.
NARRATIVE_NAME = "saturday"
NARRATIVE_FILE = "narrative/saturday.md"
BODY_LINE = 9
HEADER_LINE = 13
SEPARATOR_LINE = 14


def row_line(n: int) -> int:
    return SEPARATOR_LINE + n


ROW1 = "| holds | [[borrowers]] | [[quick-checkout]] | Said twice. |"
ROW2 = "| is addressed by | [[quick-checkout]] | [[self-checkout]] | |"


def narrative_text(
    status: str = "done", rows: tuple[str, ...] = (ROW1, ROW2), body: str | None = None
) -> str:
    body = (
        body
        if body is not None
        else (
            "The desk was busy: [[borrowers]] queued, wanting [[quick-checkout]] through [[self-checkout]]."
        )
    )
    return (
        "---\ntype: narrative\n"
        f"status: {status}\n"
        'title: "Saturday at the desk"\n'
        'description: "A Saturday at the lending desk."\n'
        "timeframe: past\n---\n\n"
        f"{body}\n\n## Edges told\n\n"
        "| type | from | to | note |\n|---|---|---|---|\n" + "\n".join(rows) + "\n"
    )


def build_base(root: Path, status: str = "done", cap: int = 3) -> Vault:
    """The clean fixture vault: zero messages at every status of the narrative."""
    v = Vault(root)
    v.write("scat.toml", f"stakeholder_group_cap = {cap}\n")
    for type_, items in NODES.items():
        for name, title in items:
            v.write(f"{type_}/{name}.md", page_text(type_, title))
    v.write(NARRATIVE_FILE, narrative_text(status))
    return v


# --------------------------------------------------------------------------------------------- expectations
@dataclass
class Exp:
    rule: str
    severity: str
    file: str
    where: str | None = None
    what: str | re.Pattern | None = None
    line: int | None = None
    col: int | None = None
    fix: object = None  # a str: the single `Fix:` line; ("choose one", [options]); see parse_fix
    fix_has: tuple[str, ...] = ()
    fix_lacks: tuple[str, ...] = ()
    head: str | None = None
    fix_sorted: bool = False  # compare the options as a set (order is judged by its own test)


def pair(name: str, st: str) -> tuple[str, str]:
    """(rule id, severity) of a pair rule at the narrative's status."""
    return (f"SCAT-DONE-{name}", "error") if st == "done" else (f"SCAT-DRAFT-{name}", "warning")


def parse_fix(text: str):
    """('single', text) for one `Fix:` line, else ('choose', header, [option texts]) from the printed lines."""
    lines = [ln for ln in text.split("\n") if ln.strip()]
    if len(lines) == 1 and lines[0].startswith("  Fix: "):
        return ("single", lines[0][len("  Fix: ") :])
    header = lines[0].strip()
    options = []
    for i, ln in enumerate(lines[1:], start=1):
        m = re.match(r"^\s+(\d+)\.\s(.*)$", ln)
        assert m, f"unparsable fix line {ln!r} in {text!r}"
        assert int(m.group(1)) == i, f"options are not numbered 1..n in {text!r}"
        options.append(m.group(2))
    return ("choose", header, options)


def check_fix(p: Problem, e: Exp, errors: list[str]) -> None:
    if e.fix is not None:
        got = parse_fix(p.fix_text)
        if isinstance(e.fix, str):
            want = ("single", e.fix)
        else:
            header, options = e.fix
            want = ("choose", header, list(options))
        if e.fix_sorted and got[0] == "choose" and want[0] == "choose":
            got = (got[0], got[1], sorted(got[2]))
            want = (want[0], want[1], sorted(want[2]))
        if got != want:
            errors.append(f"fix of {p.brief()}\n    want {want}\n    got  {got}")
    for needle in e.fix_has:
        if needle not in p.fix_text:
            errors.append(f"fix of {p.brief()} lacks {needle!r}; fix was:\n{p.fix_text}")
    for needle in e.fix_lacks:
        if needle in p.fix_text:
            errors.append(f"fix of {p.brief()} has {needle!r}; fix was:\n{p.fix_text}")


def match_one(p: Problem, e: Exp) -> bool:
    if (p.rule, p.severity, p.file) != (e.rule, e.severity, e.file):
        return False
    if e.where is not None and p.where != e.where:
        return False
    return not (e.line is not None and p.line != e.line)


def assert_messages(
    problems: list[Problem], expected: list[Exp], allow: tuple[str, ...] = ()
) -> None:
    """Every expected message is present exactly once and nothing else is, but for rules in `allow`."""
    errors: list[str] = []
    left = list(problems)
    for e in expected:
        hits = [p for p in left if match_one(p, e)]
        if not hits:
            errors.append(f"missing: {e.severity} [{e.rule}] {e.file} {e.where!r} line={e.line}")
            continue
        p = hits[0]
        left.remove(p)
        if e.what is not None:
            ok = e.what.search(p.what) if isinstance(e.what, re.Pattern) else p.what == e.what
            if not ok:
                errors.append(f"what of {p.brief()}\n    want {e.what!r}\n    got  {p.what!r}")
        if e.col is not None and p.column != e.col:
            errors.append(f"column of {p.brief()}: want {e.col}, got {p.column}")
        if e.head is not None and p.brief() != e.head:
            errors.append(f"head\n    want {e.head!r}\n    got  {p.brief()!r}")
        check_fix(p, e, errors)
    for p in left:
        if p.rule not in allow:
            errors.append(f"unexpected: {p.brief()}")
    assert not errors, "\n".join(errors)


# --------------------------------------------------------------------------------------------- fix application
class FixError(AssertionError):
    pass


def _sub_slots(text: str, slots: dict[str, str]) -> str:
    for k, v in slots.items():
        text = text.replace(k, v)
    return text


BARE_FIELDS = {
    "type",
    "status",
    "kind",
    "timeframe",
}  # page contracts 1: written bare; title and description quoted


def apply_edits(v: Vault, edits: list[dict], slots: dict[str, str]) -> None:
    """Apply one option's edits to the files as checked (machine interface, 'Fixes')."""
    by_file: dict[str, list[dict]] = {}
    renames: list[dict] = []
    for ed in edits:
        if ed["action"] in ("rename-file", "delete-file"):
            renames.append(ed)
        else:
            by_file.setdefault(ed["file"], []).append(ed)
    for file, eds in by_file.items():
        raw = v.read(file)
        lines = raw.splitlines(keepends=True)
        line_eds = [e for e in eds if e["action"] in ("replace-text", "delete-line")]
        field_eds = [e for e in eds if e["action"] in ("set-field", "delete-field")]
        for e in sorted(line_eds, key=lambda e: (e["line"], e.get("column") or 0), reverse=True):
            i = e["line"] - 1
            assert 0 <= i < len(lines), f"edit line {e['line']} outside {file}: {e}"
            body = lines[i].rstrip("\r\n")
            eol = lines[i][len(body) :]
            if e["action"] == "delete-line":
                if e["find"] != body:
                    raise FixError(
                        f"delete-line find {e['find']!r} is not line {e['line']} {body!r} of {file}"
                    )
                del lines[i]
                continue
            find, replace = e["find"], _sub_slots(e["replace"], slots)
            if find == "" or find not in body:
                raise FixError(
                    f"replace-text find {find!r} not on line {e['line']} {body!r} of {file}"
                )
            col = e.get("column")
            if col is not None:
                if body[col - 1 : col - 1 + len(find)] != find:
                    raise FixError(
                        f"replace-text find {find!r} is not at column {col} of line {e['line']} {body!r} of {file}"
                    )
                body = body[: col - 1] + replace + body[col - 1 + len(find) :]
            else:
                body = body.replace(find, replace)
            lines[i] = body.replace("\n", eol or "\n") + eol
        text = "".join(lines)
        for e in field_eds:
            text = _apply_field(file, text, e, slots)
        v.write(file, text.replace("\r\n", "\n"), crlf="\r\n" in raw)
    for e in renames:
        src = v.path(e["file"])
        if e["action"] == "delete-file":
            src.unlink()
        else:
            dest = v.path(e["to"]) if "/" in e["to"] else src.with_name(e["to"])
            src.rename(dest)


def _apply_field(file: str, text: str, e: dict, slots: dict[str, str]) -> str:
    key = e["field"]
    nl = "\r\n" if "\r\n" in text else "\n"
    lines = text.split(nl)
    if file.endswith(".toml"):
        new = f"{key} = {_sub_slots(str(e.get('value', '')), slots)}"
        pat = re.compile(rf"^{re.escape(key)}\s*=")
        idx = next((i for i, ln in enumerate(lines) if pat.match(ln)), None)
        if idx is None:
            lines.insert(0, new)
        else:
            lines[idx] = new
        return nl.join(lines)
    if lines[0].strip() != "---":  # a file with no frontmatter gets a block at the very top
        lines = ["---", "---"] + lines
    close = [i for i, ln in enumerate(lines) if ln.strip() == "---"][1]
    pat = re.compile(rf"^{re.escape(key)}\s*:")
    idx = next((i for i, ln in enumerate(lines[:close]) if pat.match(ln)), None)
    if e["action"] == "delete-field":
        if idx is not None:
            del lines[idx]
        return nl.join(lines)
    value = _sub_slots(str(e["value"]), slots)
    new = f"{key}: {value if key in BARE_FIELDS else json.dumps(value, ensure_ascii=False)}"
    if idx is None:
        lines.insert(close, new)
    else:
        end = idx + 1  # the field's whole value goes: its continuation lines too
        while end < close and (lines[end].startswith((" ", "\t")) or lines[end].startswith("- ")):
            end += 1
        lines[idx:end] = [new]
    return nl.join(lines)


def run_command(v: Vault, argv: list[str]) -> tuple[int, str]:
    return scat_main(*argv, "--root", str(v.root))


def apply_option(v: Vault, option: dict, slots: dict[str, str] | None = None) -> None:
    """An option applies its edits, then its command."""
    slots = slots or {}
    apply_edits(v, option.get("edits", []), slots)
    if option.get("command"):
        argv = [_sub_slots(a, slots) for a in option["command"]["argv"]]
        code, out = run_command(v, argv)
        if code != 0:
            raise FixError(f"command {argv} failed ({code}): {out[:400]}")


def options_of(p: Problem) -> list[dict]:
    fix = p.fix
    return fix["options"] if fix.get("options") else [fix]


def rule_counts(problems: list[Problem]) -> dict[str, int]:
    out: dict[str, int] = {}
    for p in problems:
        out[p.rule] = out.get(p.rule, 0) + 1
    return out


def check_fix_clears(
    v: Vault,
    tmp_factory,
    problem: Problem,
    before: list[Problem],
    slots: dict[str, str] | None = None,
    no_other: bool = True,
) -> list[str]:
    """Apply every applicable option of the problem's fix, each to a fresh copy. Return the failures.

    A fix clears its mismatch when the count of messages of that rule drops by one, and it creates no other when no
    rule's count rises and no rule appears that was not there.
    """
    failures: list[str] = []
    want_before = rule_counts(before)
    existing = set(v.snapshot())
    for n, option in enumerate(options_of(problem), start=1):
        if not option.get("edits") and not option.get("command"):
            continue  # advisory or manual: nothing to apply
        copy = v.copy_to(tmp_factory())
        label = f"{problem.rule} option {n} ({option.get('text', '')[:70]!r})"
        try:
            apply_option(copy, option, slots)
        except FixError as boom:
            failures.append(f"{label}: could not be applied: {boom}")
            continue
        after = [
            p for p in copy.check() if p.file in existing
        ]  # a page the fix creates is its own business
        got = rule_counts(after)
        deleting = any(e["action"] == "delete-line" for e in option.get("edits", []))
        dropped = want_before.get(problem.rule, 0) - got.get(problem.rule, 0)
        if dropped != 1 and not (deleting and dropped >= 1):
            failures.append(
                f"{label}: did not clear exactly its message; {problem.rule} {want_before.get(problem.rule, 0)} -> "
                f"{got.get(problem.rule, 0)}\n      now: {[p.brief() for p in after]}"
            )
        for rule, count in got.items():
            if no_other and rule != problem.rule and count > want_before.get(rule, 0):
                failures.append(
                    f"{label}: created another message ({rule} {want_before.get(rule, 0)} -> {count})\n"
                    f"      now: {[p.brief() for p in after]}"
                )
        extra = [r for r in got if r not in want_before and r != problem.rule]
        if extra and no_other:
            failures.append(f"{label}: created messages of new rules {extra}")
    return failures


# --------------------------------------------------------------------------------------------- an oracle for ends
CELL_SPLIT = re.compile(r"(?<!\\)\|")
LINK = re.compile(r"!?\[\[([^\]]*)\]\]")


def oracle_ends(v: Vault) -> list[tuple[str, int, str, str, str]]:
    """For every row end in the vault that is not a link or not a node: (file, row n, cell, kind, narrative status).

    kind is 'nolink', 'nopage' or 'notnode'. Written from the page contracts' reading of the table, with no use of
    the tool: the first table under a heading `Edges told`, rows below the separator, cells between unescaped bars.
    """
    pages: dict[str, str] = {}
    for p in sorted(v.root.rglob("*.md")):
        if any(part.startswith(".") for part in p.relative_to(v.root).parts):
            continue
        text = p.read_bytes().decode("utf-8").replace("\r\n", "\n")
        m = re.match(r"---\n(.*?)\n---\n", text, re.DOTALL)
        if not m:
            continue
        t = re.search(r"^type:\s*(\S+)\s*$", m.group(1), re.MULTILINE)
        if t:
            pages[p.stem] = t.group(1)
    found = []
    for p in sorted(v.root.rglob("*.md")):
        rel = str(p.relative_to(v.root))
        text = p.read_bytes().decode("utf-8").replace("\r\n", "\n")
        if pages.get(p.stem) != "narrative":
            continue
        st = re.search(r"^status:\s*(\S+)", text, re.MULTILINE).group(1)
        lines = text.split("\n")
        start = next(
            (
                i
                for i, ln in enumerate(lines)
                if re.match(r"#+\s*edges told\s*$", ln, re.IGNORECASE)
            ),
            None,
        )
        if start is None:
            continue
        table = []
        for ln in lines[start + 1 :]:
            if ln.strip().startswith("|"):
                table.append(ln)
            elif table:
                break
            elif ln.strip() == "":
                continue
            else:
                break
        for n, row in enumerate(table[2:], start=1):
            cells = [c.strip() for c in CELL_SPLIT.split(row.strip())[1:-1]]
            if len(cells) != 4:
                continue
            for name, cell in (("from", cells[1]), ("to", cells[2])):
                links = LINK.findall(cell)
                stripped = LINK.sub("", cell).strip()
                if len(links) != 1 or stripped:
                    found.append((rel, n, name, "nolink", st))
                    continue
                target = re.split(r"[|#^]", links[0].replace("\\", ""))[0].strip()
                if target not in pages:
                    found.append((rel, n, name, "nopage", st))
                elif pages[target] not in ("group", "concern", "affordance", "technology"):
                    found.append((rel, n, name, "notnode", st))
    return found


END_RULE = {"nolink": "END-NOLINK", "nopage": "END-NOPAGE", "notnode": "END-NOTNODE"}


def unseen_mismatches(v: Vault, problems: list[Problem] | None = None) -> list[str]:
    """Row ends that are not a node or not a link and have no message of the right rule, and messages of the end
    rules with no such end."""
    problems = problems if problems is not None else v.check()
    ends = oracle_ends(v)
    have = {(p.file, p.where): p for p in problems if "-END-" in p.rule}
    out = []
    seen = set()
    for file, n, cell, kind, st in ends:
        key = (file, f"row {n} cell `{cell}`")
        seen.add(key)
        p = have.get(key)
        want_rule, want_sev = pair(END_RULE[kind], st)
        if p is None:
            out.append(f"unseen: {file} row {n} {cell} ({kind}) has no message")
        elif (p.rule, p.severity) != (want_rule, want_sev):
            out.append(
                f"{file} row {n} {cell}: expected {want_sev} {want_rule}, got {p.severity} {p.rule}"
            )
    for key, p in have.items():
        if key not in seen:
            out.append(f"spurious: {p.brief()}")
    return out
