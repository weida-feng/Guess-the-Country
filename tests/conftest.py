from pathlib import Path

import pytest

from mapguesser.data import load_countries

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def countries():
    return load_countries(ROOT / "data/countries.json", ROOT / "assets/maps")
