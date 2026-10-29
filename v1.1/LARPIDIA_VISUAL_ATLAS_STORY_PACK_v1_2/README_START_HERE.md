# LARPIDIA – Visual Atlas & Story Pack v1.2 (návod)

Balík pro školní projekt o fiktivním ostrovním státě **Larpidie** (a menším ostrově **Paraland**): **20 fotografických scén, 4 videí, mapa s pinem ke každé scéně, finální anglické prompty a offline galerie.**

> **Důležité – poctivě:** fotografie ani videa v tomto balíku **nejsou vygenerované**. Neměl jsem k dispozici žádný obrazový ani video generátor (placené nástroje se bez výslovného souhlasu nepoužívají). Všechno ostatní je hotové: scény, mapy, prompty, metadata, storyboardy, galerie. Stav všech scén je **prompt-ready**.

## Co kde je
| Složka / soubor | Obsah |
|---|---|
| `06_GALLERY/index.html` | **Začněte tady.** Offline galerie (dvojklik): mapy, popisy, tlačítko *Prompt (EN)* s kopírováním, metadata, filtry |
| `03_PHOTO_PROMPTS/` | 20 samostatných finálních anglických promptů (`PHOTO_xx_….txt`) + `ALL_PHOTO_PROMPTS.md` |
| `02_MAP_PINS/` | mapa s pinem ke každé scéně (20 fotek + 4 videa) a přehledová mapa všech scén |
| `04_PHOTO_METADATA/` | metadata scén (`PHOTO_xx.json`) + `ALL_PHOTO_METADATA.json` |
| `05_VIDEO/` | 4 videa: storyboard, finální video prompt, mapa a metadata v samostatné složce |
| `01_PHOTOS/` | sem ukládejte vygenerované fotky (viz níže) |
| `07_CITY_OPTIONAL/` | volitelné: styl starého Larpingtonu pro konzistenci promptů, přehled městských scén, paleta |
| `MANIFEST.csv` | přehled všech scén (stav, lokalita, kamerový bod, soubory) |

## Jak z toho udělat fotky (3 kroky)
1. Otevřete `06_GALLERY/index.html`, na kartě scény klikněte na **Prompt (EN)** a **Kopírovat**.
2. Vložte prompt do ChatGPT (obrázky) nebo Gemini; nastavte stejný poměr stran (9:16 nebo 16:9). Referenční obrázek přikládat nemusíte; mapa slouží lidem, ne generátoru.
3. Výsledek uložte do `01_PHOTOS/` pod názvem `PHOTO_01.jpg` … `PHOTO_20.jpg` (nebo `.png`, `.webp`). Při dalším otevření galerie se karta sama aktualizuje a stav se změní na *generated*.

Videa: z hotové fotografie (např. `PHOTO_09`) udělejte první snímek a vložte video prompt z `05_VIDEO/VIDEO_xx_…/`.

## Stavy a značení
- **prompt-ready** = scéna, mapa, prompt a metadata jsou hotové, obrázek chybí; **generated** = ve `01_PHOTOS/` je obrázek; **not generated** = zatím nic.
- **ID lokalit** jsou skutečná ID z registru atlasu (např. `M-01`, `N-03`, `C-02`, `PL-06`) nebo z plánu města (`CP-B07`). Nic jsem nevymýšlel.
- **PROPOSED CAMERA POINT** = navržené kamerové stanoviště, které není v registru. Vždy je odlišené od registrované lokality (modrý fotoaparát × červený pin). Souřadnice jsou **lokální km atlasu**, nikoli GPS.
- Mapové podklady jsou **simulovaná satelitní vizualizace** fiktivního světa.

## Co jsem ověřoval (a nenašel)
Každý kamerový bod leží na souši (kromě mola v marině), je ve správné nadmořské výšce (nejvyšší vrchol 560 m) a z modelu terénu (a ve městě i výšky domů) jsem ověřil, že cíl pohledu je skutečně viditelný (např. kostel z Tržní ulice, Larpington z vyhlídky u hráze, Paraland z hrotu poloostrova).

## Kam dál
Přegenerování balíku po změně atlasu: `python atlas/scripts/build_story_pack.py` (z kořene projektu). Rozhodnutí týmu o geografii najdete v `atlas/docs/FINAL_SUMMARY.md`.
