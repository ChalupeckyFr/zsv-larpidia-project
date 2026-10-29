# Kontrolní seznam ke schválení (atlas 1.0-draft)

Zaškrtněte *schváleno*, nebo napište změnu. Cokoli nezaškrtnuté zůstává `proposed`. Po vyplnění se změny zapíšou do `bible_patch_v1.1.json` (nová minor verze atlasu) a atlas se zmrazí jako v1.0.

## 1. Geometrie a polohy (D1, D7)

| ☐ | Položka | Výchozí volba | Kde |
|---|---|---|---|
| ☐ | Obrys ostrovů – varianta B | zmrazeno (SHA-256 `ffca09ac…`) | `current/geometry/` |
| ☐ | Rámec 24 × 16 km, průliv 1,5 km | ponechat | `docs/CONFLICTS_AND_DECISIONS.md` R-01 |
| ☐ | Odchylka T-04 Ōru Maito (オールマイト): 56/20 → 56/23.0 % (0.48 km) | přijmout | `registry/deviations.csv` |
| ☐ | Odchylka T-05 Aokawa (青川): 73/24 → 73/26.5 % (0.4 km) | přijmout | `registry/deviations.csv` |
| ☐ | Odchylka A-01 Hlavní regionální letiště: 83/37 → 82/40.0 % (0.537 km) | přijmout | `registry/deviations.csv` |
| ☐ | Polohy ostatních 20 bodů z tabulky GEOGRAPHY | beze změny | `registry/places.csv` |

## 2. Doprava a hlavní město (D8, D10, D11, D12)

| ☐ | Položka | Výchozí volba | Kde |
|---|---|---|---|
| ☐ | R1: útesy ≤ 293 m a 3 tunely (2,2 km) v SZ | potvrzeno jako návrh (R-07) | `docs/F3_HUMAN_NOTES.md` |
| ☐ | L1 jako linka s koncovou smyčkou v jeskyni (~262°) | potvrzeno jako návrh | tamtéž |
| ☐ | L2 oblouk Západ–Sever–Východ, L3 okruh + větev na Paraland, 3 přestupy | potvrzeno jako návrh | tamtéž |
| ☐ | Přístavy C-02, I-03, H-01, H-02; letiště A-01 (1 900 m) a A-02 (700 m) | návrh | `current/human/ports_airports.geojson` |
| ☐ | O19: parlament uprostřed Náměstí čtyř a čtyři správní budovy ve větrníku | ano (alternativa: parlament u přístavu) | `docs/F7_CAPITAL_NOTES.md` |
| ☐ | Zastavěné území hlavního města 6.31 km² (staré město u přístavu, Východní nábřeží, zelené klíny) | ano | C-18 |
| ☐ | Hotel HV-01 na promenádě, muzeum u Centrálního parku | ano | C-19, O22 |
| ☐ | Prodloužení tepny RD-12 k nábřeží (Přístavní třída) | ano | C-20 |
| ☐ | Vzhled satelitních podkladů S-01/S-02 po doladění | schválit nebo napsat, co vadí | `current/renders/` |

## 3. Jména a modelová čísla (D2, D5, D9)

| ☐ | Položka | Výchozí volba | Kde |
|---|---|---|---|
| ☐ | 44 navržených jmen míst (cs/en/ja) | ponechat jako pracovní | `registry/names_proposed.csv` |
| ☐ | Larpington a čtyři čtvrtě (Chalupecká, Kynčlova, Klimečkova, Žemličkova) | D2 | `docs/NAMES_AND_DEVIATIONS_TO_APPROVE.md` |
| ☐ | Názvy ulic a míst plánu města (O25) | pracovní | `capital/cp_objects.csv` |
| ☐ | Rozlohy 175 + 14 km², populace 32 000 (modelové rozdělení) | D5, C-16 | `docs/F3_HUMAN_NOTES.md` |
| ☐ | Výšky vrcholů M-01 560.0 m (kanon 560), M-02 510.0 m, M-03 440.0 m (modelové) | ponechat | `docs/F2_RELIEF_NOTES.md` |
| ☐ | O15: poloha larpiditu se nezakresluje | beze změny | O15 |

## Po schválení

1. `atlas/scripts/snapshot.py v1.0 …` (zmrazení), 2. sloučení patche do `data/larpidia_world_bible.json` jako verze 1.1 (jen po výslovném souhlasu týmu), 3. nový SHA-256 originálů do `ORIGINALS_SHA256.txt`.
