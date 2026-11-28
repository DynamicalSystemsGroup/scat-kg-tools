"""WP16-R2: a vault coded breadth first (all nodes, then narratives one at a time) and one coded depth first (a
narrative first, its ends stubbed by `record-edge` and `stub-links`, then the nodes). After every step no mismatch is
unseen: every row end that is not a node or not a link has a message of the right end rule and severity, and no end
message is given for an end that is a link to a node. The oracle (`indep_kit.oracle_ends`) reads the table by the page
contracts and never calls the tool."""

import pytest
from indep_kit import Vault, oracle_ends, page_text, unseen_mismatches

HEAD = "\n## Edges told\n\n| from | type | to | note |\n|---|---|---|---|\n"


def sh(v, *args):
    code, doc = v.scat(*args)
    return code, doc


def stub(v, type_, name):
    code, doc = sh(v, "stub", name, "--type", type_)
    assert code == 0 and doc["ok"], doc


def fill_node(v, type_, name, title):
    v.write(f"{type_}/{name}.md", page_text(type_, title, "done", f"About {title}."))


def append_row(v, narrative, row):
    path = f"narrative/{narrative}.md"
    text = v.read(path)
    if "| from | type | to | note |" not in text:
        text = text.rstrip("\n") + "\n" + HEAD
    v.write(path, text.rstrip("\n") + "\n" + row + "\n")


def drop_row(v, narrative, row):
    path = f"narrative/{narrative}.md"
    v.write(path, v.read(path).replace(row + "\n", ""))


def account(v, narrative, body, status="draft"):
    """Give a stubbed narrative its account, description and timeframe, keeping any table."""
    path = f"narrative/{narrative}.md"
    text = v.read(path)
    text = text.replace(
        "timeframe:\n",
        f'description: "The {narrative} account."\ntimeframe: past\n',
    )
    text = text.replace("status: stub", f"status: {status}")
    head, sep, rest = text.partition("\n---\n")
    _head2, _, tail = rest.partition("\n## Edges told")
    new = head + sep + "\n" + body + "\n" + (("\n## Edges told" + tail) if _ else "")
    v.write(path, new)


def name_ends(v, narrative, *names):
    """Name in the account the nodes the rows join, as `done` wants (SCAT-DONE-END-NOTINACCOUNT)."""
    path = f"narrative/{narrative}.md"
    text = v.read(path)
    said = " ".join(f"[[{n}]]" for n in names)
    v.write(path, text.replace("\n## Edges told", f"\nThe rows join {said}.\n\n## Edges told", 1))


N1_ENDS = ("borrowers", "quick-checkout", "self-checkout", "booking-app", "elders", "safe-handling")
N2_ENDS = ("borrowers", "quick-checkout", "volunteers", "safe-handling")


def set_done(v, name):
    code, doc = sh(v, "set-status", name, "done")
    assert code == 0 and doc["ok"], doc


NODE_TITLES = {
    "group": {"borrowers": "Borrowers", "volunteers": "Volunteers", "elders": "Elders"},
    "concern": {"quick-checkout": "Quick checkout", "safe-handling": "Safe handling"},
    "affordance": {"self-checkout": "Self checkout"},
    "technology": {"booking-app": "Booking app"},
}


def fill_all_nodes(v):
    for type_, items in NODE_TITLES.items():
        for name, title in items.items():
            if v.exists(f"{type_}/{name}.md"):
                fill_node(v, type_, name, title)


def breadth_steps():
    steps = []

    def stubs(v):
        for type_, items in NODE_TITLES.items():
            for name in items:
                if name != "elders":
                    stub(v, type_, name)

    steps.append(("stub every node", stubs))
    steps.append(("fill the nodes", fill_all_nodes))
    steps.append(("stub narrative n1", lambda v: stub(v, "narrative", "n1")))
    steps.append(
        (
            "write n1's account",
            lambda v: account(
                v, "n1", "Linked: [[borrowers]], [[quick-checkout]], [[self-checkout]]."
            ),
        )
    )
    steps.append(
        (
            "row with a plain-text end",
            lambda v: append_row(v, "n1", "| borrowers | holds | [[quick-checkout]] | |"),
        )
    )
    steps.append(
        (
            "make the end a link",
            lambda v: v.edit(
                "narrative/n1.md", "| borrowers | holds |", "| [[borrowers]] | holds |"
            ),
        )
    )
    steps.append(
        (
            "second row by hand",
            lambda v: append_row(
                v, "n1", "| [[quick-checkout]] | is addressed by | [[self-checkout]] | |"
            ),
        )
    )
    steps.append(
        (
            "third row by record-edge",
            lambda v: sh(
                v, "record-edge", "provided-by", "self-checkout", "booking-app", "--told-by", "n1"
            ),
        )
    )
    steps.append(
        (
            "row linking a page that does not exist",
            lambda v: append_row(v, "n1", "| [[elders]] | holds | [[safe-handling]] | |"),
        )
    )
    steps.append(("stub-links makes the page", lambda v: sh(v, "stub-links")))
    steps.append(
        (
            "a row ending at a narrative",
            lambda v: append_row(v, "n1", "| [[n1]] | holds | [[safe-handling]] | |"),
        )
    )
    steps.append(
        ("remove that row", lambda v: drop_row(v, "n1", "| [[n1]] | holds | [[safe-handling]] | |"))
    )
    steps.append(("empty end", lambda v: append_row(v, "n1", "|  | holds | [[safe-handling]] | |")))
    steps.append(
        (
            "remove the empty-end row",
            lambda v: drop_row(v, "n1", "|  | holds | [[safe-handling]] | |"),
        )
    )
    steps.append(("fill elders", fill_all_nodes))
    steps.append(("n1's account names the ends", lambda v: name_ends(v, "n1", *N1_ENDS)))
    steps.append(("n1 done", lambda v: set_done(v, "n1")))
    steps.append(("stub narrative n2", lambda v: stub(v, "narrative", "n2")))
    steps.append(
        ("write n2's account", lambda v: account(v, "n2", "Linked: [[borrowers]], [[volunteers]]."))
    )
    steps.append(
        (
            "n2 row by record-edge",
            lambda v: sh(
                v, "record-edge", "holds", "borrowers", "quick-checkout", "--told-by", "n2"
            ),
        )
    )
    steps.append(
        (
            "n2 second row by record-edge",
            lambda v: sh(
                v, "record-edge", "holds", "volunteers", "safe-handling", "--told-by", "n2"
            ),
        )
    )
    steps.append(("n2's account names the ends", lambda v: name_ends(v, "n2", *N2_ENDS)))
    steps.append(("n2 done", lambda v: set_done(v, "n2")))
    return steps


def depth_steps():
    steps = []
    steps.append(("stub narrative n1 first", lambda v: stub(v, "narrative", "n1")))
    steps.append(
        (
            "record-edge stubs both ends",
            lambda v: sh(
                v, "record-edge", "holds", "borrowers", "quick-checkout", "--told-by", "n1"
            ),
        )
    )
    steps.append(
        (
            "record-edge, second",
            lambda v: sh(
                v,
                "record-edge",
                "addressed-by",
                "quick-checkout",
                "self-checkout",
                "--told-by",
                "n1",
            ),
        )
    )
    steps.append(
        (
            "record-edge, third",
            lambda v: sh(
                v, "record-edge", "provided-by", "self-checkout", "booking-app", "--told-by", "n1"
            ),
        )
    )
    steps.append(
        (
            "row linking a page that does not exist",
            lambda v: append_row(v, "n1", "| [[elders]] | holds | [[safe-handling]] | |"),
        )
    )
    steps.append(("stub-links makes both", lambda v: sh(v, "stub-links")))
    steps.append(
        (
            "row with plain text ends",
            lambda v: append_row(v, "n1", "| volunteers | holds | safe-handling | |"),
        )
    )
    steps.append(
        (
            "make them links",
            lambda v: v.edit(
                "narrative/n1.md",
                "| volunteers | holds | safe-handling | |",
                "| [[volunteers]] | holds | [[safe-handling]] | |",
            ),
        )
    )
    steps.append(
        (
            "remove that row",
            lambda v: drop_row(v, "n1", "| [[volunteers]] | holds | [[safe-handling]] | |"),
        )
    )
    steps.append(
        (
            "n1's account and fields",
            lambda v: account(
                v, "n1", "Linked: [[borrowers]], [[quick-checkout]], [[self-checkout]]."
            ),
        )
    )
    steps.append(("then the nodes", fill_all_nodes))
    steps.append(("n1's account names the ends", lambda v: name_ends(v, "n1", *N1_ENDS)))
    steps.append(("n1 done", lambda v: set_done(v, "n1")))
    steps.append(("stub narrative n2", lambda v: stub(v, "narrative", "n2")))
    steps.append(
        (
            "n2 row by record-edge",
            lambda v: sh(
                v, "record-edge", "holds", "borrowers", "quick-checkout", "--told-by", "n2"
            ),
        )
    )
    steps.append(
        (
            "n2 row, new end stubbed",
            lambda v: sh(
                v, "record-edge", "holds", "volunteers", "safe-handling", "--told-by", "n2"
            ),
        )
    )
    steps.append(
        ("n2 account", lambda v: account(v, "n2", "Linked: [[borrowers]], [[volunteers]]."))
    )
    steps.append(("fill the nodes", fill_all_nodes))
    steps.append(("n2's account names the ends", lambda v: name_ends(v, "n2", *N2_ENDS)))
    steps.append(("n2 done", lambda v: set_done(v, "n2")))
    return steps


def edges_of(v):
    """(type, from, to) of every row of every narrative, by the page contracts' reading."""
    import re

    out = set()
    verbs = {
        "holds": "holds",
        "is addressed by": "addressed-by",
        "addressed-by": "addressed-by",
        "is provided by": "provided-by",
        "provided-by": "provided-by",
    }
    for p in sorted(v.root.glob("narrative/*.md")):
        for line in p.read_text().split("\n"):
            m = re.match(
                r"^\|\s*\[\[([^\]|]+)[^\]]*\]\]\s*\|\s*(holds|is addressed by|addressed-by|is provided by|provided-by)\s*\|\s*\[\[([^\]|]+)[^\]]*\]\]",
                line,
            )
            if m:
                out.add((verbs[m.group(2)], m.group(1), m.group(3)))
    return out


@pytest.fixture(scope="module")
def results():
    return {}


@pytest.mark.parametrize("path", ["breadth", "depth"])
def test_no_mismatch_is_ever_unseen(tmp_path, path, results):
    v = Vault(tmp_path / "v")
    v.write("scat.toml", "attribution = 'disallowed'\nstakeholder_group_cap = 3\n")
    steps = breadth_steps() if path == "breadth" else depth_steps()
    seen_kinds = set()
    failures = []
    for n, (label, step) in enumerate(steps, start=1):
        step(v)
        problems = v.check()
        bad = unseen_mismatches(v, problems)
        if bad:
            failures.append(f"step {n} ({label}): {bad}")
        seen_kinds |= {kind for _, _, _, kind, _ in oracle_ends(v)}
        # the check of a page one link away agrees with the vault-wide check on that page's end messages
        for narrative in ("n1", "n2"):
            if v.exists(f"narrative/{narrative}.md"):
                mine = [p.text for p in v.check(narrative) if "-END-" in p.rule]
                wide = [
                    p.text
                    for p in problems
                    if "-END-" in p.rule and p.file == f"narrative/{narrative}.md"
                ]
                if mine != wide:
                    failures.append(
                        f"step {n} ({label}): {narrative} page check differs from vault check"
                    )
    assert not failures, "\n".join(failures)
    # the oracle was not trivially empty: this path met every kind of end mismatch the steps stage
    assert {"nolink", "nopage"} <= seen_kinds
    if path == "breadth":
        assert "notnode" in seen_kinds
    final = v.check()
    assert [p for p in final if p.severity == "error"] == []
    assert v.status_of("n1") == "done" and v.status_of("n2") == "done"
    results[path] = edges_of(v)


def test_both_orders_end_with_the_same_edges(tmp_path, results):
    if len(results) < 2:
        pytest.fail("run the two coding-order tests together")
    assert results["breadth"] == results["depth"]
    assert results["breadth"] == {
        ("holds", "borrowers", "quick-checkout"),
        ("addressed-by", "quick-checkout", "self-checkout"),
        ("provided-by", "self-checkout", "booking-app"),
        ("holds", "elders", "safe-handling"),
        ("holds", "volunteers", "safe-handling"),
    }
