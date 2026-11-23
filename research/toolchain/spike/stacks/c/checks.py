"""Stack C checks: no graph store; markdown + frontmatter + wikilinks parsed per call.

    check_page(vault, stem)          the page alone (its outgoing links resolved against the directory)
    check_neighborhood(vault, stem)  the page plus every page within one link, either direction
    check_vault(vault)               every page

Every Violation carries file, field, rule id, message and fix (R-2). Nothing here writes (R-4).
"""

import difflib
import re
from dataclasses import dataclass
from pathlib import Path

import yaml
from pydantic import ValidationError

from .models import MODELS, STATUSES, WIKILINK

try:
    _Loader = yaml.CSafeLoader
except AttributeError:  # pragma: no cover - libyaml missing
    _Loader = yaml.SafeLoader

LINK_ONLY = re.compile(r"^\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]$")


def _a(name):
    return ("an " if name[0] in "AEIOU" else "a ") + name


SLUG_OF_CLASS = {m.CLASS: slug for slug, m in MODELS.items()}


@dataclass(frozen=True)
class Violation:
    file: str
    field: str
    rule: str
    message: str
    fix: str

    def __str__(self):
        return (
            f"{self.file}: field `{self.field}`: [{self.rule}] {self.message}\n    fix: {self.fix}"
        )


class Page:
    """One parsed page: raw frontmatter dict, body text, and parse problems."""

    def __init__(self, stem, text):
        self.stem = stem
        self.file = f"{stem}.md"
        self.fm = None
        self.body = ""
        self.error = None
        self.model = None
        self.model_errors = []
        if not text.startswith("---\n"):
            self.error = "no frontmatter block (file must start with a line `---`)"
            return
        end = text.find("\n---\n", 3)
        if end < 0:
            end = text.find("\n---", 3)
            if end < 0 or text[end + 4 :].strip("\n"):
                self.error = "frontmatter block is not closed by a line `---`"
                return
        try:
            fm = yaml.load(text[4 : end + 1], Loader=_Loader)
        except yaml.YAMLError as e:
            self.error = f"frontmatter is not valid YAML ({str(e).splitlines()[0]})"
            return
        if not isinstance(fm, dict):
            self.error = "frontmatter is not a key: value mapping"
            return
        self.fm = fm
        self.body = text[end + 5 :]

    @property
    def type(self):
        return self.fm.get("type") if self.fm else None

    def validate(self):
        cls = MODELS.get(self.type)
        if cls is None:
            return
        try:
            self.model = cls.model_validate(self.fm)
        except ValidationError as e:
            self.model_errors = e.errors()

    def link_fields(self):
        """(field, [raw entries]) for the link fields this page's type declares."""
        cls = MODELS.get(self.type)
        if cls is None:
            return []
        return [(f, self.fm[f]) for f in cls.LINKS if self.fm.get(f) is not None]

    def body_links(self):
        return [m.group(1).strip() for m in WIKILINK.finditer(self.body)]


class Vault:
    """A directory of <stem>.md files. Caches parsed pages for the life of the object only."""

    def __init__(self, directory):
        self.dir = Path(directory)
        self.stems = sorted(p.stem for p in self.dir.glob("*.md"))
        self._stemset = set(self.stems)
        self._pages = {}

    def exists(self, stem):
        return stem in self._stemset

    def page(self, stem):
        if stem not in self._pages:
            p = Page(stem, (self.dir / f"{stem}.md").read_text(encoding="utf-8"))
            self._pages[stem] = p
        return self._pages[stem]

    def of_class(self, cls_name):
        slug = SLUG_OF_CLASS[cls_name]
        return [s for s in self.stems if self.page(s).type == slug]

    def inbound(self, stem):
        """Pages that link to `stem` anywhere (frontmatter or body); scans every file's text."""
        out = []
        for s in self.stems:
            if s == stem:
                continue
            text = (self.dir / f"{s}.md").read_text(encoding="utf-8")
            if any(m.group(1).strip() == stem for m in WIKILINK.finditer(text)):
                out.append(s)
        return out


def _entries(raw):
    return raw if isinstance(raw, list) else None


def _fix_dangling(v, page, field, target):
    near = difflib.get_close_matches(target, v.stems, n=1, cutoff=0.8)
    if near:
        return (
            f"replace `[[{target}]]` with `[[{near[0]}]]` (the closest existing page name; "
            f"if you meant a new page instead, create {target}.md)"
        )
    cls = MODELS[page.type].LINKS.get(field)
    if cls:
        slug = SLUG_OF_CLASS[cls]
        return (
            f"create {target}.md containing the lines `---`, `type: {slug}`, `status: stub`, "
            f'`title: "{target.replace("-", " ").capitalize()}"`, `---`; '
            f"or point `{field}` at an existing {cls} page"
        )
    return f"create {target}.md (a stub page) or remove `[[{target}]]` from the body"


def _candidates(v, page, field, cls_name):
    """Existing pages of cls_name reachable one hop from this page via its other links."""
    found = []
    for f, raw in page.link_fields():
        for e in _entries(raw) or []:
            m = LINK_ONLY.match(e) if isinstance(e, str) else None
            if not m or not v.exists(m.group(1)):
                continue
            t = v.page(m.group(1))
            for g, r in t.link_fields():
                if MODELS[t.type].LINKS.get(g) == cls_name:
                    found += [
                        mm.group(1)
                        for x in _entries(r) or []
                        if isinstance(x, str) and (mm := LINK_ONLY.match(x))
                    ]
    return sorted(set(found))


def check_page(v, stem):
    p = v.page(stem)
    out = []
    F = p.file
    if p.error:
        return [
            Violation(
                F,
                "(frontmatter)",
                "SCAT-FM-PARSE",
                p.error,
                "start the file with `---`, then `type:`, `status:`, `title:` lines, then `---`",
            )
        ]
    if p.type not in MODELS:
        got = repr(p.type) if p.type is not None else "missing"
        return [
            Violation(
                F,
                "type",
                "SCAT-FM-TYPE",
                f"`type` is {got}, not a known page type",
                f"set `type:` to one of: {', '.join(sorted(MODELS))}",
            )
        ]
    p.validate()
    for e in p.model_errors:
        field = str(e["loc"][0]) if e["loc"] else "(page)"
        if e["type"] == "missing":
            fix = {
                "status": "add the line `status: draft` (or `stub`, or `done` if the page is complete)",
                "title": f'add the line `title: "{stem.replace("-", " ").capitalize()}"` (edit as wanted)',
            }.get(field, f"add the line `{field}: <value>`")
            out.append(
                Violation(
                    F, field, "SCAT-FM-REQUIRED", "required field is missing at every status", fix
                )
            )
        elif field == "status":
            out.append(
                Violation(
                    F,
                    "status",
                    "SCAT-FM-STATUS",
                    f"`status` is {p.fm.get('status')!r}",
                    f"set `status:` to one of: {', '.join(STATUSES)}",
                )
            )
        else:
            out.append(
                Violation(
                    F,
                    field,
                    "SCAT-FM-SHAPE",
                    f"{e['msg']} (got {e.get('input')!r})",
                    f"write `{field}` as a YAML list of quoted wikilinks "
                    f'(`- "[[stem]]"`) or, for text fields, a quoted string',
                )
            )
    done = p.fm.get("status") == "done"
    cls = MODELS[p.type]
    bad_fields = {str(e["loc"][0]) for e in p.model_errors if e["loc"]}
    if done and not p.fm.get("description") and "description" not in bad_fields:
        out.append(
            Violation(
                F,
                "description",
                "SCAT-DONE-DESCRIPTION",
                "required field is missing on a page with `status: done`",
                'add the line `description: "<one sentence>"` (only you can write the sentence); '
                "or, if the page is not finished, change `status: done` to `status: draft`",
            )
        )
    if done:
        for f in cls.REQUIRED_LINKS:
            raw = p.fm.get(f)
            if not raw:
                target = cls.LINKS[f]
                cand = _candidates(v, p, f, target)
                if cand:
                    ex = "".join(f'\n      - "[[{c}]]"' for c in cand)
                    hint = f"; found via pages this page already links, confirm they fit:\n      {f}:{ex}\n    "
                else:
                    pool = v.of_class(target)
                    hint = (
                        f"; no candidate derivable from this page's links; {len(pool)} {target} pages "
                        f"exist, e.g. {', '.join(f'[[{s}]]' for s in pool[:3])}"
                    )
                out.append(
                    Violation(
                        F,
                        f,
                        "SCAT-DONE-LINK",
                        f"{cls.CLASS} with `status: done` needs at least one `{f}` link "
                        f"(to {_a(target)} page)",
                        f"add `{f}:` listing at least one {target} page (which one is your choice{hint}) "
                        "-- or change `status: done` to `status: draft`",
                    )
                )
    # links: checked at every status (R-3)
    for f, raw in p.link_fields():
        ents = _entries(raw)
        if ents is None:
            out.append(
                Violation(
                    F,
                    f,
                    "SCAT-LINK-SHAPE",
                    f"`{f}` must be a list of quoted wikilinks, got {raw!r}",
                    f'write `{f}:` then an indented `- "[[stem]]"` line per link',
                )
            )
            continue
        want = cls.LINKS[f]
        for e in ents:
            m = LINK_ONLY.match(e) if isinstance(e, str) else None
            if not m:
                out.append(
                    Violation(
                        F,
                        f,
                        "SCAT-LINK-SHAPE",
                        f"entry {e!r} is not a quoted wikilink",
                        'write it as `- "[[stem]]"`',
                    )
                )
                continue
            t = m.group(1).strip()
            if not v.exists(t):
                out.append(
                    Violation(
                        F,
                        f,
                        "SCAT-LINK-DANGLING",
                        f"[[{t}]] does not exist (no file {t}.md)",
                        _fix_dangling(v, p, f, t),
                    )
                )
                continue
            tt = v.page(t)
            got = MODELS[tt.type].CLASS if tt.type in MODELS else None
            if got is not None and got != want:
                pool = [
                    s
                    for s in v.of_class(want)
                    if s not in {x[2:-2] for x in ents if isinstance(x, str)}
                ]
                out.append(
                    Violation(
                        F,
                        f,
                        "SCAT-LINK-ENDPOINT",
                        f"[[{t}]] is {_a(got)} page, but `{f}` must link {want} pages",
                        f"replace `[[{t}]]` with {_a(want)} page (your choice; e.g. "
                        f"{', '.join(f'[[{s}]]' for s in pool[:3])}; {len(pool)} available), "
                        f"or delete that line if the link is wrong",
                    )
                )
    for t in p.body_links():
        if not v.exists(t):
            out.append(
                Violation(
                    F,
                    "(body)",
                    "SCAT-LINK-DANGLING",
                    f"[[{t}]] does not exist (no file {t}.md)",
                    _fix_dangling(v, p, "(body)", t),
                )
            )
    return out


def neighborhood(v, stem):
    p = v.page(stem)
    outs = set()
    if p.fm is not None:
        for _, raw in p.link_fields():
            for e in _entries(raw) or []:
                m = LINK_ONLY.match(e) if isinstance(e, str) else None
                if m:
                    outs.add(m.group(1).strip())
        outs |= set(p.body_links())
    members = {stem} | {s for s in outs if v.exists(s)} | set(v.inbound(stem))
    return sorted(members)


def check_neighborhood(v, stem):
    return [x for s in neighborhood(v, stem) for x in check_page(v, s)]


def check_vault(v):
    return [x for s in v.stems for x in check_page(v, s)]
