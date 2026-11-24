"""The three scopes, ok, ordering and format, the example vault, and that checks never write."""

import os
import re
from pathlib import Path

import pytest
from helpers import (
    EXAMPLES,
    SC,
    base,
    coded,
    doc,
    got,
    links,
    report_of,
    run,
    seeded,
    vault,
)

from scat_kg.checks import (
    DEFERRED,
    PAGE_RULES,
    SEVERITY,
    VAULT_RULES,
    check_neighborhood,
    check_page,
    check_vault,
    neighborhood,
)
from scat_kg.vault import read_vault

STAFF = "stakeholder-group/staff.md"
TECH = "technology/booking-app.md"


def snapshot(root: Path) -> dict:
    out = {}
    for dirpath, dirnames, filenames in os.walk(root):
        for n in dirnames:
            out[str(Path(dirpath, n))] = ("dir",)
        for n in filenames:
            p = Path(dirpath, n)
            out[str(p)] = ("file", p.stat().st_size, p.stat().st_mtime_ns, p.read_bytes())
    return out


def test__clean_fixture__every_scope_gives_nothing(make_vault):
    v = vault(make_vault)
    assert check_vault(v).problems == ()
    for page in v.pages:
        assert check_page(v, page).problems == ()
        assert check_neighborhood(v, page).problems == ()
    assert check_vault(v).ok


def test__scopes__a_defect_in_a_neighbor_is_in_the_neighborhood_not_the_page(make_vault):
    v = vault(make_vault, {STAFF: doc("stakeholder-group", "Staff", description=None)})
    assert check_page(v, SC).problems == ()  # the defect is on staff, not on the scenario
    near = check_neighborhood(v, SC)
    assert [(p.rule, p.file) for p in near.problems] == [("SCAT-DONE-FIELD", STAFF)]
    assert not near.ok
    own = check_page(v, STAFF)
    assert got(own) == got(near)  # the same page gives the same message at every scope


def test__scopes__a_defect_two_links_away_is_outside_the_neighborhood(make_vault):
    v = vault(make_vault, {TECH: doc("technology", "Booking app", description=None)})
    # SC links raw, groups, concerns and affordances, and the architecture links the technology
    assert check_neighborhood(v, SC).problems == ()
    assert [p.file for p in check_neighborhood(v, "kiosk-pitch-coded").problems] == [TECH]


def test__scopes__the_neighborhood_follows_links_in_both_directions(make_vault):
    v = vault(make_vault)
    names = {p.name for p in neighborhood(v, "staff")}
    # backlinks only: the relation page, the coded scenario, and the class page whose table lists the group
    assert names == {"staff", "desk-day-coded", "staff-holds-safe-handling", "stakeholder-groups"}
    names = {p.name for p in neighborhood(v, "desk-day-coded")}
    assert names == {"desk-day-coded", "desk-day", "staff", "safe-handling", "self-checkout"}


def test__scopes__a_defect_in_a_page_that_links_here_is_in_the_neighborhood(make_vault):
    v = vault(make_vault, {SC: coded(status="done", affordances="")})
    assert [(p.rule, p.file) for p in check_neighborhood(v, "staff").problems] == [
        ("SCAT-DONE-LINK", SC)
    ]
    assert check_page(v, "staff").problems == ()


def test__scopes__the_address_may_be_a_name_a_path_or_a_page(make_vault):
    v = vault(make_vault, {STAFF: doc("stakeholder-group", "Staff", description=None)})
    expect = got(check_page(v, "staff"))
    assert got(check_page(v, STAFF)) == expect == got(check_page(v, v.address("staff").page))
    with pytest.raises(LookupError):
        check_page(v, "no-such-page")


def test__scopes__vault_rules_run_at_page_scope_only_for_a_group_page(make_vault):
    files = {"scat.toml": "stakeholder_group_cap = 1\n"}
    v = vault(make_vault, files)
    assert [p.rule for p in check_page(v, "staff").problems] == ["SCAT-CAP"]
    assert [p.rule for p in check_neighborhood(v, "staff").problems] == ["SCAT-CAP"]
    assert check_page(v, "safe-handling").problems == ()
    assert [p.rule for p in check_vault(v).problems] == ["SCAT-CAP"]
    # the neighborhood of a concern holds the heldby page and the scenario, but no group page
    assert check_neighborhood(v, "safe-handling").problems == ()
    # one that holds a group page in its neighbors does
    assert [p.rule for p in check_neighborhood(v, "desk-day-coded").problems] == ["SCAT-CAP"]


# errors block, warnings do not


def test__errors_block_and_warnings_do_not(make_vault):
    warn = report_of(make_vault, {SC: coded(status="draft", groups="")})
    assert [p.severity for p in warn.problems] == ["warning"] and warn.ok
    assert warn.errors == () and len(warn.warnings) == 1
    err = report_of(make_vault, {SC: coded(groups="")})
    assert [p.severity for p in err.problems] == ["error"] and not err.ok
    both = report_of(
        make_vault,
        {
            SC: coded(groups="", body="quick checkout\n"),
            STAFF: doc("stakeholder-group", "S", status="draft", description=None),
        },
    )
    assert {p.severity for p in both.problems} == {"error", "warning"} and not both.ok
    assert all(p.severity == SEVERITY[p.rule] for p in both.problems)


def test__every_rule_has_one_severity_and_none_is_deferred():
    assert DEFERRED == {} and SEVERITY["SCAT-INDEX-STALE"] == "warning"  # every rule is implemented
    assert len(SEVERITY) == 28
    assert len(PAGE_RULES) + len(VAULT_RULES) >= 15


# order and format


def test__messages_are_in_the_catalogues_order_and_format(make_vault):
    files = {
        SC: coded(groups="", concerns=links("concerns", "safe-handling", "ghost")),
        "concern/careful-keeping.md": doc(
            "concern", "C", description=None, extra=links("conflicts", "quick-checkout")
        ),
    }
    r = report_of(make_vault, files)
    assert [(p.file, p.rule) for p in r.problems] == [
        ("concern/careful-keeping.md", "SCAT-DONE-FIELD"),
        (SC, "SCAT-DONE-LINK"),
        (SC, "SCAT-LINK-DANGLING"),
    ]
    head = re.compile(
        r"^(error|warning) \[SCAT-[A-Z-]+\] \S+( field `\w+`| link \[\[[^\]]+\]\]| frontmatter| text `.*`): .+$"
    )
    for p in r.problems:
        text = p.render().split("\n")
        assert head.match(text[0]), text[0]
        assert all(line.startswith("  ") for line in text[1:]) and text[1].startswith("  Fix")
    assert r.render().count("\n  Fix") == 3


def test__line_and_column_appear_in_the_location_only_where_the_catalogue_gives_them(make_vault):
    r = report_of(
        make_vault, {SC: coded(body="quick checkout\n", concerns=links("concerns", "ghost"))}
    )
    first = [p.render().split("\n")[0] for p in r.problems]
    assert any(re.match(r"^error \[SCAT-LINK-DANGLING\] \S+:\d+ field", x) for x in first)
    assert any(re.match(r"^warning \[SCAT-MENTION\] \S+:\d+:\d+ text", x) for x in first)


# the examples (WP5-R8)


def test__examples__no_errors_and_only_the_warning_the_readme_names():
    v = read_vault(EXAMPLES)
    report = check_vault(v)
    assert report.ok and report.errors == ()
    assert [(p.rule, p.file) for p in report.problems] == [
        ("SCAT-DRAFT-FIELD", "heldby/volunteer-staff-holds-careful-record-keeping.md")
    ]
    for page in v.pages:
        for scope in ("page", "neighborhood"):
            r = run(v, scope, page)
            assert r.errors == (), (page.path, r.render())
            assert {(p.rule, p.file) for p in r.problems} <= {
                ("SCAT-DRAFT-FIELD", "heldby/volunteer-staff-holds-careful-record-keeping.md")
            }


# checks never write (R-4)


def test__checks_leave_the_directory_unchanged(make_vault):
    files = {
        SC: coded(
            groups="",
            body="quick checkout [[ghost]]\n",
            concerns=links("concerns", "safe-handling", "ghost"),
        ),
        "concern/quick-checkout.md": doc(
            "concern", "Q", extra=links("conflicts", "quick-checkout")
        ),
        "notes.md": "words\n",
        "scat.toml": "stakeholder_group_cap = 1\n",
        "bad.md": "---\ntype: concern\n\tstatus: done\n---\n",
    }
    v = vault(make_vault, files)
    root = v.root
    before = snapshot(root)
    full = check_vault(v)
    assert len(full.problems) > 5  # the vault really is full of defects
    for page in v.pages:
        check_page(v, page)
        check_neighborhood(v, page)
    assert snapshot(root) == before


def test__checks_leave_the_example_vault_unchanged():
    before = snapshot(EXAMPLES)
    v = read_vault(EXAMPLES)
    check_vault(v)
    for page in v.pages:
        check_page(v, page)
        check_neighborhood(v, page)
    assert snapshot(EXAMPLES) == before


# nothing a vault holds may crash a check


WEIRD = {
    "w/type-list.md": "---\ntype: [a, b]\n---\n",
    "w/type-null.md": "---\ntype:\n---\n",
    "w/status-num.md": "---\ntype: concern\nstatus: 5\ntitle: 7\ndescription: [1, 2]\nconflicts: 5\n---\n",
    "w/links-weird.md": "---\ntype: scenario-coded\nstatus: done\ntitle: x\ndescription: x\nraw: {a: b}\ngroups: 3\n"
    'concerns:\n  - [[a, b]]\n  - null\n  - 2.5\naffordances: "[[a]]"\n---\n[[\n]]\n![[x]] [[|]] [[^]]\n',
    "w/relation-weird.md": "---\ntype: heldby\nstatus: done\ntitle: x\ndescription: x\ngroup:\n  - 1\nconcern: [[x]]\n---\n",
    "w/class-weird.md": "---\ntype: class\nindexes: [x]\ntitle: 5\n---\n",
    "w/date.md": "---\ntype: concern\nstatus: done\ntitle: 2024-01-01\ndescription: x\n---\n",
    "w/bom.md": "﻿---\ntype: concern\nstatus: done\ntitle: b\ndescription: x\n---\nquick checkout\n",
    "w/empty.md": "",
    "w/only-fence.md": "---\n",
    "scat.toml": "stakeholder_group_cap = true\n",
}


def test__no_vault_content_crashes_a_check(make_vault):
    v = vault(make_vault, WEIRD)
    report = check_vault(v)
    assert not report.ok
    for page in v.pages:
        check_page(v, page)
        check_neighborhood(v, page)
    assert check_vault(v).render() == report.render()  # deterministic


def test__invalid_utf8_and_crlf_are_read(make_vault):
    files = {"w/latin1.md": b"---\ntype: concern\nstatus: done\ntitle: \xe9\ndescription: x\n---\n"}
    assert check_vault(vault(make_vault, files)).problems == ()


def test__base_fixture_is_the_one_the_tests_start_from(make_vault):
    assert len(base()) == 16
    seeded(make_vault, {})
