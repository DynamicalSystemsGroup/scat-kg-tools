"""Shared page parser for the spike: frontmatter + wikilinks -> dict.

Usage: uv run python common.py <vault-dir>   (prints page and link counts)
"""
import re
import sys
from pathlib import Path

import frontmatter

WIKILINK = re.compile(r"\[\[([^\]|#]+?)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")


def _strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for v in value.values():
            yield from _strings(v)
    elif isinstance(value, (list, tuple)):
        for v in value:
            yield from _strings(v)


def parse_page(path):
    """Return {name, path, meta, body, fm_links, body_links, links}.

    name = filename stem (what Obsidian shows). links = targets in frontmatter
    values and body, in order, de-duplicated.
    """
    path = Path(path)
    post = frontmatter.load(path)
    fm_links = [m.strip() for s in _strings(post.metadata) for m in WIKILINK.findall(s)]
    body_links = [m.strip() for m in WIKILINK.findall(post.content)]
    return {
        "name": path.stem,
        "path": str(path),
        "meta": dict(post.metadata),
        "body": post.content,
        "fm_links": fm_links,
        "body_links": body_links,
        "links": list(dict.fromkeys(fm_links + body_links)),
    }


def parse_vault(vault_dir):
    return [parse_page(p) for p in sorted(Path(vault_dir).glob("*.md"))]


if __name__ == "__main__":
    pages = parse_vault(sys.argv[1])
    print(f"pages={len(pages)} links={sum(len(p['links']) for p in pages)}")
