"""Seeded defects for the rules that read more than one page, and the two vault-level rules."""

import pytest
from helpers import SC, coded, doc, line_of, links, report_of, seeded, stub

BOTH = "SCAT-CONFLICT-BOTH"
CAREFUL = "concern/careful-keeping.md"
QUICK = "concern/quick-checkout.md"
CONFLICT_FIX = (
    "Fix: none needed if both belong in this record. Holding both sides is allowed and is what the warning "
    "marks, a place where two concerns pull apart. If one was coded here by mistake, delete its line "
    '`- "[[careful-keeping]]"` or `- "[[quick-checkout]]"` under `concerns`.'
)


def holds_both(status="done"):
    return coded(status=status, concerns=links("concerns", "careful-keeping", "quick-checkout"))


def declared(a_declares=False, b_declares=False):
    """The two concerns, with the conflict declared on careful-keeping, on quick-checkout, or both."""
    return {
        CAREFUL: doc(
            "concern",
            "Careful keeping",
            extra=links("conflicts", "quick-checkout") if a_declares else "",
        ),
        QUICK: doc(
            "concern",
            "Quick checkout",
            extra=links("conflicts", "careful-keeping") if b_declares else "",
        ),
    }


@pytest.mark.parametrize(
    ("a", "b", "on"),
    [
        (True, False, "[[careful-keeping]]"),
        (False, True, "[[quick-checkout]]"),
        (True, True, "[[careful-keeping]], [[quick-checkout]]"),
    ],
)
def test__scat_conflict_both__one_or_both_sides_declared(make_vault, a, b, on):
    page = holds_both()
    r = seeded(
        make_vault,
        declared(a, b) | {SC: page},
        (BOTH, SC, "field `concerns`", CONFLICT_FIX),
    )
    assert r.ok and r.problems[0].severity == "warning"
    assert r.problems[0].what.endswith(f"(declared on {on})")
    assert r.problems[0].line == line_of(page, "concerns:")


@pytest.mark.parametrize("status", ["stub", "draft", "done"])
def test__scat_conflict_both__same_message_at_every_status(make_vault, status):
    seeded(
        make_vault,
        declared(True) | {SC: holds_both(status)},
        (BOTH, SC, "field `concerns`", CONFLICT_FIX),
    )


def test__scat_conflict_both__one_concern_only_gives_none(make_vault):
    seeded(make_vault, declared(True))


def test__scat_conflict_both__no_declaration_gives_none(make_vault):
    seeded(make_vault, declared() | {SC: holds_both()})


def test__scat_conflict_both__coded_architecture_too(make_vault):
    path = "architecture-coded/kiosk-pitch-coded.md"
    page = doc(
        "architecture-coded",
        "K",
        extra=links("raw", "kiosk-pitch")
        + links("concerns", "careful-keeping", "quick-checkout")
        + links("affordances", "self-checkout")
        + links("technologies", "booking-app"),
    )
    r = report_of(make_vault, declared(True) | {path: page})
    assert [(p.rule, p.file) for p in r.problems] == [(BOTH, path)]


SELF = "SCAT-CONFLICT-SELF"


def test__scat_conflict_self__a_concern_lists_itself(make_vault):
    page = doc("concern", "Safe handling", extra=links("conflicts", "safe-handling"))
    path = "concern/safe-handling.md"
    fix = 'Fix: delete the line `- "[[safe-handling]]"` under `conflicts`'
    r = seeded(make_vault, {path: page}, (SELF, path, "field `conflicts`", fix))
    assert r.problems[0].line == line_of(page, "safe-handling]]")


def test__scat_conflict_self__the_other_pair_still_counts_for_conflict_both(make_vault):
    path = QUICK
    files = {
        path: doc(
            "concern",
            "Quick checkout",
            extra=links("conflicts", "quick-checkout", "careful-keeping"),
        ),
        SC: holds_both(),
    }
    fix = 'Fix: delete the line `- "[[quick-checkout]]"` under `conflicts`'
    seeded(
        make_vault,
        files | {CAREFUL: doc("concern", "Careful keeping")},
        (SELF, path, "field `conflicts`", fix),
        (BOTH, SC, "field `concerns`", CONFLICT_FIX),
    )


DUP = "SCAT-REL-DUPLICATE"
KEPT = "heldby/staff-holds-safe-handling.md"
COPY = "heldby/more/zzz-copy.md"


def copy_page(notes=None, **kw):
    extra = 'group: "[[staff]]"\nconcern: "[[safe-handling]]"' + (
        f'\nnotes: "{notes}"' if notes else ""
    )
    return doc("heldby", "Z", extra=extra, **kw)


def dup_fix(first):
    return (
        "Fix, two steps:\n"
        f"     1. {first}\n"
        "     2. delete heldby/more/zzz-copy.md, then run `scat index` (REPL: `scat_kg.index()`) and change every "
        "link that named `zzz-copy` to `[[staff-holds-safe-handling]]` (each shows as SCAT-LINK-DANGLING-BODY "
        "on the next check)"
    )


def test__scat_rel_duplicate__later_name_is_reported_without_notes(make_vault):
    first = (
        f"in {KEPT}: copy any part of the body of {COPY} you want to keep "
        f"(`notes` of {COPY} has no text to move)"
    )
    r = seeded(make_vault, {COPY: copy_page()}, (DUP, COPY, "frontmatter", dup_fix(first)))
    assert r.ok


def test__scat_rel_duplicate__notes_are_added_when_the_kept_page_has_none(make_vault):
    first = f'in {KEPT}: add the line `notes: "my account"`, and copy any part of the body of {COPY} you want to keep'
    seeded(make_vault, {COPY: copy_page("my account")}, (DUP, COPY, "frontmatter", dup_fix(first)))


def test__scat_rel_duplicate__notes_are_joined_when_both_have_text(make_vault):
    kept = doc(
        "heldby", "H", extra='group: "[[staff]]"\nconcern: "[[safe-handling]]"\nnotes: "kept"'
    )
    first = (
        f'in {KEPT}: replace the line `notes: "kept"` with `notes: "kept my account"`, '
        f"and copy any part of the body of {COPY} you want to keep"
    )
    seeded(
        make_vault,
        {KEPT: kept, COPY: copy_page("my account")},
        (DUP, COPY, "frontmatter", dup_fix(first)),
    )


def test__scat_rel_duplicate__notes_replace_an_empty_notes_line(make_vault):
    kept = doc("heldby", "H", extra='group: "[[staff]]"\nconcern: "[[safe-handling]]"\nnotes: ""')
    first = (
        f'in {KEPT}: replace the line `notes: ""` with `notes: "my account"`, '
        f"and copy any part of the body of {COPY} you want to keep"
    )
    seeded(
        make_vault,
        {KEPT: kept, COPY: copy_page("my account")},
        (DUP, COPY, "frontmatter", dup_fix(first)),
    )


def test__scat_rel_duplicate__same_concern_with_two_groups_gives_none(make_vault):
    page = doc("heldby", "B", extra='group: "[[borrowers]]"\nconcern: "[[safe-handling]]"')
    seeded(make_vault, {"heldby/borrowers-holds-safe-handling.md": page})


def test__scat_rel_duplicate__other_relations_sharing_an_endpoint_give_none(make_vault):
    page = doc(
        "addresses", "A", extra='concern: "[[safe-handling]]"\naffordance: "[[self-checkout]]"'
    )
    seeded(make_vault, {"addresses/self-checkout-addresses-safe-handling.md": page})


def test__scat_rel_duplicate__a_duplicate_of_a_duplicate_is_two_messages(make_vault):
    second = "heldby/more/zzz-copy-2.md"
    r = report_of(make_vault, {COPY: copy_page(), second: copy_page()})
    assert [(p.rule, p.file) for p in r.problems] == [
        (DUP, second),
        (DUP, COPY),
    ]  # `-` sorts before `.`


MENTION = "SCAT-MENTION"


def mention_fix(n, written, link):
    return f"Fix: on line {n} replace `{written}` with `{link}`"


def test__scat_mention__title_in_plain_text(make_vault):
    page = coded(body="First line.\n  We talked about quick checkout today.\n")
    n = line_of(page, "We talked")
    r = seeded(
        make_vault,
        {SC: page},
        (
            MENTION,
            SC,
            "text `quick checkout`",
            mention_fix(n, "quick checkout", "[[quick-checkout|quick checkout]]"),
        ),
    )
    assert (r.problems[0].line, r.problems[0].column) == (n, 19)
    assert r.ok


def test__scat_mention__case_is_ignored_and_the_text_is_kept_as_written(make_vault):
    page = coded(body="Quick Checkout matters.\n")
    n = line_of(page, "Quick Checkout")
    seeded(
        make_vault,
        {SC: page},
        (
            MENTION,
            SC,
            "text `Quick Checkout`",
            mention_fix(n, "Quick Checkout", "[[quick-checkout|Quick Checkout]]"),
        ),
    )


def test__scat_mention__the_page_name_gets_a_plain_link(make_vault):
    page = coded(body="the quick-checkout idea\n")
    n = line_of(page, "the quick")
    seeded(
        make_vault,
        {SC: page},
        (
            MENTION,
            SC,
            "text `quick-checkout`",
            mention_fix(n, "quick-checkout", "[[quick-checkout]]"),
        ),
    )


def test__scat_mention__column_counts_characters(make_vault):
    r = report_of(make_vault, {SC: coded(body="héllo wörld quick checkout\n")})
    assert r.problems[0].column == 13


def test__scat_mention__reported_once_at_the_first_occurrence(make_vault):
    page = coded(body="quick checkout, then quick checkout again\n")
    r = report_of(make_vault, {SC: page})
    assert [(p.line, p.column) for p in r.problems] == [(line_of(page, "then"), 1)]


def test__scat_mention__plain_and_linked_gives_none(make_vault):
    seeded(make_vault, {SC: coded(body="quick checkout and [[quick-checkout|that]]\n")})


def test__scat_mention__inside_code_or_a_wikilink_gives_none(make_vault):
    seeded(make_vault, {SC: coded(body="`quick checkout` and [[safe-handling|quick checkout]]\n")})


def test__scat_mention__a_technology_on_a_scenario_gives_none(make_vault):
    seeded(make_vault, {SC: coded(body="the booking app is open\n")})


def test__scat_mention__a_raw_page_is_exempt(make_vault):
    path = "scenario-raw/desk-day.md"
    page = doc("scenario-raw", "D", extra=links("coded", "desk-day-coded"), body="quick checkout\n")
    seeded(make_vault, {path: page})


def test__scat_mention__short_names_are_not_matched(make_vault):
    files = {"concern/tea.md": doc("concern", "Tea"), SC: coded(body="a cup of tea\n")}
    seeded(make_vault, files)


BACK = "SCAT-RAW-BACKLINK"
RAW = "scenario-raw/desk-day.md"
CODED_LINE = '`- "[[desk-day-coded]]"`'


def raw_page(extra="", **kw):
    return doc("scenario-raw", "Desk day", extra=extra, **kw)


def test__scat_raw_backlink__no_coded_field(make_vault):
    fix = f"Fix: in {RAW} add `coded:` and under it the line {CODED_LINE}"
    r = seeded(make_vault, {RAW: raw_page()}, (BACK, RAW, "field `coded`", fix))
    assert r.ok


def test__scat_raw_backlink__coded_names_another_page(make_vault):
    other = "scenario-coded/other.md"
    files = {RAW: raw_page(links("coded", "other")), other: coded(raw=links("raw", "desk-day"))}
    fix = f"Fix: add under `coded:` in {RAW} the line {CODED_LINE}"
    seeded(make_vault, files, (BACK, RAW, "field `coded`", fix))


def test__scat_raw_backlink__empty_list_is_replaced(make_vault):
    fix = f"Fix: in {RAW} replace the line `coded: []` with `coded:` and under it the line {CODED_LINE}"
    seeded(make_vault, {RAW: raw_page("coded: []\n")}, (BACK, RAW, "field `coded`", fix))


def test__scat_raw_backlink__flow_list_keeps_its_pages(make_vault):
    other = "scenario-coded/other.md"
    files = {RAW: raw_page('coded: ["[[other]]"]\n'), other: coded(raw=links("raw", "desk-day"))}
    fix = (
        f'Fix: in {RAW} replace the line `coded: ["[[other]]"]` with `coded:` and under it '
        'the lines `- "[[other]]"` then `- "[[desk-day-coded]]"`'
    )
    seeded(make_vault, files, (BACK, RAW, "field `coded`", fix))


def test__scat_raw_backlink__listed_back_gives_none(make_vault):
    seeded(make_vault, {})


def test__scat_raw_backlink__one_message_per_coded_page(make_vault):
    other = "scenario-coded/other.md"
    files = {RAW: raw_page(), other: coded(raw=links("raw", "desk-day"))}
    r = report_of(make_vault, files)
    assert [p.what.split("]]")[0] for p in r.problems] == ["[[desk-day-coded", "[[other"]


UNCODED = "SCAT-RAW-UNCODED"


def uncoded_files(raw_extra="", status="done"):
    """desk-day has no coded page, and nothing names it; desk-day-coded now derives from `other-raw`."""
    return {
        RAW: raw_page(raw_extra, status=status),
        "scenario-raw/other-raw.md": doc(
            "scenario-raw", "Other raw", extra=links("coded", "desk-day-coded")
        ),
        SC: coded(raw=links("raw", "other-raw")),
    }


def uncoded_fix(step1):
    return (
        "Fix, two steps, in this order:\n"
        f"     1. in {RAW}: {step1}\n"
        f"     2. run {stub('<coded-page-name>', 'scenario-coded')}; the operation writes `raw` on the new page "
        "itself, listing this page (until it runs, the new `coded` link shows as SCAT-LINK-DANGLING)"
    )


SLOT = '`coded:` and under it the line `- "[[<coded-page-name>]]"` (author: choose the name)'


def test__scat_raw_uncoded__done_raw_page_with_nothing_coded(make_vault):
    r = seeded(
        make_vault, uncoded_files(), (UNCODED, RAW, "field `coded`", uncoded_fix(f"add {SLOT}"))
    )
    assert r.ok


def test__scat_raw_uncoded__empty_coded_is_replaced(make_vault):
    fix = uncoded_fix(f"replace the line `coded: []` with {SLOT}")
    seeded(make_vault, uncoded_files("coded: []\n"), (UNCODED, RAW, "field `coded`", fix))


@pytest.mark.parametrize("status", ["stub", "draft"])
def test__scat_raw_uncoded__not_before_done(make_vault, status):
    seeded(make_vault, uncoded_files(status=status))


def test__scat_raw_uncoded__architecture_raw_names_the_architecture_key(make_vault):
    path = "architecture-raw/kiosk-pitch.md"
    files = {
        path: doc("architecture-raw", "Kiosk pitch"),
        "architecture-raw/other.md": doc(
            "architecture-raw", "Other", extra=links("coded", "kiosk-pitch-coded")
        ),
        "architecture-coded/kiosk-pitch-coded.md": doc(
            "architecture-coded",
            "K",
            extra=links("raw", "other")
            + links("concerns", "quick-checkout")
            + links("affordances", "self-checkout")
            + links("technologies", "booking-app"),
        ),
    }
    r = report_of(make_vault, files)
    assert [p.rule for p in r.problems] == [UNCODED]
    assert "--type architecture-coded" in r.problems[0].fix


def test__scat_raw_uncoded__after_step_one_alone_the_new_link_dangles(make_vault):
    files = uncoded_files(links("coded", "new-coded"))
    r = report_of(make_vault, files)
    assert [(p.rule, p.file) for p in r.problems] == [("SCAT-LINK-DANGLING", RAW)]


def test__scat_raw_uncoded__after_both_steps_it_is_clean(make_vault):
    files = uncoded_files(links("coded", "new-coded"))
    files["scenario-coded/new-coded.md"] = doc(
        "scenario-coded",
        "New coded",
        status="stub",
        description=None,
        extra=links("raw", "desk-day"),
    )
    seeded(make_vault, files)


def test__scat_raw_uncoded__after_step_two_alone_it_stays(make_vault):
    files = uncoded_files()
    files["scenario-coded/new-coded.md"] = doc(
        "scenario-coded", "New coded", status="stub", description=None
    )
    r = report_of(make_vault, files)
    assert [p.rule for p in r.problems] == [UNCODED]


CAP = "SCAT-CAP"
CONFIG = "SCAT-CAP-CONFIG"
GROUPS = {
    f"stakeholder-group/{n}.md": doc("stakeholder-group", n.title()) for n in ("g-one", "g-two")
}


def test__scat_cap__four_groups_over_a_cap_of_three(make_vault):
    cap_fix = (
        "Fix, choose one:\n"
        "  1. write `stakeholder_group_cap = 4` in scat.toml (the cap protects against identifying "
        "individuals; raise it only if the plan allows)\n"
        "  2. fold 1 group(s) into the others (move their standpoints into another group's "
        "`description`) and delete those pages"
    )
    r = seeded(make_vault, GROUPS, (CAP, "scat.toml", "field `stakeholder_group_cap`", cap_fix))
    assert r.problems[0].what == (
        "the vault holds 4 stakeholder-group pages, over the cap of 3: borrowers, g-one, g-two, staff"
    )


def test__scat_cap__a_stub_group_still_counts(make_vault):
    stub_group = doc("stakeholder-group", "Stub", status="stub", description=None)
    r = report_of(
        make_vault, {"stakeholder-group/a.md": stub_group, "stakeholder-group/b.md": stub_group}
    )
    assert [p.rule for p in r.problems] == [CAP]
    assert r.problems[0].what.endswith(
        "holds 4 stakeholder-group pages, over the cap of 3: a, b, borrowers, staff"
    )


def test__scat_cap__at_the_cap_gives_none(make_vault):
    seeded(make_vault, {"stakeholder-group/g-one.md": GROUPS["stakeholder-group/g-one.md"]})


def write_config(text):
    return {"scat.toml": text}


def config_fix(verb, groups=2):
    least = f", so choose at least {groups}" if groups else ""
    return (
        f"Fix: {verb} `stakeholder_group_cap = <number you choose>` (author) in scat.toml; choose a whole "
        f"number of 1 or more (the vault has {groups} stakeholder-group pages now{least})"
    )


ADD = "add the line"
WHERE = "field `stakeholder_group_cap`"


def test__scat_cap_config__file_missing(make_vault):
    r = seeded(make_vault, {}, (CONFIG, "scat.toml", WHERE, config_fix(ADD)), remove=("scat.toml",))
    assert r.problems[0].what == "the file is missing"


def test__scat_cap_config__invalid_toml(make_vault):
    r = seeded(
        make_vault,
        write_config("stakeholder_group_cap = \n"),
        (CONFIG, "scat.toml", WHERE, config_fix(ADD)),
    )
    assert r.problems[0].what.startswith("the file is not valid TOML: ")


def test__scat_cap_config__key_missing(make_vault):
    r = seeded(
        make_vault, write_config("other = 1\n"), (CONFIG, "scat.toml", WHERE, config_fix(ADD))
    )
    assert r.problems[0].what == "the key is missing"


@pytest.mark.parametrize("written", ['"three"', "0", "2.5", "3.0"])
def test__scat_cap_config__bad_value_is_replaced(make_vault, written):
    verb = f"replace the line `stakeholder_group_cap = {written}` with"
    r = seeded(
        make_vault,
        write_config(f"stakeholder_group_cap = {written}\n"),
        (CONFIG, "scat.toml", WHERE, config_fix(verb)),
    )
    assert r.problems[0].what == f"the value `{written}` is not a TOML integer of 1 or more"


def test__scat_cap_config__no_groups_drops_the_at_least_clause(make_vault):
    files = {"scat.toml": "stakeholder_group_cap = 0\n"}
    r = report_of(
        make_vault, files, remove=("stakeholder-group/staff.md", "stakeholder-group/borrowers.md")
    )
    config = [p for p in r.problems if p.rule == CONFIG]
    assert config[0].fix.endswith("(the vault has 0 stakeholder-group pages now)")
