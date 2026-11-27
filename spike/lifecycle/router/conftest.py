import pytest
from lc_harness import MEAS


@pytest.fixture(scope="session", autouse=True)
def _fresh_measurements():
    MEAS.unlink(missing_ok=True)
    yield
