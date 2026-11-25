"""WP16-R2: a mismatch vault for each pair of R-23 (architecture section 4, as the catalogue's section 6 maps them to
the row model), at stub, draft and done; each fix applied clears its mismatch and creates no other.
"""

import pytest
from indep_kit import (
    NARRATIVE_FILE as NF,
)
from indep_kit import (
    ROW1,
    STATUSES,
    check_fix_clears,
    page_text,
    pair,
    row_line,
)

HEADER = "| from | type | to | note |"
SEP = "|---|---|---|---|"
SLOTS = {
    "<node you choose>": "borrowers",
    "<heading you choose>": "Told edges",
    "<one sentence you write>": "A sentence.",
}

VARIANTS = []


def variant(name, rule, statuses=STATUSES, slots=None, allow=()):
    def deco(fn):
        for st in statuses:
            VARIANTS.append(
                pytest.param(fn, rule, st, slots or {}, allow, id=f"{rule}:{name}@{st}")
            )
        return fn

    return deco


def row(v, text, n=1):
    v.edit(NF, v.line(NF, row_line(n)), text)


# ----- L-N: the three end rules ---------------------------------------------------------------------------------
@variant("text-is-a-page-name", "END-NOLINK")
def _(v):
    row(v, "| borrowers | holds | [[quick-checkout]] | |")


@variant("text-new-name", "END-NOLINK")
def _(v):
    row(v, "| New group | holds | [[quick-checkout]] | |")


@variant("empty-cell", "END-NOLINK", slots={"<node you choose>": "volunteers"})
def _(v):
    row(v, "|  | holds | [[quick-checkout]] | |")


@variant("empty-to-cell", "END-NOLINK", slots={"<node you choose>": "safe-handling"})
def _(v):
    row(v, "| [[borrowers]] | holds | | |")


@variant("two-links", "END-NOLINK")
def _(v):
    row(v, "| [[borrowers]] and [[volunteers]] | holds | [[quick-checkout]] | |")


@variant("to-text", "END-NOLINK")
def _(v):
    row(v, "| [[borrowers]] | holds | quick checkout | |")


@variant("no-page", "END-NOPAGE")
def _(v):
    row(v, "| [[ghost]] | holds | [[quick-checkout]] | |")


@variant("no-page-near-match", "END-NOPAGE")
def _(v):
    row(v, "| [[borrower]] | holds | [[quick-checkout]] | |")


@variant("no-page-to-end", "END-NOPAGE")
def _(v):
    row(v, "| [[self-checkout]] | is provided by | [[ghost-tech]] | |")


@variant("illegal-name", "END-NOPAGE")
def _(v):
    row(v, "| [[Safety briefing]] | holds | [[quick-checkout]] | |")


@variant("typeless-file", "END-NOPAGE")
def _(v):
    v.write("notes.md", "Just notes.\n")
    row(v, "| [[notes]] | holds | [[quick-checkout]] | |")


@variant("typeless-file-with-frontmatter", "END-NOPAGE")
def _(v):
    v.write("notes.md", '---\ntitle: "Mine"\n---\nJust notes.\n')
    row(v, "| [[notes]] | holds | [[quick-checkout]] | |")


@variant("at-the-cap", "END-NOPAGE")
def _(v):
    v.write("scat.toml", "stakeholder_group_cap = 2\nlink_suggestions = true\n")
    row(v, "| [[ghost]] | holds | [[quick-checkout]] | |")


@variant("narrative-page", "END-NOTNODE")
def _(v):
    v.write("narrative/other.md", page_text("narrative", "Other", "draft", extra="timeframe: past"))
    row(v, "| [[other]] | holds | [[quick-checkout]] | |")


@variant("narrative-page-no-candidate", "END-NOTNODE", slots={"<node you choose>": "borrowers"})
def _(v):
    v.write("narrative/other.md", page_text("narrative", "Other", "draft", extra="timeframe: past"))
    v.edit(NF, "[[borrowers]] queued", "people queued")
    row(v, "| [[other]] | holds | [[quick-checkout]] | |")


@variant("invalid-type-page", "END-NOTNODE")
def _(v):
    v.write("concern/odd-page.md", page_text("gadget", "Odd page", "draft"))
    row(v, "| [[borrowers]] | holds | [[odd-page]] | |")


@variant("empty-type-page", "END-NOTNODE")
def _(v):
    v.write("concern/odd-page.md", '---\ntype:\nstatus: draft\ntitle: "Odd page"\n---\n')
    row(v, "| [[borrowers]] | holds | [[odd-page]] | |")


# ----- L-T, nearest case: a row whose two ends are not links is two messages ---------------------------------------
@variant("both-ends-not-links", "END-NOLINK")
def _(v):
    row(v, "| borrowers | holds | quick-checkout | |")


# ----- E-N: other problems of the table ---------------------------------------------------------------------------
@variant("layers-swap", "TABLE-LAYERS")
def _(v):
    row(v, "| [[quick-checkout]] | holds | [[borrowers]] | |")


@variant("layers-retype", "TABLE-LAYERS")
def _(v):
    row(v, "| [[safe-handling]] | holds | [[self-checkout]] | |")


@variant("layers-not-neighbours", "TABLE-LAYERS")
def _(v):
    row(v, "| [[borrowers]] | holds | [[self-checkout]] | |")


@variant("type-unknown", "TABLE-TYPE")
def _(v):
    row(v, "| [[borrowers]] | owns | [[quick-checkout]] | |")


@variant("type-empty", "TABLE-TYPE")
def _(v):
    row(v, "| [[borrowers]] |  | [[quick-checkout]] | |")


@variant("type-near", "TABLE-TYPE")
def _(v):
    row(v, "| [[borrowers]] | holdz | [[quick-checkout]] | |")


@variant("duplicate", "TABLE-DUPLICATE")
def _(v):
    v.edit(NF, ROW1 + "\n", ROW1 + "\n" + ROW1 + "\n")


@variant("duplicate-verb-and-slug", "TABLE-DUPLICATE")
def _(v):
    v.edit(
        NF, ROW1 + "\n", ROW1 + "\n| [[borrowers]] | holds | [[quick-checkout]] | other note |\n"
    )


@variant("row-three-cells", "TABLE-ROW")
def _(v):
    row(v, "| [[borrowers]] | holds | [[quick-checkout]] |")


@variant("row-no-closing-bar", "TABLE-ROW")
def _(v):
    row(v, "| [[borrowers]] | holds | [[quick-checkout]] | n")


@variant("row-three-cells-no-bar", "TABLE-ROW")
def _(v):
    row(v, "| [[borrowers]] | holds | [[quick-checkout]]")


@variant("row-five-cells", "TABLE-ROW")
def _(v):
    row(v, "| [[borrowers]] | holds | [[quick-checkout]] | x | y |")


@variant("row-two-cells", "TABLE-ROW")
def _(v):
    row(v, "| [[borrowers]] | holds |")


@variant("header-wrong-name", "TABLE-HEADER")
def _(v):
    v.edit(NF, HEADER, "| from | kind | to | note |")


@variant("header-three-columns", "TABLE-HEADER")
def _(v):
    v.edit(NF, HEADER, "| from | type | to |")


@variant("header-bad-separator", "TABLE-HEADER")
def _(v):
    v.edit(NF, SEP, "| a | b |")


@variant("header-no-separator", "TABLE-HEADER")
def _(v):
    v.edit(NF, SEP + "\n", "")


@variant(
    "header-alone", "TABLE-HEADER", allow=("SCAT-NOEDGES",)
)  # the mended table has no row (G1)
def _(v):
    v.edit(
        NF,
        SEP + "\n" + ROW1 + "\n| [[quick-checkout]] | is addressed by | [[self-checkout]] | |\n",
        "",
    )


@variant("second-heading", "TABLE-SECOND")
def _(v):
    v.write(
        NF,
        v.read(NF)
        + "\n## Edges told\n\n"
        + HEADER
        + "\n"
        + SEP
        + "\n| [[volunteers]] | holds | [[safe-handling]] | |\n",
    )


@variant("second-table", "TABLE-SECOND")
def _(v):
    v.write(
        NF,
        v.read(NF)
        + "\nMore.\n\n"
        + HEADER
        + "\n"
        + SEP
        + "\n| [[volunteers]] | holds | [[safe-handling]] | |\n",
    )


@variant("dangling-body", "LINK-DANGLING-BODY", statuses=("draft",))
def _(v):
    v.edit(NF, "through [[self-checkout]].", "through [[self-checkout]]. See [[phantom-tool]].")


@variant("mention-in-note-cell", "MENTION", statuses=("draft",))
def _(v):
    row(v, "| [[borrowers]] | holds | [[quick-checkout]] | Raised safe handling here |")


@variant("mention-in-body", "MENTION", statuses=("draft",))
def _(v):
    v.edit(
        NF,
        "through [[self-checkout]].",
        "through [[self-checkout]]. The safe handling of tools mattered.",
    )


def rules_of(rule, st):
    if rule in ("LINK-DANGLING-BODY", "MENTION"):
        return {f"SCAT-{rule}"}
    return {pair(rule, st)[0]}


@pytest.mark.parametrize("fn,rule,st,slots,allow", VARIANTS)
def test_each_fix_clears_its_mismatch_and_creates_no_other(
    make_base, tmp_factory, fn, rule, st, slots, allow
):
    v = make_base(st)
    fn(v)
    before = v.check()
    targets = [p for p in before if p.rule in rules_of(rule, st)]
    assert targets, f"the variant made no {rule} message: {[p.brief() for p in before]}"
    failures = []
    for p in targets:
        assert p.fix, p.brief()
        failures += check_fix_clears(v, tmp_factory, p, before, {**SLOTS, **slots}, allowed=allow)
    assert not failures, "\n".join(failures)


def test_every_fix_is_data_with_a_kind_and_options_are_alternatives_or_steps(make_base):
    v = make_base("done")
    row(v, "| borrowers | holds | [[ghost]] | |")
    for p in v.check():
        assert p.fix["kind"] in ("exact", "options", "slot", "advisory", "manual")
        for o in p.fix.get("options", []):
            assert o["kind"] in ("exact", "slot", "advisory", "manual")
            if o["kind"] in ("advisory", "manual"):
                assert not o.get("edits") and not o.get("command")


# ----- L-E: no message ---------------------------------------------------------------------------------------------
@pytest.mark.parametrize("st", STATUSES)
def test_L_E_a_narrative_that_links_both_ends_without_a_row_gets_no_message(make_base, st):
    v = make_base(st)
    v.edit(NF, ROW1 + "\n", "")
    body = v.read(NF)
    assert "[[borrowers]]" in body and "[[quick-checkout]]" in body and "| holds |" not in body
    assert v.check() == []
    assert v.check(NF) == [] and v.check("saturday", neighborhood=True) == []


@pytest.mark.parametrize("st", STATUSES)
def test_L_E_a_row_with_linked_ends_alone_is_conformant(make_base, st):
    v = make_base(st)
    v.edit(
        NF,
        "The desk was busy: [[borrowers]] queued, wanting [[quick-checkout]] through [[self-checkout]].",
        "Quiet.",
    )
    assert v.check() == []


# ----- E-T: a table off a narrative, and rows past the first table, tell no edge --------------------------------
def test_E_T_a_table_on_a_concern_page_is_not_read(make_base):
    v = make_base("done")
    v.write(
        "concern/safe-handling.md",
        page_text(
            "concern",
            "Safe handling",
            "done",
            body="## Edges told\n\n" + HEADER + "\n" + SEP + "\n| ghost | holds | [[nowhere]] | |",
        ),
    )
    # the link is an ordinary body link: only the dangling-body rule speaks, and no row rule does
    rules = {p.rule for p in v.check()}
    assert rules == {"SCAT-LINK-DANGLING-BODY"}


# ----- N-T: a mismatch of a narrative is an error once it is done; setting done is refused -------------------------
def test_N_T_mismatch_is_a_warning_before_done_an_error_at_done_and_blocks_done(make_base):
    v = make_base("draft")
    row(v, "| borrowers | holds | [[quick-checkout]] | |")
    (p,) = v.check()
    assert (p.rule, p.severity) == ("SCAT-DRAFT-END-NOLINK", "warning")
    code, doc = v.scat("set-status", "saturday", "done")
    assert code == 1 and doc["refused"][0]["problems"][0]["rule"] == "SCAT-DONE-END-NOLINK"
    v.edit(NF, "status: draft", "status: done")
    (p,) = v.check()
    assert (p.rule, p.severity) == ("SCAT-DONE-END-NOLINK", "error")


def test_the_mismatch_in_one_narrative_does_not_change_another_pages_messages(make_base):
    v = make_base("done")
    before = {p.file for p in v.check()}
    row(v, "| [[ghost]] | holds | [[quick-checkout]] | |")
    after = v.check()
    assert {p.file for p in after} == {NF} and before == set()
    for page in ("borrowers", "quick-checkout"):
        assert v.check(page) == []
