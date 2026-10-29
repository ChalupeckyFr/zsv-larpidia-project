"""Ověří, že obrázek vygenerovaný externím nástrojem drží tvar ostrova z atlasu (IoU masky souše).

Použití:
    python atlas/scripts/verify_sat.py S-01 cesta/k/vygenerovanemu.png [--threshold 0.95] [--overlay out.png]
    python atlas/scripts/verify_sat.py S-01 --self          # kontrola vlastního renderu atlasu

Postup: obraz se přepočte na rozměr reference, voda (moře i jezero) se rozpozná podle převahy modré/tyrkysové,
výsledek se vyčistí mediánovým filtrem a porovná s referenční maskou. Počítá IoU souše, poměr ploch, posun těžiště
a nejlepší celočíselný posun (zjištění chybného zarovnání). Návratový kód 0 = shoda ≥ prahu.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
RENDERS = ROOT / "current" / "renders"


def reference_water(name):
    land = np.asarray(Image.open(RENDERS / f"{name}_mask_land.png")) > 127
    cls = np.asarray(Image.open(RENDERS / f"{name}_mask_classes.png"))
    water = (~land) | (cls == 8)
    return land, water


def segment_water(rgb: np.ndarray) -> np.ndarray:
    r, g, b = [rgb[..., i].astype(np.int16) for i in range(3)]
    blue_dom = (b - r > 28) & (b >= g - 18)
    turq = (g - r > 55) & (b - r > 40)
    dark_sea = (b > r + 12) & (b > 70) & (r < 90)
    return blue_dom | turq | dark_sea


def metrics(ref_land, gen_land, max_shift=12):
    inter = np.logical_and(ref_land, gen_land).sum()
    union = np.logical_or(ref_land, gen_land).sum()
    iou = inter / max(union, 1)
    area_ratio = gen_land.sum() / max(ref_land.sum(), 1)
    ys, xs = np.nonzero(ref_land)
    yg, xg = np.nonzero(gen_land)
    shift = (float(xg.mean() - xs.mean()), float(yg.mean() - ys.mean())) if len(xg) else (0.0, 0.0)
    best = (iou, 0, 0)
    for dy in range(-max_shift, max_shift + 1, 3):
        for dx in range(-max_shift, max_shift + 1, 3):
            g2 = np.roll(np.roll(gen_land, dy, axis=0), dx, axis=1)
            u = np.logical_or(ref_land, g2).sum()
            v = np.logical_and(ref_land, g2).sum() / max(u, 1)
            if v > best[0] + 1e-4:
                best = (v, dx, dy)
    return {"iou": float(iou), "area_ratio": float(area_ratio), "centroid_shift_px": shift, "best_iou_with_shift": float(best[0]), "best_shift_px": (best[1], best[2])}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("name", choices=["S-01", "S-02"])
    ap.add_argument("image", nargs="?")
    ap.add_argument("--self", action="store_true", help="zkontroluje vlastní render atlasu (S-0x_base.png)")
    ap.add_argument("--threshold", type=float, default=0.95)
    ap.add_argument("--overlay", help="uloží náhled s referenčním pobřežím červeně")
    a = ap.parse_args(argv)
    path = RENDERS / f"{a.name}_base.png" if a.self else Path(a.image)
    ref_land, ref_water = reference_water(a.name)
    H, W = ref_land.shape
    im = Image.open(path).convert("RGB")
    ar_ref, ar_im = W / H, im.width / im.height
    if abs(ar_ref - ar_im) / ar_ref > 0.02:
        print(f"VAROVÁNÍ: poměr stran {ar_im:.3f} se liší od reference {ar_ref:.3f}; obraz se natáhne", file=sys.stderr)
    im = im.resize((W, H), Image.BICUBIC)
    rgb = np.asarray(im)
    water = segment_water(rgb)
    water_img = Image.fromarray((water.astype(np.uint8) * 255), "L").filter(ImageFilter.MedianFilter(7))
    water = np.asarray(water_img) > 127
    gen_land = ~water                       # jezero se v obraze počítá jako voda
    ref_land_eff = ~ref_water               # souš bez jezera
    m = metrics(ref_land_eff, gen_land)
    ok = m["iou"] >= a.threshold
    print(f"{a.name} · {path.name}: IoU souše {m['iou']:.4f} (práh {a.threshold}) · poměr ploch {m['area_ratio']:.3f} · "
          f"posun těžiště {m['centroid_shift_px'][0]:+.1f}/{m['centroid_shift_px'][1]:+.1f} px · "
          f"nejlepší posun {m['best_shift_px']} → IoU {m['best_iou_with_shift']:.4f}")
    print("VÝSLEDEK:", "tvar odpovídá atlasu" if ok else "TVAR NEODPOVÍDÁ – upravte prompt (silnější vazba na referenci) nebo opravte obraz")
    if a.overlay:
        edge = np.asarray(Image.fromarray((ref_land_eff.astype(np.uint8) * 255), "L").filter(ImageFilter.FIND_EDGES)) > 40
        out = rgb.copy()
        out[edge] = (255, 40, 40)
        Image.fromarray(out).save(a.overlay)
        print("přehled uložen:", a.overlay)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
