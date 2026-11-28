"""merge: fold one node page into another of the same type.

`merge(a, b)` rewrites every link to `a` in the bodies of the narratives and node pages to a link to `b`, appends
`a`'s body to `b` under a heading that names `a`, drops `a`'s description (`b`'s is kept), removes `a`'s page and
makes sure the index pages exist. `b`'s status and other fields are untouched, and so is every page of a contributor
(a contributor page is outside the four layers: a merge never reads or writes one, and refuses when one links `a`).

Nothing is written until the whole merge has been tried out. Every new file text is built in memory, written into a
temporary copy of the vault, and judged there: the check must show no error the vault did not have, no link to `a`
may remain, and the knowledge graph must equal the old one with `a` renamed `b` (edges, the narratives that tell
them, fingerprints). Only then is the real vault written; otherwise the merge is refused and writes nothing.
`plan=True` does all of that and then writes nothing: it is what the merge would do.
"""

import re
import shutil
import tempfile
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from scat_tools.checks import check_vault
from scat_tools.graph import Graph, load, read_table
from scat_tools.ops.common import find_page, open_vault
from scat_tools.ops.files import NotUtf8, join_lines, line_ending, read_lines, replace_file
from scat_tools.ops.index import index
from scat_tools.ops.result import Refusal, Result, refused, reports_mode
from scat_tools.tbox import TBOX
from scat_tools.vault import (
    _BODY_LINK,
    CONTRIBUTOR,
    Page,
    Vault,
    blank_code,
    link_target,
    read_vault,
)

OP = "merge"
NARRATIVE = TBOX.table_type.slug
NODE_TYPES = ", ".join(TBOX.layers)
NAME_FIX = f"name two node pages of one type ({NODE_TYPES}): `scat merge A B` folds A into B"


@dataclass(frozen=True)
class MergeResult(Result):
    """What `merge` returns when it ran (or, with `plan`, when it would run)."""

    a: str = ""
    b: str = ""
    plan: bool = False
    removed: tuple[str, ...] = ()  # the page that was (or would be) removed: a's
    done_narratives: tuple[str, ...] = ()  # `done` narratives whose text changed (they stay `done`)
    links_rewritten: tuple[tuple[str, int], ...] = ()  # (file, links) for each file that holds some

    def to_dict(self) -> dict:
        out = super().to_dict()
        if self.ok:
            out["plan"] = self.plan
            out["removed"] = list(self.removed)
            out["done_narratives"] = list(self.done_narratives)
            out["links_rewritten"] = [{"file": f, "links": n} for f, n in self.links_rewritten]
        return out

    def lines(self) -> list[str]:
        if self.refused:
            return super().lines()
        count = dict(self.links_rewritten)
        total = sum(count.values())
        if self.plan:
            out = [
                f"merge plan: `{self.a}` is folded into `{self.b}`; nothing is written",
                f"  {total} link{'' if total == 1 else 's'} to `{self.a}` would be rewritten",
            ]
        else:
            out = [
                (
                    f"merged `{self.a}` into `{self.b}`: "
                    f"{total} link{'' if total == 1 else 's'} rewritten"
                ),
            ]
        w = self.plan
        out += [f"{'would create' if w else 'created'} {p}" for p in self.created]
        for p in self.changed:
            n = count.get(p)
            head = f"{'would change' if w else 'changed'} {p}"
            out.append(head + (f" ({n} link{'' if n == 1 else 's'})" if n else ""))
        out += [f"{'would remove' if w else 'removed'} {p}" for p in self.removed]
        if self.done_narratives:
            k = len(self.done_narratives)
            out.append(
                f"{'would change' if w else 'changed'} {k} `done` narrative{'' if k == 1 else 's'} "
                "(they stay `done`): " + ", ".join(self.done_narratives)
            )
        out += [f"note: {n}" for n in self.notes]
        return out


# ---------------------------------------------------------------------------------------------------------
# Refusals shared with the split plan
# ---------------------------------------------------------------------------------------------------------


def _not_node(page: Page, ref: str) -> Refusal:
    if page.type == CONTRIBUTOR:
        what = "a contributor page, and a merge never reads or writes one"
    elif page.type == NARRATIVE:
        what = "a narrative, not a node page"
    else:
        what = "not a node page"
    return Refusal(ref, f"{page.path} is {what}", NAME_FIX)


def _a(word: str) -> str:
    return f"an {word}" if word[:1] in "aeiou" else f"a {word}"


def resolve_node(op: str, vault: Vault, ref: object) -> tuple[Page | None, Refusal | None]:
    """The node page `ref` names (a name or a path), or the refusal that says why it is none."""
    if not isinstance(ref, str):
        return None, Refusal(repr(ref), "a page is named by a string", "pass the page's name")
    page, bad = find_page(op, vault, ref)
    if bad:
        return None, bad.refused[0]
    if page.type not in TBOX.layers:
        return None, _not_node(page, ref)
    return page, None


def linking_pages(vault: Vault, name: str) -> tuple[list[Page], list[tuple[Page, int]]]:
    """The pages whose body links `name`: those a merge may rewrite, and (page, line) of each contributor link."""
    by_path = {p.path: p for p in vault.pages}
    ok: dict[str, Page] = {}
    contributors: list[tuple[Page, int]] = []
    for b in vault.inbound(name):
        page = by_path[b.source]
        if page.type == CONTRIBUTOR:
            contributors.append((page, b.line))
        else:
            ok[page.path] = page
    return sorted(ok.values(), key=lambda p: p.path), contributors


def error_refusals(vault: Vault, paths: set[str]) -> list[Refusal]:
    """One refusal for each page in `paths` (and `scat.toml`) that has an error: the pages an operation reads."""
    report = check_vault(vault)
    out = []
    for file in sorted({p.file for p in report.errors} & (paths | {"scat.toml"})):
        errs = [p for p in report.errors if p.file == file]
        out.append(
            Refusal(
                file,
                f"{len(errs)} error{'' if len(errs) == 1 else 's'} in a page this reads: "
                + "; ".join(f"[{p.rule}] {p.where}: {p.what}" for p in errs),
                f"run `scat check {file}`, fix what it names, then run this again",
            )
        )
    return out


# ---------------------------------------------------------------------------------------------------------
# Rewriting links
# ---------------------------------------------------------------------------------------------------------


def _new_link(inner: str, a: str, b: str, alias: bool, escape: bool) -> str:
    """The link text `[[...]]` for `[[inner]]` with the target `a` made `b`, the heading and alias kept.

    A bare name gets the alias `a` (so the reader still sees `a`), its bar escaped in a table line.
    """
    head = re.split(r"[|#^]", inner, maxsplit=1)[0]
    rest = inner[len(head) :]
    name = head.rstrip("\\").strip()
    at = head.index(name)
    head = head[:at] + b + head[at + len(name) :]
    if alias and not rest:
        rest = ("\\|" if escape else "|") + a
    return "[[" + head + rest + "]]"


def rewrite_body(
    body: list[str], a: str, b: str, narrative: bool
) -> tuple[list[str], int, list[tuple[int, str]]]:
    """The body lines with every page link to `a` pointed at `b`, how many were rewritten, and the
    (line index, heading) of each rewritten link that names a heading.

    A link in code (a fence or a span) is not a link and is left. A bare link in prose becomes `[[b|a]]`; a link
    that is a whole `from` or `to` cell of an `Edges told` row stays bare, `[[b]]`; an embed stays bare too; an
    alias, a heading or a block reference is kept. Every other character is kept.
    """
    blanked = blank_code("\n".join(body)).split("\n")
    ends: set[tuple[int, int, int]] = set()
    if narrative:
        table = read_table(body, 0).table
        for row in table.rows if table else ():
            for cell in (row.cell("from"), row.cell("to")):
                if cell is not None and cell.target == a:
                    ends.add((cell.line, cell.start, cell.end))
    out, count, headings = [], 0, []
    for i, line in enumerate(body):
        hits = [m for m in _BODY_LINK.finditer(blanked[i]) if link_target(m.group(1)) == a]
        for m in reversed(hits):
            inner = line[m.start() + 2 : m.end() - 2]
            if link_target(inner) != a:
                continue
            embed = m.start() > 0 and line[m.start() - 1] == "!"
            bare = embed or any(i == n and s <= m.start() and m.end() <= e for n, s, e in ends)
            if (h := re.match(r"[^|#^]*#([^|^]*)", inner)) and h.group(1).strip():
                headings.append((i, h.group(1).replace("\\", "").strip()))
            new = _new_link(inner, a, b, alias=not bare, escape=line.lstrip().startswith("|"))
            line = line[: m.start()] + new + line[m.end() :]
            count += 1
        out.append(line)
    return out, count, headings


_HEADING = re.compile(r"^ {0,3}#{1,6}[ \t]+(.*?)(?:[ \t]+#+)?[ \t]*$")


def _headings(lines: list[str]) -> set[str]:
    """The ATX headings in lines, lower-cased."""
    return {m.group(1).strip().casefold() for ln in lines if (m := _HEADING.match(ln))}


def _split(lines: list[tuple[str, str]]) -> int:
    """The index of the first body line: the line after the closing `---` of the frontmatter."""
    texts = [t for t, _ in lines]
    return texts.index("---", 1) + 1


@dataclass
class _Plan:
    old: dict[str, bytes]  # path -> bytes as they are
    new: dict[str, bytes]  # path -> bytes as they would be (a's page is not here: it is removed)
    counts: dict[str, int]  # path -> links rewritten
    done: list[str]  # names of `done` narratives whose text changes
    appended: bool  # a's body goes into b
    notes: list[str]  # links whose heading now reaches b's own section


def _build(vault: Vault, a: Page, b: Page) -> _Plan | Refusal:
    """The new text of every file a merge writes."""
    pages, _ = linking_pages(vault, a.name)
    todo = {p.path: p for p in pages} | {a.path: a, b.path: b}
    old, new, counts, done = {}, {}, {}, []
    a_body: list[str] = []
    heads: list[tuple[str, int, str]] = []  # (path, file line, heading) of a link to a heading
    for path, page in sorted(todo.items()):
        try:
            lines, bom = read_lines(vault.root / path)
        except NotUtf8 as e:
            return Refusal(path, str(e), "save the file as UTF-8, then run this again")
        first = _split(lines)
        body, n, hs = rewrite_body(
            [t for t, _ in lines[first:]], a.name, b.name, page.type == NARRATIVE
        )
        if path != a.path:
            heads += [(path, first + i + 1, h) for i, h in hs]
        lines = lines[:first] + [(t, e) for t, (_, e) in zip(body, lines[first:], strict=True)]
        old[path] = (vault.root / path).read_bytes()
        counts[path] = n
        if path == a.path:
            a_body = body
        elif path == b.path:
            b_lines, b_bom, b_first = lines, bom, first
        else:
            if n:
                new[path] = join_lines(lines, bom)
                if page.type == NARRATIVE and page.status == "done":
                    done.append(page.name)
    # b: its own links rewritten, then a's body under a heading that names a
    while a_body and not a_body[0].strip():
        a_body.pop(0)
    while a_body and not a_body[-1].strip():
        a_body.pop()
    appended = bool(a_body)
    both = _headings(a_body) & _headings([t for t, _ in b_lines[b_first:]])
    clash = [
        f"the link `[[{a.name}#{h}]]` at {path} line {n} now reaches the section `{h}` that "
        f"`{b.name}` already had, not the one added from `{a.name}`"
        for path, n, h in sorted(heads)
        if h.casefold() in both
    ]
    if appended:
        eol = line_ending(b_lines)
        while b_lines and not b_lines[-1][0].strip():
            b_lines.pop()
        if b_lines and not b_lines[-1][1]:
            b_lines[-1] = (b_lines[-1][0], eol)
        b_lines += [("", eol), (f"## From {a.name}", eol), ("", eol)]
        b_lines += [(t, eol) for t in a_body]
    if appended or counts[b.path]:
        new[b.path] = join_lines(b_lines, b_bom)
    # a's own links to itself count where they land: in b
    counts[b.path] += counts.pop(a.path)
    return _Plan(
        {p: old[p] for p in new},
        new,
        {p: n for p, n in counts.items() if n},
        sorted(done),
        appended,
        clash,
    )


# ---------------------------------------------------------------------------------------------------------
# Trying it out
# ---------------------------------------------------------------------------------------------------------

_LINK = re.compile(r"\[\[([^\[\]\n]*)\]\]")


def _plain(note: str, a: str, b: str) -> str:
    """A row's note with each link read as the name it reaches (`a` read as `b`): notes compare as text."""
    return _LINK.sub(lambda m: f"[[{b if (t := link_target(m.group(1))) == a else t}]]", note)


def _snapshot(g: Graph, a: str, b: str, rename: bool) -> dict:
    """Nodes, edges with their tellings, and fingerprints; with `rename`, `a` read as `b`."""

    def r(n: str) -> str:
        return b if rename and n == a else n

    edges: dict[tuple, set] = {}
    for e in g.edges:
        edges.setdefault((e.type, r(e.from_node), r(e.to_node)), set()).update(
            (t.narrative, _plain(t.note, a, b)) for t in e.tellings
        )
    return {
        "nodes": {r(n.name) for ns in g.nodes.values() for n in ns},
        "edges": edges,
        "fingerprints": {
            n.name: (
                frozenset(r(x) for x in n.nodes),
                frozenset((k.type, r(k.from_node), r(k.to_node)) for k in n.edges),
            )
            for n in g.narratives
        },
        "excluded": {x.narrative for x in g.excluded},
        "skipped": len(g.skipped),
        "unreadable": len(g.unreadable),
    }


def _graph_differences(before: Graph, after: Graph, a: str, b: str) -> list[str]:
    was, now = _snapshot(before, a, b, True), _snapshot(after, a, b, False)
    out = []
    for key, what in (
        ("nodes", "the nodes"),
        ("edges", "the edges or the narratives that tell them"),
        ("fingerprints", "a narrative's fingerprint"),
        ("excluded", "the narratives left out as uncoded"),
        ("skipped", "the rows that tell no edge"),
        ("unreadable", "the pages with unreadable frontmatter"),
    ):
        if was[key] != now[key]:
            out.append(f"{what} would differ from the old graph with `{a}` renamed `{b}`")
    return out


def _error_key(p) -> tuple:
    return (p.rule, p.file, p.where, p.what)


def _try_out(
    vault: Vault, before: Graph, a: Page, b: Page, plan: _Plan
) -> tuple[list[str], list[str]]:
    """Write the merge into a temporary copy of the vault and judge it: (why not, index files made)."""
    with tempfile.TemporaryDirectory(prefix="scat-merge-") as td:
        tmp = Path(td) / "vault"
        shutil.copytree(vault.root, tmp, ignore=shutil.ignore_patterns(".*"))
        for path, data in plan.new.items():
            replace_file(tmp / path, data)
        (tmp / a.path).unlink()
        made = index(root=tmp)
        if made.refused:
            return [f"{r.subject}: {r.why}" for r in made.refused], []
        after = read_vault(tmp)
        problems: list[str] = []
        new_errors = Counter(map(_error_key, check_vault(after).errors)) - Counter(
            map(_error_key, check_vault(vault).errors)
        )
        problems += [
            f"the merge would add an error: [{k[0]}] {k[1]}, {k[2]}: {k[3]}" for k in new_errors
        ]
        left = [
            f"{p.path} line {link.line}"
            for p in after.pages
            for link in p.links
            if link.target == a.name
        ]
        if left:
            problems.append(f"a link to `{a.name}` would remain: " + ", ".join(left))
        problems += _graph_differences(before, load(tmp), a.name, b.name)
        return problems, list(made.created)


# ---------------------------------------------------------------------------------------------------------
# The operation
# ---------------------------------------------------------------------------------------------------------


def _duplicate_rows(before: Graph, a: str, b: str) -> list[Refusal]:
    """The narratives where the merge would make two rows tell one edge: both rows are listed."""
    out = []
    for n in before.narratives:
        groups: dict[tuple, list] = {}
        for row in n.rows:
            if not row.well_formed or row.edge_type is None:
                continue
            ends = tuple(b if x == a else x for x in (row.from_target, row.to_target))
            groups.setdefault((row.edge_type, *ends), []).append(row)
        for rows in groups.values():
            same = {(r.edge_type, r.from_target, r.to_target) for r in rows}
            if len(same) > 1:
                where = " and ".join(f"line {r.line} `{r.text.strip()}`" for r in rows)
                fix = "delete one of the two rows (put its note in the other first), then run this again"
                if n.status == "done":
                    fix = (
                        f"this narrative is `done`: you move it out of `done` first (`scat set-status "
                        f"{n.name} draft`), then delete one of the two rows (put its note in the other "
                        "first), then run this again"
                    )
                out.append(
                    Refusal(
                        n.path,
                        f"the merge would make two rows tell one edge: {where}",
                        fix,
                    )
                )
    return out


@reports_mode
def merge(a: str, b: str, *, plan: bool = False, root: str | Path = ".") -> Result:
    """Fold node page `a` into node page `b` of the same type. With `plan=True`, show it and write nothing."""
    if not isinstance(plan, bool):
        return refused(OP, repr(plan), "plan must be True or False", "pass True or False")
    vault, bad = open_vault(OP, root)
    if bad:
        return bad
    pa, ra = resolve_node(OP, vault, a)
    pb, rb = resolve_node(OP, vault, b)
    if ra or rb:
        return Result(OP, refused=tuple(r for r in (ra, rb) if r))
    if pa.path == pb.path:
        return refused(OP, a, "the two names are the same page", NAME_FIX)
    if pa.type != pb.type:
        return refused(
            OP,
            f"{a} and {b}",
            f"`{a}` is {_a(pa.type)} and `{b}` is {_a(pb.type)}: a merge needs two pages of one type",
            NAME_FIX,
        )
    pages, contributors = linking_pages(vault, pa.name)
    at: dict[str, list[int]] = {}
    for page, line in contributors:
        at.setdefault(page.path, []).append(line)
    refusals = [
        Refusal(
            path,
            f"this contributor page links `{pa.name}` at line "
            + ", ".join(str(n) for n in sorted(set(lines)))
            + ", and a merge never writes one",
            "take the link out of the contributor page by hand, then run this again",
        )
        for path, lines in sorted(at.items())
    ]
    refusals += error_refusals(vault, {pa.path, pb.path} | {p.path for p in pages})
    before = load(root)
    refusals += _duplicate_rows(before, pa.name, pb.name)
    if refusals:
        return Result(OP, refused=tuple(refusals))
    built = _build(vault, pa, pb)
    if isinstance(built, Refusal):
        return Result(OP, refused=(built,))
    try:
        why, made = _try_out(vault, before, pa, pb, built)
    except OSError as e:
        return Result(
            OP,
            refused=(
                Refusal(
                    "the vault",
                    f"could not write: {e}",
                    "check the permissions of the vault's folders, then run this again",
                ),
            ),
        )
    if why:
        return Result(
            OP,
            refused=tuple(
                Refusal(
                    f"{a} and {b}",
                    w,
                    "nothing was written; look at the pages the merge changes by hand, "
                    "or fix the vault, then run this again",
                )
                for w in why
            ),
        )
    if not plan:
        if bad := _write(vault, pa, built):
            return Result(OP, refused=(bad,))
        made = list(index(root=root).created)
    notes = [
        f"the body of `{pa.name}` is appended to `{pb.name}` under `## From {pa.name}`"
        if built.appended
        else f"`{pa.name}` has no body, so nothing is appended to `{pb.name}`",
        (
            f"the description of `{pa.name}` is dropped; `{pb.name}` keeps its own, and its status "
            f"(`{pb.fields.get('status')}`) and other fields are unchanged"
        ),
    ]
    if isinstance(pa.fields.get("description"), str) and not pb.fields.get("description"):
        notes.append(f"`{pb.name}` has no description: add one, `{pa.name}`'s is not kept")
    notes += built.notes
    frontmatter = [
        f"{p.path} (field `{k}`)"
        for p in vault.pages
        if p.type != CONTRIBUTOR
        for k in _fm(p, pa.name)
    ]
    if frontmatter:
        notes.append(
            f"a link to `{pa.name}` in frontmatter is not rewritten (a merge rewrites bodies only): "
            + ", ".join(frontmatter)
        )
    if built.done:
        notes.append(
            "a `done` narrative whose text changes stays `done`: read it again before you rely on it"
        )
    return MergeResult(
        OP,
        created=tuple(sorted(made)),
        changed=tuple(sorted(built.new)),
        notes=tuple(notes),
        a=pa.name,
        b=pb.name,
        plan=plan,
        removed=(pa.path,),
        done_narratives=tuple(built.done),
        links_rewritten=tuple(sorted(built.counts.items())),
    )


def _fm(page: Page, name: str) -> list[str]:
    """The frontmatter fields of `page` that hold a link to `name`."""

    def has(v) -> bool:
        if isinstance(v, str):
            return any(link_target(m.group(1)) == name for m in _BODY_LINK.finditer(v))
        if isinstance(v, list | tuple):
            return any(has(x) for x in v)
        if isinstance(v, dict):
            return any(has(x) for x in v.values())
        return False

    return [k for k, v in page.fields.items() if has(v)]


def _write(vault: Vault, a: Page, plan: _Plan) -> Refusal | None:
    """Write the changed files, then remove a's page; on a failure put everything back."""
    root = vault.root
    for path, was in plan.old.items():
        if (root / path).read_bytes() != was:
            return Refusal(
                path, "the file changed while the merge was being prepared", "run this again"
            )
    a_was = (root / a.path).read_bytes()
    done: list[str] = []
    try:
        for path, data in sorted(plan.new.items()):
            replace_file(root / path, data)
            done.append(path)
        (root / a.path).unlink()
    except BaseException as e:
        lost = []
        for path in done:
            try:
                replace_file(root / path, plan.old[path])
            except OSError:
                lost.append(path)
        try:
            if not (root / a.path).exists():
                (root / a.path).write_bytes(a_was)
        except OSError:
            lost.append(a.path)
        if not isinstance(e, OSError):
            if lost:
                e.add_note("could not be restored: " + ", ".join(lost))
            raise
        why = f"could not write: {e}"
        if lost:
            why += "; these files could not be put back as they were: " + ", ".join(lost)
        return Refusal("the vault", why, "check the files' permissions")
    return None
