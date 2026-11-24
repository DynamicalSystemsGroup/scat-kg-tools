from pathlib import Path

import pytest

from scat_analysis import load_graph

HERE = Path(__file__).resolve().parent
CASE_STUDY = HERE.parent / "notebook" / "case-study"
SYNTHETIC = HERE.parent / "synth" / "vault"


@pytest.fixture(scope="session")
def case():
    return load_graph(CASE_STUDY)


@pytest.fixture(scope="session")
def synth():
    return load_graph(SYNTHETIC)
