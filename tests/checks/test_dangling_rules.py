"""Seeded defects for SCAT-LINK-DANGLING (frontmatter) and SCAT-LINK-DANGLING-BODY."""

from helpers import SC, choose, coded, doc, line_of, links, report_of, seeded, stub

D = "SCAT-LINK-DANGLING"
DB = "SCAT-LINK-DANGLING-BODY"
BRIEFING = {"affordance/safety-briefing.md": doc("affordance", "Safety briefing")}
CAP_NOTE = (
    "(the vault is at its cap of 3 stakeholder groups, so a new group page would break SCAT-CAP; "
    "choose an existing group)"
)


def aff(target):
    return coded(affordances=links("affordances", "self-checkout", target))


def replace_aff(old, new):
    return f'replace `- "[[{old}]]"` with `- "[[{new}]]"`'


def test__scat_link_dangling__a_typo_offers_the_near_match_then_a_stub(make_vault):
    fix = choose(
        replace_aff("safety-briefings", "safety-briefing")
        + " (the closest existing affordance page)",
        f"run {stub('safety-briefings', 'affordance')} to create it as a stub",
    )
    seeded(
        make_vault, BRIEFING | {SC: aff("safety-briefings")}, (D, SC, "field `affordances`", fix)
    )


def test__scat_link_dangling__no_near_match_offers_the_stub_only(make_vault):
    fix = f"Fix: run {stub('zzzzzz', 'affordance')} to create it as a stub"
    seeded(make_vault, {SC: aff("zzzzzz")}, (D, SC, "field `affordances`", fix))


def test__scat_link_dangling__line_is_the_item_line(make_vault):
    page = aff("zzzzzz")
    r = report_of(make_vault, {SC: page})
    assert r.problems[0].line == line_of(page, "zzzzzz")


def test__scat_link_dangling__wrong_case_is_variant_c_with_one_option(make_vault):
    fix = "Fix: " + replace_aff("Safety-Briefing", "safety-briefing")
    r = seeded(
        make_vault, BRIEFING | {SC: aff("Safety-Briefing")}, (D, SC, "field `affordances`", fix)
    )
    assert (
        "is not a legal page name" in r.problems[0].what
    )  # near match and derived name are one page


def test__scat_link_dangling__illegal_name_with_no_page_replaces_then_stubs(make_vault):
    fix = (
        "Fix: "
        + replace_aff("Safety briefing", "safety-briefing")
        + f", then run {stub('safety-briefing', 'affordance')} to create it as a stub"
    )
    seeded(make_vault, {SC: aff("Safety briefing")}, (D, SC, "field `affordances`", fix))


def test__scat_link_dangling__derived_name_is_a_page_of_another_type(make_vault):
    # `Quick-Checkout` derives `quick-checkout`, a concern: replacing would only trade this error for another
    fix = (
        "Fix: (`quick-checkout` is a concern page, so replacing the link with it would only trade "
        "this error for SCAT-LINK-ENDPOINT)"
    )
    seeded(make_vault, {SC: aff("Quick-Checkout")}, (D, SC, "field `affordances`", fix))


def test__scat_link_dangling__non_latin_name_needs_a_hand_choice(make_vault):
    fix = "Fix: choose a legal page name by hand (contract section 2), then write the link with it"
    seeded(make_vault, {SC: aff("Привет")}, (D, SC, "field `affordances`", fix))


def test__scat_link_dangling__file_without_type_is_variant_b(make_vault):
    fix = 'Fix: put these lines in a block between two `---` lines at the very top of notes.md: `type: affordance`, `status: stub`, `title: "Notes"`'
    r = seeded(
        make_vault,
        {SC: aff("notes"), "notes.md": "just words\n"},
        (D, SC, "field `affordances`", fix),
    )
    assert "notes.md exists but has no `type`" in r.problems[0].what


def test__scat_link_dangling__file_with_frontmatter_but_no_type_lists_the_missing_keys(make_vault):
    fix = (
        "Fix: add these lines to the frontmatter of notes.md: `type: affordance`, `status: stub`; "
        'replace the line `title:` in notes.md with `title: "Notes"`'
    )
    text = "---\nauthor: me\ntitle:\n---\nwords\n"
    seeded(make_vault, {SC: aff("notes"), "notes.md": text}, (D, SC, "field `affordances`", fix))


def test__scat_link_dangling__group_at_the_cap_withholds_the_stub(make_vault):
    files = {
        "stakeholder-group/third.md": doc("stakeholder-group", "Third"),
        SC: coded(groups=links("groups", "staff", "funders")),
    }
    seeded(make_vault, files, (D, SC, "field `groups`", f"Fix: {CAP_NOTE}"))


def test__scat_link_dangling__group_under_the_cap_offers_the_stub(make_vault):
    fix = f"Fix: run {stub('funders', 'stakeholder-group')} to create it as a stub"
    seeded(
        make_vault,
        {SC: coded(groups=links("groups", "staff", "funders"))},
        (D, SC, "field `groups`", fix),
    )


def test__scat_link_dangling__on_a_relation_page_the_stub_is_the_endpoints_type(make_vault):
    path = "heldby/staff-holds-safe-handling.md"
    page = doc("heldby", "H", extra='group: "[[funders]]"\nconcern: "[[safe-handling]]"')
    fix = f"Fix: run {stub('funders', 'stakeholder-group')} to create it as a stub"
    seeded(make_vault, {path: page}, (D, path, "field `group`", fix))


def test__scat_link_dangling__illegal_name_next_to_a_file_without_type(make_vault):
    fix = (
        "Fix: "
        + replace_aff("Notes", "notes-2")
        + f", then run {stub('notes-2', 'affordance')} to create it as a stub"
    )
    r = seeded(
        make_vault, {SC: aff("Notes"), "Notes.md": "words\n"}, (D, SC, "field `affordances`", fix)
    )
    assert "Notes.md exists but is not a page" in r.problems[0].what


# the body


def body(text):
    return coded(body=text)


def test__scat_link_dangling_body__name_a_field_elsewhere_names_gives_one_type(make_vault):
    files = {
        "concern/careful-keeping.md": doc(
            "concern", "C", extra=links("conflicts", "ghost-concern")
        ),
        SC: body("See [[ghost-concern]].\n"),
    }
    n = line_of(files[SC], "See [[")
    fix = choose(
        f"run {stub('ghost-concern', 'concern')} to create a concern page",
        f"on line {n} replace `[[ghost-concern]]` with `ghost-concern` to keep the words and drop the link",
    ) + (
        "\n(you can also name the page in the right link field of this page, which entails its stub "
        "with that type)"
    )
    front = "Fix: run " + stub("ghost-concern", "concern") + " to create it as a stub"
    seeded(
        make_vault,
        files,
        (D, "concern/careful-keeping.md", "field `conflicts`", front),
        (DB, SC, "link [[ghost-concern]]", fix),
    )


def test__scat_link_dangling_body__unknown_name_offers_the_class_types_minus_technology(make_vault):
    page = body("See [[nothing-here]].\n")
    n = line_of(page, "See [[")
    fix = choose(
        f"run {stub('nothing-here', 'stakeholder-group')} to create a stakeholder-group page",
        f"run {stub('nothing-here', 'concern')} to create a concern page",
        f"run {stub('nothing-here', 'affordance')} to create an affordance page",
        f"on line {n} replace `[[nothing-here]]` with `nothing-here` to keep the words and drop the link",
    ) + (
        "\n(technology left out: a scenario-coded page should not link to it)"
        "\n(you can also name the page in the right link field of this page, which entails its stub "
        "with that type)"
    )
    r = seeded(make_vault, {SC: page}, (DB, SC, "link [[nothing-here]]", fix))
    assert r.problems[0].line == n


def test__scat_link_dangling_body__near_match_comes_first(make_vault):
    page = body("See [[quick-chekout]].\n")
    n = line_of(page, "See [[")
    r = report_of(make_vault, {SC: page})
    fix = r.problems[0].fix
    assert (
        fix.split("\n")[1]
        == f"  1. on line {n} replace `[[quick-chekout]]` with `[[quick-checkout]]`"
    )


def test__scat_link_dangling_body__illegal_name_offers_replace_then_stub(make_vault):
    page = body("See [[Safety briefing]].\n")
    n = line_of(page, "See [[")
    fix = report_of(make_vault, {SC: page}).problems[0].fix.split("\n")
    swap = f"on line {n} replace `[[Safety briefing]]` with `[[safety-briefing]]`, then run "
    assert f"  2. {swap}{stub('safety-briefing', 'concern')} to create a concern page" in fix
    assert not any("--type technology" in ln for ln in fix)
    assert (
        f"  4. on line {n} replace `[[Safety briefing]]` with `Safety briefing` to keep the words and drop the link"
        in fix
    )


def test__scat_link_dangling_body__names_that_are_not_page_links_give_none(make_vault):
    text = "```\n[[code-only]]\n```\nA [[photo.png]], [[v1.2-notes]], [[#Heading]], [[^blk]] and `[[span]]`.\n"
    seeded(make_vault, {SC: body(text)})


def test__scat_link_dangling_body__block_reference_names_the_page_before_the_caret(make_vault):
    r = report_of(make_vault, {SC: body("See [[ghost^abc123]].\n")})
    assert [(p.rule, p.where) for p in r.problems] == [(DB, "link [[ghost]]")]


def test__scat_link_dangling_body__same_link_twice_on_a_line_is_one_message_with_a_count(
    make_vault,
):
    r = report_of(make_vault, {SC: body("See [[ghost]] and [[ghost]].\n")})
    assert len(r.problems) == 1 and r.problems[0].repeat == 2
    assert r.problems[0].render().split("\n")[0].endswith("(x2)")


def test__scat_link_dangling_body__group_stub_is_withheld_at_the_cap(make_vault):
    files = {
        "stakeholder-group/third.md": doc("stakeholder-group", "Third"),
        SC: body("See [[nothing-here]].\n"),
    }
    r = report_of(make_vault, files)
    fix = r.problems[0].fix
    assert "--type stakeholder-group" not in fix and CAP_NOTE in fix
    assert "--type concern" in fix


def test__scat_link_dangling_body__file_without_type_gets_the_lines_per_type(make_vault):
    r = report_of(make_vault, {SC: body("See [[notes]].\n"), "notes.md": "words\n"})
    fix = r.problems[0].fix
    assert (
        "put these lines in a block between two `---` lines at the very top of notes.md: `type: concern`"
        in fix
    )
