"""Seeded defects for the SCAT-FM-* rules and SCAT-NAME. Test names carry the rule id (see test_coverage)."""

import pytest
from helpers import choose, doc, got, region_for, report_of, seeded, set_status

C = "concern/safe-handling.md"
H = "heldby/staff-holds-safe-handling.md"
ONE = "Fix: make the frontmatter a block of `key: value` lines between two lines containing only `---`, at the very top of the file; start from the first line the parser rejected"
PARSE = "SCAT-FM-PARSE"


def test__scat_fm_parse__closing_line_missing(make_vault):
    seeded(
        make_vault,
        {C: "---\ntype: concern\nstatus: done\ntitle: x\n"},
        (PARSE, C, "frontmatter", ONE),
    )


def test__scat_fm_parse__tab_indented_key(make_vault):
    bad = "---\ntype: concern\n\tstatus: done\n---\n"
    r = seeded(make_vault, {C: bad}, (PARSE, C, "frontmatter", ONE))
    assert r.problems[0].line == 3  # the line the parser rejected


def test__scat_fm_parse__colon_in_title(make_vault):
    bad = "---\ntype: concern\nstatus: done\ntitle: a: b\n---\n"
    seeded(make_vault, {C: bad}, (PARSE, C, "frontmatter", ONE))


def test__scat_fm_parse__clean_cases_give_none(make_vault):
    crlf = (
        '---\r\ntype: concern\r\nstatus: done\r\ntitle: "S"\r\ndescription: "D"\r\n---\r\nbody\r\n'
    )
    seeded(
        make_vault, {C: crlf, "README.md": "# Not a page\n", "notes/loose.md": "no frontmatter\n"}
    )


def test__scat_fm_parse__cascade_unreadable_page_is_no_source(make_vault):
    # links to the unreadable page are not endpoint-checked either: one message, on the page itself
    bad = "---\ntype: concern\n\tstatus: done\n---\n"
    seeded(make_vault, {C: bad}, (PARSE, C, "frontmatter", ONE))


REQ = "SCAT-FM-REQUIRED"
TITLE = "the page name with each - replaced by a space and the first letter upper case; reword it if you like"
STATUS_FIX = f"Fix: run {set_status('safe-handling')}; use `stub` or `done` instead of `draft` if that is the truth"


def test__scat_fm_required__status_missing(make_vault):
    seeded(
        make_vault,
        {C: doc("concern", "Safe handling", status=None)},
        (REQ, C, "field `status`", STATUS_FIX),
    )


def test__scat_fm_required__status_present_but_empty(make_vault):
    page = '---\ntype: concern\nstatus:\ntitle: "Safe handling"\ndescription: "D"\n---\n'
    seeded(make_vault, {C: page}, (REQ, C, "field `status`", STATUS_FIX))


@pytest.mark.parametrize("status", ["stub", "draft", "done"])
def test__scat_fm_required__title_missing_at_each_status(make_vault, status):
    page = f"---\ntype: concern\nstatus: {status}\ndescription: D\n---\n"
    fix = f'Fix: add the line `title: "Safe handling"` ({TITLE})'
    seeded(make_vault, {C: page}, (REQ, C, "field `title`", fix))


def test__scat_fm_required__title_empty_is_replaced(make_vault):
    page = "---\ntype: concern\nstatus: stub\ntitle:\n---\n"
    fix = f'Fix: replace the line `title:` with `title: "Safe handling"` ({TITLE})'
    seeded(make_vault, {C: page}, (REQ, C, "field `title`", fix))


def test__scat_fm_required__title_of_a_relation_page_uses_its_endpoints(make_vault):
    page = (
        '---\ntype: heldby\nstatus: stub\ngroup: "[[staff]]"\nconcern: "[[safe-handling]]"\n---\n'
    )
    fix = 'Fix: add the line `title: "Staff holds Safe handling"` (the title a stub of this pair gets)'
    seeded(make_vault, {H: page}, (REQ, H, "field `title`", fix))


def test__scat_fm_required__title_of_a_class_page_is_the_default(make_vault):
    page = "---\ntype: class\nindexes: concern\ndescription: D\n---\n" + region_for(
        make_vault, "concerns"
    )
    fix = 'Fix: add the line `title: "Concerns"` (the default title of the `concerns` class page)'
    seeded(
        make_vault, {"class/concerns.md": page}, (REQ, "class/concerns.md", "field `title`", fix)
    )


def test__scat_fm_required__indexes_of_a_named_class_page(make_vault):
    page = '---\ntype: class\ntitle: "Concerns"\ndescription: D\n---\n' + region_for(
        make_vault, "concerns"
    )
    fix = "Fix: add the line `indexes: concern`"
    seeded(
        make_vault, {"class/concerns.md": page}, (REQ, "class/concerns.md", "field `indexes`", fix)
    )


def test__scat_fm_required__indexes_of_another_class_page_is_a_choice(make_vault):
    page = '---\ntype: class\ntitle: "Foo"\ndescription: D\n---\n'
    keys = [
        "stakeholder-group",
        "concern",
        "affordance",
        "technology",
        "heldby",
        "addresses",
        "attributes",
    ]
    fix = choose(*[f"add the line `indexes: {k}`" for k in keys])
    seeded(make_vault, {"class/foo.md": page}, (REQ, "class/foo.md", "field `indexes`", fix))


TYPE = "SCAT-FM-TYPE"


def test__scat_fm_type__near_match_is_exact(make_vault):
    seeded(
        make_vault,
        {C: doc("Concern", "Safe handling")},
        (TYPE, C, "field `type`", "Fix: change it to `type: concern`"),
    )


def test__scat_fm_type__no_near_match_lists_the_twelve(make_vault):
    report = report_of(make_vault, {C: doc("gadget", "Safe handling")})
    assert [p.rule for p in report.problems] == [TYPE]  # links to it give no endpoint error
    fix = report.problems[0].fix
    assert fix.startswith("Fix, choose the one that describes this page:\n  1. `type: addresses` (")
    keys = [ln.split("`")[1] for ln in fix.split("\n")[1:]]
    assert keys == sorted(keys) and len(keys) == 12 and "type: scenario-raw" in keys


RL = "SCAT-FM-REQUIRED-LINK"


A = "addresses/self-checkout-addresses-quick-checkout.md"
T = "attributes/self-checkout-attributed-to-booking-app.md"
ENDPOINTS = [
    (H, "heldby", "group", "stakeholder-group", 'concern: "[[safe-handling]]"'),
    (H, "heldby", "concern", "concern", 'group: "[[staff]]"'),
    (A, "addresses", "concern", "concern", 'affordance: "[[self-checkout]]"'),
    (A, "addresses", "affordance", "affordance", 'concern: "[[quick-checkout]]"'),
    (T, "attributes", "affordance", "affordance", 'technology: "[[booking-app]]"'),
    (T, "attributes", "technology", "technology", 'affordance: "[[self-checkout]]"'),
]


@pytest.mark.parametrize("status", ["stub", "draft", "done"])
@pytest.mark.parametrize(("path", "type_", "key", "expected", "rest"), ENDPOINTS)
def test__scat_fm_required_link__each_endpoint_at_each_status(
    make_vault, path, type_, key, expected, rest, status
):
    page = doc(type_, "T", status=status, extra=rest)
    fix = f'Fix: add the line `{key}: "[[<one {expected} page you choose>]]"` (author)'
    r = report_of(make_vault, {path: page})
    assert got(r) == [(RL, path, f"field `{key}`", fix)], r.render()
    assert r.problems[0].what.startswith("missing; ")


def test__scat_fm_required_link__empty_value_is_replaced(make_vault):
    page = doc("heldby", "H", extra='group: "[[staff]]"\nconcern: ')
    fix = 'Fix: replace the line `concern:` with `concern: "[[<one concern page you choose>]]"` (author)'
    seeded(make_vault, {H: page}, (RL, H, "field `concern`", fix))


STATUS = "SCAT-FM-STATUS"


def test__scat_fm_status__near_match_is_exact(make_vault):
    seeded(
        make_vault,
        {C: doc("concern", "Safe handling", status="Done")},
        (STATUS, C, "field `status`", "Fix: change it to `status: done`"),
    )


def test__scat_fm_status__no_near_match_is_a_choice(make_vault):
    fix = (
        "Fix, choose one: `status: stub` (just started), `status: draft` (being written), "
        "`status: done` (finished)"
    )
    seeded(
        make_vault,
        {C: doc("concern", "Safe handling", status="finished")},
        (STATUS, C, "field `status`", fix),
    )


IDX = "SCAT-FM-INDEXES"


def test__scat_fm_indexes__near_match_is_exact(make_vault):
    page = doc("class", "Concerns", status=None, extra="indexes: concerns") + region_for(
        make_vault, "concerns"
    )
    fix = "Fix: change it to `indexes: concern`"
    seeded(
        make_vault, {"class/concerns.md": page}, (IDX, "class/concerns.md", "field `indexes`", fix)
    )


def test__scat_fm_indexes__no_near_match_lists_the_seven(make_vault):
    page = doc("class", "Concerns", status=None, extra="indexes: widgets") + region_for(
        make_vault, "concerns"
    )
    keys = [
        "stakeholder-group",
        "concern",
        "affordance",
        "technology",
        "heldby",
        "addresses",
        "attributes",
    ]
    fix = choose(*[f"`indexes: {k}`" for k in keys])
    seeded(
        make_vault, {"class/concerns.md": page}, (IDX, "class/concerns.md", "field `indexes`", fix)
    )


SHAPE = "SCAT-FM-SHAPE"


def test__scat_fm_shape__one_item_list_is_exact(make_vault):
    page = '---\ntype: concern\nstatus: done\ntitle:\n  - "Safe handling"\ndescription: "D"\n---\n'
    fix = 'Fix: replace the field with the line `title: "Safe handling"`'
    seeded(make_vault, {C: page}, (SHAPE, C, "field `title`", fix))


def test__scat_fm_shape__mapping_has_no_exact_fix(make_vault):
    page = '---\ntype: concern\nstatus: done\ntitle:\n  a: b\ndescription: "D"\n---\n'
    fix = "Fix: replace the field with one line of text you write"
    seeded(make_vault, {C: page}, (SHAPE, C, "field `title`", fix))


def test__scat_fm_shape__unquoted_yes_is_quoted(make_vault):
    page = '---\ntype: concern\nstatus: done\ntitle: yes\ndescription: "D"\n---\n'
    fix = 'Fix: replace the field with the line `title: "yes"`'
    seeded(make_vault, {C: page}, (SHAPE, C, "field `title`", fix))


def test__scat_fm_shape__a_number_is_quoted(make_vault):
    page = '---\ntype: concern\nstatus: done\ntitle: "S"\ndescription: 42\n---\n'
    fix = 'Fix: replace the field with the line `description: "42"`'
    seeded(make_vault, {C: page}, (SHAPE, C, "field `description`", fix))


def test__scat_fm_shape__null_is_missing_not_shape(make_vault):
    page = '---\ntype: concern\nstatus: done\ntitle: "S"\ndescription: ~\n---\n'
    assert [p.rule for p in report_of(make_vault, {C: page}).problems] == ["SCAT-DONE-FIELD"]


NAME = "SCAT-NAME"


SHARED = " (two pages share the name: change only the links that meant this page; the links meant for the other page keep `[[concerns]]`)"


def _name_fix(old, new):
    return f"Fix: change the file name to `{new}.md`, then change the links that meant this page from `[[{old}]]` to `[[{new}]]`"


def test__scat_name__space_and_capital(make_vault):
    path = "concern/Safe Tool.md"
    seeded(
        make_vault,
        {path: doc("concern", "Safe Tool")},
        (NAME, path, "frontmatter", _name_fix("Safe Tool", "safe-tool")),
    )


def test__scat_name__over_64_characters(make_vault):
    old = "a" * 65
    path = f"concern/{old}.md"
    seeded(
        make_vault,
        {path: doc("concern", "Long thing")},
        (NAME, path, "frontmatter", _name_fix(old, "long-thing")),
    )


def test__scat_name__reserved_name(make_vault):
    path = "concern/con.md"
    seeded(
        make_vault,
        {path: doc("concern", "Con")},
        (NAME, path, "frontmatter", _name_fix("con", "con-2")),
    )


def test__scat_name__doubled_hyphen(make_vault):
    path = "concern/a--b.md"
    seeded(
        make_vault,
        {path: doc("concern", "A b")},
        (NAME, path, "frontmatter", _name_fix("a--b", "a-b")),
    )


def test__scat_name__accented_title_derives_ascii(make_vault):
    path = "concern/Café menu.md"
    seeded(
        make_vault,
        {path: doc("concern", "Café menu")},
        (NAME, path, "frontmatter", _name_fix("Café menu", "cafe-menu")),
    )


def test__scat_name__non_latin_title_needs_a_hand_choice(make_vault):
    path = "concern/Привет.md"
    fix = "Fix: choose a legal name by hand (contract section 2)"
    seeded(make_vault, {path: doc("concern", "Привет")}, (NAME, path, "frontmatter", fix))


def test__scat_name__same_name_in_two_folders_reports_the_later_path(make_vault):
    path = "concern/quick-checkout.md"  # sorts after affordance/
    other = "affordance/quick-checkout.md"
    fix = (
        _name_fix("quick-checkout", "quick-checkout-2")
        + " (two pages share the name: change only the links that meant this page; "
        "the links meant for the other page keep `[[quick-checkout]]`)"
    )
    seeded(
        make_vault, {other: doc("affordance", "Quick checkout")}, (NAME, path, "frontmatter", fix)
    )


def test__scat_name__class_page_with_the_wrong_name(make_vault):
    path = "class/foo.md"
    page = doc("class", "Concerns", status=None, extra="indexes: concern")
    seeded(make_vault, {path: page}, (NAME, path, "frontmatter", _name_fix("foo", "concerns")))


def test__scat_name__class_page_with_its_own_name_is_fine(make_vault):
    page = doc("class", "Concerns", status=None, extra="indexes: concern") + region_for(
        make_vault, "concerns"
    )
    seeded(make_vault, {"class/concerns.md": page})


def test__scat_name__a_content_page_may_not_take_a_class_name(make_vault):
    path = "concern/concerns.md"
    seeded(
        make_vault,
        {path: doc("concern", "Concerns")},
        (
            NAME,
            path,
            "frontmatter",
            _name_fix("concerns", "concerns-2")
            + SHARED,  # the class page `concerns` shares the name
        ),
    )


def test__scat_fm_type__an_invalid_type_is_checked_by_no_rule_that_needs_it(make_vault):
    # no title, no description, a link field the real type would not list: the page has no usable type
    page = '---\ntype: gadget\nstatus: done\ngroups:\n  - "[[ghost]]"\n---\n'
    r = report_of(make_vault, {C: page})
    assert [p.rule for p in r.problems] == ["SCAT-FM-TYPE"]
