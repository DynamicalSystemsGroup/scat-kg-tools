"""SCAT-UNCODED (WP21-G2): a narrative that links no node page is excluded, and the check says so (a warning)."""

import pytest
from helpers import DESK, doc, narrative, report_of, rules_of, seeded, uncoded

import scat_tools

NO_LINK = "Nothing here names a node.\n"


@pytest.mark.parametrize("status", ["stub", "draft", "done"])
def test__scat_uncoded__a_narrative_with_no_link_gets_the_warning_at_every_status(
    make_vault, status
):
    page = narrative(status=status, account=NO_LINK, section="")
    r = seeded(
        make_vault, {DESK: page}, uncoded(DESK)
    )  # one message: SCAT-NOEDGES stays silent on an uncoded narrative
    assert r.ok and r.problems[0].severity == "warning"


@pytest.mark.parametrize("scope", ["vault", "page", "neighborhood"])
def test__scat_uncoded__the_same_message_at_every_scope(make_vault, scope):
    page = narrative(account=NO_LINK, section="")
    seeded(make_vault, {DESK: page}, uncoded(DESK), scope=scope, page=DESK)


def test__scat_uncoded__silent_when_the_account_links_a_node_page_and_there_is_no_row(make_vault):
    page = narrative(account="Only the [[staff]] spoke.\n", section="")
    assert "SCAT-UNCODED" not in rules_of(report_of(make_vault, {DESK: page}))


def test__scat_uncoded__silent_when_the_link_is_in_a_list_beyond_the_text(make_vault):
    page = narrative(account="No names.\n\n## Linked beyond the text\n\n- [[staff]]\n", section="")
    assert "SCAT-UNCODED" not in rules_of(report_of(make_vault, {DESK: page}))


def test__scat_uncoded__silent_when_the_only_link_is_a_row_end(make_vault):
    page = narrative(account=NO_LINK, rows=("| [[staff]] | holds | [[safe-handling]] | |",))
    assert "SCAT-UNCODED" not in rules_of(report_of(make_vault, {DESK: page}))


@pytest.mark.parametrize(
    "account",
    ["See [[desk-day]] and [[nowhere]].\n", "Code `[[staff]]` is no link.\n"],
    ids=["not-a-node-or-no-page", "code-span"],
)
def test__scat_uncoded__still_fires_when_the_only_links_are_not_node_pages(make_vault, account):
    page = narrative(account=account, section="")
    assert "SCAT-UNCODED" in rules_of(report_of(make_vault, {DESK: page}))


def test__scat_uncoded__fires_only_on_a_narrative(make_vault):
    assert "SCAT-UNCODED" not in rules_of(
        report_of(make_vault, {"concern/safe-handling.md": doc("concern", "Safe handling")})
    )


def test__scat_uncoded__does_not_refuse_set_status_done(make_vault):
    page = narrative(status="draft", account=NO_LINK, section="")
    root = make_vault(
        {"scat.toml": "attribution = 'disallowed'\nstakeholder_group_cap = 3\n", DESK: page}
    )
    result = scat_tools.set_status("desk-day", "done", root=root)
    assert result.ok, str(result)


def test__scat_noedges__a_coded_narrative_with_only_an_account_link_is_conformant(make_vault):
    page = narrative(account="Only the [[staff]] spoke.\n", section="")
    r = report_of(make_vault, {DESK: page})
    assert r.ok and rules_of(r) == [
        "SCAT-NOEDGES"
    ]  # a warning: it tells no edge, and its fingerprint has a node
