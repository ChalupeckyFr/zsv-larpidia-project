"""Zmrazí zvolenou variantu obrysu jako kanonickou geometrii atlasu.

Použití:  python atlas/scripts/freeze_outline.py B
Zkopíruje work/outline/variants/<X>/ → current/geometry/ pod kanonickými názvy a zapíše outline_FROZEN.json.
Další fáze (reliéf, lidská vrstva, registr, SVG) čtou už jen `current/geometry/outline_coast.json`.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from canon import ATLAS  # noqa: E402

key = sys.argv[1]
src = ATLAS / "work" / "outline" / "variants" / key
dst = ATLAS / "current" / "geometry"
dst.mkdir(parents=True, exist_ok=True)
names = {
    f"outline_{key}.svg": "outline.svg",
    f"outline_{key}_local_km.geojson": "outline_local_km.geojson",
    f"outline_{key}_pseudo_wgs84.geojson": "outline_pseudo_wgs84.geojson",
    f"outline_{key}_coast.json": "outline_coast.json",
    f"outline_{key}_report.json": "outline_report.json",
}
for a, b in names.items():
    shutil.copy2(src / a, dst / b)
report = json.loads((dst / "outline_report.json").read_text(encoding="utf-8"))
meta = {
    "frozen_variant": key, "frozen_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
    "decision": "R-06: tým zvolil variantu B (členitější) dne 2026-10-23",
    "seed": report["noise"]["seed"], "deviations": report["deviations"],
    "coast_sha256": hashlib.sha256((dst / "outline_coast.json").read_bytes()).hexdigest(),
    "main_area_km2": report["main"]["area_km2"], "para_area_km2": report["para"]["area_km2"], "strait_km": report["strait_km"],
}
(dst / "outline_FROZEN.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
print("Zmrazeno:", key, meta["coast_sha256"][:12], f"{meta['main_area_km2']} / {meta['para_area_km2']} km², průliv {meta['strait_km']} km")
