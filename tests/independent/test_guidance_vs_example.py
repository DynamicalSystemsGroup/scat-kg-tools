"""D-085 (c): the prior-art readout's guidance-versus-example gap, as a test case in the new model.

The readout (Q3) found that assurances-audits-accountability's guidance asks for links and file names equal to ids,
and that its own example does neither. In this model the id of a page is its name, the file name without `.md`
(page contracts 2); the guidance is "file name equals id equals link target"; and a link resolves only on the exact
name (page contracts 2, 3).

What the tool can say, and what it cannot:
- It has no rule that reads a guidance statement and an example and compares them: R-1 keeps content out of
  conformance, and the readout's own advice is that no rule infer anything from a name. So the case is not
  expressible as a rule. The gap is flagged, and the tests below do not pretend otherwise (see the last test: an
  example inside a code fence, which is where a document's examples live, is never read).
- It can say the nearest thing: where a vault's own pages are the example, a file name that is not the legal id
  (SCAT-NAME) and a link that is not the exact id (SCAT-LINK-DANGLING-BODY, SCAT-*-END-NOPAGE), each with the fix
  that makes the example follow the guidance. Those are tested here, and the contract's own examples are run through
  the tool, which is the check that the written guidance and its examples agree.
"""

import re
from pathlib import Path

from indep_kit import (
    NARRATIVE_FILE as NF,
)
from indep_kit import (
    Vault,
    check_fix_clears,
    page_text,
)

CONTRACTS = Path(__file__).resolve().parents[2] / "contracts" / "page-contracts.md"


def test_example_names_that_are_not_ids_are_named_with_a_fix_to_the_id(make_base, tmp_factory):
    """The example's file names do not equal ids: every one is a SCAT-NAME with the rename to the id."""
    v = make_base("draft")
    for title in ("Safety Briefing", "Tool Library Hours"):
        v.write(f"concern/{title}.md", page_text("concern", title, "draft"))
    problems = v.check()
    names = {p.file: p for p in problems}
    assert set(names) == {"concern/Safety Briefing.md", "concern/Tool Library Hours.md"}
    assert all(p.rule == "SCAT-NAME" and p.severity == "error" for p in problems)
    assert (
        "change the file name to `safety-briefing.md`"
        in names["concern/Safety Briefing.md"].fix_text
    )
    assert (
        "change the file name to `tool-library-hours.md`"
        in names["concern/Tool Library Hours.md"].fix_text
    )
    for p in problems:
        assert check_fix_clears(v, tmp_factory, p, problems, no_other=True) == []


def test_example_links_that_are_not_ids_are_named_with_a_fix_to_the_id(make_base, tmp_factory):
    """The example's links do not equal ids (a title, a different case): each is an error naming the exact id."""
    v = make_base("draft")
    v.write("concern/safety-briefing.md", page_text("concern", "Safety Briefing", "draft"))
    v.edit(
        NF,
        "through [[self-checkout]].",
        "through [[self-checkout]]. See [[Safety Briefing]] and [[Safety-Briefing]].",
    )
    problems = v.check()
    assert [p.rule for p in problems] == ["SCAT-LINK-DANGLING-BODY"] * 2
    assert {p.where for p in problems} == {"link [[Safety Briefing]]", "link [[Safety-Briefing]]"}
    for p in problems:
        target = re.search(r"\[\[(.+)\]\]", p.where).group(1)
        assert f"replace `[[{target}]]` with `[[safety-briefing]]`" in p.fix_text
        opt = p.fix["options"][0]
        assert opt["edits"][0]["replace"] == "[[safety-briefing]]"
        # (the keep-the-words option rightly leaves a plain mention behind, so only clearing is judged)
        assert check_fix_clears(v, tmp_factory, p, problems, no_other=False) == []


def test_example_row_ends_that_are_not_ids_are_mismatches_with_a_fix_to_the_id(make_base):
    v = make_base("done")
    v.write("group/tool-borrowers.md", page_text("group", "Tool borrowers"))
    v.edit(NF, "| [[borrowers]] | holds", "| [[Tool Borrowers]] | holds")
    (p,) = v.check()
    assert (p.rule, p.severity, p.where) == ("SCAT-DONE-END-NOPAGE", "error", "row 1 cell `from`")
    assert "[[tool-borrowers]]" in p.fix_text


def test_example_that_does_neither_gets_both_kinds_of_message(make_base):
    """The readout's own case in one vault: names are not ids and links are not ids."""
    v = make_base("done")
    v.write("concern/Safe Tool Use.md", page_text("concern", "Safe Tool Use"))
    v.edit(
        NF,
        "| [[borrowers]] | holds | [[quick-checkout]]",
        "| [[borrowers]] | holds | [[Safe tool use]]",
    )
    rules = sorted(p.rule for p in v.check())
    assert rules == ["SCAT-DONE-END-NOPAGE", "SCAT-NAME"]


def test_the_guidance_itself_is_not_something_the_tool_can_contradict(make_base):
    """The gap, stated as a test. A page that states the guidance and shows a contradicting example inside a code
    fence gets no message: code is never a link, so the contradiction is outside what the tool reads."""
    v = make_base("done")
    guidance = (
        "Links are written with the exact page name, `[[page-name]]`.\n\n"
        "```\nExample: see [[Safe Tool Use]] and [[Quick Checkout]].\n```\n"
    )
    v.write(
        "concern/safe-handling.md", page_text("concern", "Safe handling", "done", body=guidance)
    )
    assert v.check() == []


# --------------------------------------------------------------------------------------------------- the contracts
def _blocks():
    text = CONTRACTS.read_text()
    return re.findall(r"```[a-z]*\n(.*?)```", text, re.DOTALL)


def test_the_contracts_example_table_is_conformant_under_the_contracts_own_rules(tmp_path):
    """Guidance (page contracts 4: how a narrative's table is written) against its example: build the narrative the
    section shows and let the tool stub the ends the rows entail; no error may remain."""
    tables = [
        b
        for b in _blocks()
        if b.lstrip().startswith("## Edges told") and "| from | type | to | note |" in b
    ]
    assert tables, "page contracts section 4 no longer shows an example table"
    v = Vault(tmp_path / "v")
    v.write("scat.toml", "attribution = 'disallowed'\nstakeholder_group_cap = 3\n")
    v.write(
        "narrative/example.md",
        '---\ntype: narrative\nstatus: draft\ntitle: "Example"\ndescription: "d"\ntimeframe: past\n---\n\n'
        + tables[0],
    )
    code, doc = v.scat("stub-links")
    assert code == 0 and doc["ok"], doc
    problems = v.check()
    assert [p for p in problems if p.severity == "error"] == [], [p.text for p in problems]


def test_the_contracts_example_stub_is_what_stub_links_writes(tmp_path):
    """Page contracts 6 shows the row `| [[safety-briefing]] | is provided by | [[booking-app]] | |` and says which
    files it creates, with title "Safety briefing"; the example block of the stub is the page the tool writes."""
    text = CONTRACTS.read_text()
    assert "[[safety-briefing]] | is provided by | [[booking-app]]" in text
    v = Vault(tmp_path / "v")
    v.write("scat.toml", "attribution = 'disallowed'\nstakeholder_group_cap = 3\n")
    v.write(
        "narrative/example.md",
        '---\ntype: narrative\nstatus: draft\ntitle: "Example"\ndescription: "d"\ntimeframe: past\n---\n\n'
        "## Edges told\n\n| from | type | to | note |\n|---|---|---|---|\n"
        "| [[safety-briefing]] | is provided by | [[booking-app]] | |\n",
    )
    code, doc = v.scat("stub-links")
    assert code == 0 and sorted(doc["created"]) == [
        "affordance/safety-briefing.md",
        "technology/booking-app.md",
    ]
    shown = [b for b in _blocks() if b.startswith("---\ntype: <the node type's slug>")]
    assert shown, "page contracts 6 no longer shows the stub block"
    assert v.read("affordance/safety-briefing.md").replace("\r\n", "\n") == (
        '---\ntype: affordance\nstatus: stub\ntitle: "Safety briefing"\n---\n'
    )
    shown_keys = [ln.split(":")[0] for ln in shown[0].strip().splitlines()]
    written_keys = [
        ln.split(":")[0] for ln in v.read("affordance/safety-briefing.md").strip().splitlines()
    ]
    assert shown_keys == written_keys == ["---", "type", "status", "title", "---"]
    assert shown[0].strip().splitlines()[2] == "status: stub"


def _page_examples():
    out = []
    for b in _blocks():
        m = re.match(r"---\ntype: (group|concern|affordance|technology)\n", b)
        if m:
            out.append((m.group(1), b))
    return out


def test_the_contracts_example_pages_are_conformant_at_their_stated_status(tmp_path):
    """Each field-table example page of page contracts 8 (and the shape example of 1) is a page the tool accepts."""
    examples = _page_examples()
    assert len(examples) >= 4, "page contracts 8 no longer shows the node-page examples"
    v = Vault(tmp_path / "v")
    v.write("scat.toml", "attribution = 'disallowed'\nstakeholder_group_cap = 3\n")
    for i, (type_, block) in enumerate(examples):
        v.write(f"{type_}/example-{type_}-{i}.md", block.split("\n\nFree text")[0].rstrip() + "\n")
    problems = v.check()
    assert [p for p in problems if p.severity == "error"] == [], [p.text for p in problems]
