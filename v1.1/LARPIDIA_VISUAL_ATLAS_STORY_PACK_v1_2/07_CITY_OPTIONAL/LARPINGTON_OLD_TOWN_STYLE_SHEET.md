# Larpington – styl starého města a přístavu (pomocný list ke scénám 3, 4, 15, 18, 20 a ke Videu 02)

Pomůcka pro **konzistenci promptů**: co je v kánonu a v plánu CP-01 a co je jen doporučená stylizace. Nic se tím nemění v atlasu ani v bibli.

## 1. Kánon (approved) a historie
- Architektura: „Anglické a velšské cihlové a kamenné domy, mechem porostlé stěny, zahrady, kostely, romantická náměstí a zámky, kombinované s japonskými úzkými ulicemi.“ (World Bible, `architectural_mix`, approved)
- První britští osadníci kolem roku 1600 postavili přístavy, kostely, tržiště a venkovská sídla (`founding_story`, approved).
- Historické jižní centrum Larpingtonu s přístavem C-02 (nábřeží, butiky, promenády; vlnolam proti tajfunům z jihu).

## 2. Rozměry z plánu CP-01 (modelové, `proposed`)
| Prvek | Hodnota |
|---|---|
| Uličky starého města (třída L) | šířka 5 m |
| Místní ulice (třída C) | 10 m, ve starém městě 8 m |
| Přístavní promenáda (CP-PR01) | ≈ 19 m široká, podél celého nábřeží (Nábřeží 16. června) |
| Domy ve starém městě (ilustrativní) | 2–3 podlaží, výška okapu 7–10 m, sedlové střechy, hloubka ≈ 11 m, šířka 7–12 m |
| Kostel CP-B07 (Kostel sv. Jiří – pracovně) | loď 40 × 15 m, příčná loď 14 × 28 m, výška ≈ 20 m, cihla a kámen, mech |
| Kostelní náměstí CP-SQ04 | 74 × 60 m, lípy |
| Tržní náměstí CP-SQ03 / Tržní hala CP-B08 | 100 × 66 m / 54 × 22 m, výška ≈ 10 m |
| Prémiový hotel CP-B09 (HV-01) | 64 × 36 m, výška ≈ 20 m (nejvyšší budova promenády) |
| Přístavní úřad a celnice CP-B10 | 46 × 22 m, výška ≈ 9 m (historická budova) |
| Terminál lodní linky CP-B11 + molo | 38 × 16 m + molo 22 × 68 m |
| Přístav C-02 | pánev se dvěma kamennými vlnolamy, malé lodě (nákladní přístav je jinde, I-03) |

## 3. Barvy střech z plánu (generátor domů `cp_houses.py`)
- Staré město: #ac6046, #a05440, #ba7052, #7e5646, #c48c68, #68686e
- Promenáda: #ba7052, #c89670, #ac6046, #d6cebe, #96546a

## 4. Doporučená paleta pro prompty (stylizace, ne kánon)
| Materiál | Popis | Orientační barva |
|---|---|---|
| Cihla | tmavší červenohnědá, patinovaná | #a86248 |
| Terakotová taška | teplá, místy zelenavé skvrny od mechu | #ba7052 |
| Břidlice | studená šedá | #68686e |
| Medový vápenec | rámy dveří a oken, schody kostela | #d2b98a |
| Mech a břečťan | na zdech, střešních hřebenech, parapetech | #6b8a4a |
| Omítka | krémová, jen místy | #e8dcc2 |
| Železo | černé kování, lucerny, brány | #2a2a2e |
| Voda v přístavu | zelenomodrá, klidná | #3f8a92 |

## 5. Pravidla pro konzistenci
1. Nikdy neukazovat mrakodrapy, neony, čitelné nápisy ani reálné značky; všechny ceduli a vývěsní štíty nechat bez písma.
2. Domy 2–3 podlaží, sedlové střechy, cihla a kámen, mech; zahrádky za nízkými kamennými zídkami.
3. Kostel je **farní, anglický** (ne gotická katedrála): věž s ostrou střechou, cihla a kámen, špičatý oblouk dveří.
4. Přístav je **historický**: dřevěné rybářské lodě, plachetnice; žádné kontejnery ani jeřáby.
5. Světlo: ráno a večer teplé a měkké, přes den lehká atmosférická mlha od moře; v noci teplá okenní světla a nasvícený kostel.
6. Lidé: v těchto scénách nejsou; auto jen v bodě 20 (klasické, nenápadně bokem).

## 6. Kde jsou scény v Larpingtonu
| Scéna | Kamerový bod (lokální m plánu) | Cíl pohledu |
|---|---|---|
| PHOTO 03 Old Larpington | Tržní ulice, u 2856 / 3371 | Kostelní náměstí a věž kostela (W) |
| PHOTO 04 Old Harbour | přístavní promenáda, 3135 / 3600 | promenáda a pánev (ENE) |
| PHOTO 15 Rooftop Night | střecha hotelu CP-B09, 3528 / 3407 (oko 21,5 m) | osvětlené staré město (W) |
| PHOTO 18 Church Courtyard | jihozápadní roh náměstí, 2757 / 3373 | boční vstup kostela (ENE) |
| PHOTO 20 Heritage Street | Tržní ulice, 3358 / 3365 | Tržní náměstí a hala (ENE) |
| VIDEO 02 Entering the Old Church | západ Kostelního náměstí, 2752 / 3351 | západní portál a loď (E) |

Plán města: `atlas/current/capital/` (SVG, PNG, GeoJSON); satelitní reference: `atlas/current/renders/S-03_base.png` (2 m/px).
