"""The three scopes, ok, ordering and format, the example vault, and that checks never write."""

import os
import re
from pathlib import Path

import pytest
from helpers import (
    CATALOGUE,
    DESK,
    EXAMPLES,
    KIOSK,
    base,
    catalogue_severities,
    doc,
    narrative,
    report_of,
    row,
    rules_of,
    seeded,
    vault,
)

import scat_tools
from scat_tools.checks import (
    DEFERRED,
    PAGE_RULES,
    SEVERITY,
    VAULT_RULES,
    check_neighborhood,
    check_page,
    check_vault,
    neighborhood,
)
from scat_tools.vault import read_vault

STAFF = "group/staff.md"
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


def messages(report) -> list[str]:
    return [p.render() for p in report.problems]


def test__clean_fixture__every_scope_gives_nothing(make_vault):
    v = vault(make_vault)
    assert check_vault(v).problems == ()
    for page in v.pages:
        assert check_page(v, page).problems == ()
        assert check_neighborhood(v, page).problems == ()
    assert check_vault(v).ok


def test__scopes__a_defect_in_a_neighbor_is_in_the_neighborhood_not_the_page(make_vault):
    v = vault(make_vault, {STAFF: doc("group", "Staff", description=None)})
    assert check_page(v, DESK).problems == ()  # the defect is on staff, not on the narrative
    near = check_neighborhood(v, DESK)
    assert [(p.rule, p.file) for p in near.problems] == [("SCAT-DONE-FIELD", STAFF)]
    assert not near.ok
    assert messages(check_page(v, STAFF)) == messages(
        near
    )  # the same page gives the same message at every scope


def test__scopes__a_defect_two_links_away_is_outside_the_neighborhood(make_vault):
    v = vault(make_vault, {TECH: doc("technology", "Booking app", description=None)})
    # the desk-day narrative links no technology; the kiosk pitch links the booking app
    assert check_neighborhood(v, DESK).problems == ()
    assert [p.file for p in check_neighborhood(v, KIOSK).problems] == [TECH]
    assert (
        check_neighborhood(v, "self-checkout").problems == ()
    )  # a node reached only through the narrative's rows


def test__scopes__the_neighborhood_follows_links_in_both_directions(make_vault):
    v = vault(make_vault)
    assert {p.name for p in neighborhood(v, "staff")} == {"staff", "desk-day"}  # a backlink only
    assert {p.name for p in neighborhood(v, DESK)} == {
        "desk-day",
        "staff",
        "safe-handling",
        "borrowers",
        "quick-checkout",
        "self-checkout",
    }
    assert {p.name for p in neighborhood(v, "quick-checkout")} == {
        "quick-checkout",
        "careful-keeping",  # its relationship annotation links it
        "desk-day",
        "kiosk-pitch",
    }


def test__scopes__a_defect_in_a_page_that_links_here_is_in_the_neighborhood(make_vault):
    v = vault(make_vault, {DESK: narrative(description=None)})
    assert [p.file for p in check_neighborhood(v, "staff").problems] == [DESK]
    assert check_page(v, "staff").problems == ()


def test__scopes__the_address_may_be_a_name_a_path_or_a_page(make_vault):
    v = vault(make_vault, {STAFF: doc("group", "Staff", description=None)})
    by_page = check_page(v, v.address(STAFF).page)
    assert messages(check_page(v, "staff")) == messages(check_page(v, STAFF)) == messages(by_page)
    with pytest.raises(LookupError):
        check_page(v, "nope")


def test__scopes__the_same_page_gives_the_same_messages_at_every_scope(make_vault):
    files = {
        STAFF: doc("group", "Staff", description=None),
        DESK: narrative(status="draft", timeframe=None, rows=(row("holds", "staff", "ghost"),)),
        "concern/safe-handling.md": doc("concern", "Safe handling", body="\nSee [[ghost2]].\n"),
    }
    v = vault(make_vault, files)
    whole = check_vault(v).problems
    for p in v.pages:
        mine = [m.render() for m in whole if m.file == p.path]
        assert messages(check_page(v, p)) == mine
        assert [m.render() for m in check_neighborhood(v, p).problems if m.file == p.path] == mine


def test__scopes__vault_rules_run_at_page_scope_only_for_a_group_page(make_vault):
    v = vault(make_vault, {"scat.toml": "attribution = 'disallowed'\nstakeholder_group_cap = 1\n"})
    assert rules_of(check_page(v, STAFF)) == ["SCAT-CAP"]
    assert rules_of(check_page(v, "concern/safe-handling.md")) == []
    assert rules_of(check_neighborhood(v, DESK)) == [
        "SCAT-CAP"
    ]  # the narrative's neighborhood holds groups
    assert rules_of(check_neighborhood(v, "concern/careful-keeping.md")) == []
    assert rules_of(check_vault(v)) == ["SCAT-CAP"]


def test__errors_block_and_warnings_do_not(make_vault):
    warn = report_of(
        make_vault, {DESK: narrative(status="draft", rows=(row("holds", "staff", "ghost"),))}
    )
    assert warn.ok and len(warn.warnings) == 1 and not warn.errors
    err = report_of(make_vault, {DESK: narrative(rows=(row("holds", "staff", "ghost"),))})
    assert not err.ok and len(err.errors) == 1 and not err.warnings


def test__every_rule_has_one_severity_and_none_is_deferred():
    stated = catalogue_severities()
    assert len(stated) == 42
    assert SEVERITY == stated
    assert DEFERRED == {}
    assert PAGE_RULES and VAULT_RULES
    for stem in (
        "TABLE-HEADER",
        "TABLE-ROW",
        "TABLE-TYPE",
        "TABLE-LAYERS",
        "TABLE-SECOND",
        "TABLE-DUPLICATE",
    ):
        assert (SEVERITY[f"SCAT-DRAFT-{stem}"], SEVERITY[f"SCAT-DONE-{stem}"]) == (
            "warning",
            "error",
        )
    for stem in ("END-NOLINK", "END-NOPAGE", "END-NOTNODE", "END-NOTINACCOUNT"):
        assert (SEVERITY[f"SCAT-DRAFT-{stem}"], SEVERITY[f"SCAT-DONE-{stem}"]) == (
            "warning",
            "error",
        )
    assert not [r for r in stated if "REFUSED" in r]  # an operation rule: no `scat check` prints it


def test__retired_ids_are_never_printed(make_vault):
    retired = re.findall(
        r"\| (SCAT-[A-Z-]+)(?:, (SCAT-[A-Z-]+))? \| retired \|", CATALOGUE.read_text()
    )
    ids = {i for pair in retired for i in pair if i}
    assert "SCAT-INDEX-STALE" in ids and "SCAT-CONFLICT-SELF" in ids and not ids & set(SEVERITY)


def test__messages_are_in_the_catalogues_order_and_format(make_vault):
    files = {
        "concern/safe-handling.md": doc(
            "concern", "Safe handling", body="\nSee [[ghost]] and [[ghost2]].\n"
        ),
        "affordance/self-checkout.md": doc("affordance", "Self checkout", description=None),
        DESK: narrative(
            status="draft",
            timeframe=None,
            rows=(row("holds", "staff", "ghost"), row("holds", "ghost2", "safe-handling")),
        ),
    }
    report = report_of(make_vault, files)
    keys = [
        (
            p.file.encode(),
            -1 if p.line is None else p.line,
            -1 if p.column is None else p.column,
            p.rule,
        )
        for p in report.problems
    ]
    assert keys == sorted(keys)
    assert [p.file for p in report.problems][:2] == [
        "affordance/self-checkout.md",
        "concern/safe-handling.md",
    ]
    heads = [m.split("\n")[0] for m in messages(report)]
    assert all(re.match(r"(error|warning) \[SCAT-[A-Z-]+\] [^ ]+ ", h) for h in heads)
    # the same line and column sort by rule id: the two ghosts on one line of the concern page
    assert [p.where for p in report.problems if p.file == "concern/safe-handling.md"] == [
        "link [[ghost]]",
        "link [[ghost2]]",
    ]


def test__line_and_column_appear_in_the_location_only_where_the_catalogue_gives_them(make_vault):
    files = {
        "concern/safe-handling.md": doc(
            "concern", "Safe handling", status=None, body="\nSee [[ghost]] and a briefing.\n"
        ),
        DESK: narrative(
            status="draft",
            rows=("| [[staff]] | holds | [[safe-handling]]", "| [[staff]] | holds | ghost | |"),
        ),
    }
    report = report_of(make_vault, files)
    shown = {p.rule: p.render().split(" ")[2] for p in report.problems}
    assert shown["SCAT-FM-REQUIRED"] == "concern/safe-handling.md"  # a field: no line
    assert shown["SCAT-LINK-DANGLING-BODY"] == "concern/safe-handling.md:7"  # a link: the line
    assert shown["SCAT-MENTION"] == "concern/safe-handling.md:7:21"  # a mention: line and column
    assert shown["SCAT-DRAFT-TABLE-ROW"] == f"{DESK}:16:1"  # a row: its first `|`
    assert shown["SCAT-DRAFT-END-NOLINK"] == f"{DESK}:17:23"  # a cell: its first character


def test__examples__no_errors_and_only_the_two_warnings_the_readme_names():
    v = read_vault(EXAMPLES)
    report = check_vault(v)
    assert report.ok and not report.errors
    # the draft narrative is unfinished on purpose: no `description` and no `timeframe`
    assert [(p.rule, p.file, p.where) for p in report.problems] == [
        ("SCAT-DRAFT-FIELD", "narrative/funders-meeting.md", "field `description`"),
        ("SCAT-DRAFT-FIELD", "narrative/funders-meeting.md", "field `timeframe`"),
    ]
    for page in v.pages:
        mine = [m.render() for m in report.problems if m.file == page.path]
        assert messages(check_page(v, page)) == mine
        assert [
            m.render() for m in check_neighborhood(v, page).problems if m.file == page.path
        ] == mine


def test__checks_leave_the_directory_unchanged(make_vault):
    root = vault(make_vault, {STAFF: doc("group", "Staff", description=None)}).root
    before = snapshot(root)
    v = read_vault(root)
    check_vault(v)
    check_page(v, STAFF)
    check_neighborhood(v, DESK)
    scat_tools.check(root=root)
    assert snapshot(root) == before


def test__checks_leave_the_example_vault_unchanged():
    before = snapshot(EXAMPLES)
    check_vault(read_vault(EXAMPLES))
    scat_tools.check(root=EXAMPLES)
    assert snapshot(EXAMPLES) == before


def test__no_vault_content_crashes_a_check(make_vault):
    junk = {
        "concern/a.md": "---\n---\n",
        "concern/b.md": "---\ntype: [1, 2]\n---\n",
        "concern/c.md": "---\ntype: concern\nstatus: [x]\ntitle: {a: b}\n---\n[[\n]]\n[[a]][[b]]|\n",
        "narrative/d.md": "---\ntype: narrative\nstatus: draft\ntitle: D\n---\n## Edges told\n|\n|||\n| a |\n",
        "narrative/e.md": "---\ntype: narrative\nstatus: draft\ntitle: E\n---\n# edges TOLD #\n| from | type | to | note |\n|:-:|--|\n| x |\n",
        "narrative/f.md": "---\ntype: narrative\nstatus: done\n---\n## Edges told\n\n| from | type | to | note |\n|---|---|---|---|\n| [[ ]] | holds | ![[c]] | `|` |\n| [[c]] | holds\n",
        "bin.md": b"\xff\xfe\x00 not utf-8",
        "x/.hidden.md": "---\ntype: concern\n---\n",
    }
    v = vault(make_vault, junk)
    check_vault(v)
    for p in v.pages:
        check_page(v, p)
        check_neighborhood(v, p)


def test__invalid_utf8_and_crlf_are_read(make_vault):
    page = b'---\ntype: concern\nstatus: done\ntitle: "Safe handling"\ndescription: "D"\n---\n\xff body\n'
    seeded(make_vault, {"concern/safe-handling.md": page, DESK: narrative().replace("\n", "\r\n")})
    seeded(make_vault, {DESK: narrative().replace("\n", "\r\n")})
    seeded(make_vault, {DESK: "\ufeff" + narrative()})  # a byte order mark is dropped
    ghost = narrative(status="draft", rows=(row("holds", "staff", "ghost"),))
    assert messages(report_of(make_vault, {DESK: ghost})) == messages(
        report_of(make_vault, {DESK: ghost.replace("\n", "\r\n")})
    )


def test__base_fixture_is_the_one_the_tests_start_from(make_vault):
    v = vault(make_vault)
    assert sorted(p.type for p in v.pages) == sorted(
        ["group"] * 2 + ["concern"] * 3 + ["affordance"] * 2 + ["technology"] + ["narrative"] * 2
    )
    assert all(p.status == "done" for p in v.pages)
    assert len(base()) == len(v.pages) + 1  # the pages and scat.toml
