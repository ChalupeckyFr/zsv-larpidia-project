"""Vytvoří docs/canon_extract.csv: každé geografické tvrzení kanonu + zdroj + stav.

Stavy a hodnoty u položek z bible se čtou přímo z JSON (nic se neopisuje ručně).
Sloupec `atlas_objects` se plní v pozdějších fázích (matice dohledatelnosti).
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from canon import ATLAS, geo_ref_table, load_bible  # noqa: E402

B = load_bible()

# (claim_id, oblast, tvrzení česky, zdroj: "bible:cesta" | "doc:soubor#oddíl", fáze, stav pro doc zdroje, poznámka)
ROWS = [
    # ---- World Bible: geography
    ("K-001", "poloha", "Souostroví v Tichém oceánu jižně od hlavních japonských ostrovů", "bible:geography.macro_location", "F1", "", ""),
    ("K-002", "poloha", "Pracovní souřadnice 33,9 N / 137,6 E (hypotetická alternativní geografie)", "bible:geography.working_coordinates", "F1", "", "pseudo-lon/lat jen jako hypotetické"),
    ("K-003", "rozloha", "Hlavní ostrov 150–200 km²", "bible:geography.main_island_area_km2", "F1", "", "schválený rozsah"),
    ("K-004", "rozloha", "Pracovní rozloha hlavního ostrova 175 km²", "bible:geography.working_main_area_km2", "F1", "", ""),
    ("K-005", "rozloha", "Paraland 14 km²", "bible:geography.paraland_area_km2", "F1", "", ""),
    ("K-006", "ostrovy", "Dva ostrovy: Larpidie (hlavní) a Paraland (turistický)", "bible:geography.islands", "F1", "", ""),
    ("K-007", "ostrovy", "Paraland = paradise island, hravě připomíná Paralen; není zdravotnické zařízení", "bible:geography.paraland_etymology", "F5", "", "pojmenování"),
    ("K-008", "doprava", "Paraland spojen třetí železniční linkou pod mořem s krátkým proskleným úsekem", "bible:geography.paraland_connection", "F3", "", "inženýrsky náročný prvek"),
    ("K-009", "poloha", "Paraland jihovýchodně od hlavního ostrova za úzkým průlivem", "bible:geography.paraland_location_relative", "F1", "", ""),
    ("K-010", "poloha", "Vzdálenost (průliv) 1,5 km", "bible:geography.paraland_distance_km", "F1", "", "rozhodnuto týmem; MAP_PROMPT 2–3 km se nepoužije"),
    ("K-011", "reliéf", "Nejvyšší vrchol 500–600 m", "bible:geography.highest_peak_m", "F2", "", ""),
    ("K-012", "reliéf", "Pracovní výška nejvyššího vrcholu 560 m", "bible:geography.working_peak_m", "F2", "", ""),
    ("K-013", "reliéf", "Třívrcholové pohoří: jedna prudší sjezdovková hora, jeden zaoblený vrchol pro turistiku a paragliding", "bible:geography.mountains", "F2", "", "viz rozpor C-04"),
    ("K-014", "klima", "Horké léto, výrazná roční období, občasný sníh; v 560 m jen krátká sezona/zasněžování", "bible:geography.climate", "F2", "", ""),
    ("K-015", "příroda", "Lesy, louky, prameny, vodopády, přehrada, písčité pláže, skalnaté pobřeží, 10m sráz s vyhlídkou, krystalová jeskyně", "bible:geography.natural_features", "F2", "", ""),
    ("K-016", "silnice", "Dlouhá okružní pobřežní silnice s odbočkami na vyhlídky, pláže, lesy", "bible:geography.coast_ring_road", "F3", "", ""),
    ("K-017", "stezky", "Hustá síť cyklotras, pěších tras a přístupů k pramenům", "bible:geography.cycling_walking", "F3", "", ""),
    ("K-018", "zóny", "Zóny: Z/SZ hory a útesy; střední Z přehrada, vodopády, jeskyně; sever japonská městečka; V/SV průmysl, letiště; J/JV hlavní město; JV Paraland", "bible:geography.spatial_zones", "F1", "", ""),
    ("K-019", "rizika", "Tajfuny, bouře, zemětřesení; bezpečné umístění zásob vody a kritické infrastruktury", "bible:geography.disaster_planning", "F3", "", "vlnolam jižního přístavu"),
    # ---- World Bible: urbanism
    ("K-020", "města", "Pracovní název hlavního města: Larpington", "bible:urbanism.capital_name", "F4", "", "D2"),
    ("K-021", "města", "Čtyři čtvrti hlavního města podle příjmení autorů", "bible:urbanism.capital_four_districts", "F7", "", "D2"),
    ("K-022", "města", "Povinná města: Praha, Cimprlichovo Hradiště, Havlišovo Doupě, Ōru Maito", "bible:urbanism.must_include_towns", "F3", "", ""),
    ("K-023", "města", "Další návrhová města: Aokawa, Hoshimachi", "bible:urbanism.other_towns", "F3", "", "Hoshimachi nemá souřadnice"),
    ("K-024", "architektura", "Směs anglicko-velšské a japonské architektury", "bible:urbanism.architectural_mix", "F4", "", "pro foto/video vazby"),
    ("K-025", "města", "Role hlavního města: kultura, památky, obchody, státní instituce, přístav, MHD", "bible:urbanism.capital_roles", "F7", "", ""),
    ("K-026", "průmysl", "Vzdušné zelené průmyslové areály se školami, školkami, restauracemi", "bible:urbanism.industry_style", "F3", "", ""),
    ("K-027", "Paraland", "Paraland: hotely, aquaparky, lesy, zříceniny, hrad/zámek, promenáda, malé historické sídlo", "bible:urbanism.tourism_island", "F3", "", ""),
    ("K-028", "Paraland", "Kapacitní rezervace ubytování; návštěvníci Paralandu mohou na hlavní ostrov", "bible:urbanism.tourist_access_policy", "F4", "", ""),
    ("K-029", "hlavní ostrov", "Menší počet prémiových hotelů na hlavním ostrově", "bible:urbanism.main_island_vip_lodging", "F3", "", ""),
    # ---- World Bible: mobility
    ("K-030", "doprava", "Elektrifikovaný vozový park včetně přestavěných klasických karoserií", "bible:mobility.electric_vehicles", "F4", "", "vizuální vazba"),
    ("K-031", "doprava", "Bezplatné půjčování lehkých elektrických dopravních prostředků v zónách", "bible:mobility.public_micromobility", "F7", "", ""),
    ("K-032", "železnice", "Tři linky L1, L2, L3 (názvy proposed)", "bible:mobility.rail_lines", "F3", "", "role schváleny, jména ne"),
    ("K-033", "železnice", "L1 vyvýšený zážitkový vlak s jeskyní a vodopádem; L2 historicky stylizované povrchové; L3 převážně podzemní včetně Paralandu", "bible:mobility.rail_line_roles_approved", "F3", "", ""),
    ("K-034", "železnice", "L3 jako svižné metro, ne dálková rychlodráha", "bible:mobility.rail_speed_note", "F3", "", ""),
    ("K-035", "přístavy", "Alespoň 3 přístavy: historický, nákladní, severní rybářský, marina Paraland", "bible:mobility.seaports", "F3", "", ""),
    ("K-036", "letiště", "Přibližně dvě letiště: hlavní regionální + malá plocha na Paralandu", "bible:mobility.airports", "F3", "", ""),
    # ---- World Bible: economy / history (prostorově významné)
    ("K-037", "průmysl", "Mořské mikrořasy jako surovina bio-ropy (závod u nákladního přístavu)", "bible:economy.renewable_feedstock", "F3", "", "I-02"),
    ("K-038", "příroda", "Larpidit: omezené naleziště, žádná masová těžba", "bible:economy.gemstone", "F3", "", "poloha naleziště není určena (otázka O15)"),
    ("K-039", "průmysl", "Významné exportní podniky vlastní stát", "bible:economy.state_enterprises", "F3", "", ""),
    ("K-040", "historie", "První britští osadníci kolem roku 1600: přístavy, kostely, tržiště, venkovská sídla", "bible:history.founding_story", "F4", "", "místo prvního přístavu není určeno (O16)"),
    ("K-041", "zemědělství", "Obilí a omezená rýže na zavlažovaných terasách", "bible:history.agriculture", "F2", "", "poloha teras není určena (O17)"),
    ("K-042", "kultura", "Interaktivní muzeum historie (Košťálova éra, archiv, komentované prohlídky)", "bible:history.museum", "F7", "", "poloha v hlavním městě – výchozí volba"),
    ("K-043", "bezpečnost", "Vyhlídky na útesech s bezpečným přístupem; žádné návody na skoky", "bible:visitor_experience.activities_safety", "F3", "", ""),
    ("K-044", "výstupy", "Požadované mapy: satelitně stylizovaný pohled, fyzická, politická, historická, plán hlavního města", "bible:output_requirements.cartography", "F5", "", ""),
    ("K-045", "rozhodnutí", "D1: potvrdit půdorys a souřadnice obou ostrovů (175 + 14 km², 33,9 N / 137,6 E)", "bible:open_decisions", "F8", "needs_decision", "otevřený bod D1"),
    # ---- GEOGRAPHY_AND_CANON.md (pracovní návrh)
    ("K-050", "orientace", "Sever nahoře, východ vpravo", "doc:references/GEOGRAPHY_AND_CANON.md#Závazná orientace", "F1", "proposed", ""),
    ("K-051", "tvar", "Hlavní ostrov protažený západ–východ, mírně členité pobřeží, západní zalesněná vysočina, nižší východ", "doc:references/GEOGRAPHY_AND_CANON.md#Závazná orientace", "F1", "proposed", ""),
    ("K-052", "tvar", "Silueta (PROPOSED): protáhlé tělo, dvě severní zátoky, západní skalnatý mys, jižní záliv kolem historického přístavu, užší jihovýchodní poloostrov", "doc:references/GEOGRAPHY_AND_CANON.md#Tvarová referenční pravidla ostrovů", "F1", "proposed", "kontrolováno analýzou zátok"),
    ("K-053", "tvar", "Paraland přibližně oválný, západní marina, severní historické městečko, východní lesy", "doc:references/GEOGRAPHY_AND_CANON.md#Tvarová referenční pravidla ostrovů", "F1", "proposed", ""),
    ("K-054", "zóny", "Vnitrozemský západ: horské řeky, vodopád, krasová/vulkanická jeskyně, přehradní jezero", "doc:references/GEOGRAPHY_AND_CANON.md#Závazná orientace", "F2", "proposed", ""),
    ("K-055", "zóny", "Východ/severovýchod: rovná průmyslová nížina a regionální letiště", "doc:references/GEOGRAPHY_AND_CANON.md#Závazná orientace", "F3", "proposed", ""),
    ("K-056", "zóny", "Jih/jihovýchod: pláže a hlavní město s historickým přístavem", "doc:references/GEOGRAPHY_AND_CANON.md#Závazná orientace", "F2", "proposed", ""),
    ("K-057", "souřadnice", "Souřadnice jsou normalizované % uvnitř referenčního obdélníku, ne GPS; X na východ, Y na jih", "doc:references/GEOGRAPHY_AND_CANON.md#Souřadnice pro návrhovou schematickou mapu", "F1", "proposed", "rámec 24 × 16 km (rozhodnutí týmu)"),
    ("K-058", "Paraland", "Paraland: západní marina a terminál L3; sever staré městečko, zřícenina, hrad; jih/střed resorty, aquapark; východ lesy, okruh, pláže v zátokách", "doc:references/GEOGRAPHY_AND_CANON.md#Paraland — referenční rozložení", "F3", "proposed", ""),
    ("K-059", "Paraland", "Paraland: jen malá plocha pro lehká letadla (PROPOSED), ne druhé velké letiště", "doc:references/GEOGRAPHY_AND_CANON.md#Paraland — referenční rozložení", "F3", "proposed", ""),
    ("K-060", "železnice", "L1: vyvýšený okruh z města do západní přírody; zastávka u vodopádu; tunel do osvětlené jeskyně, trať objíždí asi ¾ obvodu", "doc:references/GEOGRAPHY_AND_CANON.md#Železniční síť", "F3", "proposed", "rozpor C-05: okruh × linka"),
    ("K-061", "železnice", "L2: povrchové elektrické historicky stylizované vlaky; městečka a ekologická průmyslová zóna", "doc:references/GEOGRAPHY_AND_CANON.md#Železniční síť", "F3", "proposed", ""),
    ("K-062", "železnice", "L3: převážně podzemní rychlá doprava po hlavním městě a pod průlivem na Paraland, ~3 přestupy na L2; krátká výhledová galerie", "doc:references/GEOGRAPHY_AND_CANON.md#Železniční síť", "F3", "proposed", "rozpor C-06"),
    ("K-063", "silnice", "Okružní pobřežní silnice se nesmí zaměnit za železniční okruh; lesní odbočky, cyklotrasy a stezky napojené na vyhlídky a studánky", "doc:references/GEOGRAPHY_AND_CANON.md#Železniční síť", "F3", "proposed", ""),
    ("K-064", "kontrola", "Povinná kontrola foto/videa: location_id | pohled kam | strana | roční doba | styly | blízké | vzdálené body", "doc:references/GEOGRAPHY_AND_CANON.md#Povinná kontrola fotografie / videa", "F4", "proposed", "pole registru pro foto vazby"),
    ("K-065", "plán města", "Plán hlavního města: samostatná městská mapa, bloky, náměstí, přístav, muzeum, 4 správní budovy, parlament, zastávky L2/L3, školy, parky, kostel, obchody, půjčovny, promenáda; měřítko jen podle skutečných délek", "doc:references/GEOGRAPHY_AND_CANON.md#Postup pro plán hlavního města", "F7", "proposed", "v této etapě jen podklad"),
    # ---- ostatní dokumenty
    ("K-070", "tvar", "MAP_PROMPT: průliv 2–3 km (zatím návrh 1,5 km)", "doc:templates/MAP_PROMPT.md#Kanonická sekvence", "F1", "proposed", "rozpor C-01, vyřešeno: 1,5 km"),
    ("K-071", "výstupy", "Dva povinné satelitní snímky: S-01 Larpidie, S-02 Paraland (simulovaná vizualizace fiktivního ostrova)", "doc:templates/MAP_PROMPT.md#Dva povinné snímky ostrovů", "F6", "proposed", ""),
    ("K-072", "výstupy", "Plán hlavního města je v MAP_PROMPT označen M-01 (koliduje s ID vrcholu M-01)", "doc:templates/MAP_PROMPT.md#M-01 / Plán hlavního města", "F7", "proposed", "rozpor C-03, navrženo ID CP-01"),
    ("K-073", "výstupy", "Historická mapa 1608–1800: stejné pobřeží, jen dobová znalost a sídla", "doc:templates/MAP_PROMPT.md#Historická mapa", "F8", "proposed", "mimo rozsah této etapy"),
    ("K-074", "pravidlo", "Mapa: vektorové pobřeží (SVG/GeoJSON) → reliéf → lidská vrstva → styl → popisky jako textové vrstvy (cs i ja)", "doc:templates/MAP_PROMPT.md#Kanonická sekvence", "F5", "proposed", ""),
    ("K-075", "pravidlo", "Pláže ne na útesovém severozápadě; hory ne uvnitř nížinného města; Paraland je samostatný menší ostrov", "doc:SKILL.md#Fáze 2", "F2", "proposed", ""),
    ("K-076", "letiště", "REALISM: jedno malé až střední regionální letiště a jedna malá plocha na Paralandu; ne dvě obří", "doc:references/REALISM_AND_ZSV.md#Inženýrství", "F3", "proposed", ""),
    ("K-077", "inženýrství", "Podmořské spojení: jen krátký kontrolovaný panoramatický úsek", "doc:references/REALISM_AND_ZSV.md#Inženýrství", "F3", "proposed", ""),
    ("K-078", "inženýrství", "Jeskyně: umělá/rozšířená návštěvnická galerie; světlíky; světelné krystaly", "doc:references/REALISM_AND_ZSV.md#Inženýrství", "F3", "proposed", ""),
    ("K-079", "klima", "Rizika: tajfuny, eroze, vítr, seismika; pitná voda z deště, povodí, podzemních zásob, přehrady", "doc:references/REALISM_AND_ZSV.md#Zeměpis a klima", "F2", "proposed", ""),
    ("K-080", "pravidlo", "Při sporu: výslovné nové schválení > schválené údaje v bibli > návrhy v souborech > preference generátoru", "doc:README.md#Úpravy a verzování", "F0", "approved", "pravidlo priority"),
]


def resolve(path: str):
    node = B
    for part in path.split("."):
        node = node[part]
    return node


def excerpt(v, n=230):
    s = json.dumps(v, ensure_ascii=False, separators=(",", ":"))
    return s if len(s) <= n else s[: n - 1] + "…"


def main() -> None:
    out = ATLAS / "docs" / "canon_extract.csv"
    cols = ["claim_id", "area", "claim_cs", "source_type", "source", "status", "value_excerpt", "planned_phase", "atlas_objects", "note"]
    rows = []
    for cid, area, claim, src, phase, doc_status, note in ROWS:
        stype, ref = src.split(":", 1)
        if stype == "bible":
            if ref == "open_decisions":
                status, val = doc_status or "needs_decision", excerpt(B["open_decisions"][0])
            else:
                node = resolve(ref)
                status, val = node.get("status", ""), excerpt(node.get("value"))
        else:
            status, val = doc_status, ""
        rows.append([cid, area, claim, stype, ref, status, val, phase, "", note])

    # tabulka souřadnic (auto)
    for i, r in enumerate(geo_ref_table(), 1):
        rows.append([f"K-1{i:02d}", "souřadnice", f"{r['id']} {r['name_doc']} @ X={r['X_pct']} % Y={r['Y_pct']} % "
                     f"(= {r['x_km']:.2f} km, {r['y_km']:.2f} km)",
                     "doc", "references/GEOGRAPHY_AND_CANON.md#tabulka", "proposed",
                     f"existence: {r['exist_status']}; jméno: {r['name_status']}; polohy: proposed",
                     "F1", "", r["must_keep"]])

    with out.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(cols)
        w.writerows(rows)

    by = {}
    for r in rows:
        by[r[5]] = by.get(r[5], 0) + 1
    print(f"canon_extract.csv: {len(rows)} řádků; stavy: {by}")


if __name__ == "__main__":
    main()
