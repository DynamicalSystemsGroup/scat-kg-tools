"""A clean fixture vault for the seeded-defect tests, and the helpers that compare messages to golden ones.

Every seeded test starts from `base()` (which checks with zero messages), changes exactly one thing, and
expects exactly the messages it names: nothing more. A golden message is the four elements D-032 says to
compare: rule id, file, field or link, and the exact fix.
"""

import re
from pathlib import Path

from scat_kg.checks import check_neighborhood, check_page, check_vault
from scat_kg.ops.index import class_page_text, index_region
from scat_kg.ops.names import CLASS_PAGES
from scat_kg.vault import read_vault

ROOT = Path(__file__).parents[2]
EXAMPLES = ROOT / "contracts" / "examples"
CATALOGUE = ROOT / "contracts" / "rule-catalogue.md"


def doc(type_, title, *, status="done", description="D", extra="", body="") -> str:
    """A page. `description` None leaves it out; `status` None leaves it out (class pages)."""
    lines = ["---", f"type: {type_}"]
    if status is not None:
        lines.append(f"status: {status}")
    lines.append(f'title: "{title}"')
    if description is not None:
        lines.append(f'description: "{description}"')
    lines.append(extra.rstrip("\n")) if extra else None
    lines.append("---")
    return "\n".join(lines) + "\n" + body


def links(key, *names) -> str:
    return f"{key}:\n" + "".join(f'  - "[[{n}]]"\n' for n in names)


def base() -> dict[str, str]:
    """A small vault with a page of every type but class, all `done`, and no message from any rule."""
    return {
        "scat.toml": "stakeholder_group_cap = 3\n",
        "stakeholder-group/staff.md": doc("stakeholder-group", "Staff"),
        "stakeholder-group/borrowers.md": doc("stakeholder-group", "Borrowers"),
        "concern/safe-handling.md": doc("concern", "Safe handling"),
        "concern/quick-checkout.md": doc("concern", "Quick checkout"),
        "concern/careful-keeping.md": doc(
            "concern", "Careful keeping", extra=links("conflicts", "quick-checkout")
        ),
        "affordance/self-checkout.md": doc("affordance", "Self checkout"),
        "affordance/briefing.md": doc("affordance", "Briefing"),
        "technology/booking-app.md": doc("technology", "Booking app"),
        "heldby/staff-holds-safe-handling.md": doc(
            "heldby",
            "Staff holds Safe handling",
            extra='group: "[[staff]]"\nconcern: "[[safe-handling]]"',
        ),
        "addresses/self-checkout-addresses-quick-checkout.md": doc(
            "addresses",
            "Self checkout addresses Quick checkout",
            extra='concern: "[[quick-checkout]]"\naffordance: "[[self-checkout]]"',
        ),
        "attributes/self-checkout-attributed-to-booking-app.md": doc(
            "attributes",
            "Self checkout attributed to Booking app",
            extra='affordance: "[[self-checkout]]"\ntechnology: "[[booking-app]]"',
        ),
        "scenario-raw/desk-day.md": doc(
            "scenario-raw",
            "Desk day",
            extra="timeframe: past\n" + links("coded", "desk-day-coded"),
        ),
        "scenario-coded/desk-day-coded.md": doc(
            "scenario-coded",
            "Desk day, coded",
            extra=links("raw", "desk-day")
            + links("groups", "staff")
            + links("concerns", "safe-handling")
            + links("affordances", "self-checkout"),
        ),
        "architecture-raw/kiosk-pitch.md": doc(
            "architecture-raw",
            "Kiosk pitch",
            extra="timeframe: future\n" + links("coded", "kiosk-pitch-coded"),
        ),
        "architecture-coded/kiosk-pitch-coded.md": doc(
            "architecture-coded",
            "Kiosk pitch, coded",
            extra=links("raw", "kiosk-pitch")
            + links("concerns", "quick-checkout")
            + links("affordances", "self-checkout")
            + links("technologies", "booking-app"),
        ),
    }


def vault(make_vault, overrides=None, remove=()):
    """The fixture vault with the overrides applied, plus the class pages `index` would write.

    A class page the test supplies (or removes with `remove`, then it stays missing) is left as given.
    """
    files = base()
    files.update(overrides or {})
    for r in remove:
        files.pop(r)
    root = make_vault(files)
    v = read_vault(root)
    for name in CLASS_PAGES:
        path = f"class/{name}.md"
        if path not in files and path not in remove:
            (root / "class").mkdir(exist_ok=True)
            (root / path).write_text(class_page_text(name, index_region(v, name)), encoding="utf-8")
    return read_vault(root)


def report_of(make_vault, overrides=None, remove=(), scope="vault", page=None):
    return run(vault(make_vault, overrides, remove), scope, page)


def region_for(make_vault, name):
    """The generated region of class page `name` for the fixture vault: a seeded class page that is
    meant to be current (so SCAT-INDEX-STALE has nothing to say about it) ends with this."""
    return index_region(vault(make_vault), name)


def catalogue_severities() -> dict[str, str]:
    """Rule id -> severity, as the catalogue's table in section 3 states them."""
    return dict(
        re.findall(r"^\| (SCAT-[A-Z-]+) \| (error|warning) \|", CATALOGUE.read_text(), re.MULTILINE)
    )


def got(report) -> list[tuple]:
    return [p.elements for p in report.problems]


def seeded(make_vault, overrides=None, *expected, remove=(), scope="vault", page=None):
    """Check the vault at `scope` and expect exactly `expected` (rule, file, where, fix) messages."""
    v = vault(make_vault, overrides, remove)
    report = run(v, scope, page)
    assert got(report) == list(expected), "\n" + report.render()
    stated = catalogue_severities()
    assert all(p.severity == stated[p.rule] for p in report.problems)  # at the catalogue's severity
    return report


def run(v, scope="vault", page=None):
    if scope == "vault":
        return check_vault(v)
    if scope == "page":
        return check_page(v, page)
    return check_neighborhood(v, page)


# The catalogue's operation phrases, written out once (section 1, "Operations the fixes name").
def set_status(name, status="draft"):
    return f'`scat set-status {name} {status}` (REPL: `scat_kg.set_status("{name}", "{status}")`)'


def stub(name, key):
    return f'`scat stub {name} --type {key}` (REPL: `scat_kg.stub("{name}", type="{key}")`)'


def lines(*rows) -> str:
    """A block of YAML lines inside a fix, indented as the catalogue shows them."""
    return "\n".join("       " + r for r in rows)


def choose(*options) -> str:
    return "\n".join(["Fix, choose one:"] + [f"  {i}. {o}" for i, o in enumerate(options, 1)])


def line_of(text: str, needle: str) -> int:
    """The 1-based line of the first line containing `needle`."""
    return next(i for i, ln in enumerate(text.split("\n"), 1) if needle in ln)


def coded(status="done", **override) -> str:
    """The base coded scenario, with any of its four link blocks replaced (or left out with "")."""
    parts = {
        "raw": links("raw", "desk-day"),
        "groups": links("groups", "staff"),
        "concerns": links("concerns", "safe-handling"),
        "affordances": links("affordances", "self-checkout"),
        "extra": "",
        "body": "",
    }
    parts.update(override)
    body = parts.pop("body")
    return doc(
        "scenario-coded", "Desk day, coded", status=status, extra="".join(parts.values()), body=body
    )


SC = "scenario-coded/desk-day-coded.md"
AC = "architecture-coded/kiosk-pitch-coded.md"
HELDBY = "heldby/staff-holds-safe-handling.md"
ATTR = "attributes/self-checkout-attributed-to-booking-app.md"
