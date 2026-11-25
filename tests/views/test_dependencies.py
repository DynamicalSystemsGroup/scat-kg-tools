"""R4: the drawing library is an optional extra; the core runtime dependencies are exactly three."""

import re
import subprocess
import tomllib
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORE = {"pydantic", "PyYAML", "rdflib"}


def test_core_dependencies_are_exactly_pydantic_pyyaml_rdflib():
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    assert set(project["dependencies"]) == CORE and len(project["dependencies"]) == 3
    assert [re.split(r"[<>=!~ ]", d)[0] for d in project["optional-dependencies"]["draw"]] == [
        "matplotlib"
    ]


def test_the_built_wheel_requires_only_the_three_and_offers_the_draw_extra(tmp_path):
    subprocess.run(
        ["uv", "build", "--wheel", "--out-dir", str(tmp_path)],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    (wheel,) = tmp_path.glob("*.whl")
    with zipfile.ZipFile(wheel) as z:
        meta = z.read(next(n for n in z.namelist() if n.endswith(".dist-info/METADATA"))).decode()
    header = meta.split("\n\n", 1)[0]
    requires = [
        ln.split(": ", 1)[1] for ln in header.splitlines() if ln.startswith("Requires-Dist")
    ]
    plain = {re.split(r"[<>=!~ ;\[]", r)[0] for r in requires if "extra ==" not in r}
    assert {n.lower() for n in plain} == {n.lower() for n in CORE}
    assert "Provides-Extra: draw" in header.splitlines()
    assert any("matplotlib" in r and re.search(r"extra == ['\"]draw['\"]", r) for r in requires)
