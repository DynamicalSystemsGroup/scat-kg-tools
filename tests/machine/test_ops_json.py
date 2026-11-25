"""WP11-U3: every operation's result as data. Each of the nine commands, through the CLI (`--json`) and
through the API (`to_dict()`): valid against the schema, one JSON document on stdout, equal to each other,
and the exit code unchanged by `--json`."""

import json
import shutil
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

import scat_kg
from scat_kg.cli import main

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = json.loads((ROOT / "contracts" / "machine-interface.schema.json").read_text("utf-8"))
VALIDATOR = Draft202012Validator(SCHEMA)
EXAMPLES = ROOT / "contracts" / "examples"


def copies(tmp_path):
    """Two copies of the example vault (it has only warnings): one for the CLI, one for the API."""
    out = []
    for name in ("cli", "api"):
        dest = tmp_path / name
        shutil.copytree(EXAMPLES, dest)
        out.append(dest)
    return out


def run_cli(argv, capsys):
    code = main(argv)
    return code, capsys.readouterr()


# (id, CLI words after `scat`, the API call, expected ok, expected kind)
CASES = [
    ("check ok", ["check"], lambda r: scat_kg.check(root=r), True, "check"),
    ("check page", ["check", "quick-checkout"], lambda r: scat_kg.check("quick-checkout", root=r), True, "check"),
    ("check no page", ["check", "no-such-page"], lambda r: scat_kg.check("no-such-page", root=r), False, "operation"),
    ("check neighborhood needs page", ["check", "--neighborhood"], lambda r: scat_kg.check(neighborhood=True, root=r), False, "operation"),
    ("status ok", ["status"], lambda r: scat_kg.status(root=r), True, "status"),
    ("status page", ["status", "quick-checkout"], lambda r: scat_kg.status("quick-checkout", root=r), True, "status"),
    ("status neighborhood", ["status", "quick-checkout", "--neighborhood"], lambda r: scat_kg.status("quick-checkout", neighborhood=True, root=r), True, "status"),
    ("status no page", ["status", "no-such-page"], lambda r: scat_kg.status("no-such-page", root=r), False, "operation"),
    ("set-status ok", ["set-status", "quick-checkout", "stub"], lambda r: scat_kg.set_status("quick-checkout", "stub", root=r), True, "operation"),
    ("set-status bad", ["set-status", "quick-checkout", "nearly"], lambda r: scat_kg.set_status("quick-checkout", "nearly", root=r), False, "operation"),
    ("index ok", ["index"], lambda r: scat_kg.index(root=r), True, "operation"),
    ("stub ok", ["stub", "fresh-idea", "--type", "concern"], lambda r: scat_kg.stub("fresh-idea", "concern", root=r), True, "operation"),
    ("stub index", ["stub", "x", "--type", "index"], lambda r: scat_kg.stub("x", "index", root=r), False, "operation"),
    ("stub edge type", ["stub", "x", "--type", "holds"], lambda r: scat_kg.stub("x", "holds", root=r), False, "operation"),
    ("stub bad name", ["stub", "Not A Name!", "--type", "concern"], lambda r: scat_kg.stub("Not A Name!", "concern", root=r), False, "operation"),
    ("stub-links ok", ["stub-links"], lambda r: scat_kg.stub_links(root=r), True, "operation"),
    ("set-status done refused", ["set-status", "funders-meeting", "done"], lambda r: scat_kg.set_status("funders-meeting", "done", root=r), False, "operation"),
    ("record-edge ok", ["record-edge", "holds", "borrowers", "careful-record-keeping", "--told-by", "funders-meeting", "--note", "n"], lambda r: scat_kg.record_edge("holds", "borrowers", "careful-record-keeping", ["funders-meeting"], "n", root=r), True, "operation"),
    ("record-edge new narrative", ["record-edge", "holds", "borrowers", "fresh", "--told-by", "story"], lambda r: scat_kg.record_edge("holds", "borrowers", "fresh", "story", root=r), True, "operation"),
    ("record-edge unchanged", ["record-edge", "holds", "borrowers", "quick-checkout", "--told-by", "saturday-at-the-lending-desk"], lambda r: scat_kg.record_edge("holds", "borrowers", "quick-checkout", "saturday-at-the-lending-desk", root=r), True, "operation"),
    ("record-edge bad type", ["record-edge", "owns", "a", "b", "--told-by", "n"], lambda r: scat_kg.record_edge("owns", "a", "b", "n", root=r), False, "operation"),
    ("record-edge into done", ["record-edge", "holds", "borrowers", "careful-record-keeping", "--told-by", "saturday-at-the-lending-desk"], lambda r: scat_kg.record_edge("holds", "borrowers", "careful-record-keeping", "saturday-at-the-lending-desk", root=r), False, "operation"),
    ("remove-edge nothing to do", ["remove-edge", "funders", "quick-checkout"], lambda r: scat_kg.remove_edge("funders", "quick-checkout", root=r), True, "operation"),
    ("remove-edge from done", ["remove-edge", "borrowers", "quick-checkout"], lambda r: scat_kg.remove_edge("borrowers", "quick-checkout", root=r), False, "operation"),
    ("remove-edge no node", ["remove-edge", "ghost", "quick-checkout"], lambda r: scat_kg.remove_edge("ghost", "quick-checkout", root=r), False, "operation"),
    ("stub-links no page", ["stub-links", "no-such-page"], lambda r: scat_kg.stub_links("no-such-page", root=r), False, "operation"),
]  # fmt: skip


@pytest.mark.parametrize("case", CASES, ids=[c[0] for c in CASES])
def test_cli_json_equals_api_and_is_valid(case, tmp_path, capsys):
    _, words, call, ok, kind = case
    cli_root, api_root = copies(tmp_path)
    code, out = run_cli([*words, "--json", "--root", str(cli_root)], capsys)
    doc = json.loads(out.out)  # exactly one JSON document: json.loads rejects anything after it
    assert out.err == ""
    assert out.out == json.dumps(doc, indent=2, ensure_ascii=False) + "\n"
    api = call(api_root)
    assert doc == api.to_dict()
    assert VALIDATOR.is_valid(doc), list(VALIDATOR.iter_errors(doc))[:1]
    assert (doc["ok"], doc["kind"]) == (ok, kind)
    assert code == (0 if ok else 1)
    assert api.ok is ok


@pytest.mark.parametrize("case", CASES, ids=[c[0] for c in CASES])
def test_exit_code_and_text_do_not_depend_on_json(case, tmp_path, capsys):
    _, words, _, ok, _ = case
    plain_root, json_root = copies(tmp_path)
    code, out = run_cli([*words, "--root", str(plain_root)], capsys)
    code_json, _ = run_cli([*words, "--json", "--root", str(json_root)], capsys)
    assert code == code_json == (0 if ok else 1)
    assert not out.out.lstrip().startswith("{")  # the text form is untouched


def test_operation_names_are_command_names(tmp_path, capsys):
    root = copies(tmp_path)[0]
    for words, name in [
        (["check", "nope"], "check"),
        (["status", "nope"], "status"),
        (["set-status", "quick-checkout", "stub"], "set-status"),
        (["index"], "index"),
        (["stub", "zed", "--type", "concern"], "stub"),
        (["record-edge", "holds", "a", "b", "--told-by", "n"], "record-edge"),
        (["remove-edge", "a", "b"], "remove-edge"),
        (["stub-links"], "stub-links"),
    ]:
        _, out = run_cli([*words, "--json", "--root", str(root)], capsys)
        assert json.loads(out.out)["operation"] == name


@pytest.mark.parametrize("command", ["check", "status"])
def test_not_a_vault_is_an_operation_refusal(command, tmp_path, capsys):
    missing = tmp_path / "nowhere"
    code, out = run_cli([command, "--json", "--root", str(missing)], capsys)
    doc = json.loads(out.out)
    assert code == 1
    assert (doc["kind"], doc["operation"], doc["ok"]) == ("operation", command, False)
    assert VALIDATOR.is_valid(doc)


@pytest.mark.parametrize("command", ["check", "status"])
def test_page_not_found_is_an_operation_refusal(command, tmp_path, capsys):
    root = copies(tmp_path)[0]
    code, out = run_cli([command, "ghost", "--json", "--root", str(root)], capsys)
    doc = json.loads(out.out)
    assert code == 1
    assert (doc["kind"], doc["operation"], doc["ok"]) == ("operation", command, False)
    assert doc["refused"][0]["subject"] == "ghost"
    assert VALIDATOR.is_valid(doc)


def test_check_with_only_warnings_is_ok_and_with_an_error_is_not(tmp_path, capsys):
    root = copies(tmp_path)[0]
    code, out = run_cli(["check", "--json", "--root", str(root)], capsys)
    doc = json.loads(out.out)
    assert doc["problems"] and {p["severity"] for p in doc["problems"]} == {"warning"}
    assert (doc["ok"], code) == (True, 0)
    page = next(root.glob("concern/*.md"))
    page.write_text("---\ntype: concern\nstatus: bogus\ntitle: T\n---\n", encoding="utf-8")
    code, out = run_cli(["check", "--json", "--root", str(root)], capsys)
    doc = json.loads(out.out)
    assert "error" in {p["severity"] for p in doc["problems"]}
    assert (doc["ok"], code) == (False, 1)
    assert VALIDATOR.is_valid(doc)


def test_status_rows_null_what_is_not_a_string(tmp_path):
    root = copies(tmp_path)[0]
    (root / "concern" / "odd.md").write_text(
        "---\ntype: concern\nstatus: 7\ntitle: T\n---\n", encoding="utf-8"
    )
    (root / "concern" / "odder.md").write_text("---\ntype: [a]\ntitle: T\n---\n", encoding="utf-8")
    doc = scat_kg.status(root=root).to_dict()
    rows = {r["name"]: r for r in doc["rows"]}
    assert rows["odd"]["status"] is None and rows["odd"]["type"] == "concern"
    assert rows["odder"]["type"] is None
    assert VALIDATOR.is_valid(doc)
    assert set(doc["counts"]) == {"stub", "draft", "done", "other"}  # no `none` in version 2


def option_kinds(result):
    return [o["kind"] for r in result.to_dict()["refused"] for o in r["fix"]["options"]]


def test_refusal_fixes_are_data(tmp_path):
    root = copies(tmp_path)[0]
    r = scat_kg.stub("x", "index", root=root)
    (refusal,) = r.to_dict()["refused"]
    (opt,) = refusal["fix"]["options"]
    assert refusal["fix"]["kind"] == opt["kind"] == "exact"
    assert opt["command"] == {"argv": ["index"], "repl": "scat_kg.index()"}
    assert r.refused[0].fix == "run `scat index` (REPL: `scat_kg.index()`)"
    # a refusal with no command in it is one manual option holding the text shown today
    r = scat_kg.set_status("quick-checkout", "nearly", root=root)
    (opt,) = r.to_dict()["refused"][0]["fix"]["options"]
    assert opt["kind"] == "manual" and opt["text"] == r.refused[0].fix and "command" not in opt


def test_the_done_refusal_has_a_rule_and_problems_and_a_plain_refusal_has_neither(tmp_path):
    root = copies(tmp_path)[0]
    (ref,) = scat_kg.set_status("funders-meeting", "done", root=root).to_dict()["refused"]
    assert ref["rule"] == "SCAT-DONE-REFUSED" and {p["rule"] for p in ref["problems"]} == {
        "SCAT-DONE-FIELD"
    }
    assert [o["kind"] for o in ref["fix"]["options"]] == ["advisory", "exact"]
    (plain,) = scat_kg.record_edge("owns", "a", "b", "n", root=root).to_dict()["refused"]
    assert "rule" not in plain and "problems" not in plain


def test_record_and_remove_edge_name_the_edge_and_the_rows(tmp_path):
    root = copies(tmp_path)[0]
    doc = scat_kg.record_edge("holds", "borrowers", "fresh", "story", root=root).to_dict()
    assert doc["edge"] == {
        "type": "holds",
        "from": "borrowers",
        "to": "fresh",
        "narratives": ["story"],
    }
    assert doc["created"] == ["concern/fresh.md", "narrative/story.md"]
    assert [r["narrative"] for r in doc["rows_added"]] == ["story"] and doc["rows_removed"] == []
    gone = scat_kg.remove_edge("borrowers", "fresh", root=root).to_dict()
    assert gone["edge"]["narratives"] == [] and gone["rows_added"] == []
    assert [r["narrative"] for r in gone["rows_removed"]] == ["story"] and VALIDATOR.is_valid(gone)


def test_index_refusal_is_a_refusal_with_a_fix(tmp_path):
    root = copies(tmp_path)[0]
    shutil.rmtree(root / "index")
    (root / "index").write_text("a file", encoding="utf-8")
    doc = scat_kg.index(root=root).to_dict()
    assert VALIDATOR.is_valid(doc) and not doc["ok"]
    assert (
        doc["refused"][0]["subject"] == "index"
        and "scat index" in doc["refused"][0]["fix"]["options"][0]["text"]
    )


def test_stub_links_two_types_gives_a_slot(tmp_path):
    root = copies(tmp_path)[0]
    (root / "narrative" / "dual.md").write_text(
        "---\ntype: narrative\nstatus: draft\ntitle: D\n---\n\n## Edges told\n\n"
        "| type | from | to | note |\n|---|---|---|---|\n"
        "| holds | [[borrowers]] | [[ghost]] | |\n| is addressed by | [[quick-checkout]] | [[ghost]] | |\n",
        encoding="utf-8",
    )
    r = scat_kg.stub_links(root=root)
    doc = r.to_dict()
    assert VALIDATOR.is_valid(doc)
    (refusal,) = [x for x in doc["refused"] if "different types" in x["why"]]
    assert refusal["fix"]["kind"] == "options"
    manual, slot = refusal["fix"]["options"]
    assert manual["kind"] == "manual"
    assert slot["kind"] == "slot" and slot["command"]["author_slot"] == "<type>"
    assert slot["command"]["argv"] == ["stub", "ghost", "--type", "<type>"]
