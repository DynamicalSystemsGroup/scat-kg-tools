"""WP24-G1, R1: evidence never reads a narrative's `attributed_to` and never lists a contributor page.

For each vault in `VAULTS` (a builder that makes a folder under tmp_path; add a builder here to put another vault,
such as the G6 vault, under the same tests) and for every node page of it, the evidence document is the same
  - with contributor pages added,
  - with `attributed_to` stripped (where the mode allows a narrative to name no one),
  - with `attributed_to` naming other contributors,
in each of the three modes. A contributor page is in no narrative, adjacent node, edge or paragraph. A paragraph is
the coder's body text, as written. The only field that may move is a paragraph's `line` when a variant adds or
removes frontmatter lines, so that field is left out of the comparison unless the variant keeps the line count.
"""

import re
import shutil
from pathlib import Path

import pytest

import scat_kg
from scat_kg.graph import load

ROOT = Path(__file__).resolve().parents[2]
EXAMPLES = ROOT / "contracts" / "examples"
RANGE = ROOT / "research" / "range" / "koi" / "vault"
PEOPLE = ("ada-quill", "bo-marsh", "cy-reed")
ATTRIBUTED = re.compile(r"^attributed_to:.*\n", re.MULTILINE)


def examples(mode: str, named: bool):
    """The example vault in `mode`; `named`: every narrative names all of PEOPLE, who have pages."""

    def build(tmp: Path) -> Path:
        root = tmp / f"examples-{mode}"
        shutil.copytree(EXAMPLES, root)
        (root / "scat.toml").write_text(
            f'attribution = "{mode}"\nstakeholder_group_cap = 3\n', "utf-8"
        )
        if named:
            add_contributors(root, PEOPLE)
            set_attributed(root, PEOPLE)
        return root

    return build


def the_range_vault(tmp: Path) -> Path:
    root = tmp / "range"
    shutil.copytree(RANGE, root)
    return root


# (id, builder, mode). Extend with the G6 vault's three copies, one per mode.
VAULTS = [
    ("examples-disallowed", examples("disallowed", False), "disallowed"),
    ("examples-optional-unnamed", examples("optional", False), "optional"),
    ("examples-optional", examples("optional", True), "optional"),
    ("examples-required", examples("required", True), "required"),
    ("range-disallowed", the_range_vault, "disallowed"),
]


def add_contributors(root: Path, names) -> None:
    for who in names:
        page = root / "contributor" / f"{who}.md"
        page.parent.mkdir(exist_ok=True)
        page.write_text(f'---\ntype: contributor\nstatus: done\ntitle: "{who}"\n---\n', "utf-8")


def set_attributed(root: Path, names) -> None:
    line = "attributed_to: [" + ", ".join(f'"[[{w}]]"' for w in names) + "]\n"
    for path in (root / "narrative").glob("*.md"):
        text = ATTRIBUTED.sub("", path.read_text("utf-8"), count=1)
        path.write_text(text.replace("\n---\n", "\n" + line + "---\n", 1), "utf-8")


def strip_attributed(root: Path) -> None:
    for path in (root / "narrative").glob("*.md"):
        path.write_text(ATTRIBUTED.sub("", path.read_text("utf-8"), count=1), "utf-8")


def documents(root: Path) -> dict[str, dict]:
    """The evidence document of every node page of the vault."""
    nodes = [n.name for ns in load(root).nodes.values() for n in ns]
    assert nodes
    return {n: scat_kg.evidence(n, root=root).to_dict() for n in nodes}


def without_lines(docs: dict) -> dict:
    out = {}
    for node, d in docs.items():
        d = {**d, "narratives": [dict(n) for n in d["narratives"]]}
        for n in d["narratives"]:
            n["paragraphs"] = [{k: v for k, v in p.items() if k != "line"} for p in n["paragraphs"]]
        out[node] = d
    return out


def names_in(value) -> set[str]:
    """Every string in a document, to look for a contributor's name."""
    if isinstance(value, str):
        return {value}
    if isinstance(value, dict):
        return {s for k, v in value.items() for s in names_in(k) | names_in(v)}
    if isinstance(value, list):
        return {s for v in value for s in names_in(v)}
    return set()


@pytest.fixture(params=VAULTS, ids=[v[0] for v in VAULTS])
def made(request, tmp_path):
    _name, build, mode = request.param
    return build(tmp_path), mode


def test_the_vault_is_conformant_and_carries_its_mode(made):
    root, mode = made
    assert not scat_kg.check(root=root).errors
    assert all(d["mode"] == mode for d in documents(root).values())


def test_adding_contributor_pages_changes_nothing(made, tmp_path):
    root, _ = made
    before = documents(root)
    other = tmp_path / "with-pages"
    shutil.copytree(root, other)
    add_contributors(other, ("di-fox", "ed-wren", "zz-last", "aa-first"))
    assert documents(other) == before  # the same, line for line: no narrative file changed


def test_no_contributor_is_in_any_document(made, tmp_path):
    root, _ = made
    other = tmp_path / "with-pages"
    shutil.copytree(root, other)
    add_contributors(other, ("di-fox", "ed-wren"))
    # the contributor names are in no field of any document; a paragraph is the body text as written, which no
    # narrative of these vaults uses to name one
    strings = names_in(list(documents(other).values()))
    for who in (*PEOPLE, "di-fox", "ed-wren"):
        assert not any(who in s for s in strings), who


def test_stripping_attributed_to_changes_nothing(made, tmp_path):
    root, mode = made
    if mode == "required":
        pytest.skip(
            "a required-mode narrative that names no one is an error, and a view refuses on it"
        )
    before = documents(root)
    other = tmp_path / "stripped"
    shutil.copytree(root, other)
    strip_attributed(other)
    assert without_lines(documents(other)) == without_lines(before)


def test_naming_other_contributors_changes_nothing(made, tmp_path):
    root, mode = made
    if mode == "disallowed":
        pytest.skip("a disallowed-mode narrative cannot name a contributor")
    before = documents(root)
    other = tmp_path / "renamed"
    shutil.copytree(root, other)
    add_contributors(other, ("di-fox",))
    set_attributed(
        other, ("di-fox",)
    )  # one name in the field instead of three: the same number of lines
    assert without_lines(documents(other)) == without_lines(before)


def test_a_contributor_page_is_refused_as_the_node(made, tmp_path):
    root, _ = made
    other = tmp_path / "with-pages"
    shutil.copytree(root, other)
    add_contributors(other, ("di-fox",))
    r = scat_kg.evidence("di-fox", root=other)
    assert not r.ok and "no node has this name" in str(r)
