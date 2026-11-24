"""The rules about the vault as a whole: SCAT-CAP and SCAT-CAP-CONFIG (contract section 10)."""

import re

from scat_kg.checks import fixes
from scat_kg.checks.ctx import Ctx, vault_rule
from scat_kg.fix import FixOption

FILE = "scat.toml"
KEY = "stakeholder_group_cap"
WHERE = f"field `{KEY}`"


def _written(ctx: Ctx) -> str:
    """The value of the cap line as written in scat.toml (the reader keeps only a repr of it)."""
    text = (ctx.vault.root / FILE).read_bytes().decode("utf-8", errors="replace")
    m = re.search(r"^\s*stakeholder_group_cap\s*=\s*(.*?)\s*(?:#.*)?$", text, re.MULTILINE)
    return m.group(1) if m else (ctx.vault.config.detail or "")


@vault_rule
def cap_config(ctx: Ctx):
    cfg = ctx.vault.config
    if cfg.problem is None:
        return []
    n = len(ctx.groups)
    value = _written(ctx) if cfg.problem == "bad-value" else ""
    what = {
        "missing": "the file is missing",
        "invalid-toml": f"the file is not valid TOML: {cfg.detail}",
        "key-missing": "the key is missing",
        "bad-value": f"the value `{value}` is not a TOML integer of 1 or more",
    }[cfg.problem]
    verb = (
        f"replace the line `stakeholder_group_cap = {value}` with"
        if cfg.problem == "bad-value"
        else "add the line"
    )
    least = f", so choose at least {n}" if n >= 1 else ""
    slot = "<number you choose>"
    fix = fixes.single(
        fixes.option(
            "slot",
            f"{verb} `stakeholder_group_cap = {slot}` (author) in scat.toml; choose a whole "
            f"number of 1 or more (the vault has {n} stakeholder-group pages now{least})",
            fixes.set_field(FILE, KEY, slot, author_slot=slot),
        )
    )
    return [ctx.problem("SCAT-CAP-CONFIG", FILE, WHERE, what, fix, on=KEY)]


@vault_rule
def cap(ctx: Ctx):
    cap_value, n = ctx.vault.config.cap, len(ctx.groups)
    if cap_value is None or n <= cap_value:
        return []
    names = ", ".join(sorted(p.name for p in ctx.groups))
    fix = fixes.alternatives(
        [
            FixOption(
                "manual",
                f"cluster {n - cap_value} group(s) into the others, by shared standpoint: move their "
                "standpoints into another group's `description`, change every link to them to point "
                "at that group, and delete those pages",
            ),
            fixes.option(
                "exact",
                f"or, only if the plan allows more groups, write `stakeholder_group_cap = {n}` in "
                "scat.toml (the cap protects against identifying individuals)",
                fixes.set_field(FILE, KEY, n),
            ),
        ]
    )
    what = f"the vault holds {n} stakeholder-group pages, over the cap of {cap_value}: {names}"
    return [ctx.problem("SCAT-CAP", FILE, WHERE, what, fix, on=KEY)]
