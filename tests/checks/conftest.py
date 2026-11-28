"""WP11-R1 and R2 over every check test (see tests/machine/scat_harness.py): every Report a test produces is
validated against the machine-interface schema, and a sample of its fix commands is run or parsed."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "machine"))
import scat_harness

from scat_tools.checks import run as checks_run


@pytest.fixture(autouse=True)
def _schema_and_fix_harness(monkeypatch, request):
    monkeypatch.setattr(checks_run, "_run", scat_harness.wrap(checks_run._run))
    scat_harness.tests_seen.add(request.node.nodeid)
    yield
