import pytest

from scat_kg.vault import read_vault

TEMPLATE = '---\ntype: concern\nstatus: draft\ntitle: ""\n---\n'
REAL = '---\ntype: concern\nstatus: draft\ntitle: "Real"\ndescription: "A real one."\n---\n'


def cap_problem(root):
    return read_vault(root).config.problem


def test_templates_folder_is_not_read(make_vault):
    root = make_vault(
        {
            "scat.toml": "attribution = 'disallowed'\nstakeholder_group_cap = 3\n",
            "templates/concern.md": TEMPLATE,
            "templates/deep/more.md": TEMPLATE,
            "templates/note.md": "no frontmatter\n",
            ".obsidian/x.md": TEMPLATE,
            "concern/real.md": REAL,
        }
    )
    v = read_vault(root)
    assert [p.path for p in v.pages] == ["concern/real.md"]
    assert v.non_pages == ()
    assert "concern" not in v.by_name


def test_custom_templates_folder(make_vault):
    root = make_vault(
        {
            "scat.toml": 'attribution = "disallowed"\nstakeholder_group_cap = 3\ntemplates_folder = "skel"\n',
            "skel/concern.md": TEMPLATE,
            "templates/concern.md": REAL,
        }
    )
    v = read_vault(root)
    assert [p.path for p in v.pages] == ["templates/concern.md"]


@pytest.mark.parametrize("bad", ["3", "true", '""', '"/"', "[]"])
def test_bad_value_falls_back_to_default(make_vault, bad):
    root = make_vault(
        {
            "scat.toml": f"attribution = 'disallowed'\nstakeholder_group_cap = 3\ntemplates_folder = {bad}\n",
            "templates/concern.md": TEMPLATE,
            "concern/real.md": REAL,
        }
    )
    v = read_vault(root)
    assert v.config.templates_folder == "templates"
    assert [p.path for p in v.pages] == ["concern/real.md"]


def test_extra_key_does_not_trigger_cap_config(make_vault):
    root = make_vault(
        {
            "scat.toml": 'attribution = "disallowed"\nstakeholder_group_cap = 3\ntemplates_folder = "skel"\n'
        }
    )
    v = read_vault(root)
    assert v.config.problem is None and v.config.cap == 3
    assert cap_problem(root) is None


def test_bad_cap_still_reported_with_templates_key(make_vault):
    root = make_vault(
        {
            "scat.toml": 'attribution = "disallowed"\nstakeholder_group_cap = "x"\ntemplates_folder = "skel"\n'
        }
    )
    assert cap_problem(root) == "bad-value"
