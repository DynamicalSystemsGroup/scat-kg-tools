"""List the catalogue's rule ids that have no seeded-defect test (WP5-R1). Expected: nothing.

    uv run python tests/scripts/rules_without_tests.py

A seeded-defect test is a test function named `test__<rule id, lower case, - as _>__<what is seeded>`
(the convention in tests/checks/test_coverage.py). This reads the catalogue's section 3 table and the test
files' function names (no test is run), prints one id per line, and exits 1 when any is listed.
"""

import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOGUE = ROOT / "contracts" / "rule-catalogue.md"
TESTS = ROOT / "tests"


def catalogue_ids() -> list[str]:
    text = CATALOGUE.read_text(encoding="utf-8")
    return re.findall(r"^\| (SCAT-[A-Z-]+) \| (?:error|warning) \|", text, re.MULTILINE)


def seeded_ids() -> set[str]:
    found = set()
    for path in sorted(TESTS.rglob("test_*.py")):
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                parts = node.name.split("__")
                if parts[0] == "test" and len(parts) >= 3 and parts[1].startswith("scat_"):
                    found.add(parts[1].upper().replace("_", "-"))
    return found


def rules_without_tests() -> list[str]:
    have = seeded_ids()
    return [i for i in catalogue_ids() if i not in have]


def main() -> int:
    missing = rules_without_tests()
    for rule in missing:
        print(rule)
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
