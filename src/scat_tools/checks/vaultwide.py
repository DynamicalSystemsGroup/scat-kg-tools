"""The rules about the vault as a whole: SCAT-MODE-CONFIG, SCAT-CAP, SCAT-CAP-CONFIG, SCAT-SUGGEST-CONFIG
(contract section 10)."""

import re

from scat_tools.checks import fixes
from scat_tools.checks.ctx import Ctx, vault_rule
from scat_tools.fix import FixOption
from scat_tools.vault import ATTRIBUTION_KEY, MODES

FILE = "scat.toml"
KEY = "stakeholder_group_cap"
SUGGEST_KEY = "link_suggestions"
WHERE = f"field `{KEY}`"


def _written(ctx: Ctx, key: str = KEY) -> str:
    """The value of a line as written in scat.toml (the reader keeps only a repr of it)."""
    text = (ctx.vault.root / FILE).read_bytes().decode("utf-8", errors="replace")
    m = re.search(rf"^\s*{key}\s*=\s*(.*?)\s*(?:#.*)?$", text, re.MULTILINE)
    return m.group(1) if m else (ctx.vault.config.detail or "")


MODE_CHOICES = {
    "required": "a `done` narrative must name who it is attributed to",
    "optional": "a narrative may name who it is attributed to",
    "disallowed": "no narrative names who it is attributed to",
}


@vault_rule
def mode_config(ctx: Ctx):
    """The attribution mode is declared and known; read before the rest of the config (contract section 10)."""
    cfg = ctx.vault.config
    if cfg.attribution_problem is None:
        return []
    if cfg.attribution_problem == "key-missing":
        what, verb = "the key is missing", "add the line"
    else:
        written = _written(ctx, ATTRIBUTION_KEY)
        what = f"the value `{written}` is not one of `required`, `optional`, `disallowed`"
        verb = f"replace the line `{ATTRIBUTION_KEY} = {written}` with"
    options = []
    for i, mode in enumerate(MODES):
        lead = f"{verb} " if i == 0 else "or with "
        options.append(
            fixes.option(
                "exact",
                f'{lead}`{ATTRIBUTION_KEY} = "{mode}"` ({MODE_CHOICES[mode]})'
                + (" in scat.toml" if i == 0 else ""),
                fixes.set_field(FILE, ATTRIBUTION_KEY, mode),
            )
        )
    where = f"field `{ATTRIBUTION_KEY}`"
    return [
        ctx.problem(
            "SCAT-MODE-CONFIG", FILE, where, what, fixes.alternatives(options), on=ATTRIBUTION_KEY
        )
    ]


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
            f"number of 1 or more (the vault has {n} group pages now{least})",
            fixes.set_field(FILE, KEY, slot, author_slot=slot),
        )
    )
    return [ctx.problem("SCAT-CAP-CONFIG", FILE, WHERE, what, fix, on=KEY)]


@vault_rule
def suggest_config(ctx: Ctx):
    bad = ctx.vault.config.link_suggestions_bad
    if bad is None:
        return []
    written = _written(ctx, SUGGEST_KEY)
    what = f"the value `{written}` is not a TOML boolean, `true` or `false`"
    fix = fixes.alternatives(
        [
            fixes.option(
                "exact",
                f"replace the line `{SUGGEST_KEY} = {written}` with `{SUGGEST_KEY} = true` "
                "(show the link suggestions)",
                fixes.set_field(FILE, SUGGEST_KEY, True),
            ),
            fixes.option(
                "exact",
                f"or with `{SUGGEST_KEY} = false` (the default: no link suggestions)",
                fixes.set_field(FILE, SUGGEST_KEY, False),
            ),
        ]
    )
    where = f"field `{SUGGEST_KEY}`"
    return [ctx.problem("SCAT-SUGGEST-CONFIG", FILE, where, what, fix, on=SUGGEST_KEY)]


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
    what = f"the vault holds {n} group pages, over the cap of {cap_value}: {names}"
    return [ctx.problem("SCAT-CAP", FILE, WHERE, what, fix, on=KEY)]
