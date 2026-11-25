"""Obsidian's table editor re-pads columns (D-088, page contracts 4 'Cells'): a padded table, a table of alias links,
`\\|` in cells, tabs and no-break spaces, CRLF lines, all give the same messages as the compact form, and their fixes
still apply and clear."""

import pytest
from indep_kit import (
    NARRATIVE_FILE as NF,
)
from indep_kit import (
    STATUSES,
    Vault,
    check_fix_clears,
    narrative_text,
)

NBSP = " "
CLEAN = [
    ("holds", "[[borrowers]]", "[[quick-checkout]]", "Said twice."),
    ("is addressed by", "[[quick-checkout|the checkout]]", "[[self-checkout\\|the desk]]", ""),
    ("is provided by", "![[self-checkout]]", "[[booking-app]]", "a \\| b"),
    ("addressed-by", "[[safe-handling]]", "[[self-checkout]]", "slug spelling"),
]
DEFECTS = {
    "nolink": ("holds", "volunteers", "[[safe-handling]]", ""),
    "empty": ("holds", "", "[[safe-handling]]", ""),
    "nopage": ("holds", "[[ghost]]", "[[safe-handling]]", ""),
    "notnode": ("holds", "[[saturday]]", "[[safe-handling]]", ""),
    "layers": ("holds", "[[quick-checkout]]", "[[volunteers]]", "wrong way"),
    "type": ("owns", "[[volunteers]]", "[[safe-handling]]", ""),
    "duplicate": ("holds", "[[borrowers]]", "[[quick-checkout]]", "again"),
    "two-links": ("holds", "[[volunteers]] [[borrowers]]", "[[safe-handling]]", ""),
}
STYLES = ["compact", "obsidian", "spaces", "tabs-nbsp", "crlf", "crlf-obsidian"]


def render(rows, style):
    head = ("type", "from", "to", "note")
    if style in ("compact", "crlf"):
        lines = ["| " + " | ".join(head) + " |", "|---|---|---|---|"]
        lines += ["| " + " | ".join(r) + " |" for r in rows]
    elif style in ("obsidian", "crlf-obsidian"):
        widths = [max(len(c[i]) for c in [head, *rows]) for i in range(4)]
        widths = [max(w, 3) for w in widths]
        fmt = lambda r: "| " + " | ".join(c.ljust(w) for c, w in zip(r, widths)) + " |"
        lines = [fmt(head), "| " + " | ".join("-" * w for w in widths) + " |"] + [
            fmt(r) for r in rows
        ]
    elif style == "spaces":
        lines = ["|   " + "   |   ".join(head) + "   |", "|  ---  |  ---  |  ---  |  ---  |"]
        lines += ["|   " + "   |   ".join(r) + "   |" for r in rows]
    else:  # tabs-nbsp
        lines = ["|\t" + "\t|\t".join(head) + "\t|", "|---|---|---|---|"]
        lines += ["|" + NBSP + ("|" + NBSP).join(c + NBSP for c in r) + "|" for r in rows]
    return lines


def build(tmp_path, rows, style, status):
    v = Vault(tmp_path / f"v-{style}-{status}")
    v.write("scat.toml", "stakeholder_group_cap = 3\n")
    from indep_kit import NODES, page_text

    for type_, items in NODES.items():
        for name, title in items:
            v.write(f"{type_}/{name}.md", page_text(type_, title))
    text = narrative_text(status, ())
    head, _ = text.split("| type | from | to | note |")
    crlf = style.startswith("crlf")
    v.write(NF, head + "\n".join(render(rows, style)) + "\n", crlf=crlf)
    return v


def norm(p):
    return (
        p.rule,
        p.severity,
        p.file,
        p.line,
        p.where,
        p.what,
        p.fix["kind"],
        len(p.fix.get("options", [])),
    )


@pytest.mark.parametrize("style", STYLES)
@pytest.mark.parametrize("st", STATUSES)
def test_clean_table_is_clean_in_every_form(tmp_path, st, style):
    v = build(tmp_path, CLEAN, style, st)
    assert [p.brief() for p in v.check()] == []


@pytest.mark.parametrize("style", [s for s in STYLES if s != "compact"])
@pytest.mark.parametrize("st", ("draft", "done"))
def test_padded_forms_give_the_messages_of_the_compact_form(tmp_path, st, style):
    rows = CLEAN + list(DEFECTS.values())
    compact = build(tmp_path, rows, "compact", st).check()
    assert len(compact) >= 8, [p.brief() for p in compact]  # the defects are really seen
    other = build(tmp_path, rows, style, st).check()
    assert sorted(map(norm, other), key=repr) == sorted(map(norm, compact), key=repr)


@pytest.mark.parametrize("style", ["obsidian", "tabs-nbsp", "crlf-obsidian"])
@pytest.mark.parametrize("name", sorted(DEFECTS))
def test_fixes_of_a_padded_table_apply_and_clear(tmp_path, tmp_factory, name, style):
    v = build(tmp_path, CLEAN + [DEFECTS[name]], style, "done")
    before = v.check()
    assert before
    failures = []
    for p in before:
        failures += check_fix_clears(v, tmp_factory, p, before, {"<node you choose>": "volunteers"})
    assert not failures, "\n".join(failures)


def test_padding_changes_nothing_about_which_ends_are_nodes(tmp_path):
    rows = [("holds", "[[ borrowers ]]", "[[  quick-checkout  ]]", "spaces inside the link")]
    v = build(tmp_path, rows, "obsidian", "done")
    assert v.check() == []
