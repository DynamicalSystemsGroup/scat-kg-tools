"""Drawings (M6): a view drawn as four columns, one per layer, in layer order. Needs the extra `draw` (matplotlib).

    from scat_kg import draw
    d = draw.fingerprint("dry-july")      # a narrative's nodes and edges
    d = draw.fingerprint("dry-july", candidates=True)   # and its rule-4 candidates dashed
    d = draw.layered(["dry-july"])        # the layered view; none: every narrative
    d.png(); d.svg()                      # the image, as bytes and as text; Jupyter shows `d` itself
    d.save("dry-july.png")                # the explicit write: `.png` or `.svg`

A drawing is the view's data first (`view.to_dict()`, never the graph again) and then marks. Each node is a box in
its layer's column, labelled with its name (and its status, in brackets, when that is not `done`); each edge is a
line between neighbouring columns; the layer is named at the top of its column and has its own colour, so colour
is never the only sign. Within a column the nodes keep the view's order, by name. Nothing is ordered or sized by a
measure. The same call gives the same bytes: fixed fonts, no dates, no random seeds. Nothing is written except
by `save`. Where a view refuses, so does the drawing, with the same refusal.
"""

import io
import textwrap
from dataclasses import dataclass
from pathlib import Path

from scat_kg import views
from scat_kg.ops.files import replace_file
from scat_kg.ops.result import Refusal, Result
from scat_kg.tbox import TBOX

OPERATION = "draw"
INSTALL = 'pip install "scat-kg[draw]"'
SUFFIXES = (".png", ".svg")

# Okabe-Ito, one colour per layer (safe for the common kinds of colour blindness), and the box is a pale tint of it.
COLOURS = {
    "group": "#0072B2",
    "concern": "#E69F00",
    "affordance": "#009E73",
    "technology": "#CC79A7",
}
DPI = 100
ROW = 0.3  # inches between two nodes of a column
HEAD = 1.1  # inches above the nodes: title and layer labels
FOOT = 0.6  # inches below the nodes: the legend line
MIN_BODY = 1.2
DASH = (0, (4, 3))


@dataclass(frozen=True)
class _Mark:
    """What a drawing shows, as plain data: the columns in layer order, and lines between node names."""

    title: str
    columns: tuple[tuple[str, tuple[tuple[str, str], ...]], ...]  # (layer, ((name, label), ...))
    lines: tuple[tuple[str, str, bool], ...]  # (from name, to name, dashed)
    legend: str


def _label(node: dict) -> str:
    status = node.get("status")
    return node["name"] if not status or status == "done" else f"{node['name']} ({status})"


def _columns(nodes_by_layer: dict[str, list[dict]]) -> tuple:
    return tuple(
        (layer, tuple((n["name"], _label(n)) for n in nodes_by_layer.get(layer, ())))
        for layer in TBOX.layers
    )


def _fingerprint_mark(data: dict) -> _Mark:
    n = data["narratives"][0]
    by_layer = {layer: [x for x in n["nodes"] if x["type"] == layer] for layer in TBOX.layers}
    lines = [(e["from"], e["to"], False) for e in n["edges"]]
    lines += [(c["from"], c["to"], True) for c in n.get("candidates", ())]
    return _Mark(
        f"{n['name']} ({n['status']})",
        _columns(by_layer),
        tuple(lines),
        "solid line: an edge a row of this narrative tells."
        + (" dashed line: a link with no row (a candidate)." if "candidates" in n else ""),
    )


def _layered_mark(data: dict) -> _Mark:
    names = data["narratives"]
    if not names:
        title = "layered view of no narratives"
    elif len(names) <= 5:
        title = "layered view of " + ", ".join(names)
    else:
        title = f"layered view of {len(names)} narratives"
    return _Mark(
        title,
        _columns(data["nodes"]),
        tuple((e["from"], e["to"], False) for e in data["edges"]),
        "line: an edge a row of a drawn narrative tells.",
    )


# ---------------------------------------------------------------------------------------------------------
# Marks
# ---------------------------------------------------------------------------------------------------------


def _tint(colour: str, keep: float = 0.22) -> str:
    """The colour mixed into white: the box is pale so the name stays readable."""
    rgb = [int(colour[i : i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(255 - (255 - c) * keep):02x}" for c in rgb)


def _render(mark: _Mark, fmt: str) -> bytes:
    import matplotlib
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    from matplotlib.figure import Figure
    from matplotlib.patches import Rectangle

    longest = max((len(lab) for _, col in mark.columns for _, lab in col), default=10)
    tallest = max((len(col) for _, col in mark.columns), default=0)
    spacing = max(3.0, 0.075 * longest + 1.0)  # inches between two column centres
    width = 4 * spacing
    body = max(MIN_BODY, ROW * tallest)
    height = HEAD + body + FOOT
    mid = FOOT + body / 2

    rc = {
        "font.family": "DejaVu Sans",
        "svg.fonttype": "none",  # text stays text: a name in the image is a name in the file
        "svg.hashsalt": "scat-kg",
    }
    with matplotlib.rc_context(rc):
        fig = Figure(figsize=(width, height), dpi=DPI, facecolor="white")
        FigureCanvasAgg(fig)
        ax = fig.add_axes((0, 0, 1, 1))
        ax.set_xlim(-0.5, 3.5)  # x: the column number; y: inches from the bottom
        ax.set_ylim(0, height)
        ax.axis("off")

        pos: dict[str, tuple[float, float]] = {}
        for x, (_, col) in enumerate(mark.columns):
            for i, (name, _) in enumerate(col):
                pos[name] = (x, mid + ((len(col) - 1) / 2 - i) * ROW)
        for a, b, dashed in mark.lines:
            if a in pos and b in pos:
                ax.plot(
                    [pos[a][0], pos[b][0]],
                    [pos[a][1], pos[b][1]],
                    color="#4d4d4d",
                    lw=0.9,
                    ls=DASH if dashed else "-",
                    zorder=1,
                )
        title = "\n".join(textwrap.wrap(mark.title, int(width * 8), break_on_hyphens=False))
        ax.text(1.5, height - 0.3, title, ha="center", va="center", fontsize=12, zorder=3)
        for x, (layer, col) in enumerate(mark.columns):
            ax.text(
                x, height - HEAD + 0.25, layer, ha="center", va="center", fontsize=10,
                fontweight="bold", color="#222222", zorder=3,
            )  # fmt: skip
            for name, label in col:
                ax.text(
                    *pos[name], label, ha="center", va="center", fontsize=8, color="black",
                    bbox={
                        "boxstyle": "round,pad=0.25",
                        "fc": _tint(COLOURS[layer]),
                        "ec": COLOURS[layer],
                        "lw": 1.2,
                    },
                    zorder=2,
                )  # fmt: skip
        if tallest == 0:
            ax.add_patch(
                Rectangle(
                    (-0.45, FOOT), 3.9, body, fill=False, ec="#888888", lw=1, ls=DASH, zorder=1
                )
            )
            ax.text(1.5, mid, "no nodes", ha="center", va="center", fontsize=11, color="#444444")
        ax.text(1.5, FOOT / 2, mark.legend, ha="center", va="center", fontsize=8, color="#333333")

        buf = io.BytesIO()
        meta = {"Software": None} if fmt == "png" else {"Date": None, "Creator": "scat-kg"}
        fig.savefig(buf, format=fmt, dpi=DPI, facecolor="white", metadata=meta)
    return buf.getvalue()


# ---------------------------------------------------------------------------------------------------------
# The drawing
# ---------------------------------------------------------------------------------------------------------


def _shown(path: Path, root: Path) -> str:
    """The path in the Result: vault-relative with `/` inside the vault, else as given."""
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _no_write(path: Path, why: str, fix: str) -> Result:
    return Result(OPERATION, refused=(Refusal(path.as_posix(), why, fix),))


@dataclass(frozen=True)
class Drawing:
    """A view drawn: `png()`, `svg()`, and `save(path)`, the one call that writes."""

    mark: _Mark
    root: Path = Path(".")

    def png(self) -> bytes:
        return _render(self.mark, "png")

    def svg(self) -> str:
        return _render(self.mark, "svg").decode("utf-8")

    def _repr_png_(self) -> bytes:
        return self.png()

    def save(self, path: str | Path) -> Result:
        """Write the image to `path` (`.png` or `.svg`); a file with the same content is left alone."""
        path = Path(path)
        if path.suffix.lower() not in SUFFIXES:
            return _no_write(
                path,
                f"`{path.suffix or path.name}` is not an image type this draws",
                f"end the file name with {' or '.join(SUFFIXES)}, for example `{path.stem or 'drawing'}.png`",
            )
        if path.is_dir():
            return _no_write(
                path,
                "a folder has the name of the file the image goes in",
                f"give a file name with `--out`, such as `{(path / 'drawing.png').as_posix()}`",
            )
        data = self.png() if path.suffix.lower() == ".png" else self.svg().encode("utf-8")
        shown = _shown(path, self.root)
        try:
            if not path.exists():
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
                return Result(OPERATION, created=(shown,))
            if path.read_bytes() == data:
                return Result(OPERATION, unchanged=(shown,))
            replace_file(path, data)
            return Result(OPERATION, changed=(shown,))
        except OSError as e:
            return _no_write(
                path,
                f"could not write: {e}",
                "check that the folder exists and that you may write in it",
            )


def _need_matplotlib() -> Result | None:
    try:
        import matplotlib  # noqa: F401
    except ImportError:
        return Result(
            OPERATION,
            refused=(
                Refusal(
                    "matplotlib",
                    "drawing needs the library matplotlib, which is not installed",
                    INSTALL,
                ),
            ),
        )
    return None


def fingerprint(
    narrative: str, *, candidates: bool = False, root: str | Path = "."
) -> Drawing | Result:
    """Draw a narrative's fingerprint: its nodes and edges; `candidates=True` adds its rule-4 candidates dashed."""
    if bad := _need_matplotlib():
        return bad
    if not isinstance(narrative, str):
        return views._refuse(
            "fingerprint",
            repr(narrative),
            "a drawing needs the name of one narrative",
            "pass the name of one narrative as a string",
        )
    view = views.fingerprint(narrative, candidates=candidates, root=root)
    if not isinstance(view, views.View):
        return view
    return Drawing(_fingerprint_mark(view.data), Path(root))


def layered(narratives: list[str] | None = None, *, root: str | Path = ".") -> Drawing | Result:
    """Draw the layered view of the named narratives (none: every narrative)."""
    if bad := _need_matplotlib():
        return bad
    view = views.layered(narratives, root=root)
    if not isinstance(view, views.View):
        return view
    return Drawing(_layered_mark(view.data), Path(root))
