"""WP11-U5: the fixes of the link rules (SCAT-LINK-DANGLING-BODY and the pairs SCAT-*-END-*) are typed data that match
their text, and the exact options that carry edits clear their problem (see fixcases.verify)."""

import fixcases as fc
import helpers as H

C = "concern/safe-handling.md"
D = H.DESK
R = H.row


def body(text, **kw):
    return {C: H.doc("concern", "Safe handling", body=f"\n{text}\n"), **kw}


def rows(*extra, status="draft", **kw):
    return {D: H.narrative(status=status, rows=extra, **kw)}


def end(rule, *cells, status="draft"):
    return rule, rows(f"| {cells[0]} | holds | {cells[1]} | |", status=status)


DANGLING = "SCAT-LINK-DANGLING-BODY"
CASES = [
    ("dangling-five-types", DANGLING, body("See [[ghost]]."), ()),
    ("dangling-near", DANGLING, body("See [[safe-handlin]]."), ()),
    ("dangling-alias", DANGLING, body("See [[safe-handlin|the briefing]]."), ()),
    ("dangling-illegal", DANGLING, body("See [[Safety briefing]]."), ()),
    ("dangling-illegal-derived-is-a-page", DANGLING, body("See [[Careful keeping]]."), ()),
    ("dangling-hand", DANGLING, body("See [[Привет]]."), ()),
    ("dangling-typeless", DANGLING, body("See [[notes]].", **{"notes.md": "no type\n"}), ()),
    (
        "dangling-typeless-frontmatter",
        DANGLING,
        body("See [[notes]].", **{"notes.md": "---\ntitle: Notes\n---\n"}),
        (),
    ),
    (
        "dangling-at-the-cap",
        DANGLING,
        body("See [[ghost]].", **{"group/third.md": H.doc("group", "Third")}),
        (),
    ),
    (
        "dangling-inferred",
        DANGLING,
        body(
            "See [[ghost]].",
            **{D: H.narrative(rows=(*H.DESK_ROWS, R("holds", "borrowers", "ghost")))},
        ),
        (),
    ),
    ("dangling-note", DANGLING, rows(R("holds", "staff", "safe-handling", "See [[ghost]]")), ()),
]
for stem in ("DRAFT", "DONE"):
    status = "draft" if stem == "DRAFT" else "done"
    nl = f"SCAT-{stem}-END-NOLINK"
    np = f"SCAT-{stem}-END-NOPAGE"
    nn = f"SCAT-{stem}-END-NOTNODE"
    CASES += [
        (
            f"{stem}-nolink-name",
            nl,
            rows("| borrowers | holds | [[safe-handling]] | |", status=status),
            (),
        ),
        (
            f"{stem}-nolink-stub",
            nl,
            rows("| Sandra's crew | holds | [[safe-handling]] | |", status=status),
            (),
        ),
        (f"{stem}-nolink-empty", nl, rows("|  | holds | [[safe-handling]] | |", status=status), ()),
        (
            f"{stem}-nolink-two",
            nl,
            rows("| [[staff]] and [[borrowers]] | holds | [[safe-handling]] | |", status=status),
            (),
        ),
        (
            f"{stem}-nolink-to",
            nl,
            rows("| [[staff]] | holds | quick checkout | |", status=status),
            (),
        ),
        (
            f"{stem}-nopage-ghost",
            np,
            rows("| [[staff]] | holds | [[ghost]] | |", status=status),
            (),
        ),
        (
            f"{stem}-nopage-near",
            np,
            rows("| [[borrower]] | holds | [[safe-handling]] | |", status=status),
            (),
        ),
        (
            f"{stem}-nopage-illegal",
            np,
            rows("| [[staff]] | holds | [[Safety briefing]] | |", status=status),
            (),
        ),
        (
            f"{stem}-nopage-typeless",
            np,
            {**rows("| [[staff]] | holds | [[notes]] | |", status=status), "notes.md": "no type\n"},
            (),
        ),
        (
            f"{stem}-nopage-cap",
            np,
            {
                **rows("| [[ghost]] | holds | [[safe-handling]] | |", status=status),
                "group/third.md": H.doc("group", "Third"),
            },
            (),
        ),
        (
            f"{stem}-notnode-narrative",
            nn,
            rows("| [[kiosk-pitch]] | holds | [[safe-handling]] | |", status=status),
            (),
        ),
        (
            f"{stem}-notnode-slot",
            nn,
            {
                D: H.narrative(
                    status=status,
                    rows=("| [[kiosk-pitch]] | holds | [[safe-handling]] | |",),
                    account="A [[safe-handling]].\n",
                )
            },
            (),
        ),
        (
            f"{stem}-notnode-invalid-type",
            nn,
            {
                **rows("| [[staff]] | holds | [[odd]] | |", status=status),
                "concern/odd.md": H.doc("gadget", "Odd"),
            },
            (),
        ),
    ]


@fc.family(CASES)
def test_the_fix_is_typed_data_that_matches_its_text(make_vault, tmp_path, case):
    _, rule, files, remove = case
    fc.verify(make_vault, tmp_path, rule, files, remove)


def only(make_vault, case_id):
    c = next(c for c in CASES if c[0] == case_id)
    _, found = fc.problems_of(make_vault, c[2], c[3], c[1])
    (p,) = found
    return p


def test_a_stub_is_a_command_and_a_replace_then_stub_is_its_edit_and_then_the_command(make_vault):
    p = only(make_vault, "dangling-five-types")
    cmd = p.fix_data.options[0].command
    assert cmd.argv == ("stub", "ghost", "--type", "group")
    assert cmd.repl == 'scat_kg.stub("ghost", type="group")'
    assert p.fix_data.options[0].kind == "exact" and not p.fix_data.options[0].edits
    p = only(make_vault, "DRAFT-nopage-illegal")
    first = p.fix_data.options[0]
    assert (first.edits[0].action, first.edits[0].find, first.edits[0].replace) == (
        "replace-text",
        "[[Safety briefing]]",
        "[[safety-briefing]]",
    )
    assert first.command.argv == ("stub", "safety-briefing", "--type", "concern")


def test_an_alias_is_kept_by_a_replacement(make_vault):
    p = only(make_vault, "dangling-alias")
    e = p.fix_data.options[0].edits[0]
    assert (e.find, e.replace) == (
        "[[safe-handlin|the briefing]]",
        "[[safe-handling|the briefing]]",
    )
    assert p.fix_data.options[-1].edits[0].replace == "the briefing"


def test_a_typeless_file_gets_set_field_edits_for_the_keys_it_lacks(make_vault):
    p = only(make_vault, "dangling-typeless-frontmatter")
    edits = p.fix_data.options[0].edits
    assert [(e.action, e.file, e.field, e.value) for e in edits] == [
        ("set-field", "notes.md", "type", "group"),
        ("set-field", "notes.md", "status", "stub"),
    ]


def test_the_empty_cell_fix_is_the_whole_row_line_with_an_author_slot(make_vault):
    p = only(make_vault, "DRAFT-nolink-empty")
    option = p.fix_data.options[0]
    assert option.kind == "slot"
    (e,) = option.edits
    assert (e.find, e.author_slot) == ("|  | holds | [[safe-handling]] | |", "<node you choose>")
    assert e.replace == "| [[<node you choose>]] | holds | [[safe-handling]] | |"


def test_every_delete_option_is_a_delete_line_guarded_by_the_row(make_vault):
    for case_id in ("DRAFT-nolink-name", "DRAFT-nopage-ghost", "DONE-notnode-narrative"):
        p = only(make_vault, case_id)
        e = p.fix_data.options[-1].edits[0]
        assert (e.action, e.line, e.find) == (
            "delete-line",
            16,
            p.fix_data.options[-1].edits[0].find,
        )
        assert "| holds |" in e.find
