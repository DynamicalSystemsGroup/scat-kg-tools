"""The docs test, tested on synthetic pages."""

import pytest
from docs_runner import (
    copy_template,
    fenced_blocks,
    has_runnable,
    live_help,
    reference_problems,
    run_page,
    scat_argv,
)

from scat_tools.cli import _parser

PAGE = """# T

```python
x = 1
```

=== "Python"

    ```python
    y = x + 1
    ```

=== "CLI"

    ```bash
    uv run scat status
    ```

```text
raise SystemExit("never run")
uv run nonsense
```

```yaml
a: b
```
"""


def test_extracts_plain_and_tab_indented_fences():
    got = [(b.tag, b.text) for b in fenced_blocks(PAGE)]
    assert got[0] == ("python", "x = 1\n")
    assert got[1] == ("python", "y = x + 1\n")  # indent removed
    assert got[2] == ("bash", "uv run scat status\n")
    assert [t for t, _ in got] == ["python", "python", "bash", "text", "yaml"]


def test_python_blocks_share_one_session_and_text_is_never_run(tmp_path):
    (tmp_path / "scat.toml").write_text("")
    run_page("p.md", PAGE.replace("uv run scat status", "uv run scat --help"), tmp_path)


def test_failing_python_block_names_page_and_block(tmp_path):
    md = "```python\nok = 1\n```\n\n```python\nraise ValueError('boom')\n```\n"
    with pytest.raises(AssertionError) as e:
        run_page("guide.md", md, tmp_path)
    msg = str(e.value)
    assert "guide.md block 2" in msg and "raise ValueError('boom')" in msg and "boom" in msg


def test_bash_line_that_is_not_scat_fails(tmp_path):
    with pytest.raises(AssertionError, match="git clone"):
        run_page("g.md", "```bash\ngit clone x\n```\n", tmp_path)
    with pytest.raises(AssertionError):
        scat_argv("echo hi")


def test_failing_scat_command_fails(tmp_path):
    with pytest.raises(AssertionError, match="exit"):
        run_page("g.md", "```bash\nuv run scat set-status nope done\n```\n", tmp_path)


def test_bare_scat_is_mapped():
    assert scat_argv("scat check --root x")[-3:] == ["check", "--root", "x"]
    assert scat_argv("uv run scat check")[-1] == "check"


def test_has_runnable():
    assert has_runnable(PAGE)
    assert not has_runnable("```text\nx\n```\n```yaml\ny\n```\n")


def reference(live, **change):
    texts = {**live, **change}
    return "# CLI\n\n" + "".join(
        f"## {n}\n\n```text\n{t}```\n\nWords.\n\n" for n, t in texts.items()
    )


def test_help_diff_accepts_the_live_help_and_derives_subcommands():
    live = live_help(_parser())
    assert "scat" in live and "scat check" in live and len(live) >= 8
    assert reference_problems(reference(live), live) == []


def test_help_diff_catches_a_changed_word():
    live = live_help(_parser())
    bad = reference(live, **{"scat check": live["scat check"].replace("Check", "Cheque", 1)})
    assert reference_problems(bad, live) == ["## scat check: text differs from `scat check --help`"]


def test_help_diff_catches_missing_and_extra_sections():
    live = live_help(_parser())
    ref = reference({k: v for k, v in live.items() if k != "scat stub"}, **{"scat bogus": "x\n"})
    assert sorted(reference_problems(ref, live)) == [
        "extra section: ## scat bogus",
        "missing section: ## scat stub",
    ]


def test_synthetic_page_runs_against_the_template(template, tmp_path):

    scratch = tmp_path / "vault"
    copy_template(template, scratch)
    assert (scratch / "scat.toml").exists() and not (scratch / ".git").exists()
    md = "```python\nimport scat_tools\nr = scat_tools.check()\n```\n\n```bash\nuv run scat check\nuv run scat status\n```\n"
    run_page("synthetic.md", md, scratch)


def test_python_session_starts_in_the_vault_folder(tmp_path):
    md = "```python\nimport os\nassert os.getcwd() == EXPECT\n```\n"
    # the block sees the copy as its working directory, not the caller's
    src = md.replace("EXPECT", repr(str(tmp_path.resolve())))
    run_page("cwd.md", src, tmp_path)


def test_whitespace_only_change_in_help_fails():
    live = live_help(_parser())
    for new in (
        live["scat check"].replace("  ", "   ", 1),
        live["scat check"].replace(" ", "\n", 1),
    ):
        bad = reference(live, **{"scat check": new})
        assert reference_problems(bad, live) == [
            "## scat check: text differs from `scat check --help`"
        ]


def test_unreadable_command_line_names_page_and_block(tmp_path):
    with pytest.raises(AssertionError) as e:
        run_page("g.md", "```bash\nuv run scat check \\\n```\n", tmp_path)
    assert "g.md block 1" in str(e.value)
