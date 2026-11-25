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
        "Rewrite the generated table of every class page, creating a missing class page.",
        "`scat_kg.index()`",
    )
    p = command(
        "stub",
        "Create a stub page (a concern, affordance, technology, stakeholder-group or record page).",
        '`scat_kg.stub("<page-name>", type="<type-key>")`',
    )
    p.add_argument("name", metavar="NAME", help="the new page's name: a-z, 0-9 and hyphens")
    p.add_argument(
        "--type",
        required=True,
        metavar="TYPE",
        help="the page type key, one of: " + ", ".join(STUBBABLE),
    )
    p = command(  # TODO(WP16-U7): there are no relation pages now; record-edge replaces this
        "stub-pair",
        "Create the relation page for a pair, stubbing an endpoint that does not exist.",
        '`scat_kg.stub_pair("<relation>", "<endpoint-a>", "<endpoint-b>")`',
    )
    p.add_argument(
        "relation",
        metavar="RELATION",
        help="one of: "
        + ", ".join(f"{s} ({e.from_type} then {e.to_type})" for s, e in TBOX.edge_types.items()),
    )
    p.add_argument("endpoint_a", metavar="ENDPOINT-A")
    p.add_argument("endpoint_b", metavar="ENDPOINT-B")
    p = command(
        "stub-links",
        "Create the pages that link fields name and the vault lacks. PAGE limits it to one page.",
        '`scat_kg.stub_links()`, `scat_kg.stub_links("<page>")`',
    )
    p.add_argument("page", nargs="?", metavar="PAGE", help="look at this page's links only")
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
        case "stub-pair":
            return scat_kg.stub_pair(args.relation, args.endpoint_a, args.endpoint_b, root=root)
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
