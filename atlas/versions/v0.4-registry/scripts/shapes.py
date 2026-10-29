"""Řídicí body pobřeží obou ostrovů (varianty A a B). Souřadnice v km v lokálním rámci.

Typ pobřeží (`ctype`) řídí hrubost šumu a později i klasifikaci pobřeží:
cliff (útes) · rocky (skalnaté) · mixed · beach (písčité) · harbor (přístav) · industrial.
`pin` = bod, kterým pobřeží prochází přesně (šum a kalibrace plochy se v okolí utlumí).

Vše je pracovní návrh (proposed). Pevné vstupy: plochy, průliv, silueta z GEOGRAPHY_AND_CANON.md.
"""
from __future__ import annotations

# (x_km, y_km, ctype, pin)
MAIN_A = [
    (2.60, 6.40, "cliff", "N-01cape"),
    (3.00, 5.50, "cliff", None),
    (4.00, 4.95, "cliff", None),
    (5.40, 4.50, "cliff", None),
    (6.90, 4.10, "rocky", None),
    (8.40, 3.60, "rocky", None),
    (9.90, 3.20, "rocky", None),
    (11.20, 2.70, "rocky", None),
    (12.20, 2.00, "rocky", None),          # výběžek západně od zátoky Ōru Maito
    (13.00, 2.45, "mixed", None),
    (13.80, 2.65, "harbor", "H-01"),       # severní rybářský přístav (atlas_new)
    (14.60, 2.30, "mixed", None),
    (15.40, 1.90, "rocky", None),
    (16.50, 1.65, "rocky", None),          # severní mys mezi zátokami
    (17.40, 2.05, "rocky", None),
    (18.20, 2.85, "mixed", None),
    (19.15, 3.60, "beach", None),          # dno východní severní zátoky (Hoshimachi)
    (20.00, 3.30, "mixed", None),
    (20.90, 3.70, "rocky", None),
    (21.55, 4.70, "mixed", None),
    (21.60, 5.90, "mixed", None),
    (21.95, 7.40, "mixed", None),
    (22.30, 8.80, "mixed", None),
    (22.56, 10.24, "harbor", "I-03"),      # nákladní přístav ve vstupu do východní zátoky
    (22.00, 10.85, "industrial", None),
    (21.20, 11.20, "industrial", None),
    (20.50, 11.55, "mixed", None),
    (20.00, 12.00, "mixed", None),         # dno východní zátoky (šíje poloostrova)
    (20.50, 12.50, "mixed", None),
    (21.20, 12.75, "mixed", None),
    (21.80, 13.30, "beach", None),
    (21.95, 14.00, "beach", None),
    (21.65, 14.60, "beach", None),         # hrot jihovýchodního poloostrova
    (21.00, 14.75, "beach", None),
    (20.35, 14.35, "beach", None),
    (19.75, 13.55, "harbor", "P-01"),      # spojení na Paraland (šíje)
    (18.90, 13.55, "beach", None),
    (18.00, 13.85, "beach", None),
    (17.20, 14.00, "harbor", None),
    (16.32, 13.92, "harbor", "C-02"),      # historický přístav hlavního města
    (15.45, 14.20, "harbor", None),
    (14.65, 14.50, "beach", None),         # západní výběžek jižního zálivu
    (14.00, 14.30, "beach", None),
    (13.10, 13.80, "beach", None),
    (11.90, 13.25, "beach", None),
    (10.30, 12.60, "mixed", None),
    (8.80, 12.05, "mixed", None),
    (7.30, 11.55, "mixed", None),
    (5.90, 11.05, "rocky", None),
    (4.50, 10.85, "rocky", None),
    (3.55, 10.55, "cliff", None),
    (2.95, 9.25, "cliff", None),
    (2.95, 7.80, "cliff", None),
]

MAIN_B = [
    (2.65, 6.40, "cliff", "N-01cape"),
    (3.05, 5.55, "cliff", None),
    (4.10, 5.00, "cliff", None),
    (5.60, 4.60, "cliff", None),
    (7.10, 4.25, "rocky", None),
    (8.60, 3.90, "rocky", None),
    (10.10, 3.55, "rocky", None),
    (11.30, 3.00, "rocky", None),
    (12.05, 2.00, "rocky", None),          # výběžek západně od zátoky Ōru Maito
    (12.90, 2.80, "mixed", None),
    (13.70, 3.05, "harbor", "H-01"),       # severní rybářský přístav (atlas_new)
    (14.50, 2.65, "mixed", None),
    (15.30, 1.60, "rocky", None),
    (16.50, 1.10, "rocky", None),          # severní mys mezi zátokami
    (17.50, 1.60, "rocky", None),
    (18.20, 2.50, "mixed", None),
    (19.00, 3.35, "beach", None),          # dno východní severní zátoky (Hoshimachi)
    (19.90, 3.25, "mixed", None),
    (20.90, 3.05, "rocky", None),
    (21.70, 4.40, "mixed", None),
    (21.75, 6.00, "mixed", None),
    (22.05, 7.50, "mixed", None),
    (22.30, 8.90, "mixed", None),
    (22.56, 10.24, "harbor", "I-03"),
    (22.00, 10.85, "industrial", None),
    (21.15, 11.20, "industrial", None),
    (20.40, 11.55, "mixed", None),
    (19.90, 11.95, "mixed", None),
    (20.50, 12.45, "mixed", None),
    (21.40, 12.60, "mixed", None),
    (22.10, 13.15, "beach", None),
    (22.50, 13.95, "beach", None),
    (22.40, 14.90, "beach", None),         # hrot dlouhého poloostrova
    (21.75, 15.15, "beach", None),
    (21.00, 14.90, "beach", None),
    (20.35, 14.35, "beach", None),
    (19.75, 13.55, "harbor", "P-01"),
    (18.90, 13.55, "beach", None),
    (18.00, 13.85, "beach", None),
    (17.20, 14.00, "harbor", None),
    (16.32, 13.92, "harbor", "C-02"),
    (15.45, 14.25, "harbor", None),
    (14.80, 14.75, "beach", None),
    (14.15, 14.45, "beach", None),
    (13.10, 13.85, "beach", None),
    (11.90, 13.25, "beach", None),
    (10.30, 12.60, "mixed", None),
    (8.80, 12.05, "mixed", None),
    (7.30, 11.55, "mixed", None),
    (5.90, 11.05, "rocky", None),
    (4.50, 10.85, "rocky", None),
    (3.55, 10.55, "cliff", None),
    (2.95, 9.25, "cliff", None),
    (2.95, 7.80, "cliff", None),
]

# Paraland: poloměrové faktory po 15° v lokální soustavě (t=0 východ, 90 jih, 180 západ, 270 sever)
# (t, faktor, ctype, pin)
PARA_A = [
    (0, 1.01, "beach", None), (15, 0.97, "beach", None), (30, 0.84, "beach", None),    # JV chráněná zátoka
    (45, 1.00, "beach", None), (60, 1.03, "beach", None), (75, 1.04, "mixed", None),
    (90, 1.00, "beach", None), (105, 1.03, "beach", None), (120, 0.97, "mixed", None),
    (135, 1.00, "mixed", None), (150, 1.00, "mixed", None), (165, 0.94, "harbor", None),
    (180, 0.80, "harbor", "H-02"),                                                      # západní marina
    (195, 0.95, "harbor", None), (210, 1.00, "mixed", None), (225, 1.02, "rocky", None),
    (240, 1.07, "rocky", None),                                                         # hrad na výběžku
    (255, 0.95, "mixed", None), (270, 0.86, "harbor", None),                            # severní zátoka starého městečka
    (285, 0.96, "mixed", None), (300, 1.02, "mixed", None), (315, 0.98, "mixed", None),
    (330, 0.84, "beach", None), (345, 0.98, "beach", None),                             # SV chráněná zátoka
]
PARA_AXES = (2.95, 1.70)       # poloosy základní elipsy (km)
PARA_ROT_DEG = 24.0            # sklon delší osy (po směru hod. = východ dolů)
PARA_APPROACH_DEG = 38.0       # směr od hrotu poloostrova k Paralandu (JV)

VARIANTS = {
    "A": {"title": "Varianta A – věrná tabulce", "main": MAIN_A, "para": PARA_A, "deviations": {},
          "note": "Všech 23 bodů přesně podle tabulky GEOGRAPHY (0 odchylek). Kompaktnější tělo, mělčí zátoky."},
    "B": {"title": "Varianta B – členitější", "main": MAIN_B, "para": PARA_A,
          "deviations": {"T-04": (56, 23.0), "T-05": (73, 26.5), "A-01": (82, 40.0)},
          "note": "Tři body posunuty o ≤ 3 % (T-04, T-05, A-01), proto hlubší severní zátoky, výraznější mys a delší poloostrov."},
}
