"""Drawings (M6): a view drawn as columns, one per layer, in layer order (four; a fingerprint drops one for its kind). Needs the extra `draw` (matplotlib).

    from scat_tools import draw
    d = draw.fingerprint("dry-july")      # a narrative's nodes and edges
    d = draw.fingerprint("dry-july", candidates=True)   # and its rule-4 candidates dashed
    d = draw.layered(["dry-july"])        # the layered view; none: every narrative
    d = draw.trace("water")               # what a node reaches: up, down or `direction="both"` (the default)
    d.png(); d.svg()                      # the image, as bytes and as text; Jupyter shows `d` itself
    d.save("dry-july.png")                # the explicit write: `.png` or `.svg`

A fingerprint of an architecture has no stakeholder column and one of a scenario has no technology column; the footer
says how many nodes of the dropped layer the narrative links and why they are not drawn. The first column is labelled
"stakeholder" (the layer `group`).

A drawing is a query result first (a `views.View`: `view.to_dict()` is its table, never the graph again) and then
marks. `draw.render(result)` draws a result without running any query; `fingerprint`, `layered` and `trace` run the
query once and render it. `Drawing.nodes()` and `Drawing.edges()` read back what is drawn. A trace draws the
nodes it reaches and the node it starts from, whose type and status the trace result carries (`View.traced`). Each node is a box in
its layer's column, labelled with its name (and its status, in brackets, when that is not `done`); each edge is a
line between neighbouring columns; the layer is named at the top of its column and has its own colour, so colour
is never the only sign. Nothing is sized by a measure. Within a column the nodes are ordered to reduce the lines
that cross (WP35): the view's order, by name, is the start, and a fixed number of barycentre sweeps (each node by
the mean place of its neighbours in the next column) moves them; the order drawn is never worse than the start.
Parts of the drawing that share no line are bands, one above the next, the largest first, each ordered on its own,
with a thin separator between; the nodes with no line at all are the last band. `Drawing.nodes()` lists each
column top to bottom, bands included. `layered(..., mark_narratives=True)` marks each edge's line by the narrative
that tells it (colour and line style, never plain dashed, which is a candidate), black and thicker for an edge
more than one narrative tells, with a key naming each; it is reached from Python only. The same call gives the same
bytes: fixed fonts, no dates, no random seeds. Nothing is written except by `save`. Where a view refuses, so does the drawing, with the same refusal.
"""

import io
import textwrap
from dataclasses import dataclass, replace
from itertools import pairwise
from pathlib import Path

from scat_tools import views
from scat_tools.ops.files import replace_file
from scat_tools.ops.result import Refusal, Result, stamp
from scat_tools.tbox import TBOX

OPERATION = "draw"
INSTALL = 'pip install "scat-tools[draw]"'
SUFFIXES = (".png", ".svg")

# Okabe-Ito, one colour per layer (safe for the common kinds of colour blindness), and the box is a pale tint of it.
COLOURS = {
    "group": "#0072B2",
    "concern": "#E69F00",
    "affordance": "#009E73",
    "technology": "#CC79A7",
}
SHOWN = {
    "group": "stakeholder"
}  # the word at the top of a column, where it is not the layer's name
PLURAL = {
    "group": "stakeholders",
    "concern": "concerns",
    "affordance": "affordances",
    "technology": "technologies",
}
DROPPED = {
    "architecture": "group",
    "scenario": "technology",
}  # the layer a kind's fingerprint leaves out
DPI = 100
ROW = 0.3  # inches between two nodes of a column
HEAD = 1.1  # inches above the nodes: title and layer labels
FOOT = 0.6  # inches below the nodes: one line of legend
FOOT_LINE = 0.17  # inches for each further line of legend
MIN_BODY = 1.2
DASH = (0, (4, 3))
ORPHANS_SHOWN = 10  # orphan names in the footer; the rest are "and N more"
PASSES = 4  # barycentre passes (a sweep down, then a sweep up) per band
GAP = 0.7  # rows between two bands
KEY_ROW = 0.22  # inches for each row of the narrative key in the footer
SAMPLE = 0.45  # inches: the line sample in the key

# A line's style: (colour, line style, width). The plain line is what a drawing has without marking.
PLAIN = ("#4d4d4d", "-", 0.9)
CANDIDATE = ("#4d4d4d", DASH, 0.9)
# Marks for the narratives (WP35-G3): colours other than the layers' that stay apart for the common kinds of colour
# blindness (Okabe-Ito vermillion and sky blue, Tol indigo), times three line styles; none is plain dashed.
LINE_COLOURS = ("#D55E00", "#56B4E9", "#332288")
LINE_STYLES = ("-", (0, (6, 2, 1.2, 2)), (0, (1, 2.2)))  # solid, dash-dot, dotted
SHARED = ("#000000", "-", 2.2)  # an edge more than one narrative tells
SHARED_TEXT = "told by more than one narrative"
MARKS = tuple((c, ls, 1.4) for ls in LINE_STYLES for c in LINE_COLOURS)


@dataclass(frozen=True)
class _Mark:
    """What a drawing shows, as plain data: the columns in layer order, and lines between node names."""

    title: str
    columns: tuple[tuple[str, tuple[tuple[str, str], ...]], ...]  # (layer, ((name, label), ...))
    lines: tuple[tuple[str, str, bool], ...]  # (from name, to name, dashed)
    legend: str
    styles: tuple[
        tuple, ...
    ] = ()  # a line's (colour, line style, width), one for each of `lines`; none: plain
    keys: tuple[
        tuple[str, tuple], ...
    ] = ()  # (what it names, line style): the narrative key under the figure


def _label(node: dict) -> str:
    status = node.get("status")
    return node["name"] if not status or status == "done" else f"{node['name']} ({status})"


def _columns(nodes_by_layer: dict[str, list[dict]], drop: str | None = None) -> tuple:
    return tuple(
        (layer, tuple((n["name"], _label(n)) for n in nodes_by_layer.get(layer, ())))
        for layer in TBOX.layers
        if layer != drop
    )


def _fingerprint_mark(data: dict) -> _Mark:
    n = data["narratives"][0]
    by_layer = {layer: [x for x in n["nodes"] if x["type"] == layer] for layer in TBOX.layers}
    lines = [(e["from"], e["to"], False) for e in n["edges"]]
    lines += [(c["from"], c["to"], True) for c in n.get("candidates", ())]
    legend = "solid line: an edge a row of this narrative tells." + (
        " dashed line: a link with no row (a candidate)." if "candidates" in n else ""
    )
    drop = DROPPED.get(n["kind"])
    if drop:
        shown, left = SHOWN.get(drop, drop), len(by_layer[drop])
        legend += (
            f"\nno {shown} column: {'an' if n['kind'] == 'architecture' else 'a'} {n['kind']}."
        )
        if left:
            noun = shown if left == 1 else PLURAL[drop]
            legend += (
                f" {left} {noun} the narrative links {'is' if left == 1 else 'are'} not drawn."
            )
    return _Mark(f"{n['name']} ({n['status']})", _columns(by_layer, drop), tuple(lines), legend)


def _narrative_marks(data: dict) -> tuple[tuple, tuple]:
    """The style of each line and the key, when each solid edge is marked by the narrative that tells it.

    Only the narratives the view draws count. Marks go to the narratives that tell a drawn edge, in name order,
    and wrap round when there are more narratives than marks; an edge two narratives tell has `SHARED`.
    """
    drawn = set(data["narratives"])
    told = [sorted(drawn & set(e["narratives"])) for e in data["edges"]]
    names = sorted({n for t in told for n in t})
    mark = {n: MARKS[i % len(MARKS)] for i, n in enumerate(names)}
    styles = [SHARED if len(t) > 1 else mark[t[0]] for t in told]
    styles += [CANDIDATE] * len(data.get("candidates", ()))
    keys = [(n, mark[n]) for n in names]
    if any(len(t) > 1 for t in told):
        keys.append((SHARED_TEXT, SHARED))
    return tuple(styles), tuple(keys)


def _layered_mark(data: dict, mark_narratives: bool = False) -> _Mark:
    names = data["narratives"]
    if not names:
        title = "layered view of no narratives"
    elif len(names) <= 5:
        title = "layered view of " + ", ".join(names)
    else:
        title = f"layered view of {len(names)} narratives"
    lines = [(e["from"], e["to"], False) for e in data["edges"]]
    lines += [(c["from"], c["to"], True) for c in data.get("candidates", ())]
    legend = "line: an edge a row of a drawn narrative tells." + (
        " dashed line: a link with no row (a candidate)." if "candidates" in data else ""
    )
    if data.get("excluded"):
        legend += (
            " excluded (no node page linked): "
            + ", ".join(x["name"] for x in data["excluded"])
            + "."
        )
    if data.get("orphans"):
        names = [x["name"] for x in data["orphans"]]
        shown = ", ".join(names[:ORPHANS_SHOWN])
        more = len(names) - ORPHANS_SHOWN
        legend += (
            "\nno row tells these node pages: "
            + shown
            + (f" and {more} more" if more > 0 else "")
            + "."
        )
    if not mark_narratives:
        return _Mark(title, _columns(data["nodes"]), tuple(lines), legend)
    legend += "\nline colour and style: the narrative that tells the edge, named below."
    styles, keys = _narrative_marks(data)
    return _Mark(title, _columns(data["nodes"]), tuple(lines), legend, styles, keys)


def _trace_mark(data: dict, me: dict) -> _Mark:
    """`data` is a trace view's; `me` is the traced node (name, type, status), which a trace leaves out."""
    reached = [*data["up"], *data["down"], me]
    by_layer = {layer: [x for x in reached if x["type"] == layer] for layer in TBOX.layers}
    for nodes in by_layer.values():
        nodes.sort(key=lambda x: x["name"])
    way = {"up": "up", "down": "down", "both": "up and down"}[data["direction"]]
    return _Mark(
        f"trace of {me['type']} {me['name']}, {way}",
        _columns(by_layer),
        tuple((e["from"], e["to"], False) for e in data["edges"]),
        f"solid line: an edge a row of a narrative tells, walked from {me['name']}.",
    )


# ---------------------------------------------------------------------------------------------------------
# Layout: bands, then the order in each column of a band
# ---------------------------------------------------------------------------------------------------------


@dataclass(frozen=True)
class _Layout:
    rows: dict[
        str, float
    ]  # a node's row, from the top (a column is centred in its band, so it may be a half)
    total: float  # rows from the top of the first band to the bottom of the last, gaps included
    seps: tuple[float, ...]  # the row of each separator between two bands


def _crossings(cols: list[list[str]], adj: dict[str, set[str]]) -> int:
    """Pairs of lines between neighbouring columns that cross; two lines sharing a node do not."""
    total = 0
    for left, right in pairwise(cols):
        place = {n: i for i, n in enumerate(right)}
        ends = [(i, place[m]) for i, n in enumerate(left) for m in adj[n] if m in place]
        total += sum(1 for p, a in ends for q, b in ends if p < q and a > b)
    return total


def _sweep(col: list[str], fixed: list[str], adj: dict[str, set[str]]) -> list[str]:
    """`col` with the nodes that have a neighbour in `fixed` sorted by the mean place of those neighbours.

    A tie keeps the earlier order. A node with no neighbour there keeps its place.
    """
    place = {n: i for i, n in enumerate(fixed)}
    mean = {}
    for n in col:
        near = [place[m] for m in adj[n] if m in place]
        if near:
            mean[n] = sum(near) / len(near)
    moved = iter(sorted((n for n in col if n in mean), key=mean.__getitem__))
    return [next(moved) if n in mean else n for n in col]


def _order(cols: list[list[str]], adj: dict[str, set[str]]) -> list[list[str]]:
    """The columns of one band reordered to cross less: PASSES of barycentre sweeps, the best order seen wins."""
    best, fewest = cols, _crossings(cols, adj)
    cur = [list(c) for c in cols]
    for _ in range(PASSES):
        for k in range(1, len(cur)):
            cur[k] = _sweep(cur[k], cur[k - 1], adj)
        for k in range(len(cur) - 2, -1, -1):
            cur[k] = _sweep(cur[k], cur[k + 1], adj)
        if (n := _crossings(cur, adj)) < fewest:
            best, fewest = [list(c) for c in cur], n
    return best


def _layout(mark: _Mark) -> _Layout:
    """Where each node goes: the bands (parts that share no line), largest first, the nodes with no line last."""
    layer_of = {n: k for k, (_, col) in enumerate(mark.columns) for n, _ in col}
    adj: dict[str, set[str]] = {n: set() for n in layer_of}
    near: dict[str, set[str]] = {
        n: set() for n in layer_of
    }  # the same, only between neighbouring columns
    for a, b, _ in mark.lines:
        if a in layer_of and b in layer_of and a != b:
            adj[a].add(b)
            adj[b].add(a)
            if abs(layer_of[a] - layer_of[b]) == 1:
                near[a].add(b)
                near[b].add(a)
    seen: set[str] = set()
    parts: list[set[str]] = []
    for start in sorted(layer_of, key=lambda n: (layer_of[n], n)):
        if start in seen or not adj[start]:
            continue
        part, todo = {start}, [start]
        while todo:
            for m in adj[todo.pop()] - part:
                part.add(m)
                todo.append(m)
        seen |= part
        parts.append(part)
    parts.sort(key=lambda p: (-len(p), min((layer_of[n], n) for n in p)))
    lone = {n for n in layer_of if not adj[n]}
    rows: dict[str, float] = {}
    seps: list[float] = []
    top = 0.0
    for part in [*parts, *([lone] if lone else [])]:
        cols = [[n for n, _ in col if n in part] for _, col in mark.columns]
        height = max(len(c) for c in cols)
        for c in _order(cols, near):
            for i, n in enumerate(c):
                rows[n] = top + (height - len(c)) / 2 + i
        top += height
        seps.append(top - 1 + (1 + GAP) / 2)
        top += GAP
    return _Layout(rows, max(top - GAP, 0.0), tuple(seps[:-1]))


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
    lay = _layout(mark)
    spacing = max(3.0, 0.075 * longest + 1.0)  # inches between two column centres
    cols = len(mark.columns)
    width = cols * spacing
    body = max(MIN_BODY, ROW * lay.total)
    legend = "\n".join(  # a paragraph of the legend (a line of `\n`) wraps by itself
        w
        for para in mark.legend.split("\n")
        for w in textwrap.wrap(para, int(width * 12), break_on_hyphens=False)
    )
    foot = FOOT + FOOT_LINE * (legend.count("\n"))
    per_row = key_rows = 0
    if mark.keys:
        slot = (
            SAMPLE + 0.1 + 0.07 * max(len(k) for k, _ in mark.keys)
        )  # inches for a sample and a name
        per_row = max(1, int((width - 0.2) // slot))
        key_rows = -(-len(mark.keys) // per_row)
        foot += KEY_ROW * key_rows + 0.1
    height = HEAD + body + foot
    mid = foot + body / 2

    rc = {
        "font.family": "DejaVu Sans",
        "svg.fonttype": "none",  # text stays text: a name in the image is a name in the file
        "svg.hashsalt": "scat-tools",
    }
    with matplotlib.rc_context(rc):
        fig = Figure(figsize=(width, height), dpi=DPI, facecolor="white")
        FigureCanvasAgg(fig)
        ax = fig.add_axes((0, 0, 1, 1))
        ax.set_xlim(-0.5, cols - 0.5)  # x: the column number; y: inches from the bottom
        ax.set_ylim(0, height)
        ax.axis("off")

        pos: dict[str, tuple[float, float]] = {}
        for x, (_, col) in enumerate(mark.columns):
            for name, _ in col:
                pos[name] = (x, mid + ((lay.total - 1) / 2 - lay.rows[name]) * ROW)
        for i, (a, b, dashed) in enumerate(mark.lines):
            if a in pos and b in pos:
                colour, ls, lw = mark.styles[i] if mark.styles else CANDIDATE if dashed else PLAIN
                ax.plot(
                    [pos[a][0], pos[b][0]],
                    [pos[a][1], pos[b][1]],
                    color=colour,
                    lw=lw,
                    ls=ls,
                    zorder=1,
                )
        for sep in lay.seps:  # a thin line between two bands
            y = mid + ((lay.total - 1) / 2 - sep) * ROW
            ax.hlines(y, -0.45, cols - 0.55, colors="#bbbbbb", linewidths=0.6, zorder=0)
        title = "\n".join(textwrap.wrap(mark.title, int(width * 8), break_on_hyphens=False))
        ax.text(
            (cols - 1) / 2, height - 0.3, title, ha="center", va="center", fontsize=12, zorder=3
        )
        for x, (layer, col) in enumerate(mark.columns):
            ax.text(
                x, height - HEAD + 0.25, SHOWN.get(layer, layer), ha="center", va="center", fontsize=10,
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
        if lay.total == 0:
            ax.add_patch(
                Rectangle(
                    (-0.45, foot),
                    cols - 0.1,
                    body,
                    fill=False,
                    ec="#888888",
                    lw=1,
                    ls=DASH,
                    zorder=1,
                )
            )
            ax.text(
                (cols - 1) / 2,
                mid,
                "no nodes",
                ha="center",
                va="center",
                fontsize=11,
                color="#444444",
            )
        key_h = foot - FOOT - FOOT_LINE * legend.count("\n") if mark.keys else 0.0
        for i, (text, (colour, ls, lw)) in enumerate(mark.keys):
            row, col = divmod(i, per_row)
            y = key_h - 0.1 - (row + 0.5) * KEY_ROW
            x0 = -0.5 + (0.1 + col * slot) / spacing
            ax.hlines(y, x0, x0 + SAMPLE / spacing, colors=colour, linestyles=ls, linewidths=lw)
            ax.text(
                x0 + (SAMPLE + 0.1) / spacing, y, text, ha="left", va="center", fontsize=8,
                color="#333333",
            )  # fmt: skip
        ax.text(
            (cols - 1) / 2, key_h + (foot - key_h) / 2, legend, ha="center", va="center", fontsize=8, color="#333333",
            linespacing=1.2,
        )  # fmt: skip

        buf = io.BytesIO()
        meta = {"Software": None} if fmt == "png" else {"Date": None, "Creator": "scat-tools"}
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

    def nodes(self) -> list[tuple[str, str]]:
        """The nodes drawn, as (name, layer): column by column, each from the top down as drawn, bands included."""
        rows = _layout(self.mark).rows
        return [
            (name, layer)
            for layer, col in self.mark.columns
            for name, _ in sorted(col, key=lambda c: rows[c[0]])
        ]

    def edges(self) -> list[tuple[str, str, bool]]:
        """The edges drawn, as (from, to, dashed): the lines whose two ends are both drawn."""
        drawn = {name for name, _ in self.nodes()}
        return [(a, b, d) for a, b, d in self.mark.lines if a in drawn and b in drawn]

    def _repr_png_(self) -> bytes:
        return self.png()

    def save(self, path: str | Path) -> Result:
        """Write the image to `path` (`.png` or `.svg`); a file with the same content is left alone."""
        return stamp(self._write(Path(path)), self.root)

    def _write(self, path: Path) -> Result:
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


def render(result: views.View | Result, *, mark_narratives: bool = False) -> Drawing | Result:
    """Draw a query result (a fingerprint of one narrative, a layered view or a trace) without running any query.

    `mark_narratives=True` marks each edge of a layered view by the narrative that tells it; it has no effect on
    a fingerprint (one narrative tells every edge) or a trace.

    A result that is not a view, or a view this does not draw, is refused.
    """
    if bad := _need_matplotlib():
        return bad
    if not isinstance(result, views.View):
        return (
            result if isinstance(result, Result) else _cannot(repr(result), "is not a query result")
        )
    data, op = result.data, result.operation
    if op == "fingerprint":
        if len(data.get("narratives", ())) != 1:
            return _cannot(
                "fingerprint",
                f"a fingerprint of {len(data.get('narratives', ()))} narratives is not drawn",
                "ask for the fingerprint of one narrative",
            )
        return Drawing(_fingerprint_mark(data))
    if op == "layered":
        return Drawing(_layered_mark(data, mark_narratives))
    if op == "trace":
        if result.traced is None:
            return _cannot(
                "trace", "this trace result does not carry its starting node", "run `trace`"
            )
        return Drawing(_trace_mark(data, result.traced))
    return _cannot(
        op, f"a {op} result is not drawn", "draw a fingerprint, a layered view or a trace"
    )


def _cannot(subject: str, why: str, fix: str = "pass a query result from `views`") -> Result:
    return Result(OPERATION, refused=(Refusal(subject, why, fix),))


def _drawn_with(result, root, mark_narratives: bool = False) -> Drawing | Result:
    drawing = render(result, mark_narratives=mark_narratives)
    return replace(drawing, root=Path(root)) if isinstance(drawing, Drawing) else drawing


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
    return _drawn_with(view, root) if isinstance(view, views.View) else view


def layered(
    narratives: list[str] | None = None,
    *,
    candidates: bool = False,
    mark_narratives: bool = False,
    root: str | Path = ".",
) -> Drawing | Result:
    """Draw the layered view of the named narratives (none: every narrative); `candidates=True` adds their rule-4
    candidates dashed. Node pages no row tells are named in the footer.

    `mark_narratives=True` draws each solid edge in the mark (colour and line style) of the narrative that tells it,
    black and thicker where more than one tells it, with a key under the figure; candidates stay grey and dashed.
    A fingerprint or a trace has no such option: one narrative tells all of a fingerprint.
    """
    if bad := _need_matplotlib():
        return bad
    if not isinstance(mark_narratives, bool):
        return views._refuse(
            "layered",
            repr(mark_narratives),
            "mark_narratives must be True or False",
            "pass True or False",
        )
    view = views.layered(narratives, candidates=candidates, root=root)
    return _drawn_with(view, root, mark_narratives) if isinstance(view, views.View) else view


def trace(node: str, direction: str = "both", *, root: str | Path = ".") -> Drawing | Result:
    """Draw what a node reaches, `direction` up, down or both (the default), with the node itself in its column."""
    if bad := _need_matplotlib():
        return bad
    view = views.trace(node, direction, root=root)
    return _drawn_with(view, root) if isinstance(view, views.View) else view
