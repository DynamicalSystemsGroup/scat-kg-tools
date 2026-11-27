"""WP30-R5 (unit U1): the guides cover every stage and transition, name only what exists, and every path gives
the same text; the lifecycle instance is found from the source tree and from the wheel."""

import copy
import io
import json
import re
import subprocess
import sys
import zipfile
from contextlib import redirect_stdout
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

import scat_kg
from scat_kg import cli, guides

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = json.loads(
    (ROOT / "contracts" / "machine-interface.schema.json").read_text(encoding="utf-8")
)
VALIDATOR = Draft202012Validator(SCHEMA)
FIVE = ("plan", "capture", "code", "analyse", "report")
INST = guides.instance()


def words(text: str) -> int:
    return len(text.split())


def scat(*argv: str) -> tuple[int, str]:
    out = io.StringIO()
    with redirect_stdout(out):
        code = cli.main(list(argv))
    return code, out.getvalue()


def test_the_names_exist_and_the_stages_are_the_instances():
    assert guides.STAGES == FIVE == tuple(INST["stages"])
    assert scat_kg.guide is guides.guide
    assert guides.guide_text("index")
    assert guides.instance() is not guides.instance()  # a fresh copy each call
    guides.instance()["stages"].clear()
    assert guides.instance()["stages"]


# --- the instance is found from the source tree and from the package data ---------------------------------


def test_the_source_tree_reader_finds_the_instance():
    assert guides._instance_path() == ROOT / "contracts" / "lifecycle.md"


def test_the_packaged_copy_wins_when_present_and_the_source_is_the_fallback(tmp_path, monkeypatch):
    packaged = tmp_path / "lifecycle.md"
    text = (ROOT / "contracts" / "lifecycle.md").read_text(encoding="utf-8")
    packaged.write_text(text.replace("[check, status, stub, attribution]", "[check, status]"))
    monkeypatch.setattr(guides, "_PACKAGED", packaged)
    monkeypatch.setattr(guides, "_SOURCE", tmp_path / "nowhere.md")
    assert guides._instance_path() == packaged
    assert guides.instance()["stages"]["plan"]["tools"] == ["check", "status"]
    monkeypatch.setattr(guides, "_PACKAGED", tmp_path / "absent.md")
    with pytest.raises(FileNotFoundError):
        guides._instance_path()


@pytest.fixture(scope="module")
def wheel(tmp_path_factory) -> Path:
    out = tmp_path_factory.mktemp("wheel")
    subprocess.run(
        ["uv", "build", "--wheel", "--out-dir", str(out), str(ROOT)],
        check=True,
        capture_output=True,
        text=True,
    )
    (whl,) = out.glob("scat_kg-*.whl")
    return whl


def test_the_wheel_holds_the_lifecycle_file_and_the_guides(wheel):
    with zipfile.ZipFile(wheel) as z:
        names = set(z.namelist())
        assert "scat_kg/guides/lifecycle.md" in names
        for stage in FIVE:
            assert f"scat_kg/guides/{stage}.md" in names
        assert (
            z.read("scat_kg/guides/lifecycle.md")
            == (ROOT / "contracts" / "lifecycle.md").read_bytes()
        )


def test_the_installed_reader_finds_the_instance_through_the_package_data(wheel, tmp_path):
    with zipfile.ZipFile(wheel) as z:
        z.extractall(tmp_path)
    code = (
        "import sys; sys.path.insert(0, sys.argv[1]); import scat_kg.guides as g; "
        "print(g.__file__); print(g._instance_path()); print(','.join(g.STAGES)); "
        "print(len(g.guide_text('code').split()))"
    )
    run = subprocess.run(
        [sys.executable, "-I", "-c", code, str(tmp_path)],
        capture_output=True,
        text=True,
        cwd=tmp_path,
        check=True,
    )
    here, found, stages, n = run.stdout.split("\n")[:4]
    assert here.startswith(str(tmp_path))  # the unpacked wheel, not the source tree
    assert found == str(tmp_path / "scat_kg" / "guides" / "lifecycle.md")
    assert stages == ",".join(FIVE)
    assert int(n) == words(guides.guide_text("code"))


# --- each guide ----------------------------------------------------------------------------------------------


@pytest.mark.parametrize("stage", FIVE)
def test_a_stage_guide_is_at_most_400_words(stage):
    assert words(guides.guide_text(stage)) <= 400


def test_the_index_is_at_most_500_words():
    assert words(guides.guide_text("index")) <= 500


@pytest.mark.parametrize("stage", FIVE)
def test_a_stage_guide_names_only_what_exists_and_all_of_it(stage):
    spec, text = INST["stages"][stage], guides.guide_text(stage)
    for t in spec["tools"]:
        assert f"`{t}`" in text
    for p in spec["prompts"]:
        assert f"`{p}`" in text
    every_tool = {t for s in INST["stages"].values() for t in s["tools"]} | set(INST["stage_tools"])
    every_prompt = {p for s in INST["stages"].values() for p in s["prompts"]}
    for ticked in re.findall(r"`([^`]+)`", text):
        if ticked in {
            "mode",
            "scat.toml",
            "output",
            "required",
            "optional",
            "disallowed",
            "draft",
            "done",
        }:
            continue
        assert ticked in spec["tools"] + spec["prompts"], (stage, ticked)
    assert not (every_tool - set(spec["tools"])) & set(re.findall(r"`([^`]+)`", text))
    assert not (every_prompt - set(spec["prompts"])) & set(re.findall(r"`([^`]+)`", text))


@pytest.mark.parametrize("stage", FIVE)
def test_a_stage_guide_has_a_real_docs_page_and_says_what_mode_means(stage):
    parts = guides.guide(stage).to_dict()
    assert parts["docs"].startswith("docs/") and parts["docs"].endswith(".md")
    assert (ROOT / parts["docs"]).is_file()
    assert f"Docs: {parts['docs']}" in parts["text"]
    assert guides.MODE in parts["text"]
    assert "SHALL NOT" in parts["text"] and "MAY" in parts["text"]


@pytest.mark.parametrize("stage", FIVE)
def test_a_stage_guide_covers_every_transition_out_of_the_stage(stage):
    text = guides.guide_text(stage)
    outs = [t for t in INST["transitions"] if t["from"] == stage]
    assert outs
    for t in outs:
        assert re.search(
            rf"^- {t['id']} to {t['to']} \({re.escape(t['decides'])} decides\)", text, re.MULTILINE
        )
    others = {t["id"] for t in INST["transitions"] if t["from"] != stage}
    assert not any(re.search(rf"^- {i} ", text, re.MULTILINE) for i in others)
    assert guides.guide(stage).exits == [t["id"] for t in outs]


def test_the_index_covers_every_stage_and_every_transition():
    text = guides.guide_text("index")
    for name, spec in INST["stages"].items():
        assert f"- {name}: {spec['work']}" in text
    assert [t["id"] for t in INST["transitions"]] == [f"L{i}" for i in range(1, 14)]
    for t in INST["transitions"]:
        p = t["predicate"]
        line = next(ln for ln in text.splitlines() if ln.startswith(f"- {t['id']} "))
        assert f"{t['from']} to " in line and f"({t['decides']})" in line
        assert (p["check"] if p["kind"] == "detect" else p["says"]) in line
        assert f"{p['kind']}:" in line
    for tool in INST["stage_tools"]:
        assert f"`{tool}`" in text
    assert "scat guide <stage>" in text and "the person decides" in text
    assert guides.MODE in text
    assert guides.guide("index").exits == [t["id"] for t in INST["transitions"]]


def test_the_code_guide_drafts_the_account_first_and_hands_nodes_and_edges_back():
    text = " ".join(guides.guide_text("code").split())
    assert "Draft the account first" in text
    assert "find nodes and edges in it one at a time" in text
    assert "handed back to the coder" in text


def test_the_analyse_guide_names_the_drawing_tools_and_hands_revisits_back():
    text = " ".join(guides.guide_text("analyse").split())
    for tool in ("fingerprint", "layered", "trace"):
        assert f"`{tool}`" in text
    assert "`output` plot or both" in text
    assert "handed back to the coder" in text
    revisit = next(
        t["id"] for t in INST["transitions"] if (t["from"], t["to"]) == ("analyse", "code")
    )
    assert f"({revisit} below)" in text
    assert "Never change a narrative, node or contributor page" in text


def test_the_words_are_the_glossarys():
    for name in (*FIVE, "index"):
        text = guides.guide_text(name)
        assert not re.search(r"\blinks? (is|are) (an? )?edges?\b", text)
        assert "vertex" not in text and "vertices" not in text


# --- nothing about tools, prompts or exits is written twice -------------------------------------------------


def test_the_hand_written_files_name_no_tool_prompt_or_transition_except_by_placeholder():
    tools = {t for s in INST["stages"].values() for t in s["tools"]} | set(INST["stage_tools"])
    prompts = {p for s in INST["stages"].values() for p in s["prompts"]}
    ids = {t["id"] for t in INST["transitions"]}
    for stage in FIVE:
        raw = (ROOT / "src" / "scat_kg" / "guides" / f"{stage}.md").read_text(encoding="utf-8")
        for ticked in re.findall(r"`([^`]+)`", raw):
            assert ticked not in tools | prompts, (stage, ticked)
        assert not set(re.findall(r"\bL\d+\b", raw)) & ids, stage
        for kind, name in re.findall(r"\{(tool|prompt|exit):([^}]+)\}", raw):
            assert name in tools | prompts | set(FIVE), (stage, name)


def renamed(old: str, new: str) -> dict:
    inst = copy.deepcopy(INST)
    for spec in inst["stages"].values():
        spec["tools"] = [new if t == old else t for t in spec["tools"]]
        for o in spec["allowed_outputs"]:
            o["produced_by"] = o["produced_by"].replace(old, new)
    return inst


def test_changing_a_tool_name_in_the_instance_changes_the_text():
    for old in ("attribution", "merge", "export_edges", "copy_share"):
        inst = renamed(old, "zz_" + old)
        for stage in FIVE:
            before = guides._build(stage, INST)["text"]
            after = guides._build(stage, inst)["text"]
            if old in INST["stages"][stage]["tools"]:
                assert f"`zz_{old}`" in after and f"`zz_{old}`" not in before
                assert f"`{old}`" not in after
            else:
                assert after == before


def test_a_placeholder_for_a_tool_the_stage_lacks_is_refused():
    inst = renamed("fingerprint", "zz_fingerprint")
    with pytest.raises(KeyError):
        guides._build(
            "analyse", inst
        )  # analyse.md names `fingerprint`, which this instance does not offer


def test_changing_a_prompt_or_an_exit_in_the_instance_changes_the_text():
    inst = copy.deepcopy(INST)
    inst["stages"]["plan"]["prompts"] = ["zz-prompt"]
    for t in inst["transitions"]:
        if t["id"] == "L2":
            t["to"], t["trigger"] = "report", "zz-trigger"
    text = guides._build("plan", inst)["text"]
    assert "`zz-prompt`" in text and "L2 to report" in text and "zz-trigger" in text


# --- one text everywhere ------------------------------------------------------------------------------------


@pytest.mark.parametrize("name", [None, "index", *FIVE])
def test_cli_and_api_give_byte_identical_text(name):
    expect = guides.guide_text(name or "index")
    code, out = scat("guide", *([name] if name else []))
    assert code == 0
    assert out == expect + "\n"
    assert str(scat_kg.guide(name)) == expect
    assert scat_kg.guide(name).text == expect


def test_the_installed_command_gives_the_same_text():
    run = subprocess.run(
        [sys.executable, "-m", "scat_kg.cli", "guide", "code"],
        check=False,
        capture_output=True,
        text=True,
        cwd="/",
    )
    assert run.returncode == 0
    assert run.stdout == guides.guide_text("code") + "\n"


def test_an_unknown_stage_is_a_refusal_naming_the_five_stages(tmp_path):
    code, out = scat("guide", "nope")
    assert code == 1
    for stage in FIVE:
        assert stage in out
    assert "nope" in out
    refusal = scat_kg.guide("nope")
    assert refusal.ok is False
    code, out = scat("guide", "nope", "--json")
    assert code == 1
    doc = json.loads(out)
    assert (doc["kind"], doc["operation"], doc["ok"]) == ("operation", "guide", False)
    assert VALIDATOR.is_valid(doc)
    assert all(s in doc["refused"][0]["why"] for s in FIVE)


@pytest.mark.parametrize("name", [None, "index", *FIVE])
def test_the_json_document_validates_against_the_schema(name):
    code, out = scat("guide", *([name] if name else []), "--json")
    assert code == 0
    doc = json.loads(out)
    VALIDATOR.validate(doc)
    assert doc["schema_version"] == 3 and doc["kind"] == "guide" and doc["operation"] == "guide"
    assert doc["ok"] is True and doc["mode"] is None
    assert doc["stage"] == (name or "index")
    assert doc["text"] == guides.guide_text(name or "index")
    assert (doc["docs"] is None) == (name in (None, "index"))
    assert doc == scat_kg.guide(name).to_dict()


def test_the_guide_needs_no_vault(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)  # an empty folder
    assert scat("guide", "plan")[0] == 0
    assert scat_kg.guide("report").ok


def test_the_schema_stays_at_version_3():
    assert SCHEMA["$defs"]["SchemaVersion"] == {"const": 3}
    assert SCHEMA["title"].endswith("schema_version 3")
