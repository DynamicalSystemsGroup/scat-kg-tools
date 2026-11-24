"""WP10: `timeframe` on the raw pages. Missing is a warning before `done` and an error at `done`; a value
outside the three is an error at every status; each of the three values is clean. Both raw page types.
Test names carry the rule id (see test_coverage)."""

import pytest
from helpers import choose, doc, links, seeded, set_status

RAW = {
    "scenario-raw": ("scenario-raw/desk-day.md", "desk-day", "desk-day-coded"),
    "architecture-raw": ("architecture-raw/kiosk-pitch.md", "kiosk-pitch", "kiosk-pitch-coded"),
}
VALUES = ("past", "future", "mixed")
BOTH = pytest.mark.parametrize("kind", RAW)


def page(kind, timeframe, status="done"):
    """The base raw page with its `timeframe` line replaced: None leaves the line out."""
    _, _, coded = RAW[kind]
    line = "" if timeframe is None else f"timeframe: {timeframe}\n"
    return doc(kind, "T", status=status, extra=line + links("coded", coded))


def picks(verb, name, with_status=True):
    out = [f"{verb} `timeframe: {v}` (author)" for v in VALUES]
    return out + ([f"run {set_status(name)} if the page is not finished"] if with_status else [])


@BOTH
@pytest.mark.parametrize("value", VALUES)
def test__scat_fm_timeframe__each_valid_value_is_clean_at_each_status(make_vault, kind, value):
    path, _, _ = RAW[kind]
    for status in ("stub", "draft", "done"):
        seeded(make_vault, {path: page(kind, value, status)})


@BOTH
@pytest.mark.parametrize("status", ["stub", "draft", "done"])
def test__scat_fm_timeframe__near_match_is_exact(make_vault, kind, status):
    path, _, _ = RAW[kind]
    seeded(
        make_vault,
        {path: page(kind, "Past", status)},
        (
            "SCAT-FM-TIMEFRAME",
            path,
            "field `timeframe`",
            "Fix: change it to `timeframe: past`",
        ),
    )


@BOTH
@pytest.mark.parametrize("status", ["stub", "draft", "done"])
def test__scat_fm_timeframe__no_near_match_lists_the_three(make_vault, kind, status):
    path, _, _ = RAW[kind]
    fix = choose(*[f"`timeframe: {v}`" for v in VALUES])
    r = seeded(
        make_vault,
        {path: page(kind, "soon", status)},
        ("SCAT-FM-TIMEFRAME", path, "field `timeframe`", fix),
    )
    assert not r.ok and r.problems[0].what == "`soon` is not a timeframe"


@BOTH
def test__scat_done_field__timeframe_missing_at_done_offers_the_three_values(make_vault, kind):
    path, name, _ = RAW[kind]
    seeded(
        make_vault,
        {path: page(kind, None)},
        ("SCAT-DONE-FIELD", path, "field `timeframe`", choose(*picks("add the line", name))),
    )


@BOTH
@pytest.mark.parametrize("empty", ["", " # past | future | mixed"])
def test__scat_done_field__timeframe_empty_is_missing_not_invalid(make_vault, kind, empty):
    path, name, _ = RAW[kind]
    fix = choose(
        *[f"replace the line `timeframe:{empty}` with `timeframe: {v}` (author)" for v in VALUES],
        f"run {set_status(name)} if the page is not finished",
    )
    r = seeded(
        make_vault,
        {path: doc(kind, "T", extra=f"timeframe:{empty}\n" + links("coded", RAW[kind][2]))},
        ("SCAT-DONE-FIELD", path, "field `timeframe`", fix),
    )
    assert not r.ok


@BOTH
def test__scat_draft_field__timeframe_missing_at_draft_is_a_warning(make_vault, kind):
    path, _, _ = RAW[kind]
    fix = choose(*picks("add the line", "x", with_status=False)).replace(
        "Fix, choose one:", "Fix, choose one before you set status: done:"
    )
    r = seeded(
        make_vault,
        {path: page(kind, None, "draft")},
        ("SCAT-DRAFT-FIELD", path, "field `timeframe`", fix),
    )
    assert r.ok and r.problems[0].severity == "warning"


@BOTH
def test__scat_draft_field__timeframe_missing_at_stub_is_a_warning(make_vault, kind):
    path, _, _ = RAW[kind]
    fix = choose(*picks("add the line", "x", with_status=False)).replace(
        "Fix, choose one:", "Fix, choose one before you set status: done:"
    )
    r = seeded(
        make_vault,
        {path: page(kind, None, "stub")},
        ("SCAT-DRAFT-FIELD", path, "field `timeframe`", fix),
    )
    assert r.ok and r.problems[0].severity == "warning"


def test__scat_draft_field__a_stub_stays_silent_about_description(make_vault):
    seeded(
        make_vault,
        {"concern/safe-handling.md": doc("concern", "S", status="stub", description=None)},
    )
