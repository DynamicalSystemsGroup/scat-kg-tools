"""WP36-R1, R2: the pros-and-cons page says what each path's model can see; every record it cites exists."""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
PROS = (ROOT / "docs" / "path-pros-and-cons.md").read_text(encoding="utf-8")
ANALYSIS = (ROOT / "docs" / "analysis.md").read_text(encoding="utf-8")
PATHS = ["By hand", "An AI chatbot", "An AI chatbot, leave no trace", "An AI IDE", "A local LLM"]


def _sections(text: str) -> dict[str, str]:
    parts = re.split(r"^## (.+)$", text, flags=re.MULTILINE)
    return dict(zip(parts[1::2], parts[2::2], strict=True))


def _drawings_line(body: str) -> str:
    m = re.search(r"^- \*\*Drawings:\*\*(.*?)(?=^- \*\*|\Z)", body, re.DOTALL | re.MULTILINE)
    assert m, "no Drawings line"
    return " ".join(m.group(1).split())


@pytest.mark.parametrize("path", PATHS)
def test_r1_every_path_has_a_drawings_line(path):
    assert _drawings_line(_sections(PROS)[path])


@pytest.mark.parametrize("path", ["An AI chatbot", "An AI chatbot, leave no trace"])
def test_r1_a_client_claim_cites_a_record(path):
    line = _drawings_line(_sections(PROS)[path])
    assert re.search(r"acceptance/walkthroughs/[\w-]+\.md", line)


@pytest.mark.parametrize("path", ["An AI IDE", "A local LLM"])
def test_r1_ide_and_local_llm_state_our_side_and_not_untried(path):
    line = _drawings_line(_sections(PROS)[path])
    assert "not tried" not in line.lower() and "untested" not in line.lower()
    assert "image content" in line or "PNG" in line
    assert "table" in line and "svg" in line.lower()


def test_r1_cited_records_exist():
    cited = set(re.findall(r"acceptance/walkthroughs/[\w-]+\.md", PROS))
    assert cited
    for c in cited:
        assert (ROOT / c).is_file(), c
    assert (ROOT / "acceptance/walkthroughs/visual-capabilities.md").is_file()


def test_r2_analysis_names_output_values_and_formats():
    body = ANALYSIS.split("### When the assistant cannot see the drawing")[1].split(
        "## Where next"
    )[0]
    for word in ("`table`", "`both`", "PNG", "SVG", "`output`", "`format`"):
        assert word in body
    assert "plot" in ANALYSIS  # the third `output` value is named where `output` is introduced


def test_r2_analysis_agrees_with_the_server_options():
    pytest.importorskip("mcp")
    from scat_kg.mcp_server.server import FORMATS, OUTPUTS

    for value in (*OUTPUTS, *FORMATS):
        assert f"`{value}`" in ANALYSIS or value in ANALYSIS.lower()
    para = next(p for p in ANALYSIS.split("\n\n") if "each take `output`" in p)
    for value in OUTPUTS:
        assert f"`{value}`" in para
