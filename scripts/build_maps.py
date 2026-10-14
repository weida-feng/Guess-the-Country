"""Rebuild SVG outlines from the bundled Natural Earth shapefile."""

import argparse
import json
from pathlib import Path

import geopandas as gpd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "assets/maps")
    args = parser.parse_args()

    catalog = json.loads((ROOT / "data/countries.json").read_text(encoding="utf-8"))
    shapes = gpd.read_file(ROOT / "data/source/ne_10m_admin_0_map_units.shp")
    # Check every source name before writing any files.
    source_names = set(shapes["NAME"])
    missing = [
        record["source_name"] for record in catalog if record["source_name"] not in source_names
    ]
    if missing:
        parser.error(f"No geometry found for: {', '.join(missing)}")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    for record in catalog:
        country = shapes.loc[shapes["NAME"] == record["source_name"]]
        fig, ax = plt.subplots(figsize=(5, 3.5))
        try:
            country.plot(ax=ax, color="#d3d3d3", edgecolor="#172b35", linewidth=0.7)
            ax.set_axis_off()
            fig.savefig(
                args.output_dir / f"{record['id']}.svg",
                format="svg",
                bbox_inches="tight",
                metadata={"Date": None},
            )
        finally:
            plt.close(fig)
    print(f"Generated {len(catalog)} maps in {args.output_dir}")


if __name__ == "__main__":
    main()
