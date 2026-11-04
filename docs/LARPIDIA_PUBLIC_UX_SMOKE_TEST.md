# Ruční kontrola veřejného rozhraní Larpidie

## Spuštění

Z kořene projektu sestavte export a spusťte jeho lokální náhled:

```powershell
node scripts/build_public_site.mjs
node scripts/serve_static.mjs
```

Otevřete `http://localhost:4173/`. Tento server zpřístupňuje pouze sestavenou složku `public/`.

## Desktop

- [ ] Na `http://localhost:4173/atlas/current/viewer/atlas.html` vyhledejte `T-01`. Výsledek se jmenuje **Praha**, ukazuje český popis a interní ID není v kartě, štítku mapy ani detailu vidět.
- [ ] Vyhledejte `Prague`, potom `pristav` a ověřte vyhledání bez diakritiky; zkuste i výraz bez výsledku.
- [ ] Klikněte na Prahu a potom na jiný prvek mapy. Detail se pokaždé aktualizuje; u Prahy jsou souřadnice uvedené jako atlasové a výška jako `41,1 m n. m.`.
- [ ] Posuňte a přibližte mapu, přepněte jazyk popisků a otevřete/sbalte **Vrstvy a nastavení mapy**. Po výběru místa se nastavení samo sbalí.
- [ ] Na `http://localhost:4173/atlas/current/capital/capital_plan_viewer.html` vyhledejte `CP-B01`, ověřte veřejný název radnice a klikněte na radnici i sousední objekt. Ověřte, že se po každém kliknutí změní detail.
- [ ] Otevřete `http://localhost:4173/index.html#galerie`. Každá ze čtyř karet musí mít viditelný obrázek a český popisek; klikněte také do galerie přes navigaci webu.
- [ ] Ověřte obrazové logo v hlavičce/patičce úvodu, galerie, atlasu a samostatných mapových prohlížečů. V jejich patičce zkontrolujte nenápadné verze načtené z metadat.
- [ ] Otevřete 3D odkazy z atlasu a plánu města a zkontrolujte, že se zobrazí správná scéna. Cesty: `/atlas/current/viewer/terrain-3d.html` a `/atlas/current/capital/capital-3d.html`.

## Mobilní šířka

V nástrojích pro vývojáře nastavte viewport přibližně na **390 × 844 px**.

- [ ] V atlasu otevřete **Hledat místa**, vyhledejte Prahu, vyberte výsledek a klepněte na mapový prvek. Detail se zobrazí pod mapou.
- [ ] Posuňte panel podrobností až k atlasovým souřadnicím a nadmořské výšce; spodní lišta nesmí text zakrýt.
- [ ] V plánu města otevřete hledání, vyberte radnici a klepněte na její mapový prvek. Název, orientační text a odkaz na 3D se v hlavičce nesmí překrývat ani oříznout.
- [ ] V galerii ověřte, že jsou obrázky viditelné, použitelné na šířku telefonu a stránka nemá vodorovný posuvník.

## Zdrojový náhled a veřejné soubory

Pomocný stav médií je určen jen pro autorský náhled. Pokud je v prostředí dostupný Python, lze jej spustit z kořene projektu:

```powershell
py -m http.server 8000 --bind 127.0.0.1
```

Na `http://127.0.0.1:8000/index.html#galerie` klikněte na **Obrazový archiv**. Kontrolní hodnoty jsou `Hotové fotografie: 2` a `Chybějící scény: 18`; zavření tlačítkem i klávesou Escape má vrátit fokus na ovládací prvek.

- [ ] Veřejný export nesmí obsahovat tlačítko/stavový dialog, interní seznam scén ani prompty.
- [ ] V náhledu exportu ověřte, že tyto cesty vracejí 404: `/references/LARPIDIA_USTAVNI_KANON_PRACOVNI_v2.6.md`, `/docs/LARPIDIA_PUBLIC_ATLAS_GALLERY_REPAIR_REPORT.md`, `/v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/03_PHOTO_PROMPTS/ALL_PHOTO_PROMPTS.md`, `/atlas/current/registry/places.json` a `/atlas/current/capital/cp_objects.json`.
- [ ] Po vizuální kontrole 3D scén lze pro jistotu znovu spustit `node scripts/check_public_export.mjs`; ten porovnává čtyři veřejné 3D datové soubory bajt po bajtu se zdrojem.
