"""WP11-U5: the shared fix builders give the phrases the old text helpers gave, and the data a tool can run."""

import pytest

from scat_kg.checks import fixes, text
from scat_kg.cli import _parser
from scat_kg.fix import Command, Edit

NAMES = ["x", "safe-handling", "a-b-c"]


@pytest.mark.parametrize("name", NAMES)
@pytest.mark.parametrize("status", ["stub", "draft", "done"])
def test_set_status_phrase_equals_the_old_helper(name, status):
    assert fixes.phrase(fixes.set_status(name, status)) == text.set_status_cmd(name, status)


@pytest.mark.parametrize("name", NAMES)
def test_set_status_defaults_to_draft(name):
    assert fixes.phrase(fixes.set_status(name)) == text.set_status_cmd(name)


@pytest.mark.parametrize("name", NAMES + ["<coded-page-name>"])
@pytest.mark.parametrize("key", ["concern", "stakeholder-group", "raw"])
def test_stub_phrase_equals_the_old_helper(name, key):
    assert fixes.phrase(fixes.stub(name, key)) == text.stub_cmd(name, key)


def test_the_commands_carry_argv_and_repl():
    assert fixes.set_status("x", "done") == Command(
        ("set-status", "x", "done"), 'scat_kg.set_status("x", "done")'
    )
    assert fixes.stub("x", "concern").argv == ("stub", "x", "--type", "concern")
    assert fixes.stub_pair("heldby", "a", "b").argv == ("stub-pair", "heldby", "a", "b")
    assert fixes.stub_pair("heldby", "a", "b").repl == 'scat_kg.stub_pair("heldby", "a", "b")'
    assert fixes.stub_links().argv == ("stub-links",)
    assert fixes.stub_links().repl == "scat_kg.stub_links()"
    assert fixes.stub_links("p").argv == ("stub-links", "p")
    assert fixes.stub_links("p").repl == 'scat_kg.stub_links("p")'
    assert fixes.index().argv == ("index",)


def test_index_and_placeholder_phrases():
    assert fixes.phrase(fixes.index()) == "`scat index` (REPL: `scat_kg.index()`)"
    slot = "<endpoint-a>"
    assert (
        fixes.phrase(fixes.stub_pair("<relation>", slot, "<endpoint-b>"))
        == "`scat stub-pair <relation> <endpoint-a> <endpoint-b>` "
        '(REPL: `scat_kg.stub_pair("<relation>", "<endpoint-a>", "<endpoint-b>")`)'
    )


def test_run_option_kind_follows_the_slot():
    exact = fixes.run_option(fixes.set_status("x"), suffix=" now")
    assert (exact.kind, exact.text) == ("exact", f"run {text.set_status_cmd('x')} now")
    slot = fixes.run_option(fixes.stub("<n>", "concern", slot="<n>"))
    assert slot.kind == "slot" and slot.command.author_slot == "<n>"


def test_edit_constructors_give_the_five_actions():
    assert fixes.set_field("a.md", "f", "v") == Edit("set-field", "a.md", field="f", value="v")
    assert fixes.set_field("a.md", "f", "<v>", author_slot="<v>").author_slot == "<v>"
    assert fixes.delete_field("a.md", "f").to_dict() == {
        "action": "delete-field",
        "file": "a.md",
        "field": "f",
    }
    assert fixes.replace_text("a.md", 3, "x", "y", column=2).to_dict() == {
        "action": "replace-text",
        "file": "a.md",
        "line": 3,
        "column": 2,
        "find": "x",
        "replace": "y",
    }
    assert fixes.rename_file("a.md", "b.md").to_dict() == {
        "action": "rename-file",
        "file": "a.md",
        "to": "b.md",
    }
    assert fixes.delete_file("a.md").to_dict() == {"action": "delete-file", "file": "a.md"}


def test_single_takes_the_option_kind_and_alternatives_are_options():
    a = fixes.option("exact", "do a", fixes.delete_file("a.md"))
    b = fixes.option("manual", "do b")
    assert fixes.single(a).kind == "exact"
    assert fixes.alternatives([a, b]).kind == "options"
    assert fixes.alternatives([a, b]).render() == text.choose(["do a", "do b"])
    assert fixes.single(a).render() == text.one("do a")


def test_inline_reads_on_one_line():
    opts = [fixes.option("exact", f"`s: {v}`") for v in "ab"]
    f = fixes.inline(opts)
    assert f.render() == "Fix, choose one: `s: a`, `s: b`"
    assert [o["text"] for o in f.to_dict()["options"]] == ["`s: a`", "`s: b`"]
    assert len(f.to_dict()["options"]) == 2


@pytest.mark.parametrize(
    "cmd",
    [
        fixes.set_status("x", "done"),
        fixes.stub("x", "concern"),
        fixes.stub_pair("heldby", "a", "b"),
        fixes.stub_links(),
        fixes.stub_links("p"),
        fixes.index(),
    ],
)
def test_every_builder_argv_is_accepted_by_scat(cmd):
    assert _parser().parse_args(list(cmd.argv)).command == cmd.argv[0]
