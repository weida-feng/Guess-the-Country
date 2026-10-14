import json
import xml.etree.ElementTree as ET
from dataclasses import replace

import pytest

from mapguesser.data import load_countries


def test_all_165_catalog_entries_have_bilingual_names_and_valid_svg(countries):
    assert len(countries) == 165
    for country in countries:
        assert country.name_en and country.name_zh
        svg = ET.parse(country.map_path).getroot()
        assert svg.tag == "{http://www.w3.org/2000/svg}svg"
        assert svg.findall(".//{http://www.w3.org/2000/svg}path")


def test_missing_translation_falls_back_to_available_name(countries):
    country = countries[0]
    assert replace(country, name_en="").label("en") == country.name_zh
    assert replace(country, name_zh="").label("zh") == country.name_en


def write_catalog(tmp_path, countries, edits):
    records = [
        {"id": c.id, "name_en": c.name_en, "name_zh": c.name_zh, "source_name": c.source_name}
        for c in countries[:4]
    ]
    records[0].update(edits)
    path = tmp_path / "countries.json"
    path.write_text(json.dumps(records, ensure_ascii=False), encoding="utf-8")
    return path


@pytest.mark.parametrize("missing", ["name_en", "name_zh"])
def test_catalog_accepts_missing_translation(tmp_path, countries, missing):
    path = write_catalog(tmp_path, countries, {missing: None})
    loaded = load_countries(path, countries[0].map_path.parent)
    assert loaded[0].label("en")
    assert loaded[0].label("zh")


@pytest.mark.parametrize(
    ("edits", "message"),
    [
        ({"id": "../secret"}, "Invalid country ID"),
        ({"id": "albania"}, "Duplicate country ID"),
        ({"name_en": "", "name_zh": " "}, "display name"),
        ({"name_en": "Albania"}, "ambiguous"),
        ({"name_en": 0}, "must be a string"),
        ({"id": "missing-map"}, "Missing map"),
    ],
)
def test_catalog_reports_invalid_or_ambiguous_data(tmp_path, countries, edits, message):
    path = write_catalog(tmp_path, countries, edits)
    with pytest.raises(ValueError, match=message):
        load_countries(path, countries[0].map_path.parent)
