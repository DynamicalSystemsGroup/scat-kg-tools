"""The readers of the lifecycle's detect predicates: each evaluates one named condition on the vault now.

A reader is keyed by the detect's name in the lifecycle instance (`detects`) and returns `(holds, detail)`.
A detect is advice: nothing here moves a stage (contracts/lifecycle.md, section 1).
"""

from pathlib import Path

import scat_kg

NARRATIVES_DONE = "every narrative is done and the whole-vault check has no errors"


def narratives_done(root: Path) -> tuple[bool, str]:
    """Holds when there is at least one narrative, every narrative is `done`, and the check has no errors."""
    status = scat_kg.status(root=root)
    if not status.ok:
        return False, "the vault could not be read: " + "; ".join(r.why for r in status.refused)
    narratives = [r for r in status.rows if r.type == "narrative"]
    done = sum(r.status == "done" for r in narratives)
    check = scat_kg.check(root=root)
    if not check.ok and not hasattr(check, "errors"):
        return False, "the check could not run: " + "; ".join(r.why for r in check.refused)
    errors = len(check.errors)
    plural = "error" if errors == 1 else "errors"
    if not narratives:
        return False, f"there are no narratives; the check has {errors} {plural}"
    detail = f"{done} of {len(narratives)} narratives done; the check has {errors} {plural}"
    return done == len(narratives) and errors == 0, detail


READERS = {NARRATIVES_DONE: narratives_done}


def evaluate(name: str, root: Path) -> tuple[bool, str]:
    """The reader of the detect `name`, run on the vault at `root`."""
    return READERS[name](Path(root))
