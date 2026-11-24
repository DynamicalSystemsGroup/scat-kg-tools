import pytest
from opsutil import fm

from scat_kg.ops import stub, stub_links, stub_pair
from scat_kg.ops.names import derive_name, name_problem, stem_of
from scat_kg.vault import read_vault

CAP3 = {"scat.toml": "stakeholder_group_cap = 3\n"}


def group(name, title):
    return {f"stakeholder-group/{name}.md": fm("stakeholder-group", title)}


# names (section 2)


def test_name_rules():
    assert [name_problem(n) for n in ("a", "a-b", "x" * 64)] == [None] * 3
    for bad in (
        "",
        "A",
        "a--b",
        "-a",
        "a-",
        "a b",
        "a.b",
        "é",
        "x" * 65,
        "con",
        "com3",
        "lpt9",
        "concerns",
    ):
        assert name_problem(bad), bad
    assert stem_of("Safe handling of tools") == "safe-handling-of-tools"
    assert stem_of("École Ångström ß ø") == "ecole-angstrom"
    assert stem_of("日本語") == ""
    assert stem_of("a" * 63 + " b") == "a" * 63
    assert derive_name("Con", set()) == "con-2"
    assert derive_name("Concerns", set()) == "concerns-2"
    assert derive_name("Same", {"same", "same-2"}) == "same-3"
    long = "a" * 64
    assert derive_name(long, {long}) == "a" * 62 + "-2"
    assert derive_name("日本語", set()) is None


# stub


def test_stub_creates_exactly_the_skeleton_in_the_types_folder(make_vault, snap, diff):
    root = make_vault({"README.md": "x\n", **CAP3})
    before = snap(root)
    r = stub("safety-briefing", "affordance", root=root)
    assert r.ok and r.created == ("affordance/safety-briefing.md",)
    assert (root / "affordance/safety-briefing.md").read_bytes() == (
        b'---\ntype: affordance\nstatus: stub\ntitle: "Safety briefing"\n---\n'
    )
    assert set(diff(before, snap(root))) == {"affordance", "affordance/safety-briefing.md"}


def test_stub_twice_changes_nothing_the_second_time(make_vault, snap):
    root = make_vault(CAP3)
    stub("a", "concern", root=root)
    before = snap(root)
    r = stub("a", "concern", root=root)
    assert not r.ok and "already" in str(r) and not r.created
    assert snap(root) == before


@pytest.mark.parametrize(
    "name, type_, word",
    [
        ("Bad Name", "concern", "a-z"),
        ("con", "concern", "reserved"),
        ("concerns", "concern", "reserved"),
        ("x" * 65, "concern", "64"),
        ("a", "heldby", "stub-pair"),
        ("a", "class", "scat index"),
        ("a", "nonsense", "use one of"),
        ("taken", "concern", "already"),
        ("TAKEN", "concern", "a-z"),  # not a slug: the fix offers the derived name
        ("notes", "concern", "already"),  # a Markdown file that is not a page still blocks the name
    ],
)
def test_stub_refuses_and_creates_nothing(make_vault, snap, name, type_, word):
    root = make_vault(
        {"concern/taken.md": fm("concern", "T"), "docs/notes.md": "# no frontmatter\n"}
    )
    before = snap(root)
    r = stub(name, type_, root=root)
    assert not r.ok and word in str(r) and "Fix:" in str(r)
    assert snap(root) == before


def test_stub_refuses_a_name_that_differs_only_by_case_from_a_page(make_vault, snap):
    root = make_vault({"concern/Quick.md": fm("concern", "Q")})
    assert "already" in str(stub("quick", "concern", root=root))


def test_stub_never_overwrites_an_existing_page(make_vault):
    root = make_vault({"concern/a.md": fm("concern", "Mine")})
    stub("a", "concern", root=root)
    assert (root / "concern/a.md").read_text() == fm("concern", "Mine")


@pytest.mark.parametrize("slug", ["stakeholder-group", "concern", "affordance", "technology",
                                  "scenario-raw", "scenario-coded", "architecture-raw", "architecture-coded"])  # fmt: skip
def test_stub_every_accepted_type(make_vault, slug):
    root = make_vault(CAP3)
    assert stub("thing", slug, root=root).created == (f"{slug}/thing.md",)
    assert read_vault(root).by_name["thing"][0].type == slug


def test_stub_refuses_a_group_over_the_cap_and_creates_nothing(make_vault, snap):
    root = make_vault({**CAP3, **group("a", "A"), **group("b", "B"), **group("c", "C")})
    before = snap(root)
    r = stub("d", "stakeholder-group", root=root)
    assert (
        not r.ok
        and "cap of 3" in str(r)
        and "SCAT-CAP" in str(r)
        and "stakeholder_group_cap = 4" in str(r)
    )
    assert snap(root) == before
    assert stub("d", "concern", root=root).ok  # only groups are capped


def test_stub_group_under_the_cap_and_with_unusable_cap(make_vault):
    root = make_vault({**CAP3, **group("a", "A")})
    assert stub("b", "stakeholder-group", root=root).ok
    nocap = root.parent / "nocap"
    nocap.mkdir()
    r = stub("b", "stakeholder-group", root=nocap)  # no scat.toml: the cap is unknown
    assert not r.ok and "stakeholder_group_cap" in str(r) and "missing" in str(r)
    assert not (nocap / "stakeholder-group").exists()


def test_stub_raw_derives_coded_from_coded_pages_naming_it(make_vault):
    root = make_vault(
        {
            "scenario-coded/c2.md": fm("scenario-coded", "C2", extra='raw:\n  - "[[story]]"\n'),
            "scenario-coded/c1.md": fm("scenario-coded", "C1", extra='raw:\n  - "[[other]]"\n  - "[[story]]"\n'),
            "architecture-coded/ac.md": fm("architecture-coded", "AC", extra='raw:\n  - "[[story]]"\n'),
        }
    )  # fmt: skip
    stub("story", "scenario-raw", root=root)
    assert (root / "scenario-raw/story.md").read_text() == (
        '---\ntype: scenario-raw\nstatus: stub\ntitle: "Story"\ntimeframe: # past | future | mixed\ncoded:\n  - "[[c1]]"\n  - "[[c2]]"\n---\n'
    )


@pytest.mark.parametrize("slug", ["scenario-raw", "architecture-raw"])
def test_stub_of_a_raw_page_has_the_timeframe_line_after_the_title(make_vault, slug):
    root = make_vault({**CAP3})
    stub("story", slug, root=root)
    assert (root / f"{slug}/story.md").read_text() == (
        f'---\ntype: {slug}\nstatus: stub\ntitle: "Story"\ntimeframe: # past | future | mixed\n---\n'
    )


@pytest.mark.parametrize(
    "slug",
    [
        "scenario-coded",
        "architecture-coded",
        "concern",
        "affordance",
        "technology",
        "stakeholder-group",
    ],
)
def test_stub_of_any_other_page_has_no_timeframe_line(make_vault, slug):
    root = make_vault({**CAP3})
    stub("story", slug, root=root)
    assert "timeframe" not in (root / f"{slug}/story.md").read_text()


def test_stub_coded_derives_raw_from_raw_pages_naming_it(make_vault):
    root = make_vault(
        {"architecture-raw/pitch.md": fm("architecture-raw", "P", extra='coded:\n  - "[[pc]]"\n')}
    )
    stub("pc", "architecture-coded", root=root)
    assert (root / "architecture-coded/pc.md").read_text().endswith('raw:\n  - "[[pitch]]"\n---\n')
    stub("lonely", "architecture-coded", root=root)  # nothing names it: nothing pre-filled
    assert (root / "architecture-coded/lonely.md").read_text() == (
        '---\ntype: architecture-coded\nstatus: stub\ntitle: "Lonely"\n---\n'
    )


# stub_links


@pytest.fixture
def coded(make_vault):
    return make_vault(
        {
            **CAP3,
            "scenario-coded/sc.md": fm(
                "scenario-coded", "SC", "done",
                'raw:\n  - "[[told]]"\ngroups:\n  - "[[volunteers]]"\nconcerns:\n  - "[[safety]]"\n'
                'affordances:\n  - "[[briefing]]"\n  - "[[Bad Name]]"\n  - "[[here]]"\n',
                "body [[bodyonly]]\n",
            ),
            "concern/here.md": fm("concern", "Here"),
            "scenario-raw/other.md": fm("scenario-raw", "O"),
        }
    )  # fmt: skip


def test_stub_links_creates_each_entailed_page_by_the_field_table(coded, snap, diff):
    before = snap(coded)
    r = stub_links(root=coded)
    assert r.ok and set(r.created) == {
        "scenario-raw/told.md", "stakeholder-group/volunteers.md",
        "concern/safety.md", "affordance/briefing.md",
    }  # fmt: skip
    assert set(diff(before, snap(coded))) - {
        "scenario-raw",
        "stakeholder-group",
        "concern",
        "affordance",
    } == {f"{p}" for p in r.created}
    assert (
        coded / "concern/safety.md"
    ).read_text() == '---\ntype: concern\nstatus: stub\ntitle: "Safety"\n---\n'
    text = str(r)
    assert "[[Bad Name]]" in text and "not a legal name" in text  # entails nothing, says why
    assert "bodyonly" not in text  # a body link entails nothing without a type
    assert not (coded / "concern/bodyonly.md").exists()


def test_stub_links_twice_changes_nothing_the_second_time(coded, snap):
    stub_links(root=coded)
    before = snap(coded)
    r = stub_links(root=coded)
    assert not r.created and not r.changed
    assert snap(coded) == before


def test_stub_links_for_one_page_only(coded):
    (coded / "concern/here.md").write_text(
        fm("concern", "Here", extra='conflicts:\n  - "[[rival]]"\n')
    )
    r = stub_links("here", root=coded)
    assert r.created == ("concern/rival.md",)


def test_stub_links_wrong_type_and_unlisted_field_entail_nothing(make_vault):
    root = make_vault(
        {
            "concern/c.md": fm(
                "concern", "C", extra='conflicts:\n  - "[[tech]]"\ngroup: "[[ghost]]"\n'
            ),
            "technology/tech.md": fm("technology", "Tech"),
        }
    )
    r = stub_links(root=root)
    assert not r.created and not (root / "stakeholder-group/ghost.md").exists()


def test_stub_links_target_named_as_two_types_is_refused_alone(make_vault):
    root = make_vault(
        {
            **CAP3,
            "scenario-coded/s.md": fm("scenario-coded", "S", extra='concerns:\n  - "[[x]]"\naffordances:\n  - "[[x]]"\ngroups:\n  - "[[ok]]"\n'),
        }
    )  # fmt: skip
    r = stub_links(root=root)
    assert not r.ok and "different types" in str(r) and r.created == ("stakeholder-group/ok.md",)
    assert not (root / "concern/x.md").exists()


def test_stub_links_over_the_cap_creates_nothing_from_the_call(make_vault, snap):
    root = make_vault(
        {
            "scat.toml": "stakeholder_group_cap = 2\n",
            **group("g1", "G1"),
            "scenario-coded/s.md": fm("scenario-coded", "S", extra='groups:\n  - "[[g1]]"\n  - "[[g2]]"\n  - "[[g3]]"\nconcerns:\n  - "[[c]]"\n'),
        }
    )  # fmt: skip
    before = snap(root)
    r = stub_links(root=root)
    assert not r.ok and "SCAT-CAP" in str(r) and not r.created
    assert snap(root) == before  # not even the concern stub


def test_stub_links_derives_the_opposite_link_on_raw_pages(make_vault):
    root = make_vault(
        {"scenario-coded/c.md": fm("scenario-coded", "C", extra='raw:\n  - "[[story]]"\n')}
    )
    stub_links(root=root)
    assert '  - "[[c]]"' in (root / "scenario-raw/story.md").read_text()


# stub_pair


def pair_vault(make_vault, extra=None):
    return make_vault(
        {
            **CAP3,
            **group("volunteer-staff", "Volunteer staff"),
            "concern/safe-handling-of-tools.md": fm("concern", "Safe handling of tools"),
            **(extra or {}),
        }
    )


def test_stub_pair_creates_exactly_the_section_5_page(make_vault, snap, diff):
    root = pair_vault(make_vault)
    before = snap(root)
    r = stub_pair("heldby", "volunteer-staff", "safe-handling-of-tools", root=root)
    name = "volunteer-staff-holds-safe-handling-of-tools"
    assert r.ok and r.created == (f"heldby/{name}.md",)
    assert (root / f"heldby/{name}.md").read_bytes() == (
        b'---\ntype: heldby\nstatus: stub\ntitle: "Volunteer staff holds Safe handling of tools"\n'
        b'group: "[[volunteer-staff]]"\nconcern: "[[safe-handling-of-tools]]"\n---\n'
    )
    assert set(diff(before, snap(root))) == {
        "heldby",
        f"heldby/{name}.md",
    }  # endpoints existed: nothing else


@pytest.mark.parametrize(
    "relation, a, b, name, title, tail",
    [
        ("addresses", "safe-handling-of-tools", "safety-briefing", "safe-handling-of-tools-addresses-safety-briefing",
         "Safe handling of tools addresses Safety briefing", 'concern: "[[safe-handling-of-tools]]"\naffordance: "[[safety-briefing]]"'),
        ("attributes", "safety-briefing", "booking-app", "safety-briefing-attributed-to-booking-app",
         "Safety briefing attributed to Booking app", 'affordance: "[[safety-briefing]]"\ntechnology: "[[booking-app]]"'),
    ],
)  # fmt: skip
def test_stub_pair_addresses_and_attributes(make_vault, relation, a, b, name, title, tail):
    root = pair_vault(
        make_vault,
        {"affordance/safety-briefing.md": fm("affordance", "Safety briefing"), "technology/booking-app.md": fm("technology", "Booking app")},
    )  # fmt: skip
    r = stub_pair(relation, a, b, root=root)
    assert r.ok, str(r)
    assert r.created == (f"{relation}/{name}.md",)
    assert (root / f"{relation}/{name}.md").read_text() == (
        f'---\ntype: {relation}\nstatus: stub\ntitle: "{title}"\n{tail}\n---\n'
    )
    page = read_vault(root).by_name[name][0]
    assert page.type == relation and page.model_error is None


def test_stub_pair_endpoint_order_is_the_tboxs(make_vault, snap):
    root = pair_vault(make_vault)
    before = snap(root)
    r = stub_pair("heldby", "safe-handling-of-tools", "volunteer-staff", root=root)  # swapped
    assert not r.ok and "is a `concern` page, and `group` needs a `stakeholder-group`" in str(r)
    assert not r.created and snap(root) == before


def test_stub_pair_stubs_missing_endpoints_by_type_and_titles_them(make_vault):
    root = make_vault(CAP3)
    r = stub_pair("heldby", "new-group", "new-concern", root=root)
    assert set(r.created) == {
        "stakeholder-group/new-group.md", "concern/new-concern.md",
        "heldby/new-group-holds-new-concern.md",
    }  # fmt: skip
    assert (
        'title: "New group holds New concern"'
        in (root / "heldby/new-group-holds-new-concern.md").read_text()
    )
    assert (
        root / "concern/new-concern.md"
    ).read_text() == '---\ntype: concern\nstatus: stub\ntitle: "New concern"\n---\n'


def test_stub_pair_uses_an_existing_endpoints_own_title(make_vault):
    root = pair_vault(make_vault)
    (root / "stakeholder-group/volunteer-staff.md").write_text(
        fm("stakeholder-group", 'Vol \\"staff\\"')
    )
    stub_pair("heldby", "volunteer-staff", "safe-handling-of-tools", root=root)
    page = read_vault(root).of_type("heldby")[0]
    assert page.fields["title"] == 'Vol "staff" holds Safe handling of tools'
    assert page.name == "vol-staff-holds-safe-handling-of-tools"


def test_stub_pair_twice_changes_nothing_the_second_time(make_vault, snap):
    root = make_vault(CAP3)
    stub_pair("heldby", "g", "c", root=root)
    before = snap(root)
    r = stub_pair("heldby", "g", "c", root=root)
    assert r.ok and not r.created and r.unchanged == ("heldby/g-holds-c.md",)
    assert snap(root) == before


def test_stub_pair_creates_nothing_for_an_existing_pair_under_any_name(make_vault, snap):
    root = pair_vault(
        make_vault,
        {"heldby/whatever-name.md": fm("heldby", "My own", extra='group: "[[volunteer-staff]]"\nconcern: "[[safe-handling-of-tools]]"\n')},
    )  # fmt: skip
    before = snap(root)
    r = stub_pair("heldby", "volunteer-staff", "safe-handling-of-tools", root=root)
    assert r.ok and not r.created and r.unchanged == ("heldby/whatever-name.md",)
    assert "already states this pair" in str(r)
    assert snap(root) == before


def test_stub_pair_other_pair_with_one_shared_endpoint_is_a_new_page(make_vault):
    root = pair_vault(
        make_vault,
        {"heldby/x.md": fm("heldby", "X", extra='group: "[[volunteer-staff]]"\nconcern: "[[other]]"\n'), **group("borrowers", "Borrowers")},
    )  # fmt: skip
    r = stub_pair("heldby", "borrowers", "safe-handling-of-tools", root=root)
    assert r.created == ("heldby/borrowers-holds-safe-handling-of-tools.md",)


def test_stub_pair_refuses_a_group_over_the_cap_and_creates_nothing(make_vault, snap):
    root = make_vault({**CAP3, **group("a", "A"), **group("b", "B"), **group("c", "C")})
    before = snap(root)
    r = stub_pair(
        "heldby", "d", "some-concern", root=root
    )  # d would be a 4th group; the concern stub too is withheld
    assert not r.ok and "cap of 3" in str(r) and not r.created
    assert snap(root) == before
    assert stub_pair("heldby", "a", "some-concern", root=root).ok  # an existing group is fine


def test_stub_pair_refusals_write_nothing(make_vault, snap):
    root = pair_vault(
        make_vault, {"affordance/af.md": fm("affordance", "Af"), "notes/clash.md": "# x\n"}
    )
    before = snap(root)
    cases = [
        (("nonsense", "a", "b"), "use one of: addresses, attributes, heldby"),
        (("heldby", "a", "a"), "same name"),
        (("heldby", "af", "safe-handling-of-tools"), "is a `affordance` page"),
        (("heldby", "Bad Name", "safe-handling-of-tools"), "not a legal name"),
        (("heldby", "clash", "safe-handling-of-tools"), "notes/clash.md"),
    ]
    for args, word in cases:
        r = stub_pair(*args, root=root)
        assert not r.ok and word in str(r) and "Fix:" in str(r), (args, str(r))
    assert snap(root) == before


def test_stub_pair_endpoint_without_a_title_is_refused_with_the_line_to_add(make_vault):
    root = make_vault({"concern/c.md": "---\ntype: concern\nstatus: draft\n---\n", **CAP3})
    r = stub_pair("heldby", "newg", "c", root=root)
    assert not r.ok and 'title: "C"' in str(r) and not (root / "stakeholder-group/newg.md").exists()


def test_stub_pair_name_clash_gets_a_numeric_suffix(make_vault):
    root = pair_vault(
        make_vault,
        {"concern/volunteer-staff-holds-safe-handling-of-tools.md": fm("concern", "Taken")},
    )
    r = stub_pair("heldby", "volunteer-staff", "safe-handling-of-tools", root=root)
    assert r.created == ("heldby/volunteer-staff-holds-safe-handling-of-tools-2.md",)


def test_stub_pair_never_creates_relation_pages_for_other_pairs(make_vault, snap, diff):
    root = pair_vault(make_vault, {"scenario-coded/s.md": fm("scenario-coded", "S", extra='groups:\n  - "[[volunteer-staff]]"\nconcerns:\n  - "[[safe-handling-of-tools]]"\n')})  # fmt: skip
    r = stub_links(root=root)  # entails no relation page (D-031)
    assert not r.created
    assert not (root / "heldby").exists()
