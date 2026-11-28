"""The menu-bar app's build and its applet (WP22-R1, G1; D-130). The build tests run on macOS only; the applet's
text is checked everywhere."""

import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from conftest import REPO

DEPLOY = REPO / "deploy"
APPLET = (DEPLOY / "scatlab.applescript").read_text()
LAUNCHER = (DEPLOY / "scatlab.sh").read_text()
MAC_TOOLS = ("osacompile", "plutil", "codesign")


def accepted_verbs():
    """The verbs the launcher's final `case` accepts (its labels before `)`, not the usage branch)."""
    tail = LAUNCHER[LAUNCHER.rindex('case "${1:-}" in') :]
    return set(re.findall(r"^([a-z][a-z-]*)\) ", tail, re.MULTILINE))


def applet_launcher_lines():
    return [
        ln.strip() for ln in APPLET.splitlines() if "launcher" in ln and "do shell script" in ln
    ]


def test_the_launcher_accepts_the_six_verbs():
    assert accepted_verbs() == {
        "start",
        "stop",
        "status",
        "copy-key",
        "copy-address",
        "change-vault",
    }


def test_every_verb_the_applet_calls_is_one_the_launcher_accepts():
    lines = applet_launcher_lines()
    assert lines
    called = {re.search(r'launcher & " ([a-z][a-z-]*)', ln).group(1) for ln in lines}
    assert called <= accepted_verbs(), called - accepted_verbs()
    assert {
        "start",
        "stop",
        "copy-key",
        "copy-address",
        "change-vault",
    } <= called  # the menu's five buttons


def test_no_applet_line_passes_a_value_to_the_launcher():
    # after the verb only redirections and a trailing & may follow; never a variable or `quoted form of`
    verb_only = re.compile(
        r'^(set msg to )?do shell script launcher & " [a-z][a-z-]*( > /dev/null( 2>&1)?| 2>&1)?( &)?"$'
    )
    for ln in applet_launcher_lines():
        assert verb_only.match(ln), ln
    code = [
        re.sub(r"\s--\s.*$", "", ln.strip())  # a trailing comment is not code
        for ln in APPLET.splitlines()
        if not ln.strip().startswith("--")
    ]
    for ln in [
        ln for ln in code if re.search(r"\blauncher\b", ln)
    ]:  # any other use is the path's own setting
        assert ln.startswith(
            (
                "property launcher",
                "set launcher",
                "if launcher is",
                "do shell script launcher",
                "set msg to do shell script launcher",
            )
        ), ln


def test_the_build_never_targets_applications():
    build = (DEPLOY / "build-app.sh").read_text()
    assert "/Applications" not in build
    # The applet names Applications only in the move it offers a person (D-156), never under tests.
    offer = APPLET.split("on offerMove()", 1)[1].split("end offerMove", 1)[0]
    assert "/Applications" not in APPLET.replace(offer, "")
    assert 'if launcher is "" and my offerMove() then' in APPLET
    assert "out=${1:-$here/build}" in build  # the default is inside the checkout (deploy/build)


needs_mac = pytest.mark.skipif(
    sys.platform != "darwin" or not all(shutil.which(t) for t in MAC_TOOLS),
    reason="builds the macOS app: needs macOS with osacompile, plutil and codesign",
)


def tree(root):
    return {
        str(p): (p.stat().st_mtime_ns, p.stat().st_size) for p in root.rglob("*") if p.is_file()
    }


@pytest.fixture(scope="module")
def built(tmp_path_factory):
    out = tmp_path_factory.mktemp("build")
    before = {
        "deploy": tree(DEPLOY),
        "applications": sorted(p.name for p in Path("/Applications").glob("SCAT*")),
    }
    r = subprocess.run(
        ["sh", str(DEPLOY / "build-app.sh"), str(out)], check=False, capture_output=True, text=True
    )
    return out, r, before


@needs_mac
def test_the_build_gives_a_bundle_in_the_folder_it_was_given(built):
    out, r, _ = built
    assert r.returncode == 0, r.stderr
    assert [p.name for p in out.iterdir()] == ["SCATLAB.app"]
    assert (out / "SCATLAB.app" / "Contents" / "MacOS" / "applet").exists()


@needs_mac
def test_the_app_is_menu_bar_only(built):
    out, r, _ = built
    assert r.returncode == 0, r.stderr
    plist = out / "SCATLAB.app" / "Contents" / "Info.plist"
    p = subprocess.run(
        ["plutil", "-extract", "LSUIElement", "raw", "-o", "-", str(plist)],
        check=False, capture_output=True, text=True,
    )  # fmt: skip
    assert p.returncode == 0 and p.stdout.strip() == "true", p.stderr


@needs_mac
def test_the_signature_verifies_after_the_plist_edit(built):
    out, r, _ = built
    assert r.returncode == 0, r.stderr
    c = subprocess.run(
        ["codesign", "--verify", "--strict", str(out / "SCATLAB.app")],
        check=False, capture_output=True, text=True,
    )  # fmt: skip
    assert c.returncode == 0, c.stderr


@needs_mac
def test_the_build_writes_nothing_outside_its_folder(built):
    _out, r, before = built
    assert r.returncode == 0, r.stderr
    assert tree(DEPLOY) == before["deploy"]  # nothing in the checkout (no deploy/build)
    assert not (DEPLOY / "build").exists()
    assert sorted(p.name for p in Path("/Applications").glob("SCAT*")) == before["applications"]


@needs_mac
def test_the_app_is_named_scatlab_and_its_launcher_runs_from_inside_the_bundle(built, tmp_path):
    """WP37-R2: the displayed name is SCATLAB; the bundle carries the launcher and the script it sources, and the
    launcher answers from there (status changes nothing)."""
    out, r, _ = built
    assert r.returncode == 0, r.stderr
    app = out / "SCATLAB.app"
    plist = app / "Contents" / "Info.plist"
    name = subprocess.run(
        ["plutil", "-extract", "CFBundleName", "raw", "-o", "-", str(plist)],
        check=False, capture_output=True, text=True,
    )  # fmt: skip
    assert name.stdout.strip() == "SCATLAB", name.stderr
    res = app / "Contents" / "Resources"
    assert (res / "scatlab.sh").exists() and (res / "retire-old.sh").exists()
    s = subprocess.run(
        ["sh", str(res / "scatlab.sh"), "status"],
        check=False, capture_output=True, text=True, env={"PATH": "/usr/bin:/bin", "HOME": str(tmp_path)},
    )  # fmt: skip
    assert s.returncode == 1 and s.stdout.strip() == "SCATLAB is not running.", s.stderr


@needs_mac
def test_the_bundled_context_has_every_file_the_dockerfile_copies(built):
    """The app builds its image from its own copy of the source: every `COPY` source must be in that copy."""
    import re

    out, r, _ = built
    assert r.returncode == 0, r.stderr
    ctx = out / "SCATLAB.app" / "Contents" / "Resources" / "context"
    dockerfile = (ctx / "deploy" / "Dockerfile").read_text(encoding="utf-8")
    sources = re.findall(r"^COPY\s+(\S+)\s+\S+", dockerfile, re.MULTILINE)
    assert sources, "no COPY line read"
    missing = [s for s in sources if not (ctx / s).exists()]
    assert not missing, missing
