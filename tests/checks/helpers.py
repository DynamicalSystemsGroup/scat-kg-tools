"""A clean fixture vault for the seeded-defect tests, and the helpers that compare messages to golden ones.

Every seeded test starts from `base()` (which checks with zero messages), changes exactly one thing, and expects
exactly the messages it names: nothing more. A golden message is the whole text `scat check` prints for it: the
head line (severity, rule id, place, where, what) and the fix.
"""

import re
from pathlib import Path

from scat_kg.checks import check_neighborhood, check_page, check_vault
from scat_kg.vault import read_vault

ROOT = Path(__file__).parents[2]
EXAMPLES = ROOT / "contracts" / "examples"
CATALOGUE = ROOT / "contracts" / "rule-catalogue.md"

HEADER = "| from | type | to | note |"
SEP = "|---|---|---|---|"


def doc(type_, title, *, status="done", description="D", extra="", body="") -> str:
    """A page. `description` None leaves it out; `status` None leaves it out."""
    lines = ["---", f"type: {type_}"]
    if status is not None:
        lines.append(f"status: {status}")
    lines.append(f'title: "{title}"')
    if description is not None:
        lines.append(f'description: "{description}"')
    if extra:
        lines.append(extra.rstrip("\n"))
    lines.append("---")
    return "\n".join(lines) + "\n" + body


def row(type_, a, b, note="") -> str:
    return f"| [[{a}]] | {type_} | [[{b}]] | {note} |".replace("|  |", "| |")


def table(*rows, header=HEADER, sep=SEP) -> str:
    """The `Edges told` section: heading on a line of its own, then the header, the separator and the rows.
    A `None` header or separator is left out. In `narrative()` the header is on line 14."""
    lines = ["## Edges told", ""]
    if header is not None:
        lines.append(header)
    if sep is not None:
        lines.append(sep)
    lines.extend(rows)
    return "\n".join(lines) + "\n"


ACCOUNT = (
    "The [[staff]] on the desk said [[safe-handling|safe handling]] matters. The [[borrowers]] wanted "
    "[[quick-checkout|a quick checkout]] and the [[self-checkout|self checkout]] stand.\n"
)
DESK_ROWS = (
    row("holds", "staff", "safe-handling"),
    row("holds", "borrowers", "quick-checkout", "Twice."),
    row("is addressed by", "quick-checkout", "self-checkout"),
)


def narrative(
    title="Desk day",
    *,
    status="done",
    kind="scenario",
    timeframe="past",
    description="D",
    rows=DESK_ROWS,
    account=ACCOUNT,
    section=None,
    extra="",
) -> str:
    """A narrative whose `## Edges told` heading is on line 12, its header on line 14, its separator on 15 and
    row n on line 15 + n (when every optional line is present). `section` replaces the whole table section."""
    lines = ["---", "type: narrative"]
    if kind:
        lines.append(f"kind: {kind}")
    if status is not None:
        lines.append(f"status: {status}")
    lines.append(f'title: "{title}"')
    if description is not None:
        lines.append(f'description: "{description}"')
    if timeframe is not None:
        lines.append(f"timeframe: {timeframe}")
    lines.append("---")
    head = "\n".join(lines) + "\n\n" + account + "\n"
    return head + (table(*rows) if section is None else section) + extra


def base() -> dict[str, str]:
    """A small vault with a page of every type, all `done`, and no message from any rule."""
    return {
        "scat.toml": "stakeholder_group_cap = 3\n",
        "group/staff.md": doc("group", "Staff"),
        "group/borrowers.md": doc("group", "Borrowers"),
        "concern/safe-handling.md": doc("concern", "Safe handling"),
        "concern/quick-checkout.md": doc("concern", "Quick checkout"),
        "concern/careful-keeping.md": doc(
            "concern",
            "Careful keeping",
            body="\nPulls against [[quick-checkout]]: a loan written down takes time.\n",
        ),
        "affordance/self-checkout.md": doc("affordance", "Self checkout"),
        "affordance/briefing.md": doc("affordance", "Briefing"),
        "technology/booking-app.md": doc("technology", "Booking app"),
        DESK: narrative(),
        KIOSK: narrative(
            "Kiosk pitch",
            kind="architecture",
            timeframe="future",
            account=(
                "A kiosk gives [[quick-checkout|a quick checkout]]: the [[booking-app|booking app]] "
                "records the loan, which is the [[self-checkout|self checkout]].\n"
            ),
            rows=(
                row("addressed-by", "quick-checkout", "self-checkout", "Cuts the queue."),
                row("provided-by", "self-checkout", "booking-app"),
            ),
        ),
    }


DESK = "narrative/desk-day.md"
KIOSK = "narrative/kiosk-pitch.md"


def vault(make_vault, overrides=None, remove=()):
    """The fixture vault with the overrides applied (a path removed with `remove` stays missing)."""
    files = base()
    files.update(overrides or {})
    for r in remove:
        files.pop(r)
    return read_vault(make_vault(files))


def catalogue_severities() -> dict[str, str]:
    """Rule id -> severity, as the catalogue's table in section 3 states them."""
    return dict(
        re.findall(r"^\| (SCAT-[A-Z-]+) \| (error|warning) \|", CATALOGUE.read_text(), re.MULTILINE)
    )


def run(v, scope="vault", page=None):
    if scope == "vault":
        return check_vault(v)
    if scope == "page":
        return check_page(v, page)
    return check_neighborhood(v, page)


def report_of(make_vault, overrides=None, remove=(), scope="vault", page=None):
    return run(vault(make_vault, overrides, remove), scope, page)


def rules_of(report) -> list[str]:
    return [p.rule for p in report.problems]


def seeded(make_vault, overrides=None, *expected, remove=(), scope="vault", page=None):
    """Check the vault at `scope` and expect exactly the `expected` messages, each as `scat check` prints it."""
    report = run(vault(make_vault, overrides, remove), scope, page)
    assert [p.render() for p in report.problems] == list(expected), "\n" + report.render()
    stated = catalogue_severities()
    assert all(p.severity == stated[p.rule] for p in report.problems)  # at the catalogue's severity
    return report


def pair(stem, status, rest) -> str:
    """A pair message: the head line `<severity> [SCAT-<DRAFT|DONE>-<stem>] <rest>`, as the narrative's
    `status` makes it (a warning while `stub` or `draft`, an error at `done`)."""
    done = status == "done"
    return f"{'error' if done else 'warning'} [SCAT-{'DONE' if done else 'DRAFT'}-{stem}] {rest}"


def msg(head: str, *fix: str) -> str:
    """A message as `scat check` prints it: the head line, then each fix line indented two spaces."""
    return "\n".join([head, *(f"  {line}" for line in fix)])


def set_status(name, status="draft"):
    return f'`scat set-status {name} {status}` (REPL: `scat_kg.set_status("{name}", "{status}")`)'


def stub(name, key):
    return f'`scat stub {name} --type {key}` (REPL: `scat_kg.stub("{name}", type="{key}")`)'


def choose(*options, head="Fix, choose one:") -> list[str]:
    """The fix lines of alternatives, for `msg`: the head, then each option numbered and indented."""
    return [head, *(f"  {i}. {o}" for i, o in enumerate(options, 1))]


def line_of(text: str, needle: str) -> int:
    """The 1-based line of the first line containing `needle`."""
    return next(i for i, ln in enumerate(text.split("\n"), 1) if needle in ln)


def uncoded(file) -> str:
    """The SCAT-UNCODED message (WP21-G2) of a narrative that links no node page."""
    return msg(
        f"warning [SCAT-UNCODED] {file} body: the narrative links no node page, so it is excluded from the knowledge graph and every view",
        *choose(
            "link a node page where the account names one, as `[[<node-name>]]` (or list it under a "
            "heading such as `Linked beyond the text`); a node the account names with no edge needs "
            "only this link",
            "or tell an edge: a row of the table whose ends are links to node pages; if the node has "
            "no page, `scat stub <name> --type <type>` makes one",
        ),
    )
