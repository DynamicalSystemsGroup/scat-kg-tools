"""WP24-R4, R8, R10: the review view: possible duplicates and pages to re-read, from structure and never from names.

Built vaults give hand-computed answers at each threshold (a change to a constant fails a test); the G6 vault's
seeded pairs are proposed or not, as the seeds say, in all three modes and on the range vault; renaming every node
page and every link leaves the proposals the same under the map; the proposals are counted; link text is shown and
never scored; the module compares no names.
"""

import json
import re
import shutil
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from viewutil import base_files, narrative, page, tree_hash, write

import scat_tools
from scat_tools.cli import main
from scat_tools.ops.result import Result

ROOT = Path(__file__).resolve().parents[2]
NODE_PAGES = ROOT / "research" / "node-pages" / "vault"
RANGE = ROOT / "research" / "range" / "koi" / "vault"
SCHEMA = json.loads((ROOT / "contracts" / "machine-interface.schema.json").read_text("utf-8"))
VALIDATOR = Draft202012Validator(SCHEMA)

SYNONYM = ("members-not-replying", "unanswered-direct-messages")
DUPLICATE_ROW = ("digest-email", "weekly-digest")
DECOY = ("data-retention", "data-retention-schedule")
HOMONYM = "community-members"

# the number of proposals on each vault: a threshold change shows here
COUNTS = {"disallowed": 9, "optional": 9, "required": 9, "range": 6}

VAULTS = {
    **{mode: NODE_PAGES / mode for mode in ("disallowed", "optional", "required")},
    "range": RANGE,
}

TYPES = {"g": "group", "c": "concern", "a": "affordance", "t": "technology"}
EDGE = {("g", "c"): "holds", ("c", "a"): "addressed-by", ("a", "t"): "provided-by"}


def build(tmp, narratives, descriptions=None, aliases=None, pad=0):
    """A vault from `narratives`: {name: [(a, b), ...]}, each pair a row between nodes named by their first letter
    (g group, c concern, a affordance, t technology). `descriptions` is {node: text}; `aliases` {node: text}, the
    text a narrative gives its link."""
    descriptions, aliases = descriptions or {}, aliases or {}
    files = {"scat.toml": "attribution = 'disallowed'\nstakeholder_group_cap = 3\n"}
    nodes = {x for rows in narratives.values() for pair in rows for x in pair}
    for x in nodes:
        extra = f'description: "{descriptions[x]}"\n' if x in descriptions else ""
        files[f"{TYPES[x[0]]}/{x}.md"] = page(TYPES[x[0]], x, "draft", extra, "")
    for i in range(pad):  # node pages no narrative links
        files[f"technology/t-pad{i}.md"] = page("technology", f"t-pad{i}", "draft", "", "")
    for name, rows in narratives.items():
        text = "Account: " + " ".join(
            f"[[{x}|{aliases[x]}]]" if x in aliases else f"[[{x}]]"
            for x in sorted({x for pair in rows for x in pair})
        )
        table = [f"| [[{a}]] | {EDGE[(a[0], b[0])]} | [[{b}]] | |" for a, b in rows]
        files[f"narrative/{name}.md"] = narrative(name, text, table, "draft", "scenario")
    return write(tmp / "built", files)


def doc(root):
    view = scat_tools.review(root=root)
    assert view.ok, str(view)
    d = view.to_dict()
    assert VALIDATOR.is_valid(d), list(VALIDATOR.iter_errors(d))[:3]
    return d


def pairs(d):
    return {tuple(p["name"] for p in x["pages"]) for x in d["proposals"]}


def proposal(d, a, b):
    return next(x for x in d["proposals"] if tuple(p["name"] for p in x["pages"]) == (a, b))


# ---------------------------------------------------------------- the three rules, at their thresholds


def test_adjacent_nodes_at_one_half_propose_a_pair(tmp_path):
    # c1: g1 g2 a1; c2: g1 g2 a2; shared 2 of 4
    d = doc(
        build(
            tmp_path,
            {"n1": [("g1", "c1"), ("g2", "c1"), ("c1", "a1")]}
            | {"n2": [("g1", "c2"), ("g2", "c2"), ("c2", "a2")]},
        )
    )
    p = proposal(d, "c1", "c2")
    assert p["adjacent_jaccard"] == 0.5 and p["narrative_jaccard"] == 0.0
    assert p["twin_rows"] == [] and p["reason"].startswith("may be one node: 2 of 4 adjacent nodes")
    assert [x["name"] for x in p["shared_adjacent"]] == ["g1", "g2"]


def test_adjacent_nodes_below_one_half_do_not(tmp_path):
    # shared 2 of 5
    d = doc(
        build(
            tmp_path,
            {
                "n1": [("g1", "c1"), ("g2", "c1"), ("c1", "a1")],
                "n2": [("g1", "c2"), ("g2", "c2"), ("c2", "a2"), ("c2", "a3")],
            },
        )
    )
    assert ("c1", "c2") not in pairs(d)


def test_a_page_with_one_adjacent_node_is_not_proposed_on_adjacency(tmp_path):
    d = doc(build(tmp_path, {"n1": [("g1", "c1")], "n2": [("g1", "c2")]}))
    assert d["proposals"] == []


def test_descriptions_at_one_half_propose_a_pair(tmp_path):
    d = doc(
        build(
            tmp_path,
            {"n1": [("g1", "c1")], "n2": [("g2", "c2")]},
            {"c1": "alpha beta gamma delta", "c2": "alpha beta epsilon zeta"},
        )
    )
    p = proposal(d, "c1", "c2")
    assert p["description_cosine"] == 0.5 and p["adjacent_jaccard"] == 0.0
    assert "descriptions share 0.50 of their words" in p["reason"]


def test_descriptions_below_one_half_do_not(tmp_path):
    d = doc(
        build(
            tmp_path,
            {"n1": [("g1", "c1")], "n2": [("g2", "c2")]},
            {"c1": "alpha beta gamma delta", "c2": "alpha epsilon zeta theta"},
        )
    )
    assert d["proposals"] == []


def test_common_words_and_short_words_do_not_count_in_a_description(tmp_path):
    d = doc(
        build(
            tmp_path,
            {"n1": [("g1", "c1")], "n2": [("g2", "c2")]},
            {"c1": "the one of an to alpha", "c2": "the one of an to beta"},
        )
    )
    assert d["proposals"] == []


def test_a_twin_row_with_narratives_at_one_half_proposes_a_pair(tmp_path):
    # n1 tells g1 holds c1 and g1 holds c2 (a twin row); n2 links c1 only: narratives c1 {n1, n2}, c2 {n1}
    d = doc(
        build(
            tmp_path,
            {
                "n1": [("g1", "c1"), ("g1", "c2")],
                "n2": [("g2", "c1")],
            },
        )
    )
    p = proposal(d, "c1", "c2")
    assert p["narrative_jaccard"] == 0.5 and "adjacent nodes shared" not in p["reason"]
    assert [(t["narrative"], t["edge_type"], t["other_end"]) for t in p["twin_rows"]] == [
        ("n1", "holds", "g1")
    ]
    assert p["twin_rows"][0]["file"] == "narrative/n1.md" and len(p["twin_rows"][0]["lines"]) == 2
    assert "a narrative tells the same row for both (1x)" in p["reason"]


def test_a_twin_row_with_narratives_below_one_half_does_not(tmp_path):
    d = doc(
        build(
            tmp_path,
            {
                "n1": [("g1", "c1"), ("g1", "c2")],
                "n2": [("g2", "c1")],
                "n3": [("g3", "c1")],
            },
        )
    )
    assert ("c1", "c2") not in pairs(d)


def test_a_pair_that_shares_nothing_is_not_proposed_whatever_the_names(tmp_path):
    d = doc(
        build(
            tmp_path,
            {
                "n1": [("g1", "c-retention"), ("c-retention", "a1")],
                "n2": [("g2", "c-retention-schedule"), ("c-retention-schedule", "a2")],
            },
        )
    )
    assert d["proposals"] == []


def test_pages_of_different_types_are_never_paired(tmp_path):
    d = doc(
        build(
            tmp_path,
            {"n1": [("g1", "c1")], "n2": [("c1", "a1")]},
            {"g1": "alpha beta gamma delta", "a1": "alpha beta gamma delta"},
        )
    )
    assert d["proposals"] == []


# ---------------------------------------------------------------- hubs, link text


def test_a_hub_among_the_shared_adjacent_nodes_is_marked(tmp_path):
    # g1 is adjacent to c1 to c4 (4 pages, over a tenth of the pages): a hub; g2 is adjacent to c1 and c2 only
    d = doc(
        build(
            tmp_path,
            {
                "n1": [("g1", "c1"), ("g2", "c1")],
                "n2": [("g1", "c2"), ("g2", "c2")],
                "n3": [("g1", "c3")],
                "n4": [("g1", "c4")],
            },
        )
    )
    shared = {x["name"]: x["hub"] for x in proposal(d, "c1", "c2")["shared_adjacent"]}
    assert shared == {"g1": True, "g2": False}


def test_link_text_is_shown_beside_a_proposal_and_never_makes_one(tmp_path):
    shared = {"n1": [("g1", "c1")], "n2": [("g2", "c2")]}
    d = doc(build(tmp_path, shared, aliases={"c1": "the same words", "c2": "the same words"}))
    assert d["proposals"] == []  # equal link text alone proposes nothing
    d = doc(
        build(
            tmp_path / "x",
            {"n1": [("g1", "c1"), ("g2", "c1")], "n2": [("g1", "c2"), ("g2", "c2")]},
            aliases={"c1": "first words", "c2": "second words"},
        )
    )
    p = proposal(d, "c1", "c2")
    assert [x["link_texts"] for x in p["pages"]] == [["first words"], ["second words"]]


# ---------------------------------------------------------------- pages to re-read


def reread_vault(tmp_path, together):
    """g1 is told by five narratives; the first `together` tell it to c1, the others each to a concern of their own."""
    rows = {f"n{i}": [("g1", "c1" if i <= together else f"c{i}")] for i in range(1, 6)}
    return doc(build(tmp_path, rows))


def test_three_of_ten_pairs_with_a_common_end_is_listed_with_its_groups(tmp_path):
    d = reread_vault(tmp_path, 3)  # 3 of 10 pairs share an other end: 0.3
    assert [r["name"] for r in d["reread"]] == ["g1"]
    r = d["reread"][0]
    assert r["common_end_share"] == 0.3 and r["narratives"] == 5
    assert r["groups"] == [["n1", "n2", "n3"], ["n4"], ["n5"]]
    assert (
        r["reason"] == "these accounts tell this page to different other ends; read them together"
    )


def test_four_of_ten_pairs_with_a_common_end_is_not_listed(tmp_path):
    assert reread_vault(tmp_path, 4)["reread"] == []  # 6 of 10 pairs


def test_a_page_told_by_three_narratives_is_not_listed(tmp_path):
    d = doc(build(tmp_path, {f"n{i}": [("g1", f"c{i}")] for i in range(1, 4)}))
    assert d["reread"] == []


def test_a_narrative_that_only_links_the_page_is_not_counted(tmp_path):
    rows = {f"n{i}": [("g1", f"c{i}")] for i in range(1, 4)} | {"n4": [("g2", "c1")]}
    # n4 links c1 and tells no edge of g1; g1 has three telling narratives
    assert doc(build(tmp_path, rows))["reread"] == []


# ---------------------------------------------------------------- just under each threshold, and each count at its edge


def words(n, start=0):
    """n distinct words of three letters, none a common word."""
    return " ".join(
        f"q{chr(97 + (i // 26) % 26)}{chr(97 + i % 26)}" for i in range(start, start + n)
    )


def test_adjacent_nodes_just_under_one_half_do_not(tmp_path):
    # shared 25 of 51 (0.4902): c1 and c2 share g1 to g25, c1 has 13 more, c2 has 13 more
    rows = {}
    for i in range(25):
        rows[f"s1-{i}"], rows[f"s2-{i}"] = [(f"g{i}", "c1")], [(f"g{i}", "c2")]
    for i in range(13):
        rows[f"o1-{i}"], rows[f"o2-{i}"] = [(f"gh{i}", "c1")], [(f"gk{i}", "c2")]
    d = doc(build(tmp_path, rows))
    assert ("c1", "c2") not in pairs(d)


def test_adjacent_nodes_at_one_half_with_two_each_are_proposed(tmp_path):
    d = doc(
        build(tmp_path, {"n1": [("g1", "c1"), ("g2", "c1")], "n2": [("g1", "c2"), ("g2", "c2")]})
    )
    assert proposal(d, "c1", "c2")["adjacent_jaccard"] == 1.0  # two adjacent nodes each is enough


def test_descriptions_just_under_one_half_do_not(tmp_path):
    # 51 words each, 25 shared: cosine 25/51 = 0.4902
    a, b = words(51), words(25) + " " + words(26, 100)
    d = doc(build(tmp_path, {"n1": [("g1", "c1")], "n2": [("g2", "c2")]}, {"c1": a, "c2": b}))
    assert d["proposals"] == []


def test_narratives_just_under_one_half_do_not(tmp_path):
    # c1 and c2 are linked by 25 narratives in common of 51; one of them tells the twin row
    rows = {"twin": [("g0", "c1"), ("g0", "c2")]}
    for i in range(24):
        rows[f"s{i}"] = [(f"ga{i}", "c1"), (f"gb{i}", "c2")]
    for i in range(13):
        rows[f"o1-{i}"], rows[f"o2-{i}"] = [(f"gh{i}", "c1")], [(f"gk{i}", "c2")]
    d = doc(build(tmp_path, rows))
    assert ("c1", "c2") not in pairs(d)


def hub_flags(tmp_path, adjacent, total):
    """The hub flag of g1, shared by c1 and c2 and adjacent to `adjacent` concerns, in a vault of `total` node pages."""
    rows = {f"n{i}": [("g1", f"c{i}")] for i in range(1, adjacent + 1)}
    rows["n1"], rows["n2"] = [("g1", "c1"), ("g2", "c1")], [("g1", "c2"), ("g2", "c2")]
    pad = total - (2 + adjacent)  # g1, g2 and the concerns
    d = doc(build(tmp_path, rows, pad=pad))
    return {x["name"]: x["hub"] for x in proposal(d, "c1", "c2")["shared_adjacent"]}["g1"]


def test_a_node_adjacent_to_three_pages_is_not_a_hub(tmp_path):
    assert hub_flags(tmp_path, 3, 12) is False


def test_a_node_adjacent_to_four_pages_is_a_hub(tmp_path):
    assert hub_flags(tmp_path, 4, 12) is True


def test_four_pages_is_a_hub_over_a_tenth_of_39_pages(tmp_path):
    assert hub_flags(tmp_path, 4, 39) is True  # 4 is more than 3.9


def test_four_pages_is_not_a_hub_at_a_tenth_of_40_pages(tmp_path):
    assert hub_flags(tmp_path, 4, 40) is False  # 4 is not more than 4.0


def test_a_page_told_by_four_narratives_is_listed(tmp_path):
    d = doc(build(tmp_path, {f"n{i}": [("g1", f"c{i}")] for i in range(1, 5)}))
    assert [r["name"] for r in d["reread"]] == ["g1"] and d["reread"][0]["narratives"] == 4


def test_a_common_end_share_just_over_three_tenths_is_not_listed(tmp_path):
    # nine narratives: five tell g1 to c1, two to c2, one each to c3 and c4: 11 of 36 pairs, 0.3056
    rows = {
        f"n{i}": [("g1", "c1" if i <= 5 else "c2" if i <= 7 else f"c{i}")] for i in range(1, 10)
    }
    assert doc(build(tmp_path, rows))["reread"] == []


# ---------------------------------------------------------------- the G6 vault and the range vault


@pytest.fixture(scope="module", params=sorted(VAULTS))
def seeded(request):
    return request.param, doc(VAULTS[request.param])


def test_the_number_of_proposals_is_pinned(seeded):
    name, d = seeded
    assert len(d["proposals"]) == COUNTS[name]


def test_the_seeded_pairs(seeded):
    name, d = seeded
    found = pairs(d)
    if name == "range":
        assert not found & {SYNONYM, DUPLICATE_ROW, DECOY}
        return
    assert SYNONYM in found and DUPLICATE_ROW in found and DECOY not in found
    p = proposal(d, *SYNONYM)
    assert p["adjacent_jaccard"] == 1.0 and len(p["twin_rows"]) == 4
    assert {x["name"]: x["hub"] for x in p["shared_adjacent"]} == {
        "direct-message-reminder": False,
        "ethnographers": True,
    }
    assert p["pages"][0]["link_texts"] == ["members not replying", "members were not replying"]
    q = proposal(d, *DUPLICATE_ROW)
    assert q["description_cosine"] >= 0.5 and len(q["twin_rows"]) == 1


def test_the_homonym_is_listed_with_its_groups(seeded):
    name, d = seeded
    names = [r["name"] for r in d["reread"]]
    if name == "range":
        assert HOMONYM not in names
        return
    r = next(r for r in d["reread"] if r["name"] == HOMONYM)
    assert [len(g) for g in r["groups"]] == [4, 1, 1] and r["narratives"] == 6
    assert names == ["technical-team", "obsidian", "ethnographers", HOMONYM]


def test_the_order_is_by_overlap_then_name(seeded):
    _, d = seeded
    keys = [
        (
            -(x["narrative_jaccard"] + x["adjacent_jaccard"] + x["description_cosine"]),
            x["pages"][0]["name"],
            x["pages"][1]["name"],
        )
        for x in d["proposals"]
    ]
    assert keys == sorted(keys)
    for x in d["proposals"]:
        assert [p["name"] for p in x["pages"]] == sorted(p["name"] for p in x["pages"])
        assert {p["type"] for p in x["pages"]} == {x["type"]}


def test_the_document_carries_the_mode(seeded):
    name, d = seeded
    assert (d["schema_version"], d["kind"], d["operation"], d["ok"]) == (3, "view", "review", True)
    assert d["mode"] == ("disallowed" if name == "range" else name)


# ---------------------------------------------------------------- renaming leaves the proposals the same


def rename_everything(root, dest):
    shutil.copytree(root, dest)
    graph = scat_tools.load(dest)
    names = sorted(n.name for ns in graph.nodes.values() for n in ns)
    new = {
        n: f"p{len(names) - i:04d}" for i, n in enumerate(names)
    }  # the order of names is reversed
    pattern = re.compile(
        r"\[\[("
        + "|".join(re.escape(n) for n in sorted(new, key=len, reverse=True))
        + r")(?=[\]|\\#^])"
    )
    for md in sorted(dest.rglob("*.md")):
        text = pattern.sub(lambda m: "[[" + new[m.group(1)], md.read_text("utf-8"))
        md.write_text(text, "utf-8")
        if md.stem in new:
            md.rename(md.with_name(new[md.stem] + ".md"))
    return new


def mapped(d, m):
    """The document with every node name replaced by its new name, ordered by the new names."""
    out = json.loads(json.dumps(d))
    for x in out["proposals"]:
        for p in x["pages"]:
            p["name"] = m[p["name"]]
        for s in x["shared_adjacent"]:
            s["name"] = m[s["name"]]
        for t in x["twin_rows"]:
            t["other_end"] = m[t["other_end"]]
            t["lines"].sort()  # the pages are in name order, and the names changed
        x["pages"].sort(key=lambda p: p["name"])
        x["shared_adjacent"].sort(key=lambda s: s["name"])
        x["twin_rows"].sort(key=lambda t: (t["narrative"], t["edge_type"], t["other_end"]))
    for r in out["reread"]:
        r["name"] = m[r["name"]]
    out["proposals"].sort(key=lambda x: [p["name"] for p in x["pages"]])
    out["reread"].sort(key=lambda r: r["name"])
    for x in out["proposals"]:
        x.pop("reason")  # worded from the numbers, which are compared
    return out


@pytest.mark.parametrize("name", sorted(VAULTS))
def test_renaming_every_node_page_and_link_leaves_the_proposals_the_same(name, tmp_path):
    before = doc(VAULTS[name])
    copy = tmp_path / "renamed"
    new = rename_everything(VAULTS[name], copy)
    assert not scat_tools.check(root=copy).errors
    after = doc(copy)
    assert len(after["proposals"]) == len(before["proposals"]) == COUNTS[name]
    expect, got = mapped(before, new), mapped(after, {v: v for v in new.values()})
    assert got["proposals"] == expect["proposals"]
    assert got["reread"] == expect["reread"]


# ---------------------------------------------------------------- the CLI, refusals, writes nothing, no name compared


def test_the_text_form_begins_with_the_mode_and_reads_as_a_prompt(capsys):
    root = VAULTS["disallowed"]
    text = str(scat_tools.review(root=root))
    assert text.startswith(
        "attribution mode: disallowed\nreview: 9 page pairs that may be one node\n"
    )
    assert "members-not-replying ~ unanswered-direct-messages" in text
    assert "shared adjacent nodes: ethnographers (hub), direct-message-reminder" in text
    assert "pages to re-read: 4" in text
    assert "these accounts tell this page to different other ends; read them together" in text
    assert "two nodes" not in text and "duplicate" not in text


def test_the_cli_json_equals_python(capsys):
    root = VAULTS["disallowed"]
    assert main(["review", "--root", str(root), "--json"]) == 0
    assert json.loads(capsys.readouterr().out) == scat_tools.review(root=root).to_dict()


def test_it_writes_nothing(tmp_path):
    copy = tmp_path / "v"
    shutil.copytree(VAULTS["disallowed"], copy)
    before = tree_hash(copy)
    scat_tools.review(root=copy)
    assert tree_hash(copy) == before


def test_an_uncoded_narrative_is_not_used_and_is_listed(tmp_path):
    root = build(tmp_path, {"n1": [("g1", "c1")]})
    (root / "narrative" / "loose.md").write_text(
        narrative("Loose", "Words only, no node linked."), "utf-8"
    )
    d = doc(root)
    assert [x["name"] for x in d["excluded"]] == ["loose"]


def test_a_missing_vault_is_refused(tmp_path):
    r = scat_tools.review(root=tmp_path / "nowhere")
    assert isinstance(r, Result) and not r.ok


def test_an_error_in_a_page_drawn_refuses(tmp_path):
    root = write(
        tmp_path / "v",
        base_files() | {"concern/water.md": page("concern", "Water", "done", "", "Body.\n")},
    )
    r = scat_tools.review(root=root)
    assert not r.ok and "error" in str(r)
    assert VALIDATOR.is_valid(r.to_dict())


def test_a_row_that_tells_no_edge_refuses(tmp_path):
    root = write(
        tmp_path / "v",
        base_files()
        | {
            "narrative/bad.md": narrative(
                "Bad",
                "The [[water]] ran out.",
                ["| farmers | holds | [[water]] | |"],
                "draft",
                "scenario",
            )
        },
    )
    assert not scat_tools.review(root=root).ok


def test_the_view_takes_no_argument():
    with pytest.raises(TypeError):
        scat_tools.review("water")  # type: ignore[misc]


def test_the_module_compares_no_names():
    source = (ROOT / "src" / "scat_tools" / "review.py").read_text("utf-8").lower()
    for word in (
        "difflib",
        "levenshtein",
        "startswith",
        "endswith",
        "sequencematcher",
        "fuzz",
        "jaro",
        "edit_distance",
        "get_close_matches",
        "rapidfuzz",
        "soundex",
        "similar",
    ):
        assert word not in source, word
