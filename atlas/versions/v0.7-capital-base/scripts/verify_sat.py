"""Ověří, že obrázek vygenerovaný externím nástrojem drží tvar ostrova z atlasu (IoU masky souše).

Použití:
    python atlas/scripts/verify_sat.py S-01 cesta/k/vygenerovanemu.png [--threshold 0.95] [--overlay out.png]
    python atlas/scripts/verify_sat.py S-01 --self          # kontrola vlastního renderu atlasu
    python atlas/scripts/verify_sat.py S-01_oblique_S cesta/k/vygenerovanemu.jpg   # šikmý pohled: siluetu porovná s referenčním šikmým pohledem

Šikmé pohledy nemají masku z geometrie; referencí je vlastní šikmý render (obloha i moře = voda), takže se hlídá silueta pevniny a horizontu.

Postup: obraz se přepočte na rozměr reference, voda (moře i jezero) se rozpozná podle převahy modré/tyrkysové,
výsledek se vyčistí mediánovým filtrem a porovná s referenční maskou. Bílé plochy (mraky, příboj) se z porovnání vynechají.
Počítá IoU souše, poměr ploch, posun těžiště a nejlepší celočíselný posun (zjištění chybného zarovnání). Návratový kód 0 = shoda ≥ prahu.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
RENDERS = ROOT / "current" / "renders"


def segment_water(rgb: np.ndarray) -> np.ndarray:
    r, g, b = [rgb[..., i].astype(np.int16) for i in range(3)]
    blue_dom = (b - r > 28) & (b >= g - 18)
    turq = (g - r > 55) & (b - r > 40)
    dark_sea = (b > r + 12) & (b > 70) & (r < 90)
    return blue_dom | turq | dark_sea


def is_oblique(name):
    return "_oblique_" in name


def reference_water(name):
    """Nadir: maska souše z renderu. Šikmý pohled: vlastní referenční obraz se segmentuje stejnou funkcí jako ověřovaný (obloha i moře = voda)."""
    if is_oblique(name):
        rgb = np.asarray(Image.open(RENDERS / f"{name}.jpg").convert("RGB"))
        water = np.asarray(Image.fromarray((segment_water(rgb).astype(np.uint8) * 255), "L").filter(ImageFilter.MedianFilter(7))) > 127
        return ~water, water
    land = np.asarray(Image.open(RENDERS / f"{name}_mask_land.png")) > 127
    cls = np.asarray(Image.open(RENDERS / f"{name}_mask_classes.png"))
    water = (~land) | (cls == 8)
    return land, water


def bright_unknown(rgb: np.ndarray) -> np.ndarray:
    """Bílé plochy (mraky, příboj) nelze spolehlivě zařadit k vodě ani souši – vynechají se z porovnání (okraj se mírně rozšíří)."""
    mn, mx = rgb.min(axis=2).astype(np.int16), rgb.max(axis=2).astype(np.int16)
    m = (mn > 215) & (mx - mn < 30)
    return np.asarray(Image.fromarray((m.astype(np.uint8) * 255), "L").filter(ImageFilter.MaxFilter(7))) > 127


def metrics(ref_land, gen_land, max_shift=12, valid=None):
    if valid is None:
        valid = np.ones_like(ref_land, dtype=bool)
    inter = np.logical_and(np.logical_and(ref_land, gen_land), valid).sum()
    union = np.logical_and(np.logical_or(ref_land, gen_land), valid).sum()
    iou = inter / max(union, 1)
    area_ratio = np.logical_and(gen_land, valid).sum() / max(np.logical_and(ref_land, valid).sum(), 1)
    ys, xs = np.nonzero(ref_land)
    yg, xg = np.nonzero(gen_land)
    shift = (float(xg.mean() - xs.mean()), float(yg.mean() - ys.mean())) if len(xg) else (0.0, 0.0)
    best = (iou, 0, 0)
    for dy in range(-max_shift, max_shift + 1, 3):
        for dx in range(-max_shift, max_shift + 1, 3):
            g2 = np.roll(np.roll(gen_land, dy, axis=0), dx, axis=1)
            u = np.logical_and(np.logical_or(ref_land, g2), valid).sum()
            v = np.logical_and(np.logical_and(ref_land, g2), valid).sum() / max(u, 1)
            if v > best[0] + 1e-4:
                best = (v, dx, dy)
    return {"iou": float(iou), "area_ratio": float(area_ratio), "centroid_shift_px": shift, "best_iou_with_shift": float(best[0]), "best_shift_px": (best[1], best[2])}


def main(argv=None):
    ap = argparse.ArgumentParser()
    names = ["S-01", "S-02"] + sorted(p.name[:-len("_camera.json")] for p in RENDERS.glob("*_oblique_*_camera.json"))
    ap.add_argument("name", choices=names)
    ap.add_argument("image", nargs="?")
    ap.add_argument("--self", action="store_true", help="zkontroluje vlastní render atlasu (S-0x_base.png, u šikmých pohledů S-0x_oblique_….jpg)")
    ap.add_argument("--threshold", type=float, default=0.95)
    ap.add_argument("--overlay", help="uloží náhled s referenčním pobřežím červeně")
    a = ap.parse_args(argv)
    path = (RENDERS / (f"{a.name}.jpg" if is_oblique(a.name) else f"{a.name}_base.png")) if a.self else Path(a.image)
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
    valid = ~bright_unknown(rgb)
    if (~valid).mean() > 0.001:
        print(f"Poznámka: {100 * (~valid).mean():.1f} % pixelů jsou bílé plochy (mraky/příboj) – z porovnání jsou vynechány")
    m = metrics(ref_land_eff, gen_land, valid=valid)
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
