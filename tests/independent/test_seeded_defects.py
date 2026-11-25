"""WP16-R1: a seeded-defect test for every rule of contracts/rule-catalogue.md, from the catalogue's own Seed lines.

Each seed starts from the clean fixture (zero messages), injects one defect and expects exactly the messages the
catalogue's templates give: id, severity, file, place, text and Fix. Expectations are written from the catalogue
text, never from the checker's output. Pair rules run at stub, draft and done (DRAFT warning, DONE error).
"""

import re

import pytest
from indep_kit import (
    NARRATIVE_FILE as NF,
)
from indep_kit import (
    ROW1,
    ROW2,
    STATUSES,
    Exp,
    assert_messages,
    page_text,
    pair,
    row_line,
)

SEEDS = []


def seed(name, statuses=("draft",), allow=()):
    def deco(fn):
        for st in statuses:
            SEEDS.append(pytest.param(fn, st, allow, id=f"{name}@{st}"))
        return fn

    return deco


ALL = STATUSES
E_ = "error"
W_ = "warning"
HEADER = "| from | type | to | note |"
SEP = "|---|---|---|---|"
NOTE_FIX = "any text beside it belongs in the `note` cell by hand"


def stub_opt(name, key):
    art = "an" if key == "affordance" else "a"
    return f'run `scat stub {name} --type {key}` (REPL: `scat_kg.stub("{name}", type="{key}")`) to create {art} {key} page'


def draft_cmd(name):
    return f'run `scat set-status {name} draft` (REPL: `scat_kg.set_status("{name}", "draft")`)'


def put(v, type_, name, title, status="done", description="A page.", **kw):
    v.write(f"{type_}/{name}.md", page_text(type_, title, status, description, **kw))
    return f"{type_}/{name}.md"


def set_row(v, n, text):
    v.edit(NF, v.line(NF, row_line(n)), text)


def narr_exp(name, st, file=NF, **kw):
    rule, sev = pair(name, st)
    return Exp(rule, sev, file, **kw)


# ======================================================================================= frontmatter rules
@seed("FM-PARSE-no-close", ALL)
def _(v, st):
    v.write(
        "concern/broken.md", '---\ntype: concern\nstatus: draft\ntitle: "Broken"\n\nBody text.\n'
    )
    return [
        Exp(
            "SCAT-FM-PARSE",
            E_,
            "concern/broken.md",
            "frontmatter",
            "the closing --- line is missing",
            fix="make the frontmatter a block of `key: value` lines between two lines containing only `---`, at the "
            "very top of the file; start from the first line the parser rejected",
        )
    ]


@seed("FM-PARSE-tab", ALL)
def _(v, st):
    v.write("concern/broken.md", '---\ntype: concern\n\tstatus: draft\ntitle: "Broken"\n---\n')
    return [
        Exp(
            "SCAT-FM-PARSE",
            E_,
            "concern/broken.md",
            "frontmatter",
            re.compile(r".+"),
            fix_has=("Fix: make the frontmatter",),
        )
    ]


@seed("FM-PARSE-silent-cases", ("draft",))
def _(v, st):
    clean = page_text("concern", "Crlf page", "draft")
    v.write("concern/crlf-page.md", clean, crlf=True)
    v.write("README.md", "# A readme\n\nNo frontmatter.\n")
    v.write("notes/no-type.md", '---\ntitle: "No type"\n---\nbody\n')
    return []


@seed("FM-REQUIRED-status", ALL)
def _(v, st):
    v.write(
        "concern/lending-desk.md",
        '---\ntype: concern\ntitle: "Lending desk"\ndescription: "d"\n---\n',
    )
    return [
        Exp(
            "SCAT-FM-REQUIRED",
            E_,
            "concern/lending-desk.md",
            "field `status`",
            "missing",
            fix=f"{draft_cmd('lending-desk')}; use `stub` or `done` instead of `draft` if that is the truth",
        )
    ]


@seed("FM-REQUIRED-status-narrative", ("draft",))
def _(v, st):
    v.edit(NF, "status: draft\n", "")
    return [
        Exp(
            "SCAT-FM-REQUIRED",
            E_,
            NF,
            "field `status`",
            "missing",
            fix=f"{draft_cmd('saturday')}; use `stub` or `done` instead of `draft` if that is the truth",
        )
    ]


@seed("FM-REQUIRED-title", ("stub", "draft"))
def _(v, st):
    v.write("concern/lending-desk.md", f'---\ntype: concern\nstatus: {st}\ndescription: "d"\n---\n')
    return [
        Exp(
            "SCAT-FM-REQUIRED",
            E_,
            "concern/lending-desk.md",
            "field `title`",
            "missing",
            fix='add the line `title: "Lending desk"` (the page name with each - replaced by a space and the first '
            "letter upper case; reword it if you like)",
        )
    ]


@seed("FM-REQUIRED-title-narrative", ("stub", "draft"))
def _(v, st):
    v.edit(NF, 'title: "Saturday at the desk"\n', "")
    return [
        Exp(
            "SCAT-FM-REQUIRED",
            E_,
            NF,
            "field `title`",
            "missing",
            fix='add the line `title: "Saturday"` (the page name with each - replaced by a space and the first '
            "letter upper case; reword it if you like)",
        )
    ]


@seed("FM-TYPE-near", ALL)
def _(v, st):
    put(v, "concern", "odd-page", "Odd page", st, extra="")
    v.edit("concern/odd-page.md", "type: concern", "type: Concern")
    return [
        Exp(
            "SCAT-FM-TYPE",
            E_,
            "concern/odd-page.md",
            "field `type`",
            "`Concern` is not a page type",
            fix="change it to `type: concern`",
        )
    ]


FIVE = (
    "`type: affordance`",
    "`type: concern`",
    "`type: group`",
    "`type: narrative`",
    "`type: technology`",
)


def _in_order(text, needles):
    pos = [text.index(n) for n in needles]
    assert pos == sorted(pos)


@seed("FM-TYPE-list", ALL)
def _(v, st):
    put(v, "concern", "odd-page", "Odd page", st)
    v.edit("concern/odd-page.md", "type: concern", "type: gadget")
    return [
        Exp(
            "SCAT-FM-TYPE",
            E_,
            "concern/odd-page.md",
            "field `type`",
            "`gadget` is not a page type",
            fix_has=("Fix, choose the one that describes this page:",) + FIVE,
            fix_lacks=("change it to",),
        )
    ]


@seed("FM-TYPE-empty", ("draft",))
def _(v, st):
    put(v, "concern", "odd-page", "Odd page", st)
    v.edit("concern/odd-page.md", "type: concern", "type:")
    return [
        Exp(
            "SCAT-FM-TYPE",
            E_,
            "concern/odd-page.md",
            "field `type`",
            "the value is empty, which is not a page type",
            fix_has=FIVE,
        )
    ]


@seed("FM-TYPE-index", ("draft",))
def _(v, st):
    put(v, "concern", "odd-page", "Odd page", st)
    v.edit("concern/odd-page.md", "type: concern", "type: index")
    return [
        Exp(
            "SCAT-FM-TYPE",
            E_,
            "concern/odd-page.md",
            "field `type`",
            "`index` is not a page type",
            fix_has=("scat index",) + FIVE,
        )
    ]


@seed("FM-STATUS-near", ALL)
def _(v, st):
    put(v, "concern", "odd-page", "Odd page", "Done", description=None)
    return [
        Exp(
            "SCAT-FM-STATUS",
            E_,
            "concern/odd-page.md",
            "field `status`",
            "`Done` is not a status",
            fix="change it to `status: done`",
        )
    ]


@seed("FM-STATUS-list", ("draft",))
def _(v, st):
    put(v, "concern", "odd-page", "Odd page", "finished", description=None)
    return (
        [
            Exp(
                "SCAT-FM-STATUS",
                E_,
                "concern/odd-page.md",
                "field `status`",
                "`finished` is not a status",
                fix=("Fix, choose one:", None),
            )
        ]
        if False
        else [
            Exp(
                "SCAT-FM-STATUS",
                E_,
                "concern/odd-page.md",
                "field `status`",
                "`finished` is not a status",
                fix_has=(
                    "`status: stub` (just started)",
                    "`status: draft` (being written)",
                    "`status: done` (finished)",
                ),
            )
        ]
    )


@seed("FM-TIMEFRAME-near", ALL)
def _(v, st):
    v.edit(NF, "timeframe: past", "timeframe: Past")
    return [
        Exp(
            "SCAT-FM-TIMEFRAME",
            E_,
            NF,
            "field `timeframe`",
            "`Past` is not a timeframe",
            fix="change it to `timeframe: past`",
        )
    ]


@seed("FM-TIMEFRAME-list", ALL)
def _(v, st):
    v.edit(NF, "timeframe: past", "timeframe: soon")
    return [
        Exp(
            "SCAT-FM-TIMEFRAME",
            E_,
            NF,
            "field `timeframe`",
            "`soon` is not a timeframe",
            fix_has=(
                "Fix, choose one:",
                "`timeframe: past`",
                "`timeframe: future`",
                "`timeframe: mixed`",
            ),
        )
    ]


@seed("FM-KIND-near", ALL)
def _(v, st):
    v.edit(NF, "timeframe: past", "timeframe: past\nkind: Scenario")
    return [
        Exp(
            "SCAT-FM-KIND",
            E_,
            NF,
            "field `kind`",
            "`Scenario` is not a kind",
            fix=(
                "Fix, choose one:",
                [
                    "change it to `kind: scenario`",
                    (
                        "delete the line `kind: Scenario`: a narrative that is neither a scenario nor an "
                        "architecture leaves `kind` out"
                    ),
                ],
            ),
        )
    ]


@seed("FM-KIND-list", ("draft",))
def _(v, st):
    v.edit(NF, "timeframe: past", "timeframe: past\nkind: story")
    return [
        Exp(
            "SCAT-FM-KIND",
            E_,
            NF,
            "field `kind`",
            "`story` is not a kind",
            fix_has=("`kind: scenario`", "`kind: architecture`", "delete the line `kind: story`"),
        )
    ]


@seed("FM-KIND-empty-and-valid", ALL)
def _(v, st):
    v.edit(NF, "timeframe: past", "timeframe: past\nkind:")
    return []


@seed("FM-SHAPE-list", ("draft",))
def _(v, st):
    put(v, "concern", "odd-page", "Odd page", st)
    v.edit("concern/odd-page.md", 'title: "Odd page"', "title:\n  - Odd one")
    return [
        Exp(
            "SCAT-FM-SHAPE",
            E_,
            "concern/odd-page.md",
            "field `title`",
            "expected one line of text, found a list",
            fix='replace the field with the line `title: "Odd one"`',
        )
    ]


@seed("FM-SHAPE-mapping", ("draft",))
def _(v, st):
    put(v, "concern", "odd-page", "Odd page", st)
    v.edit("concern/odd-page.md", 'title: "Odd page"', "title:\n  a: b")
    return [
        Exp(
            "SCAT-FM-SHAPE",
            E_,
            "concern/odd-page.md",
            "field `title`",
            "expected one line of text, found a mapping",
            fix="replace the field with one line of text you write",
        )
    ]


@seed("FM-SHAPE-bool", ("draft",))
def _(v, st):
    put(v, "concern", "odd-page", "Odd page", st)
    v.edit("concern/odd-page.md", 'title: "Odd page"', "title: yes")
    return [
        Exp(
            "SCAT-FM-SHAPE",
            E_,
            "concern/odd-page.md",
            "field `title`",
            "expected one line of text, found a boolean",
            fix='replace the field with the line `title: "yes"`',
        )
    ]


# ======================================================================================= names
def _name_fix(new, old):
    return f"change the file name to `{new}.md`, then change the links that meant this page from `[[{old}]]` to `[[{new}]]`"


@seed("NAME-space-and-case", ("draft",))
def _(v, st):
    v.write("concern/Safe Tool.md", page_text("concern", "Safe Tool", st))
    return [
        Exp(
            "SCAT-NAME",
            E_,
            "concern/Safe Tool.md",
            "frontmatter",
            re.compile(r"^the page name `Safe Tool` is not legal \(.+\)$"),
            fix=_name_fix("safe-tool", "Safe Tool"),
        )
    ]


@seed("NAME-65-chars", ("draft",))
def _(v, st):
    name = "x" * 65
    v.write(f"concern/{name}.md", page_text("concern", "Long name", st))
    return [
        Exp(
            "SCAT-NAME",
            E_,
            f"concern/{name}.md",
            "frontmatter",
            re.compile(r"is not legal"),
            fix=_name_fix("long-name", name),
        )
    ]


@seed("NAME-reserved", ("draft",))
def _(v, st):
    v.write("concern/con.md", page_text("concern", "Con", st))
    return [
        Exp(
            "SCAT-NAME",
            E_,
            "concern/con.md",
            "frontmatter",
            re.compile(r"is not legal"),
            fix=_name_fix("con-2", "con"),
        )
    ]


@seed("NAME-double-hyphen", ("draft",))
def _(v, st):
    v.write("concern/a--b.md", page_text("concern", "A b", st))
    return [
        Exp(
            "SCAT-NAME",
            E_,
            "concern/a--b.md",
            "frontmatter",
            re.compile(r"is not legal"),
            fix=_name_fix("a-b", "a--b"),
        )
    ]


@seed("NAME-accent-title", ("draft",))
def _(v, st):
    v.write("concern/Cafe menu.md", page_text("concern", "Café menu", st))
    return [
        Exp(
            "SCAT-NAME",
            E_,
            "concern/Cafe menu.md",
            "frontmatter",
            re.compile(r"is not legal"),
            fix=_name_fix("cafe-menu", "Cafe menu"),
        )
    ]


@seed("NAME-non-latin", ("draft",))
def _(v, st):
    v.write("concern/Привет.md", page_text("concern", "Привет", st))
    return [
        Exp(
            "SCAT-NAME",
            E_,
            "concern/Привет.md",
            "frontmatter",
            re.compile(r"is not legal"),
            fix_has=("choose a legal name by hand (page contracts section 2)",),
        )
    ]


@seed("NAME-same-name-two-folders", ("draft",))
def _(v, st):
    v.write("concern/x.md", page_text("concern", "Xray hall", st))
    v.write("technology/x.md", page_text("technology", "Xray tech", st))
    return [
        Exp(
            "SCAT-NAME",
            E_,
            "technology/x.md",
            "frontmatter",
            "the page name `x` is also the name of concern/x.md",
            fix_has=(_name_fix("xray-tech", "x"),),
        )
    ]


@seed("NAME-case-only", ("draft",))
def _(v, st):
    v.write("concern/safety.md", page_text("concern", "Safety", st))
    v.write("technology/Safety.md", page_text("technology", "Safety", st))
    return [
        Exp(
            "SCAT-NAME",
            E_,
            "technology/Safety.md",
            "frontmatter",
            re.compile(r"."),
            fix=_name_fix("safety-2", "Safety"),
        )
    ]


# ======================================================================================= fields required from done
DESC_SLOT = 'add the line `description: "<one sentence you write>"` (author)'


@seed("DONE-FIELD-description-node", ("done",))
def _(v, st):
    v.write("concern/quick-checkout.md", page_text("concern", "Quick checkout", "done", None))
    return [
        Exp(
            "SCAT-DONE-FIELD",
            E_,
            "concern/quick-checkout.md",
            "field `description`",
            "missing on a page with status: done",
            fix=(
                "Fix, choose one:",
                [DESC_SLOT, f"{draft_cmd('quick-checkout')} if the page is not finished"],
            ),
        )
    ]


@seed("DONE-FIELD-description-narrative", ("done",))
def _(v, st):
    v.edit(NF, 'description: "A Saturday at the lending desk."\n', "")
    return [
        Exp(
            "SCAT-DONE-FIELD",
            E_,
            NF,
            "field `description`",
            "missing on a page with status: done",
            fix=(
                "Fix, choose one:",
                [DESC_SLOT, f"{draft_cmd('saturday')} if the page is not finished"],
            ),
        )
    ]


@seed("DONE-FIELD-description-empty", ("done",))
def _(v, st):
    v.edit(NF, 'description: "A Saturday at the lending desk."', "description:")
    return [
        Exp(
            "SCAT-DONE-FIELD",
            E_,
            NF,
            "field `description`",
            "missing on a page with status: done",
            fix_has=(
                "replace the line `description:",
                '`description: "<one sentence you write>"` (author)',
                draft_cmd("saturday"),
            ),
        )
    ]


@seed("DONE-FIELD-timeframe-absent", ("done",))
def _(v, st):
    v.edit(NF, "timeframe: past\n", "")
    return [
        Exp(
            "SCAT-DONE-FIELD",
            E_,
            NF,
            "field `timeframe`",
            "missing on a page with status: done",
            fix_has=(
                "add the line `timeframe: past`",
                "add the line `timeframe: future`",
                "add the line `timeframe: mixed`",
                draft_cmd("saturday"),
            ),
        )
    ]


@seed("DONE-FIELD-timeframe-empty", ("done",))
def _(v, st):
    v.edit(NF, "timeframe: past", "timeframe:")
    return [
        Exp(
            "SCAT-DONE-FIELD",
            E_,
            NF,
            "field `timeframe`",
            "missing on a page with status: done",
            fix_has=(
                "replace the line `timeframe:",
                "`timeframe: past`",
                "`timeframe: future`",
                "`timeframe: mixed`",
            ),
        )
    ]


@seed("DONE-FIELD-silent-before-done", ("stub", "draft"))
def _(v, st):
    v.write("concern/quick-checkout.md", page_text("concern", "Quick checkout", st, None))
    if st == "stub":
        return []
    return [
        Exp(
            "SCAT-DRAFT-FIELD",
            W_,
            "concern/quick-checkout.md",
            "field `description`",
            "missing (required once the page is done)",
            fix=f"{DESC_SLOT} before you set status: done",
        )
    ]


@seed("DRAFT-FIELD-description-narrative", ("draft",))
def _(v, st):
    v.edit(NF, 'description: "A Saturday at the lending desk."\n', "")
    return [
        Exp(
            "SCAT-DRAFT-FIELD",
            W_,
            NF,
            "field `description`",
            "missing (required once the page is done)",
            fix=f"{DESC_SLOT} before you set status: done",
        )
    ]


@seed("DRAFT-FIELD-timeframe", ("stub", "draft"))
def _(v, st):
    v.edit(NF, "timeframe: past\n", "")
    return [
        Exp(
            "SCAT-DRAFT-FIELD",
            W_,
            NF,
            "field `timeframe`",
            "missing (required once the page is done)",
            fix_has=(
                "Fix, choose one before you set status: done:",
                "`timeframe: past` (author)",
                "`timeframe: future` (author)",
                "`timeframe: mixed` (author)",
            ),
        )
    ]


def test_fresh_narrative_stub_gives_exactly_one_draft_field_message(make_base):
    v = make_base("done")
    code, doc = v.scat("stub", "fresh", "--type", "narrative")
    assert code == 0 and doc["ok"]
    problems = v.check()
    assert_messages(
        problems,
        [
            Exp(
                "SCAT-DRAFT-FIELD",
                W_,
                "narrative/fresh.md",
                "field `timeframe`",
                "missing (required once the page is done)",
            ),
            Exp(
                "SCAT-UNCODED",
                W_,
                "narrative/fresh.md",
                "body",
                "the narrative links no node page, so it is excluded from the knowledge graph and every view",
            ),
        ],
    )


# ======================================================================================= dangling body links
def _dang(target, line=9):
    return Exp("SCAT-LINK-DANGLING-BODY", E_, NF, f"link [[{target}]]", line=line)


def _body(v, extra):
    v.edit(NF, "through [[self-checkout]].", f"through [[self-checkout]]. {extra}")


def _plain(target, line=9):
    return (
        f"on line {line} replace `[[{target}]]` with `{target}` to keep the words and drop the link"
    )


@seed("DANGLING-no-near-five-options", ALL)
def _(v, st):
    _body(v, "See [[phantom-tool]].")
    e = _dang("phantom-tool")
    e.what = "does not reach a page (no page is named phantom-tool)"
    e.fix_sorted = True
    e.fix = (
        "Fix, choose one:",
        [
            stub_opt("phantom-tool", k)
            for k in ("group", "concern", "affordance", "technology", "narrative")
        ]
        + [_plain("phantom-tool")],
    )
    return [e]


@seed("DANGLING-near-match", ("draft",))
def _(v, st):
    put(v, "concern", "safety-briefing", "Safety briefing")
    _body(v, "See [[safety-briefings]].")
    e = _dang("safety-briefings")
    e.fix_sorted = True
    e.fix = (
        "Fix, choose one:",
        ["on line 9 replace `[[safety-briefings]]` with `[[safety-briefing]]`"]
        + [
            stub_opt("safety-briefings", k)
            for k in ("group", "concern", "affordance", "technology", "narrative")
        ]
        + [_plain("safety-briefings")],
    )
    return [e]


@seed("DANGLING-named-by-a-row-end-elsewhere", ("draft",), allow=("SCAT-DRAFT-END-NOPAGE",))
def _(v, st):
    v.write(
        "narrative/other-day.md",
        '---\ntype: narrative\nstatus: draft\ntitle: "Other day"\ndescription: "d"\ntimeframe: past\n---\n\n## Edges told\n\n'
        + HEADER
        + "\n"
        + SEP
        + "\n| [[ghost-row]] | holds | [[quick-checkout]] | |\n",
    )
    _body(v, "See [[ghost-row]].")
    e = _dang("ghost-row")
    e.fix = ("Fix, choose one:", [stub_opt("ghost-row", "group"), _plain("ghost-row")])
    return [e, Exp("SCAT-DRAFT-END-NOPAGE", W_, "narrative/other-day.md", "row 1 cell `from`")]


@seed("DANGLING-group-at-cap", ("draft",), allow=("SCAT-DRAFT-END-NOPAGE",))
def _(v, st):
    v.write("scat.toml", "stakeholder_group_cap = 2\n")
    v.write(
        "narrative/other-day.md",
        '---\ntype: narrative\nstatus: draft\ntitle: "Other day"\ndescription: "d"\ntimeframe: past\n---\n\n## Edges told\n\n'
        + HEADER
        + "\n"
        + SEP
        + "\n| [[ghost-row]] | holds | [[quick-checkout]] | |\n",
    )
    _body(v, "See [[ghost-row]].")
    e = _dang("ghost-row")
    e.fix_has = (
        "the vault is at its cap of 2 groups, so a new group page would break SCAT-CAP; choose an existing group",
    )
    e.fix_lacks = ("--type group",)
    return [
        e,
        Exp(
            "SCAT-DRAFT-END-NOPAGE",
            W_,
            "narrative/other-day.md",
            "row 1 cell `from`",
            fix_lacks=("--type group",),
        ),
    ]


@seed("DANGLING-case-variant-c", ("draft",))
def _(v, st):
    put(v, "concern", "safety-briefing", "Safety briefing")
    _body(v, "See [[Safety-Briefing]].")
    e = _dang("Safety-Briefing")
    e.what = re.compile(r"^does not reach a page \(Safety-Briefing is not a legal page name: .+\)$")
    e.fix = (
        "Fix, choose one:",
        [
            "on line 9 replace `[[Safety-Briefing]]` with `[[safety-briefing]]`",
            _plain("Safety-Briefing"),
        ],
    )
    return [e]


@seed("DANGLING-illegal-name-derived", ("draft",))
def _(v, st):
    _body(v, "See [[Safety briefing]].")
    e = _dang("Safety briefing")
    e.what = re.compile(r"is not a legal page name")
    e.fix_has = tuple(
        f"replace `[[Safety briefing]]` with `[[safety-briefing]]`, then run `scat stub safety-briefing --type {k}`"
        for k in ("group", "concern", "affordance", "technology", "narrative")
    ) + (_plain("Safety briefing"),)
    return [e]


@seed("DANGLING-typeless-file-variant-b", ("draft",))
def _(v, st):
    v.write("notes.md", "Just some notes.\n")
    _body(v, "See [[notes]].")
    e = _dang("notes")
    e.what = re.compile(r"notes\.md exists but has no `type`, so it is not a page")
    e.fix_has = (
        "put these lines in a block between two `---` lines at the very top of notes.md",
        "`type: group`",
        "`status: stub`",
        '`title: "Notes"`',
    )
    return [e]


@seed("DANGLING-typeless-file-with-frontmatter", ("draft",))
def _(v, st):
    v.write("notes.md", '---\ntitle: "Mine"\n---\nJust some notes.\n')
    _body(v, "See [[notes]].")
    e = _dang("notes")
    e.fix_has = (
        "add these lines to the frontmatter of notes.md",
        "`type: group`",
        "`status: stub`",
    )
    e.fix_lacks = ("title:",)
    return [e]


@seed("DANGLING-ghost-block-ref", ("draft",))
def _(v, st):
    _body(v, "See [[ghost^abc123]].")
    return [_dang("ghost")]


@seed("DANGLING-note-cell", ("draft",))
def _(v, st):
    set_row(v, 1, "| [[borrowers]] | holds | [[quick-checkout]] | see [[ghost-note]] |")
    return [_dang("ghost-note", row_line(1))]


@seed("DANGLING-not-page-links-are-silent", ALL)
def _(v, st):
    _body(v, "Images [[photo.png]] and [[v1.2-notes]] and [[#Heading]] and `[[ghost-code]]`.")
    v.edit(NF, "\n## Edges told", "\n```\n[[ghost-fence]]\n```\n\n## Edges told")
    return []


@seed("DANGLING-row-end-is-not-this-rule", ALL)
def _(v, st):
    set_row(v, 1, "| [[ghost]] | holds | [[quick-checkout]] | |")
    rule, sev = pair("END-NOPAGE", st)
    return [
        Exp(
            rule,
            sev,
            NF,
            "row 1 cell `from`",
            "[[ghost]] does not reach a page (no page is named ghost)",
        )
    ]


# ======================================================================================= cap
@seed("CAP-four-over-three", ALL)
def _(v, st):
    put(v, "group", "elders", "Elders")
    put(v, "group", "neighbours", "Neighbours")
    return [
        Exp(
            "SCAT-CAP",
            E_,
            "scat.toml",
            "field `stakeholder_group_cap`",
            re.compile(r"^the vault holds 4 group pages, over the cap of 3: .*borrowers.*"),
            fix=(
                "Fix, choose one:",
                [
                    (
                        "cluster 1 group(s) into the others, by shared standpoint: move their standpoints "
                        "into another group's `description`, change every link to them to point at that "
                        "group, and delete those pages"
                    ),
                    (
                        "or, only if the plan allows more groups, write `stakeholder_group_cap = 4` in "
                        "scat.toml (the cap protects against identifying individuals)"
                    ),
                ],
            ),
        )
    ]


@seed("CAP-at-the-cap-is-fine", ("draft",))
def _(v, st):
    put(v, "group", "elders", "Elders")
    return []


@seed("CAP-stub-group-counts", ("draft",))
def _(v, st):
    put(v, "group", "elders", "Elders", "stub", None)
    put(v, "group", "neighbours", "Neighbours", "stub", None)
    return [
        Exp(
            "SCAT-CAP",
            E_,
            "scat.toml",
            "field `stakeholder_group_cap`",
            re.compile(r"over the cap of 3"),
        )
    ]


CFG = "field `stakeholder_group_cap`"
SLOT_FIX = (
    "`stakeholder_group_cap = <number you choose>` (author) in scat.toml; choose a whole number of 1 or more",
)


def _cfg(v, text, what, fixhas=SLOT_FIX):
    if text is None:
        v.path("scat.toml").unlink()
    else:
        v.write("scat.toml", text)
    return [Exp("SCAT-CAP-CONFIG", E_, "scat.toml", CFG, what, fix_has=fixhas)]


@seed("CAP-CONFIG-file-missing", ("draft",))
def _(v, st):
    return _cfg(v, None, "the file is missing")


@seed("CAP-CONFIG-broken-line", ("draft",))
def _(v, st):
    return _cfg(v, "stakeholder_group_cap = = 3\n", re.compile(r"^the file is not valid TOML: .+"))


@seed("CAP-CONFIG-key-missing", ("draft",))
def _(v, st):
    return _cfg(v, "other = 1\n", "the key is missing")


@seed("CAP-CONFIG-string", ("draft",))
def _(v, st):
    return _cfg(
        v,
        'stakeholder_group_cap = "three"\n',
        re.compile(r"^the value `.*three.*` is not a TOML integer of 1 or more$"),
        ("replace the line `stakeholder_group_cap = ",) + SLOT_FIX,
    )


@seed("CAP-CONFIG-zero", ("draft",))
def _(v, st):
    return _cfg(
        v, "stakeholder_group_cap = 0\n", "the value `0` is not a TOML integer of 1 or more"
    )


@seed("CAP-CONFIG-float", ("draft",))
def _(v, st):
    return _cfg(
        v, "stakeholder_group_cap = 2.5\n", "the value `2.5` is not a TOML integer of 1 or more"
    )


@seed("CAP-CONFIG-float-whole", ("draft",))
def _(v, st):
    return _cfg(
        v, "stakeholder_group_cap = 3.0\n", "the value `3.0` is not a TOML integer of 1 or more"
    )


@seed("SUGGEST-CONFIG-string", ("draft",))
def _(v, st):
    v.write("scat.toml", 'stakeholder_group_cap = 3\nlink_suggestions = "yes"\n')
    what = 'the value `"yes"` is not a TOML boolean, `true` or `false`'
    return [
        Exp(
            "SCAT-SUGGEST-CONFIG",
            E_,
            "scat.toml",
            "field `link_suggestions`",
            what,
            fix_has=("`link_suggestions = true`", "`link_suggestions = false`"),
        )
    ]


# ======================================================================================= mention
def _mention(file, line, col, text, key, name, repl=None, type_="concern"):
    return Exp(
        "SCAT-MENTION",
        W_,
        file,
        f"text `{text}`",
        f"names the {type_} page [[{name}]] but does not link it",
        line=line,
        col=col,
        fix=f"on line {line} replace `{text}` with `{repl or f'[[{name}|{text}]]'}`",
    )


@seed("MENTION-plain-title", ALL)
def _(v, st):
    sentence = "Then the safe handling of tools mattered."
    _body(v, sentence)
    line = v.line(NF, 9)
    col = line.index("safe handling") + 1
    return [_mention(NF, 9, col, "safe handling", "", "safe-handling")]


@seed("MENTION-page-name-text", ("draft",))
def _(v, st):
    _body(v, "Then safe-handling mattered.")
    col = v.line(NF, 9).index("safe-handling") + 1
    return [_mention(NF, 9, col, "safe-handling", "", "safe-handling", "[[safe-handling]]")]


@seed("MENTION-plain-and-linked-is-silent", ("draft",))
def _(v, st):
    _body(v, "Safe handling came up, see [[safe-handling]].")
    return []


@seed("MENTION-code-span-is-silent", ("draft",))
def _(v, st):
    _body(v, "Then `safe handling` mattered.")
    return []


@seed("MENTION-note-cell", ALL)
def _(v, st):
    set_row(v, 1, "| [[borrowers]] | holds | [[quick-checkout]] | Raised safe handling here |")
    line = v.line(NF, row_line(1))
    col = line.index("safe handling") + 1
    return [
        _mention(
            NF,
            row_line(1),
            col,
            "safe handling",
            "",
            "safe-handling",
            "[[safe-handling\\|safe handling]]",
        )
    ]


# ======================================================================================= noedges (G1)
NOEDGES_ONE = (
    "record its edges: run `scat set-status saturday draft` "
    '(REPL: `scat_kg.set_status("saturday", "draft")`), then '
    "`scat record-edge <type> <from> <to> --told-by saturday` "
    '(REPL: `scat_kg.record_edge("<type>", "<from>", "<to>", ["saturday"])`) '
    "for each edge the account tells, then `scat set-status saturday done` "
    '(REPL: `scat_kg.set_status("saturday", "done")`)'
)
NOEDGES_TWO = (
    "or leave it as intended: a narrative may tell no edge, and this warning does not block; "
    "nothing to change"
)


def _noedges():
    return [
        Exp(
            "SCAT-NOEDGES",
            W_,
            NF,
            "table",
            "the narrative is `done` and tells no edge: its fingerprint has no edges",
            fix=("Fix, choose one:", [NOEDGES_ONE, NOEDGES_TWO]),
        )
    ]


@seed("NOEDGES-header-and-separator-only", ("done",))
def _(v, st):
    v.edit(NF, ROW1 + "\n", "")
    v.edit(NF, ROW2 + "\n", "")
    return _noedges()


@seed("NOEDGES-no-table", ("done",))
def _(v, st):
    text = v.read(NF)
    v.write(NF, text[: text.index("## Edges told")])
    return _noedges()


@seed("NOEDGES-silent-before-done", ("stub", "draft"))
def _(v, st):
    v.edit(NF, ROW1 + "\n", "")
    v.edit(NF, ROW2 + "\n", "")
    return []


# ======================================================================================= uncoded (WP21-G2)
UNCODED_ONE = (
    "link a node page where the account names one, as `[[<node-name>]]` (or list it under a "
    "heading such as `Linked beyond the text`); a node the account names with no edge needs "
    "only this link"
)
UNCODED_TWO = (
    "or tell an edge: a row of the table whose ends are links to node pages; if the node has "
    "no page, `scat stub <name> --type <type>` makes one"
)


def _uncode(v):
    text = v.read(NF)
    v.write(NF, text[: text.index("\n---\n", 4) + 5] + "\nNothing here names a node.\n")


@seed("UNCODED-no-link", ALL)
def _(v, st):
    _uncode(v)
    return [
        Exp(
            "SCAT-UNCODED",
            W_,
            NF,
            "body",
            "the narrative links no node page, so it is excluded from the knowledge graph and every view",
            fix=("Fix, choose one:", [UNCODED_ONE, UNCODED_TWO]),
        )
    ]


@seed("UNCODED-one-account-link-is-silent", ("stub", "draft"))  # at done: SCAT-NOEDGES only
def _(v, st):
    _uncode(v)
    v.edit(NF, "Nothing here names a node.", "Only the [[self-checkout]] was named.")
    return []


@seed("MENTION-from-cell-is-not-mention", ("draft",))
def _(v, st):
    set_row(v, 1, "| borrowers | holds | [[quick-checkout]] | |")
    return [Exp("SCAT-DRAFT-END-NOLINK", W_, NF, "row 1 cell `from`")]


@seed("MENTION-node-page", ("draft",))
def _(v, st):
    v.write(
        "concern/safe-handling.md",
        page_text("concern", "Safe handling", "done", body="Related to Quick checkout."),
    )
    col = v.line("concern/safe-handling.md", 8).index("Quick checkout") + 1
    return [_mention("concern/safe-handling.md", 8, col, "Quick checkout", "", "quick-checkout")]


@seed("MENTION-own-title-is-silent", ("draft",))
def _(v, st):
    v.write(
        "concern/safe-handling.md",
        page_text("concern", "Safe handling", "done", body="Safe handling is about care."),
    )
    return []


# ======================================================================================= table pairs
def _tbl(name, st, **kw):
    return narr_exp(name, st, **kw)


def _hdr(v, new):
    v.edit(NF, HEADER, new)


@seed("TABLE-HEADER-order-advisory", ALL)
def _(v, st):
    _hdr(v, "| from | to | type | note |")
    return [
        _tbl(
            "TABLE-HEADER",
            st,
            where="table header",
            line=13,
            col=1,
            what="the header row is `| from | to | type | note |`, not `| from | type | to | note |`",
            fix="reorder the columns to `from`, `type`, `to`, `note`: in the header and in every row, move the cells into this order; the tool never moves cells",
        )
    ]


@seed("TABLE-HEADER-wrong-name", ALL)
def _(v, st):
    _hdr(v, "| from | kind | to | note |")
    return [
        _tbl(
            "TABLE-HEADER",
            st,
            where="table header",
            line=13,
            col=1,
            what="the header row is `| from | kind | to | note |`, not `| from | type | to | note |`",
            fix="replace the line `| from | kind | to | note |` with `| from | type | to | note |`",
        )
    ]


@seed("TABLE-HEADER-three-columns", ("draft",))
def _(v, st):
    _hdr(v, "| from | type | to |")
    return [
        _tbl(
            "TABLE-HEADER",
            st,
            where="table header",
            line=13,
            col=1,
            what="the header row is `| from | type | to |`, not `| from | type | to | note |`",
            fix="replace the line `| from | type | to |` with `| from | type | to | note |`",
        )
    ]


@seed("TABLE-HEADER-bad-separator", ALL)
def _(v, st):
    v.edit(NF, "|---|---|---|---|", "| a | b |")
    return [
        _tbl(
            "TABLE-HEADER",
            st,
            where="table header",
            line=13,
            col=1,
            what="the line after the header row is `| a | b |`, not a separator row",
            fix="replace the line `| a | b |` with `|---|---|---|---|`",
        )
    ]


@seed("TABLE-HEADER-separator-missing", ("draft",))
def _(v, st):
    v.edit(NF, "|---|---|---|---|\n", "")
    return [
        _tbl(
            "TABLE-HEADER",
            st,
            where="table header",
            line=13,
            col=1,
            what=f"the line after the header row is `{ROW1_}`, not a separator row",
            fix="replace the line `| from | type | to | note |` with two lines, `| from | type | to | note |` then `|---|---|---|---|`",
        )
    ]


ROW1_ = "| [[borrowers]] | holds | [[quick-checkout]] | Said twice. |"


@seed("TABLE-HEADER-header-alone", ("draft",))
def _(v, st):
    v.edit(
        NF,
        "|---|---|---|---|\n"
        + ROW1_
        + "\n| [[quick-checkout]] | is addressed by | [[self-checkout]] | |\n",
        "",
    )
    return [
        _tbl(
            "TABLE-HEADER",
            st,
            where="table header",
            line=13,
            col=1,
            what="there is no separator row after the header row",
            fix="replace the line `| from | type | to | note |` with two lines, `| from | type | to | note |` then `|---|---|---|---|`",
        )
    ]


def _row(v, text, n=1):
    set_row(v, n, text)


@seed("TABLE-ROW-a-three-cells", ALL)
def _(v, st):
    _row(v, "| [[borrowers]] | holds | [[quick-checkout]] |")
    return [
        _tbl(
            "TABLE-ROW",
            st,
            where="row 1",
            line=15,
            col=1,
            what="the row has 3 cells, not 4 (from, type, to, note)",
            fix="add an empty note: replace the final `|` with `| |`",
        )
    ]


@seed("TABLE-ROW-b-no-closing-bar", ALL)
def _(v, st):
    _row(v, "| [[borrowers]] | holds | [[quick-checkout]] | n")
    return [
        _tbl(
            "TABLE-ROW",
            st,
            where="row 1",
            line=15,
            col=1,
            what="the row does not end with `|`",
            fix="write ` |` after the last cell: replace `n` with `n |`",
        )
    ]


@seed("TABLE-ROW-c-three-cells-no-bar", ("draft",))
def _(v, st):
    _row(v, "| [[borrowers]] | holds | [[quick-checkout]]")
    return [
        _tbl(
            "TABLE-ROW",
            st,
            where="row 1",
            line=15,
            col=1,
            what="the row has 3 cells, not 4 (from, type, to, note)",
            fix="write ` | |` after the last cell, which adds the empty note and the closing bar: replace `[[quick-checkout]]` with `[[quick-checkout]] | |`",
        )
    ]


@seed("TABLE-ROW-d-five-cells", ("draft",))
def _(v, st):
    _row(v, "| [[borrowers]] | holds | [[quick-checkout]] | x | y |")
    return [
        _tbl(
            "TABLE-ROW",
            st,
            where="row 1",
            line=15,
            col=1,
            what="the row has 5 cells, not 4 (from, type, to, note)",
            fix_has=("Fix, choose one:", "`\\|`", "delete the row"),
        )
    ]


@seed("TABLE-ROW-e-two-cells", ("draft",))
def _(v, st):
    _row(v, "| [[borrowers]] | holds |")
    return [
        _tbl(
            "TABLE-ROW",
            st,
            where="row 1",
            line=15,
            col=1,
            what="the row has 2 cells, not 4 (from, type, to, note)",
            fix_has=("Fix, choose one:", "delete the row", "`| from | type | to | note |`"),
        )
    ]


@seed("TABLE-ROW-escaped-bar-in-note-is-fine", ALL)
def _(v, st):
    _row(v, "| [[borrowers]] | holds | [[quick-checkout]] | a \\| b |")
    return []


@seed("TABLE-TYPE-option-1", ALL)
def _(v, st):
    _row(v, "| [[borrowers]] | owns | [[quick-checkout]] | |")
    return [
        _tbl(
            "TABLE-TYPE",
            st,
            where="row 1 cell `type`",
            line=15,
            col=19,
            what="`owns` is not an edge type (holds, is addressed by, is provided by)",
            fix=("Fix, choose one:", ["replace `owns` with `holds`", "delete the row"]),
        )
    ]


@seed("TABLE-TYPE-near-match", ("draft",))
def _(v, st):
    _row(v, "| [[quick-checkout]] | holdz | [[borrowers]] | |")
    return [
        _tbl(
            "TABLE-TYPE",
            st,
            where="row 1 cell `type`",
            line=15,
            col=24,
            what="`holdz` is not an edge type (holds, is addressed by, is provided by)",
            fix=("Fix, choose one:", ["replace `holdz` with `holds`", "delete the row"]),
        )
    ]


@seed("TABLE-TYPE-empty", ("draft",))
def _(v, st):
    _row(v, "| [[borrowers]] |  | [[quick-checkout]] | |")
    return [
        _tbl(
            "TABLE-TYPE",
            st,
            where="row 1 cell `type`",
            line=15,
            what="the value is empty, which is not an edge type (holds, is addressed by, is provided by)",
            fix=("Fix, choose one:", ["replace the empty cell with `holds`", "delete the row"]),
        )
    ]


@seed("TABLE-TYPE-unresolved-ends", ("draft",), allow=("SCAT-DRAFT-END-NOPAGE",))
def _(v, st):
    _row(v, "| [[ghost-a]] | owns | [[ghost-b]] | |")
    return [
        _tbl(
            "TABLE-TYPE",
            st,
            where="row 1 cell `type`",
            line=15,
            what="`owns` is not an edge type (holds, is addressed by, is provided by)",
            fix=(
                "Fix, choose one:",
                [
                    "replace `owns` with `holds`",
                    "replace `owns` with `is addressed by`",
                    "replace `owns` with `is provided by`",
                    "delete the row",
                ],
            ),
        ),
        Exp("SCAT-DRAFT-END-NOPAGE", W_, NF, "row 1 cell `from`"),
        Exp("SCAT-DRAFT-END-NOPAGE", W_, NF, "row 1 cell `to`"),
    ]


@seed("TABLE-TYPE-slug-and-case-are-fine", ALL)
def _(v, st):
    _row(v, "| [[borrowers]] | HOLDS | [[quick-checkout]] | |")
    _row(v, "| [[quick-checkout]] | Addressed-By | [[self-checkout]] | |", 2)
    return []


def _lay(frm, to, key_from, key_to, act_from, act_to):
    return f"`holds` joins a {key_from} to a {key_to}, but "


@seed("TABLE-LAYERS-swap", ALL)
def _(v, st):
    _row(v, "| [[quick-checkout]] | holds | [[borrowers]] | |")
    return [
        _tbl(
            "TABLE-LAYERS",
            st,
            where="row 1",
            line=15,
            col=1,
            what="`holds` joins a group to a concern, but [[quick-checkout]] is a concern page, and [[borrowers]] is a group page",
            fix=(
                "Fix, choose one:",
                [
                    "swap the two ends: replace `[[quick-checkout]] | holds | [[borrowers]]` with `[[borrowers]] | holds | [[quick-checkout]]`",
                    "delete the row",
                ],
            ),
        )
    ]


@seed("TABLE-LAYERS-retype", ("draft",))
def _(v, st):
    _row(v, "| [[quick-checkout]] | holds | [[self-checkout]] | |")
    return [
        _tbl(
            "TABLE-LAYERS",
            st,
            where="row 1",
            line=15,
            col=1,
            what=re.compile(
                r"^`holds` joins a group to a concern, but \[\[quick-checkout\]\] is a concern page, and \[\[self-checkout\]\] is an? affordance page$"
            ),
            fix=("Fix, choose one:", ["replace `holds` with `is addressed by`", "delete the row"]),
        )
    ]


@seed("TABLE-LAYERS-two-rows-through-a-node", ("draft",))
def _(v, st):
    _row(v, "| [[borrowers]] | holds | [[self-checkout]] | |")
    return [
        _tbl(
            "TABLE-LAYERS",
            st,
            where="row 1",
            line=15,
            col=1,
            what=re.compile(
                r"^`holds` joins a group to a concern, but \[\[self-checkout\]\] is an? affordance page$"
            ),
            fix_has=(
                "none of the three edge types joins a group to an affordance: tell it as two rows through a node between them",
                "delete the row",
            ),
        )
    ]


@seed("TABLE-LAYERS-one-end-unresolved", ("draft",), allow=("SCAT-DRAFT-END-NOPAGE",))
def _(v, st):
    _row(v, "| [[ghost-g]] | holds | [[borrowers]] | |")
    return [
        _tbl(
            "TABLE-LAYERS",
            st,
            where="row 1",
            line=15,
            what="`holds` joins a group to a concern, but [[borrowers]] is a group page",
        ),
        Exp("SCAT-DRAFT-END-NOPAGE", W_, NF, "row 1 cell `from`"),
    ]


SECOND_HEAD = "## Edges told"


@seed("TABLE-SECOND-heading", ALL)
def _(v, st):
    v.write(
        NF,
        v.read(NF)
        + "\n## Edges told\n\n"
        + HEADER
        + "\n"
        + SEP
        + "\n| [[volunteers]] | holds | [[safe-handling]] | |\n",
    )
    len(v.read(NF).split("\n")) - 6  # heading line
    line = v.read(NF).split("\n").index("## Edges told", 12) + 1
    return [
        _tbl(
            "TABLE-SECOND",
            st,
            where="table",
            line=line,
            what="a second heading `Edges told` on this narrative; only the first table under the first `Edges told` is read, so its rows tell no edge",
            fix_has=(
                "Fix, choose one:",
                "move the rows you want into the first table (line 13)",
                "replace the heading `## Edges told` with",
            ),
        )
    ]


@seed("TABLE-SECOND-table", ("draft",))
def _(v, st):
    v.write(
        NF,
        v.read(NF)
        + "\nMore.\n\n"
        + HEADER
        + "\n"
        + SEP
        + "\n| [[volunteers]] | holds | [[safe-handling]] | |\n",
    )
    line = v.read(NF).split("\n").index(HEADER, 14) + 1
    return [
        _tbl(
            "TABLE-SECOND",
            st,
            where="table",
            line=line,
            what="a second table on this narrative; only the first table under the first `Edges told` is read, so its rows tell no edge",
            fix_has=("move the rows you want into the first table (line 13)",),
        )
    ]


@seed("TABLE-SECOND-unreported-cases", ("draft",))
def _(v, st):
    v.write(
        NF,
        v.read(NF)
        + "\n## Edges tolds\n\n"
        + HEADER
        + "\n"
        + SEP
        + "\n| [[volunteers]] | holds | [[safe-handling]] | |\n",
    )
    v.write(
        "concern/safe-handling.md",
        page_text(
            "concern",
            "Safe handling",
            "done",
            body="## Edges told\n\n"
            + HEADER
            + "\n"
            + SEP
            + "\n| [[volunteers]] | holds | [[safe-handling]] | |",
        ),
    )
    return []


@seed("TABLE-DUPLICATE-identical", ALL)
def _(v, st):
    v.edit(NF, ROW1 + "\n", ROW1 + "\n| [[borrowers]] | holds | [[quick-checkout]] | |\n")
    return [
        _tbl(
            "TABLE-DUPLICATE",
            st,
            where="row 2",
            line=16,
            col=1,
            what="tells the same edge as row 1 (`holds`, [[borrowers]], [[quick-checkout]]); a narrative tells an edge once",
            fix="delete the row `| [[borrowers]] | holds | [[quick-checkout]] | |`",
        )
    ]


@seed("TABLE-DUPLICATE-note-sentence", ("draft",))
def _(v, st):
    v.edit(NF, ROW1 + "\n", ROW1 + "\n" + ROW1.replace("Said twice.", "Again.") + "\n")
    return [
        _tbl(
            "TABLE-DUPLICATE",
            st,
            where="row 2",
            line=16,
            fix_has=(
                "delete the row `| [[borrowers]] | holds | [[quick-checkout]] | Again. |`",
                "if its note `Again.` is worth keeping, put it in the note of row 1 first",
            ),
        )
    ]


@seed("TABLE-DUPLICATE-verb-and-slug", ("draft",))
def _(v, st):
    v.edit(
        NF, ROW2 + "\n", ROW2 + "\n| [[quick-checkout]] | addressed-by | [[self-checkout]] | |\n"
    )
    return [
        _tbl(
            "TABLE-DUPLICATE",
            st,
            where="row 3",
            line=17,
            what="tells the same edge as row 2 (`is addressed by`, [[quick-checkout]], [[self-checkout]]); a narrative tells an edge once",
        )
    ]


@seed("TABLE-DUPLICATE-third-copy", ("draft",))
def _(v, st):
    d = "| [[borrowers]] | holds | [[quick-checkout]] | |"
    v.edit(NF, ROW1 + "\n", ROW1 + "\n" + d + "\n" + d + "\n")
    return [
        _tbl("TABLE-DUPLICATE", st, where="row 2", line=16),
        _tbl("TABLE-DUPLICATE", st, where="row 3", line=17),
    ]


@seed("TABLE-DUPLICATE-two-narratives-is-silent", ("draft",))
def _(v, st):
    v.write("narrative/second.md", narrative_copy())
    return []


def narrative_copy():
    from indep_kit import narrative_text

    return narrative_text("draft").replace("Saturday at the desk", "Second telling")


# ======================================================================================= end rules
def _end(name, st, cell, row=1, **kw):
    return narr_exp(name, st, where=f"row {row} cell `{cell}`", line=row_line(row), **kw)


@seed("END-NOLINK-b-existing-name", ALL)
def _(v, st):
    _row(v, "| borrowers | holds | [[quick-checkout]] | |")
    return [
        _end(
            "END-NOLINK",
            st,
            "from",
            col=3,
            what="`borrowers` is not a link; each end of a row is one link, `[[page-name]]`",
            fix=(
                "Fix, choose one:",
                ["replace `borrowers` with `[[borrowers]]`", "delete the row"],
            ),
        )
    ]


@seed("END-NOLINK-b-new-name", ("draft",))
def _(v, st):
    _row(v, "| New group | holds | [[quick-checkout]] | |")
    return [
        _end(
            "END-NOLINK",
            st,
            "from",
            col=3,
            what="`New group` is not a link; each end of a row is one link, `[[page-name]]`",
            fix_has=(
                "replace `New group` with `[[borrowers]]`",
                "replace `New group` with `[[new-group]]`, then run `scat stub new-group --type group`",
                "delete the row",
            ),
        )
    ]


@seed("END-NOLINK-b-to-cell-derived-name", ("draft",))
def _(v, st):
    _row(v, "| [[borrowers]] | holds | quick checkout | |")
    return [
        _end(
            "END-NOLINK",
            st,
            "to",
            what="`quick checkout` is not a link; each end of a row is one link, `[[page-name]]`",
            fix_has=("replace `quick checkout` with `[[quick-checkout]]`", "delete the row"),
        )
    ]


@seed("END-NOLINK-a-empty", ALL)
def _(v, st):
    _row(v, "|  | holds | [[quick-checkout]] | |")
    return [
        _end(
            "END-NOLINK",
            st,
            "from",
            what="the cell is empty; each end of a row is one link, `[[page-name]]`",
            fix=(
                "Fix, choose one:",
                ["replace the empty cell with `[[<node you choose>]]` (author)", "delete the row"],
            ),
        )
    ]


@seed("END-NOLINK-c-two-links", ("draft",))
def _(v, st):
    _row(v, "| [[borrowers]] and [[volunteers]] | holds | [[quick-checkout]] | |")
    return [
        _end(
            "END-NOLINK",
            st,
            "from",
            col=3,
            what="`[[borrowers]] and [[volunteers]]` is not a link; each end of a row is one link, `[[page-name]]`",
            fix=(
                "Fix, choose one:",
                [
                    f"replace the cell with `[[borrowers]]`; {NOTE_FIX}",
                    f"replace the cell with `[[volunteers]]`; {NOTE_FIX}",
                    "delete the row",
                ],
            ),
        )
    ]


@seed("END-NOLINK-to-cell-empty", ("draft",))
def _(v, st):
    _row(v, "| [[borrowers]] | holds | | |")
    return [
        _end(
            "END-NOLINK",
            st,
            "to",
            what="the cell is empty; each end of a row is one link, `[[page-name]]`",
        )
    ]


@seed("END-NOLINK-alias-and-embed-are-links", ALL)
def _(v, st):
    _row(v, "| [[borrowers|the borrowers]] | holds | ![[quick-checkout]] | |")
    return []


@seed("END-NOPAGE-no-near", ALL)
def _(v, st):
    _row(v, "| [[ghost]] | holds | [[quick-checkout]] | |")
    return [
        _end(
            "END-NOPAGE",
            st,
            "from",
            col=3,
            what="[[ghost]] does not reach a page (no page is named ghost)",
            fix=("Fix, choose one:", [stub_opt("ghost", "group"), "delete the row"]),
        )
    ]


@seed("END-NOPAGE-near-match", ("draft",))
def _(v, st):
    _row(v, "| [[borrower]] | holds | [[quick-checkout]] | |")
    return [
        _end(
            "END-NOPAGE",
            st,
            "from",
            what="[[borrower]] does not reach a page (no page is named borrower)",
            fix=(
                "Fix, choose one:",
                [
                    "replace `[[borrower]]` with `[[borrowers]]`",
                    stub_opt("borrower", "group"),
                    "delete the row",
                ],
            ),
        )
    ]


@seed("END-NOPAGE-illegal-variant-c", ("draft",))
def _(v, st):
    _row(v, "| [[Safety briefing]] | holds | [[quick-checkout]] | |")
    return [
        _end(
            "END-NOPAGE",
            st,
            "from",
            what=re.compile(
                r"^\[\[Safety briefing\]\] does not reach a page \(.*not a legal page name"
            ),
            fix_has=(
                "replace `[[Safety briefing]]` with `[[safety-briefing]]`, then run `scat stub safety-briefing --type group`",
                "delete the row",
            ),
        )
    ]


@seed("END-NOPAGE-typeless-file-variant-b", ("draft",))
def _(v, st):
    v.write("notes.md", "Just notes.\n")
    _row(v, "| [[notes]] | holds | [[quick-checkout]] | |")
    return [
        _end(
            "END-NOPAGE",
            st,
            "from",
            what=re.compile(r"notes\.md exists but has no `type`, so it is not a page"),
            fix_has=(
                "put these lines in a block between two `---` lines at the very top of notes.md",
                "`type: group`",
                "delete the row",
            ),
        )
    ]


@seed("END-NOPAGE-group-at-cap", ("draft",))
def _(v, st):
    v.write("scat.toml", "stakeholder_group_cap = 2\n")
    _row(v, "| [[ghost]] | holds | [[quick-checkout]] | |")
    return [
        _end(
            "END-NOPAGE",
            st,
            "from",
            fix_has=("the vault is at its cap of 2 groups",),
            fix_lacks=("--type group",),
        )
    ]


@seed("END-NOTNODE-narrative-with-candidate", ALL)
def _(v, st):
    v.write("narrative/other.md", narrative_copy().replace("Second telling", "Other"))
    _row(v, "| [[other]] | holds | [[quick-checkout]] | |")
    return [
        _end(
            "END-NOTNODE",
            st,
            "from",
            col=3,
            what="[[other]] is a narrative page, not a node; a row joins two nodes",
            fix=(
                "Fix, choose one:",
                ["replace `[[other]]` with `[[borrowers]]`", "delete the row"],
            ),
        )
    ]


@seed("END-NOTNODE-no-candidate", ("draft",))
def _(v, st):
    v.write("narrative/other.md", narrative_copy().replace("Second telling", "Other"))
    v.edit(NF, "[[borrowers]] queued", "people queued")
    _row(v, "| [[other]] | holds | [[quick-checkout]] | |")
    return [
        _end(
            "END-NOTNODE",
            st,
            "from",
            what="[[other]] is a narrative page, not a node; a row joins two nodes",
            fix=(
                "Fix, choose one:",
                ["replace `[[other]]` with `[[<node you choose>]]` (author)", "delete the row"],
            ),
        )
    ]


@seed("END-NOTNODE-invalid-type-page", ("draft",), allow=("SCAT-FM-TYPE",))
def _(v, st):
    put(v, "concern", "odd-page", "Odd page", "draft")
    v.edit("concern/odd-page.md", "type: concern", "type: gadget")
    _row(v, "| [[odd-page]] | holds | [[quick-checkout]] | |")
    return [
        _end(
            "END-NOTNODE",
            st,
            "from",
            what="[[odd-page]] is a page with the invalid type `gadget`, not a node; a row joins two nodes",
        ),
        Exp("SCAT-FM-TYPE", E_, "concern/odd-page.md", "field `type`"),
    ]


@seed("END-NOTNODE-empty-type-page", ("draft",), allow=("SCAT-FM-TYPE",))
def _(v, st):
    put(v, "concern", "odd-page", "Odd page", "draft")
    v.edit("concern/odd-page.md", "type: concern", "type:")
    _row(v, "| [[odd-page]] | holds | [[quick-checkout]] | |")
    return [
        _end(
            "END-NOTNODE",
            st,
            "from",
            what="[[odd-page]] is a page with an empty `type`, not a node; a row joins two nodes",
        ),
        Exp("SCAT-FM-TYPE", E_, "concern/odd-page.md", "field `type`"),
    ]


# ======================================================================================= rule 4 has no rule
@seed("RULE4-candidate-has-no-message", ALL)
def _(v, st):
    v.edit(NF, ROW1 + "\n", "")
    v.edit(NF, ROW2, "| [[quick-checkout]] | is addressed by | [[self-checkout]] | |")
    # the body links borrowers and quick-checkout; no row joins them
    return []


@seed("RULE4-row-alone-is-conformant", ALL)
def _(v, st):
    v.edit(
        NF,
        "The desk was busy: [[borrowers]] queued, wanting [[quick-checkout]] through [[self-checkout]].",
        "Nothing is linked in the account.",
    )
    return []


# ======================================================================================= the driver
@pytest.mark.parametrize("fn,st,allow", SEEDS)
def test_seeded_defect(make_base, fn, st, allow):
    v = make_base(st)
    expected = fn(v, st)
    problems = v.check()
    assert_messages(problems, expected, allow)
    # the same page gives the same messages at page scope and one link away (catalogue, scopes)
    for file in sorted({e.file for e in expected if e.file.endswith(".md")}):
        vault_level = [p.text for p in problems if p.file == file]
        assert [p.text for p in v.check(file) if p.file == file] == vault_level
        assert [p.text for p in v.check(file, neighborhood=True) if p.file == file] == vault_level


def test_stub_options_follow_the_catalogue_order(make_base):
    """Catalogue, inferred types (b): the five types `group`, `concern`, `affordance`, `technology`, `narrative`, in
    that order, each a separate numbered exact command."""
    v = make_base("draft")
    _body(v, "See [[phantom-tool]].")
    (p,) = v.check()
    opts = [o["text"] for o in p.fix["options"]]
    keys = [re.search(r"--type (\w+)", t).group(1) for t in opts if "scat stub" in t]
    assert keys == ["group", "concern", "affordance", "technology", "narrative"]


def test_stub_option_text_says_to_create_a_page_of_the_key(make_base):
    v = make_base("draft")
    _body(v, "See [[phantom-tool]].")
    (p,) = v.check()
    for o in p.fix["options"][:-1]:
        assert o["kind"] == "exact" and o["command"]["argv"][0] == "stub"


def test_every_rule_of_the_catalogue_has_a_seed_that_expects_it(make_base):
    """Section 3's table lists the ids; each must be expected by at least one seed (the refusal rule has its own
    file: it is an operation, never printed by `scat check`)."""
    from pathlib import Path

    text = (Path(__file__).resolve().parents[2] / "contracts" / "rule-catalogue.md").read_text()
    table = text.split("## 3. Rules", 1)[1].split("The Fix kind column", 1)[0]
    ids = set(re.findall(r"^\| (SCAT-[A-Z0-9-]+) \|", table, re.MULTILINE))
    assert len(ids) >= 30, ids
    expected = set()
    for param in SEEDS:
        fn, st, _ = param.values
        v = make_base(st)
        expected |= {e.rule for e in fn(v, st)}
    assert ids - expected == set()
