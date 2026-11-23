"""Conformance checks: the rule catalogue as code (`contracts/rule-catalogue.md`).

    from scat_kg.vault import read_vault
    from scat_kg.checks import check_page, check_neighborhood, check_vault

    report = check_vault(read_vault("my-vault"))
    report.ok          # False when any error is present; warnings never block
    report.problems    # in the catalogue's order; each has rule, severity, file, where, what, fix

A rule is one small function in a module of this package, registered with `@page_rule` (reports on one page)
or `@vault_rule` (reports on the vault). `DEFERRED` lists the catalogue rules not implemented here yet.
"""

from scat_kg.checks import index_stale  # noqa: F401  (registers SCAT-INDEX-STALE)
from scat_kg.checks.ctx import DEFERRED, PAGE_RULES, VAULT_RULES, page_rule, vault_rule
from scat_kg.checks.problem import SEVERITY, Problem, Report
from scat_kg.checks.run import check_neighborhood, check_page, check_vault, neighborhood

__all__ = [
    "DEFERRED",
    "PAGE_RULES",
    "SEVERITY",
    "VAULT_RULES",
    "Problem",
    "Report",
    "check_neighborhood",
    "check_page",
    "check_vault",
    "neighborhood",
    "page_rule",
    "vault_rule",
]
