"""The `scat` command: a thin layer over the Python API (`scat_tools`). Same operations, same messages.

Exit code 0 when there is no error and no refusal (warnings alone are 0), 1 otherwise, 2 for a command
line that cannot be read. Every command takes `--root` (the vault folder; default: the current directory).
"""

import argparse
import json
import sys
from collections.abc import Sequence

import scat_tools
from scat_tools import draw
from scat_tools.ops.names import STUBBABLE
from scat_tools.tbox import TBOX


def _parser() -> argparse.ArgumentParser:
    top = argparse.ArgumentParser(
        prog="scat",
        description="Check and work on a SCAT knowledge-graph vault. Every command has a REPL twin "
        "(`import scat_tools`) that gives the same messages.",
        epilog="Run `scat <command> --help` for a command.",
    )
    sub = top.add_subparsers(dest="command", metavar="<command>", required=True)

    def command(name, summary, twin, parent=sub):
        p = parent.add_parser(
            name,
            help=summary,
            description=summary,
            epilog=f"REPL: {twin}",
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )
        p.add_argument(
            "--root", default=".", help="the vault folder, the one with scat.toml (default: here)"
        )
        p.add_argument(
            "--json",
            action="store_true",
            help="print the result as one JSON document (machine-interface contract), nothing else",
        )
        return p

    scope = "PAGE is a page name or its path from the vault folder; without it, the whole vault"
    p = command(
        "check",
        f"Check the vault against the rules. {scope}. Writes nothing.",
        '`scat_tools.check()`, `scat_tools.check("<page>")`, `scat_tools.check("<page>", neighborhood=True)`',
    )
    p.add_argument("page", nargs="?", metavar="PAGE", help="check this page only")
    p.add_argument(
        "--neighborhood",
        action="store_true",
        help="check PAGE and every page one link away, in either direction",
    )
    p = command(
        "status",
        f"Show each page's status and the counts. {scope}.",
        '`scat_tools.status()`, `scat_tools.status("<page>")`, `scat_tools.status("<page>", neighborhood=True)`',
    )
    p.add_argument("page", nargs="?", metavar="PAGE", help="show this page only")
    p.add_argument(
        "--neighborhood",
        action="store_true",
        help="show PAGE and every page one link away, in either direction",
    )
    p = command(
        "set-status",
        "Set a page's status to stub, draft or done.",
        '`scat_tools.set_status("<page-name>", "<status>")`',
    )
    p.add_argument("page", metavar="PAGE", help="the page's name or path")
    p.add_argument("status", metavar="STATUS", help="stub, draft or done")
    command(
        "index",
        "Write the index page `index/<type>.base` of each type that has none. Never rewrites one.",
        "`scat_tools.index()`",
    )
    p = command(
        "stub",
        "Create a stub page: a node (group, concern, affordance or technology), a narrative, or, where the "
        "vault's attribution mode is required or optional, a contributor page.",
        '`scat_tools.stub("<page-name>", type="<type>")`',
    )
    p.add_argument("name", metavar="NAME", help="the new page's name: a-z, 0-9 and hyphens")
    p.add_argument(
        "--type",
        required=True,
        metavar="TYPE",
        help="the page's type, one of: " + ", ".join(STUBBABLE),
    )
    p = command(
        "stub-links",
        "Create the node pages that the ends of rows link and the vault lacks. PAGE limits it to one page.",
        '`scat_tools.stub_links()`, `scat_tools.stub_links("<page>")`',
    )
    p.add_argument("page", nargs="?", metavar="PAGE", help="look at this page's links only")
    p = command(
        "record-edge",
        "Record an edge: add its row to each narrative named by --told-by that has none, stubbing a "
        "missing node or narrative. Leaves the links as they are. Refuses a narrative that is done.",
        '`scat_tools.record_edge("<type>", "<from>", "<to>", ["<narrative>"], note="<text>")`',
    )
    p.add_argument(
        "type",
        metavar="TYPE",
        help="one of: "
        + ", ".join(f"{s} ({e.from_type} then {e.to_type})" for s, e in TBOX.edge_types.items()),
    )
    p.add_argument("from_node", metavar="FROM", help="the name of the node at the first end")
    p.add_argument("to_node", metavar="TO", help="the name of the node at the second end")
    p.add_argument(
        "--told-by",
        action="append",
        required=True,
        metavar="NARRATIVE",
        help="the narrative that tells the edge; repeat it for each narrative",
    )
    p.add_argument("--note", default="", metavar="TEXT", help="the row's note (default: none)")
    p = command(
        "remove-edge",
        "Remove an edge: delete its rows, from the narratives named by --told-by or, without it, from "
        "every narrative that tells it. Leaves the links. Refuses a narrative that is done.",
        '`scat_tools.remove_edge("<from>", "<to>")`, `scat_tools.remove_edge("<from>", "<to>", ["<narrative>"])`',
    )
    p.add_argument("from_node", metavar="FROM", help="the name of the node at the first end")
    p.add_argument("to_node", metavar="TO", help="the name of the node at the second end")
    p.add_argument(
        "--told-by",
        action="append",
        metavar="NARRATIVE",
        help="remove the rows of this narrative only; repeat it for each narrative",
    )
    p = command(
        "merge",
        "Fold node page A into node page B, two pages of one type: every link to A in the narratives and node "
        "pages becomes a link to B, A's body is added to B under a heading that names A, A's description is "
        "dropped, and A's page is removed. A is folded into B, never the other way round. Refuses, and writes "
        "nothing, for a pair of different types, a page that is not a node page, a contributor page that links A, "
        "or a merge that would give a narrative two rows for one edge. With --plan it writes nothing and shows "
        "what the merge would do.",
        '`scat_tools.merge("<a>", "<b>")`, `scat_tools.merge("<a>", "<b>", plan=True)`',
    )
    p.add_argument("a", metavar="A", help="the node page that is folded in, and removed")
    p.add_argument("b", metavar="B", help="the node page that stays")
    p.add_argument(
        "--plan", action="store_true", help="show what the merge would do and write nothing"
    )
    p = command(
        "split-plan",
        "Show what you must re-link to split node page A in two: each narrative that links A, with every link and "
        "every Edges told row that names A. You assign each narrative to A or to a new page. Writes nothing.",
        '`scat_tools.split_plan("<a>")`',
    )
    p.add_argument("a", metavar="A", help="the node page to split")
    scope = "Writes nothing"
    p = command(
        "fingerprint",
        "Show a narrative's fingerprint: its nodes by layer and the edges its rows tell; with "
        f"--candidates, also the candidates (pairs the account links that no row joins). NARRATIVE is a name; without it, every narrative. {scope}.",
        '`scat_tools.fingerprint()`, `scat_tools.fingerprint("<narrative>", candidates=True)`',
    )
    p.add_argument("narrative", nargs="?", metavar="NARRATIVE", help="show this narrative only")
    p.add_argument(
        "--candidates",
        action="store_true",
        help="also show the candidates: pairs of nodes the account links that no row joins",
    )
    p = command(
        "edges",
        f"Show every edge of one type, with the narratives that tell it and its status. {scope}.",
        '`scat_tools.edge_table("<type>")`',
    )
    p.add_argument(
        "type",
        metavar="TYPE",
        help="one of: "
        + ", ".join(f"{s} ({e.from_type} then {e.to_type})" for s, e in TBOX.edge_types.items()),
    )
    p = command(
        "layered",
        "Show the layered view: the union of the fingerprints of the narratives named by --narrative, "
        "or, without it, of every narrative; with --candidates, also the candidates (pairs the account links that no row joins). "
        f"{scope}.",
        '`scat_tools.layered()`, `scat_tools.layered(["<narrative>"], candidates=True)`',
    )
    p.add_argument(
        "--narrative",
        action="append",
        metavar="NARRATIVE",
        help="include this narrative; repeat it for each narrative",
    )
    p.add_argument(
        "--candidates",
        action="store_true",
        help="also show the candidates: pairs of nodes the account links that no row joins",
    )
    p = command(
        "trace",
        "Follow edges from a node: up toward the groups, down toward the technologies, or both. "
        f"The node itself is left out. {scope}.",
        '`scat_tools.trace("<node>")`, `scat_tools.trace("<node>", "<direction>")`',
    )
    p.add_argument(
        "node", metavar="NODE", help="the name of a group, concern, affordance or technology"
    )
    p.add_argument(
        "--direction",
        default="both",
        metavar="DIRECTION",
        help="up, down or both (default: both)",
    )
    p = command(
        "evidence",
        "Show everything the vault says of one node page: the narratives that link it, each with the "
        "paragraph around every link and the linking sentence between >> and <<; its edges with the "
        f"narratives that tell them; and its adjacent nodes by layer. {scope}.",
        '`scat_tools.evidence("<node>")`',
    )
    p.add_argument(
        "node", metavar="NODE", help="the name of a group, concern, affordance or technology"
    )
    p = command(
        "copy-share",
        "Show, for each node page, the share of its five-word runs that appear word for word in a narrative, "
        "and the narratives they come from; the most repeated pages first. A high share is a prompt to look "
        "(`scat evidence`), not a fault. NODE is a name; without it, every node page. "
        f"{scope}.",
        '`scat_tools.copy_share()`, `scat_tools.copy_share("<node>")`',
    )
    p.add_argument(
        "node",
        nargs="?",
        metavar="NODE",
        help="the name of a group, concern, affordance or technology; without it, every node page",
    )
    command(
        "review",
        "Show where to look next: pairs of node pages of one type that may be one node (with the shared "
        "adjacent nodes, hubs marked, and the link texts coders used), and pages whose accounts tell them "
        "to different other ends, with the narratives grouped. A prompt to read, not a finding. "
        f"{scope}.",
        "`scat_tools.review()`",
    )
    command(
        "attribution",
        "Show the narratives by contributor: each contributor page with the narratives that name it, and "
        "the narratives that name none. Refuses where the vault's attribution mode is disallowed. "
        f"{scope}.",
        "`scat_tools.attribution()`",
    )
    p = command(
        "export-edges",
        "Write each edge table to DIR as `<type>.csv` and `<type>.md`. Overwrites a file only when its "
        "content differs; makes DIR if it is not there. Refuses where `scat edges` would, and then writes "
        "nothing.",
        '`scat_tools.export_edges("<dir>")`',
    )
    p.add_argument(
        "--out", required=True, metavar="DIR", help="the folder the tables go in (no default)"
    )
    p = command(
        "guide",
        "Show the guide of a lifecycle stage (plan, capture, code, analyse or report), or, without STAGE, "
        "the index of the stages and their moves. Needs no vault. Writes nothing.",
        '`scat_tools.guide()`, `scat_tools.guide("<stage>")`',
    )
    p.add_argument("stage", nargs="?", metavar="STAGE", help="the stage; without it, the index")
    drawing = sub.add_parser(
        "draw",
        help="Draw a view as an image (needs the extra `draw`): `.png` or `.svg`.",
        description="Draw a view as an image in columns by layer. Needs the extra `draw`: "
        '`pip install "scat-tools[draw]"`. The only write is the image file you name with --out.',
        epilog="REPL: `from scat_tools import draw`, then `draw.fingerprint(...)`, `draw.layered(...)` or `draw.trace(...)`",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    which = drawing.add_subparsers(dest="drawing", metavar="<drawing>", required=True)
    out_help = "the image file to write, ending in `.png` or `.svg` (no default)"
    p = command(
        "fingerprint",
        "Draw a narrative's fingerprint: its nodes and edges in columns that follow the narrative's kind; with --candidates, the "
        "candidates dashed. Refuses where `scat fingerprint` would, and then writes nothing.",
        '`draw.fingerprint("<narrative>", candidates=True).save("<file>")`',
        which,
    )
    p.add_argument("narrative", metavar="NARRATIVE", help="the narrative's name")
    p.add_argument(
        "--candidates",
        action="store_true",
        help="also draw the candidates: pairs the account links that no row joins, dashed",
    )
    p.add_argument("--out", required=True, metavar="FILE", help=out_help)
    p = command(
        "layered",
        "Draw the layered view of the narratives named by --narrative or, without it, of every "
        "narrative; with --candidates, the candidates dashed. Refuses where `scat layered` "
        "would, and then writes nothing.",
        '`draw.layered().save("<file>")`, `draw.layered(["<narrative>"], candidates=True).save("<file>")`',
        which,
    )
    p.add_argument(
        "--narrative",
        action="append",
        metavar="NARRATIVE",
        help="include this narrative; repeat it for each narrative",
    )
    p.add_argument(
        "--candidates",
        action="store_true",
        help="also draw the candidates: pairs the account links that no row joins, dashed",
    )
    p.add_argument("--out", required=True, metavar="FILE", help=out_help)
    p = command(
        "trace",
        "Draw what a node reaches: up toward the groups, down toward the technologies, or both, with the "
        "node itself in its column. Refuses where `scat trace` would, and then writes nothing.",
        '`draw.trace("<node>").save("<file>")`, `draw.trace("<node>", "<direction>").save("<file>")`',
        which,
    )
    p.add_argument(
        "node", metavar="NODE", help="the name of a group, concern, affordance or technology"
    )
    p.add_argument(
        "--direction",
        default="both",
        metavar="DIRECTION",
        help="up, down or both (default: both)",
    )
    p.add_argument("--out", required=True, metavar="FILE", help=out_help)
    return top


def run(args: argparse.Namespace):
    root = args.root
    match args.command:
        case "check":
            return scat_tools.check(args.page, neighborhood=args.neighborhood, root=root)
        case "status":
            return scat_tools.status(args.page, neighborhood=args.neighborhood, root=root)
        case "set-status":
            return scat_tools.set_status(args.page, args.status, root=root)
        case "index":
            return scat_tools.index(root=root)
        case "stub":
            return scat_tools.stub(args.name, args.type, root=root)
        case "record-edge":
            return scat_tools.record_edge(
                args.type, args.from_node, args.to_node, args.told_by, args.note, root=root
            )
        case "remove-edge":
            return scat_tools.remove_edge(args.from_node, args.to_node, args.told_by, root=root)
        case "merge":
            return scat_tools.merge(args.a, args.b, plan=args.plan, root=root)
        case "split-plan":
            return scat_tools.split_plan(args.a, root=root)
        case "stub-links":
            return scat_tools.stub_links(args.page, root=root)
        case "fingerprint":
            return scat_tools.fingerprint(args.narrative, candidates=args.candidates, root=root)
        case "edges":
            return scat_tools.edge_table(args.type, root=root)
        case "layered":
            return scat_tools.layered(args.narrative, candidates=args.candidates, root=root)
        case "trace":
            return scat_tools.trace(args.node, args.direction, root=root)
        case "evidence":
            return scat_tools.evidence(args.node, root=root)
        case "copy-share":
            return scat_tools.copy_share(args.node, root=root)
        case "review":
            return scat_tools.review(root=root)
        case "attribution":
            return scat_tools.attribution(root=root)
        case "export-edges":
            return scat_tools.export_edges(args.out, root=root)
        case "guide":
            return scat_tools.guide(args.stage)
        case "draw":
            match args.drawing:
                case "fingerprint":
                    made = draw.fingerprint(args.narrative, candidates=args.candidates, root=root)
                case "layered":
                    made = draw.layered(args.narrative, candidates=args.candidates, root=root)
                case "trace":
                    made = draw.trace(args.node, args.direction, root=root)
            return made.save(args.out) if isinstance(made, draw.Drawing) else made
    raise AssertionError(args.command)  # argparse requires a command


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    result = run(args)
    if args.json:
        print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
    else:
        print(result)
    return 0 if result.ok else 1


if __name__ == "__main__":
    sys.exit(main())
