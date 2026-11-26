"""SCAT-MODE-CONFIG (WP23-G1, R1): the vault declares its attribution mode, and it is one of the three. Test names
carry the rule id."""

import pytest
from helpers import choose, msg, report_of, rules_of, seeded

HEAD = "error [SCAT-MODE-CONFIG] scat.toml field `attribution`: {what}"
MODES = ("required", "optional", "disallowed")
TAIL = (
    'or with `attribution = "optional"` (a narrative may name who it is attributed to)',
    'or with `attribution = "disallowed"` (no narrative names who it is attributed to)',
)


def first(verb):
    return (
        f'{verb} `attribution = "required"` (a `done` narrative must name who it is attributed to)'
        " in scat.toml"
    )


def test__scat_mode_config__a_missing_key_is_refused_with_the_three_choices(make_vault):
    seeded(
        make_vault,
        {"scat.toml": "stakeholder_group_cap = 3\n"},
        msg(HEAD.format(what="the key is missing"), *choose(first("add the line"), *TAIL)),
    )


@pytest.mark.parametrize("written", ['"public"', '"Required"', "3", "true", '""'])
def test__scat_mode_config__an_unknown_value_is_replaced(make_vault, written):
    seeded(
        make_vault,
        {"scat.toml": f"attribution = {written}\nstakeholder_group_cap = 3\n"},
        msg(
            HEAD.format(
                what=f"the value `{written}` is not one of `required`, `optional`, `disallowed`"
            ),
            *choose(first(f"replace the line `attribution = {written}` with"), *TAIL),
        ),
    )


@pytest.mark.parametrize("mode", MODES)
def test__scat_mode_config__each_of_the_three_modes_is_accepted(make_vault, mode):
    r = report_of(make_vault, {"scat.toml": f'attribution = "{mode}"\nstakeholder_group_cap = 3\n'})
    assert "SCAT-MODE-CONFIG" not in rules_of(r)


def test__scat_mode_config__the_fix_is_three_exact_edits_of_the_key(make_vault):
    r = report_of(make_vault, {"scat.toml": "stakeholder_group_cap = 3\n"})
    (p,) = r.problems
    assert p.field == "attribution" and p.fix_data.kind == "options"
    assert [
        (o.kind, o.edits[0].file, o.edits[0].field, o.edits[0].value) for o in p.fix_data.options
    ] == [("exact", "scat.toml", "attribution", m) for m in MODES]


def test__scat_mode_config__runs_at_every_scope_a_group_page_is_in(make_vault):
    for scope, page in (("page", "group/staff.md"), ("neighborhood", "group/staff.md")):
        r = report_of(
            make_vault, {"scat.toml": "stakeholder_group_cap = 3\n"}, scope=scope, page=page
        )
        assert rules_of(r) == ["SCAT-MODE-CONFIG"]


def test__scat_mode_config__a_missing_or_broken_file_is_the_caps_problem_alone(make_vault):
    assert rules_of(report_of(make_vault, remove=["scat.toml"])) == ["SCAT-CAP-CONFIG"]
    assert rules_of(report_of(make_vault, {"scat.toml": "attribution = = 1\n"})) == [
        "SCAT-CAP-CONFIG"
    ]


def test__scat_mode_config__and_the_cap_problems_are_each_reported(make_vault):
    r = report_of(make_vault, {"scat.toml": "other = 1\n"})
    assert sorted(rules_of(r)) == ["SCAT-CAP-CONFIG", "SCAT-MODE-CONFIG"]
