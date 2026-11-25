"""Small text tools the rules share: names, near matches, and the pieces of a fix."""

import difflib
import re
import unicodedata

RESERVED = frozenset(
    {"con", "prn", "aux", "nul"} | {f"com{i}" for i in range(10)} | {f"lpt{i}" for i in range(10)}
)


def is_missing(value) -> bool:
    """The catalogue's Empty rule: absent, null, a blank string or an empty list."""
    return value is None or (isinstance(value, str) and not value.strip()) or value == []


def name_problem(name: str) -> str | None:
    """Why `name` is not a legal page name (contract section 2), or None when it is legal."""
    bad = next((c for c in name if not ("a" <= c <= "z" or "0" <= c <= "9" or c == "-")), None)
    if bad is not None:
        return f"it contains `{bad}`, outside a-z, 0-9 and -"
    if not name:
        return "it is empty"
    if name.startswith("-") or name.endswith("-"):
        return "it starts or ends with a hyphen"
    if "--" in name:
        return "it has two hyphens in a row"
    if len(name) > 64:
        return "it is longer than 64 characters"
    if name in RESERVED:
        return "it is a reserved name"
    return None


def stem(text: str) -> str:
    """Steps 1 to 3 of the contract's name-from-title rule (empty when nothing is left)."""
    decomposed = unicodedata.normalize("NFKD", text)
    s = "".join(c for c in decomposed if not unicodedata.category(c).startswith("M")).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:64].rstrip("-")


def free_name(text: str, taken: set[str]) -> str | None:
    """Step 4: the free derived name. `taken` holds lower-case names of existing .md files."""
    base = stem(text)
    if not base:
        return None

    def is_taken(n: str) -> bool:
        return n in RESERVED or n in taken

    if not is_taken(base):
        return base
    i = 2
    while True:
        suffix = f"-{i}"
        name = base[: 64 - len(suffix)].rstrip("-") + suffix
        if not is_taken(name):
            return name
        i += 1


def derived_name(text: str, taken: set[str]) -> str | None:
    """The stem, or the free derived name when the stem is reserved (catalogue, "Legal name")."""
    base = stem(text)
    if not base:
        return None
    return free_name(text, taken) if base in RESERVED else base


def near_match(text: str, names) -> str | None:
    """The catalogue's near match: highest ratio, at least 0.8, ties to the first in byte order."""
    best, best_ratio = None, 0.0
    for n in sorted(set(names), key=lambda s: s.encode()):
        ratio = difflib.SequenceMatcher(None, text.lower(), n.lower()).ratio()
        if ratio >= 0.8 and ratio > best_ratio:
            best, best_ratio = n, ratio
    return best


def title_from_name(name: str) -> str:
    """The title a stub gets: each `-` a space, the first letter upper case."""
    t = name.replace("-", " ")
    return t[:1].upper() + t[1:]


def quote(text: str) -> str:
    """A YAML double-quoted scalar, as the contract writes one (`"` is `\\"`, `\\` is `\\\\`)."""
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def set_status_cmd(name: str, status: str = "draft") -> str:
    return f'`scat set-status {name} {status}` (REPL: `scat_kg.set_status("{name}", "{status}")`)'


def stub_cmd(name: str, type_key: str) -> str:
    return (
        f'`scat stub {name} --type {type_key}` (REPL: `scat_kg.stub("{name}", type="{type_key}")`)'
    )


def one(text: str) -> str:
    return f"Fix: {text}"


def choose(options: list[str], notes: tuple[str, ...] = (), head: str | None = None) -> str:
    """A fix with alternatives, numbered. One alternative is just a fix. Notes follow, unnumbered."""
    if len(options) == 1 and head is None:
        out = one(options[0])
    else:
        rows = [head or "Fix, choose one:"]
        for i, o in enumerate(options, 1):
            first, *more = o.split("\n")
            rows.append(f"  {i}. {first}")
            rows.extend(more)
        out = "\n".join(rows)
    return "\n".join([out, *notes])


def steps(items: list[str], head: str = "Fix, two steps:") -> str:
    rows = [head]
    for i, s in enumerate(items, 1):
        first, *more = s.split("\n")
        rows.append(f"     {i}. {first}")
        rows.extend(more)
    return "\n".join(rows)


def capped(items: list[str], limit: int = 8) -> tuple[list[str], int]:
    return items[:limit], max(0, len(items) - limit)


def article(word: str) -> str:
    return "an" if word[:1] in "aeiou" else "a"
