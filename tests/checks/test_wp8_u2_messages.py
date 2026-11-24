"""WP8-U2: the SCAT-LINK-ENDPOINT fix must not lead into SCAT-DONE-LINK; the SCAT-CAP fix clusters first."""

from helpers import SC, coded, line_of, links, report_of
from test_graph_rules import GROUPS

ENDPOINT = "SCAT-LINK-ENDPOINT"
DONE_LINK = "SCAT-DONE-LINK"
ONLY_WRONG = links("concerns", "self-checkout")  # an affordance, the only item under `concerns`


def rules(r):
    return [p.rule for p in r.problems]


def endpoint_fix(r):
    return next(p.fix for p in r.problems if p.rule == ENDPOINT)


def test__link_endpoint__sole_wrong_item_in_a_required_field_offers_no_delete_or_move(make_vault):
    r = report_of(make_vault, {SC: coded(concerns=ONLY_WRONG)})
    fix = endpoint_fix(r)
    assert "delete the item line" not in fix
    assert "move the item line" not in fix
    assert 'replace `- "[[self-checkout]]"` with `- "[[quick-checkout]]"`' in fix
    assert "SCAT-DONE-LINK" in fix and "run `scat set-status desk-day-coded draft`" in fix


def test__link_endpoint__applying_the_offered_replacement_leaves_no_done_link_error(make_vault):
    page = coded(concerns=ONLY_WRONG)
    assert 'replace `- "[[self-checkout]]"` with `- "[[quick-checkout]]"`' in endpoint_fix(
        report_of(make_vault, {SC: page})
    )
    fixed = page.replace(
        'concerns:\n  - "[[self-checkout]]"', 'concerns:\n  - "[[quick-checkout]]"'
    )
    assert "quick-checkout" in fixed
    r = report_of(make_vault, {SC: fixed})
    assert ENDPOINT not in rules(r) and DONE_LINK not in rules(r)


def test__link_endpoint__applying_the_status_command_first_leaves_no_done_link_error(make_vault):
    page = coded(concerns=ONLY_WRONG)
    # the fix says: run `scat set-status desk-day-coded draft` first, then delete the item
    drafted = page.replace("status: done", "status: draft").replace(
        'concerns:\n  - "[[self-checkout]]"\n', "concerns:\n"
    )
    r = report_of(make_vault, {SC: drafted})
    assert DONE_LINK not in rules(r)


def test__link_endpoint__sole_wrong_item_with_no_replacement_names_the_command_first(make_vault):
    page = coded(raw=links("raw", "kiosk-pitch"))
    fix = endpoint_fix(report_of(make_vault, {SC: page}))
    assert fix == (
        "Fix: `raw` is required on a page with status: done and this is its only good item, and no "
        "existing scenario-raw page was found to replace it with: run "
        '`scat set-status desk-day-coded draft` (REPL: `scat_kg.set_status("desk-day-coded", "draft")`) '
        "first, then change the item by hand"
    )


def test__link_endpoint__another_good_item_keeps_the_move_and_delete_options(make_vault):
    page = coded(concerns=links("concerns", "safe-handling", "briefing"))
    fix = endpoint_fix(report_of(make_vault, {SC: page}))
    assert "move the item line" in fix and "delete the item line" in fix
    assert "SCAT-DONE-LINK" not in fix


def test__link_endpoint__a_draft_page_still_offers_delete(make_vault):
    page = coded(status="draft", concerns=ONLY_WRONG)
    assert "delete the item line" in endpoint_fix(report_of(make_vault, {SC: page}))


def test__scat_cap__the_fix_clusters_into_an_existing_group_before_raising_the_cap(make_vault):
    r = report_of(make_vault, GROUPS)
    cap = next(p for p in r.problems if p.rule == "SCAT-CAP")
    assert cap.fix == (
        "Fix, choose one:\n"
        "  1. cluster 1 group(s) into the others, by shared standpoint: move their standpoints into "
        "another group's `description`, change every link to them to point at that group, and "
        "delete those pages\n"
        "  2. or, only if the plan allows more groups, write `stakeholder_group_cap = 4` in "
        "scat.toml (the cap protects against identifying individuals)"
    )
    assert cap.fix.index("cluster") < cap.fix.index("stakeholder_group_cap")
    assert line_of(cap.fix, "cluster") < line_of(cap.fix, "stakeholder_group_cap")
