"""Trial adapter: rewrite [[wikilinks]] in page BODIES to OKF markdown links, or back.

usage: python -I wiki2md.py {to-md|to-wiki} SRC_DIR DST_DIR
Frontmatter is copied byte-for-byte (OKF has no typed-link syntax there).
Page name = filename stem; flat directory, so the link target is the percent-encoded file name.
"""
import re, sys
from pathlib import Path
from urllib.parse import quote, unquote

WIKI = re.compile(r"\[\[([^\]|#]+)(#[^\]|]*)?(\|[^\]]*)?\]\]")
MD = re.compile(r"\[([^\]]*)\]\(([^)\s]+?)\.md(#[^)]*)?\)")

def split(text):
    if not text.startswith("---\n"):
        return "", text
    end = text.index("\n---\n", 4) + 5
    return text[:end], text[end:]

def to_md(body):
    def r(m):
        name, head, alias = m.group(1), m.group(2) or "", (m.group(3) or "")[1:]
        label = alias or name
        return f"[{label}]({quote(name)}.md{head})"
    return WIKI.sub(r, body)

def to_wiki(body):
    def r(m):
        label, name, head = m.group(1), unquote(m.group(2)), m.group(3) or ""
        return f"[[{name}{head}]]" if label == name else f"[[{name}{head}|{label}]]"
    return MD.sub(r, body)

mode, src, dst = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
dst.mkdir(parents=True, exist_ok=True)
f = to_md if mode == "to-md" else to_wiki
for p in sorted(src.glob("*.md")):
    fm, body = split(p.read_text(encoding="utf-8"))
    (dst / p.name).write_text(fm + f(body), encoding="utf-8")
