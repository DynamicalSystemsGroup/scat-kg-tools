"""Page names and titles: the contract's section 2."""

import re
import unicodedata

from scat_kg.tbox import TBOX

RESERVED = frozenset(
    {"con", "prn", "aux", "nul"} | {f"com{i}" for i in range(10)} | {f"lpt{i}" for i in range(10)}
)

MAX_NAME = 64
_SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")

# Page types a stub operation may create for a given name: the node types and the narrative (from the TBox).
STUBBABLE = (*TBOX.layers, TBOX.table_type.slug)


def name_problem(name: str) -> str | None:
    """Why `name` is not a legal page name (section 2), or None when it is."""
    if not name:
        return "the name is empty"
    if not _SLUG.fullmatch(name):
        return "a name uses only a-z, 0-9 and single hyphens, and starts and ends with a letter or digit"
    if len(name) > MAX_NAME:
        return f"a name is at most {MAX_NAME} characters (this one has {len(name)})"
    if name in RESERVED:
        return f"`{name}` is a reserved name"
    return None


def title_from_name(name: str) -> str:
    """The title a stub gets: each `-` a space, first letter upper case (section 5)."""
    text = name.replace("-", " ")
    return text[:1].upper() + text[1:]


def stem_of(title: str) -> str:
    """Steps 1 to 3 of section 2: the name a title gives before any clash is resolved ('' if none)."""
    decomposed = unicodedata.normalize("NFKD", title)
    kept = "".join(c for c in decomposed if not unicodedata.category(c).startswith("M")).lower()
    return re.sub(r"[^a-z0-9]+", "-", kept).strip("-")[:MAX_NAME].rstrip("-")


def derive_name(title: str, taken: set[str]) -> str | None:
    """The page name for a title (section 2). `taken` holds lower-cased names that are in use.

    None when the title has no Latin letter or digit: the name is then chosen by hand.
    """
    stem = stem_of(title)
    if not stem:
        return None

    def free(n: str) -> bool:
        return n.lower() not in taken and n not in RESERVED

    if free(stem):
        return stem
    n = 2
    while True:
        suffix = f"-{n}"
        candidate = stem[: MAX_NAME - len(suffix)].rstrip("-") + suffix
        if free(candidate):
            return candidate
        n += 1


def quote(text: str) -> str:
    """A one-line YAML double-quoted scalar, as the tools always write title and description."""
    one_line = re.sub(r"\s*[\r\n]+\s*", " ", text).strip()
    return '"' + one_line.replace("\\", "\\\\").replace('"', '\\"') + '"'
