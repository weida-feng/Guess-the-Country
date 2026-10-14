"""Load an explicit bilingual catalog with stable, filesystem-safe IDs."""

import json
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Country:
    id: str
    name_en: str
    name_zh: str
    source_name: str
    map_path: Path

    def label(self, language: str) -> str:
        """Fall back to the other language when a translation is unavailable."""
        if language == "en":
            return self.name_en or self.name_zh
        if language == "zh":
            return self.name_zh or self.name_en
        raise ValueError(f"Unsupported language: {language}")


def load_countries(catalog_path: Path, maps_dir: Path) -> tuple[Country, ...]:
    records = json.loads(catalog_path.read_text(encoding="utf-8"))
    if not isinstance(records, list):
        raise ValueError("The country catalog must be a list.")

    countries = []
    identifiers = set()
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("Each country must be an object.")
        identifier = record.get("id", "")
        if not isinstance(identifier, str) or not re.fullmatch(
            r"[a-z0-9]+(?:-[a-z0-9]+)*", identifier
        ):
            raise ValueError(f"Invalid country ID: {identifier!r}")
        if identifier in identifiers:
            raise ValueError(f"Duplicate country ID: {identifier}")
        identifiers.add(identifier)

        names = []
        for field in ("name_en", "name_zh"):
            value = record.get(field)
            value = "" if value is None else value
            if not isinstance(value, str):
                raise ValueError(f"{identifier}: {field} must be a string.")
            names.append(value.strip())
        if not any(names):
            raise ValueError(f"{identifier}: at least one display name is required.")

        source_name = record.get("source_name", "")
        if not isinstance(source_name, str) or not source_name.strip():
            raise ValueError(f"{identifier}: source_name is required for map generation.")
        map_path = maps_dir / f"{identifier}.svg"
        if not map_path.is_file():
            raise ValueError(f"Missing map for {identifier}: {map_path.name}")
        countries.append(Country(identifier, *names, source_name, map_path))

    if len(countries) < 4:
        raise ValueError("At least four countries are required for a quiz.")
    for language in ("en", "zh"):
        labels = [country.label(language) for country in countries]
        if len(labels) != len(set(labels)):
            raise ValueError(f"Duplicate display names in {language} would make answers ambiguous.")
    return tuple(countries)
