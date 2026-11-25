"""The `scat` command: a thin layer over the Python API (`scat_kg`). Same operations, same messages.

Exit code 0 when there is no error and no refusal (warnings alone are 0), 1 otherwise, 2 for a command
line that cannot be read. Every command takes `--root` (the vault folder; default: the current directory).
"""

import argparse
import json
import sys
from collections.abc import Sequence

import scat_kg
from scat_kg.ops.names import STUBBABLE
from scat_kg.tbox import TBOX


def _parser() -> argparse.ArgumentParser:
    top = argparse.ArgumentParser(
        prog="scat",
        description="Check and work on a SCAT knowledge-graph vault. Every command has a REPL twin "
        "(`import scat_kg`) that gives the same messages.",
        epilog="Run `scat <command> --help` for a command.",
    )
    sub = top.add_subparsers(dest="command", metavar="<command>", required=True)

    def command(name, summary, twin):
        p = sub.add_parser(
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
        '`scat_kg.check()`, `scat_kg.check("<page>")`, `scat_kg.check("<page>", neighborhood=True)`',
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
        '`scat_kg.status()`, `scat_kg.status("<page>")`, `scat_kg.status("<page>", neighborhood=True)`',
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
        '`scat_kg.set_status("<page-name>", "<status>")`',
    )
    p.add_argument("page", metavar="PAGE", help="the page's name or path")
    p.add_argument("status", metavar="STATUS", help="stub, draft or done")
    command(
        "index",
        "Write the Base file `index/<type>.base` of each type that has none. Never rewrites one.",
        "`scat_kg.index()`",
    )
    p = command(
        "stub",
        "Create a stub page: a node (group, concern, affordance or technology) or a narrative.",
        '`scat_kg.stub("<page-name>", type="<type>")`',
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
        '`scat_kg.stub_links()`, `scat_kg.stub_links("<page>")`',
    )
    p.add_argument("page", nargs="?", metavar="PAGE", help="look at this page's links only")
    p = command(
        "record-edge",
        "Record an edge: add its row to each narrative named by --told-by that has none, stubbing a "
        "missing node or narrative. Leaves the links as they are. Refuses a narrative that is done.",
        '`scat_kg.record_edge("<type>", "<from>", "<to>", ["<narrative>"], note="<text>")`',
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
        '`scat_kg.remove_edge("<from>", "<to>")`, `scat_kg.remove_edge("<from>", "<to>", ["<narrative>"])`',
    )
    p.add_argument("from_node", metavar="FROM", help="the name of the node at the first end")
    p.add_argument("to_node", metavar="TO", help="the name of the node at the second end")
    p.add_argument(
        "--told-by",
        action="append",
        metavar="NARRATIVE",
        help="remove the rows of this narrative only; repeat it for each narrative",
    )
    return top


def run(args: argparse.Namespace):
    root = args.root
    match args.command:
        case "check":
            return scat_kg.check(args.page, neighborhood=args.neighborhood, root=root)
        case "status":
            return scat_kg.status(args.page, neighborhood=args.neighborhood, root=root)
        case "set-status":
            return scat_kg.set_status(args.page, args.status, root=root)
        case "index":
            return scat_kg.index(root=root)
        case "stub":
            return scat_kg.stub(args.name, args.type, root=root)
        case "record-edge":
            return scat_kg.record_edge(
                args.type, args.from_node, args.to_node, args.told_by, args.note, root=root
            )
        case "remove-edge":
            return scat_kg.remove_edge(args.from_node, args.to_node, args.told_by, root=root)
        case "stub-links":
            return scat_kg.stub_links(args.page, root=root)
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
