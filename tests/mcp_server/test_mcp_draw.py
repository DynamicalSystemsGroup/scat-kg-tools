"""WP28-R1, R2: the draw tools return the pictures `scat_kg.draw` makes, and the views' refusals as documents."""

import base64
import json

import pytest
from mcputil import changed, copy_vault, serve, snapshot, with_session

from scat_kg import draw
from scat_kg.ops.result import stamp

PNG = b"\x89PNG\r\n\x1a\n"
NARRATIVE = "saturday-at-the-lending-desk"
OTHER = "funders-meeting"
NODE = "self-checkout"

BAD_ROW = "| farmers | holds | [[quick-checkout]] | |"  # the `from` end is plain text, not a link
BAD = (
    '---\ntype: narrative\nstatus: done\ntitle: "Bad"\nkind: scenario\n---\n'
    "The [[quick-checkout]] failed.\n\n## Edges told\n\n| from | type | to | note |\n|---|---|---|---|\n"
    f"{BAD_ROW}\n"
)
UNCODED = '---\ntype: narrative\nstatus: draft\ntitle: "Uncoded"\n---\nNo node is linked here.\n'


@pytest.fixture(scope="module")
def vaults(tmp_path_factory):
    """The server's vault and an identical one the local draw calls run on."""
    base = tmp_path_factory.mktemp("draw")
    return copy_vault(base / "served"), copy_vault(base / "own"), base / "server.log"


@pytest.fixture(scope="module")
def url(vaults):
    served, _, log = vaults
    with serve(served, log=log) as u:
        yield u


@pytest.fixture(scope="module")
def flawed(tmp_path_factory):
    """A vault with an uncoded narrative (excluded) and a `done` narrative with an error, served and local."""
    base = tmp_path_factory.mktemp("flawed")
    roots = []
    for name in ("served", "own"):
        root = copy_vault(base / name)
        (root / "narrative" / "uncoded.md").write_text(UNCODED, encoding="utf-8")
        (root / "narrative" / "bad.md").write_text(BAD, encoding="utf-8")
        roots.append(root)
    with serve(roots[0], log=base / "server.log") as u:
        yield u, roots[0], roots[1]


def tool(url, name, args):
    async def go(s):
        res = await s.call_tool(name, args)
        assert not res.isError, res.content
        return res.content

    return with_session(url, go)


def png_of(content) -> bytes:
    assert len(content) == 1 and content[0].type == "image"
    assert content[0].mimeType == "image/png"
    data = base64.b64decode(content[0].data)
    assert data.startswith(PNG)
    return data


def svg_of(content) -> str:
    assert len(content) == 1 and content[0].type == "text"
    assert content[0].text.lstrip().startswith(("<?xml", "<svg"))
    return content[0].text


def refusal_of(content, root, made) -> dict:
    """The one text content is the view's refusal document, exactly as the local call makes it."""
    assert [c.type for c in content] == ["text"]
    doc = json.loads(content[0].text)
    assert doc["ok"] is False and doc["refused"]
    assert doc == stamp(made, root).to_dict()
    return doc


# (tool, arguments, the local draw call on the twin vault)
CASES = [
    ("draw_fingerprint", {"narrative": NARRATIVE}, lambda r: draw.fingerprint(NARRATIVE, root=r)),
    (
        "draw_fingerprint",
        {"narrative": OTHER, "candidates": True},
        lambda r: draw.fingerprint(OTHER, candidates=True, root=r),
    ),
    ("draw_layered", {}, lambda r: draw.layered(root=r)),
    (
        "draw_layered",
        {"narratives": [NARRATIVE, OTHER]},
        lambda r: draw.layered([NARRATIVE, OTHER], root=r),
    ),
    ("draw_trace", {"node": NODE}, lambda r: draw.trace(NODE, root=r)),
    (
        "draw_trace",
        {"node": NODE, "direction": "up"},
        lambda r: draw.trace(NODE, "up", root=r),
    ),
    (
        "draw_trace",
        {"node": NODE, "direction": "down"},
        lambda r: draw.trace(NODE, "down", root=r),
    ),
]


def test_the_draw_tools_are_listed(url):
    async def names(s):
        return {t.name: t for t in (await s.list_tools()).tools}

    tools = with_session(url, names)
    for n in ("draw_fingerprint", "draw_layered", "draw_trace"):
        assert n in tools
        assert "contracts/assistant.md" in tools[n].description
        assert "Writes nothing" in tools[n].description
    assert "check" in tools and "fingerprint" in tools  # the others still list, with their schemas


@pytest.mark.parametrize("name,args,local", CASES)
def test_png_is_the_picture_draw_makes(url, vaults, name, args, local):
    drawing = local(vaults[1])
    assert png_of(tool(url, name, args)) == drawing.png()
    assert png_of(tool(url, name, {**args, "format": "png"})) == drawing.png()


@pytest.mark.parametrize("name,args,local", CASES)
def test_svg_is_the_text_draw_makes(url, vaults, name, args, local):
    assert svg_of(tool(url, name, {**args, "format": "svg"})) == local(vaults[1]).svg()


def test_the_tools_write_nothing_into_the_vault(url, vaults):
    before = snapshot(vaults[0])
    for name, args, _ in CASES:
        tool(url, name, args)
        tool(url, name, {**args, "format": "svg"})
        tool(url, name, {**args, "format": "gif"})
    assert changed(before, snapshot(vaults[0])) == set()


def test_refusals_are_the_views_documents_and_no_image(url, vaults):
    own = vaults[1]
    before = snapshot(vaults[0])
    cases = [
        (
            "draw_fingerprint",
            {"narrative": "no-such-page"},
            draw.fingerprint("no-such-page", root=own),
        ),
        ("draw_fingerprint", {"narrative": NODE}, draw.fingerprint(NODE, root=own)),
        (
            "draw_layered",
            {"narratives": ["no-such-page"]},
            draw.layered(["no-such-page"], root=own),
        ),
        ("draw_trace", {"node": "no-such-page"}, draw.trace("no-such-page", root=own)),
        ("draw_trace", {"node": NARRATIVE}, draw.trace(NARRATIVE, root=own)),
        (
            "draw_trace",
            {"node": NODE, "direction": "sideways"},
            draw.trace(NODE, "sideways", root=own),
        ),
    ]
    for name, args, made in cases:
        for fmt in ("png", "svg"):
            refusal_of(tool(url, name, {**args, "format": fmt}), own, made)
    assert changed(before, snapshot(vaults[0])) == set()


def test_a_bad_format_is_refused_with_a_fix(url, vaults):
    for name, args, _ in CASES:
        doc = json.loads(tool(url, name, {**args, "format": "gif"})[0].text)
        assert doc["ok"] is False and doc["operation"] == "draw"
        assert "gif" in doc["refused"][0]["subject"]
        assert "png" in json.dumps(doc["refused"][0]["fix"]) and "svg" in doc["refused"][0]["why"]


def test_an_excluded_narrative_is_refused(flawed):
    url, _, own = flawed
    doc = refusal_of(
        tool(url, "draw_fingerprint", {"narrative": "uncoded"}),
        own,
        draw.fingerprint("uncoded", root=own),
    )
    assert "excluded" in doc["refused"][0]["why"]
    refusal_of(
        tool(url, "draw_layered", {"narratives": ["uncoded"]}),
        own,
        draw.layered(["uncoded"], root=own),
    )


def test_a_vault_the_view_refuses_gives_its_problems_and_no_image(flawed):
    url, served, own = flawed
    before = snapshot(served)
    for name, args, made in [
        ("draw_layered", {}, draw.layered(root=own)),
        ("draw_trace", {"node": NODE}, draw.trace(NODE, root=own)),
        ("draw_fingerprint", {"narrative": "bad"}, draw.fingerprint("bad", root=own)),
    ]:
        doc = refusal_of(tool(url, name, args), own, made)
        if name != "draw_trace":  # the trace refuses at the row, with no problems list
            assert doc["problems"] and {p["severity"] for p in doc["problems"]} == {"error"}
        refusal_of(tool(url, name, {**args, "format": "svg"}), own, made)
    assert changed(before, snapshot(served)) == set()
    # a narrative the error does not touch still draws
    assert (
        png_of(tool(url, "draw_fingerprint", {"narrative": OTHER}))
        == draw.fingerprint(OTHER, root=own).png()
    )
