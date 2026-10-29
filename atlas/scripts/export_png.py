"""Volitelný export SVG map do PNG (náhledy ke sdílení) přes bezhlavý Edge/Chrome, pokud je v počítači.

Spuštění:  python atlas/scripts/export_png.py
Výstup:    atlas/current/capital/capital_plan_base.png (2970 × 2100 px),
           atlas/current/svg/png/larpidia_atlas_{master,physical,political,status}.png (2970 × 2100 px)
Bez nainstalovaného prohlížeče skript nic neudělá (SVG zůstávají hlavním výstupem).
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from canon import ATLAS

BROWSERS = [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe", r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Google\Chrome\Application\chrome.exe", r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"]


def find_browser():
    return next((b for b in BROWSERS if Path(b).exists()), None)


def export(svg: Path, png: Path, exe: str, w_px=5940, h_px=4200, scale=0.5):
    """SVG se vloží do prázdné stránky jako <img> o velikosti w_px × h_px a zachytí se při měřítku `scale`."""
    html = f"<!doctype html><html><head><meta charset='utf-8'></head><body style='margin:0;background:#fff'><img src='{svg.resolve().as_uri()}' style='width:{w_px}px;height:{h_px}px;display:block'></body></html>"
    with tempfile.TemporaryDirectory() as td:
        page = Path(td) / "wrap.html"
        page.write_text(html, encoding="utf-8")
        png.parent.mkdir(parents=True, exist_ok=True)
        if png.exists():
            png.unlink()
        # vlastní profil prohlížeče: bez něj může Edge předat příkaz už běžící instanci a skončit bez snímku
        subprocess.run([exe, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--user-data-dir={Path(td) / 'profile'}", "--no-first-run", "--virtual-time-budget=20000",
                        f"--force-device-scale-factor={scale}", f"--window-size={w_px},{h_px}", f"--screenshot={png}", page.resolve().as_uri()], capture_output=True, timeout=240)
    return png.exists()


def main():
    exe = find_browser()
    if not exe:
        print("export PNG: prohlížeč (Edge/Chrome) nenalezen – přeskočeno")
        return 0
    cur = ATLAS / "current"
    jobs = [(cur / "capital" / "capital_plan_base.svg", cur / "capital" / "capital_plan_base.png")]
    for v in ("master", "physical", "political", "status"):
        s = cur / "svg" / f"larpidia_atlas_{v}_embedded.svg"
        if s.exists():
            jobs.append((s, cur / "svg" / "png" / f"larpidia_atlas_{v}.png"))
    for svg, png in jobs:
        ok = export(svg, png, exe)
        print(("OK    " if ok else "CHYBA ") + str(png.relative_to(ATLAS)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
