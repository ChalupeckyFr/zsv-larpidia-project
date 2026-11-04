# Technická poznámka k současným 3D scénám

Tato zpráva je pouze rozbor. Zdrojové soubory, výšková data, geometrie ani ovládání 3D scén nebyly upraveny.

## Použitá technologie a geometrie

Obě scény používají vlastní vykreslování přes **WebGL 1.0**, GLSL vertex/fragment shadery a nativní 'canvas'. Není zde Three.js ani Babylon.js.

- **Terén:** [terrain-3d.html](../atlas/current/viewer/terrain-3d.html) čte výškovou mřížku 297 × 210 a při vykreslení ji převzorkuje na 593 × 419 bodů. Dlaždice po 254 buňkách dávají 6 terénních GPU bufferů. Vedle nich se vykresluje oceán, vodní prvky a volitelně okružní silnice. Sezónní počasí se kreslí samostatnou 2D canvas vrstvou.
- **Larpington:** [capital-3d.html](../atlas/current/capital/capital-3d.html) vytváří batched vertex/index buffery z [capital-3d-data.js](../atlas/current/capital/capital-3d-data.js). Zdroj obsahuje následující počty polygonálních prvků v jednotlivých kategoriích:

| Kategorie | Prvků |
| --- | --- |
| blocks | 556 |
| houses | 3822 |
| future | 1153 |
| buildings | 14 |
| piers | 1 |
| streets | 1523 |
| parks | 24 |

Kreslení města slučuje domy, bloky, budovy, budoucí stavby, náměstí, silnice, dominanty a pobřežní prvky do skupin bufferů. Alternativní přírodní režim v [capital-3d-nature.js](../atlas/current/capital/capital-3d-nature.js) seskupuje bloky, parky, trávníky, domy, budovy, zeleň a cesty.

## Kamera a ovládání

V obou scénách tažení ukazatelem otáčí kameru; kolečko upravuje rychlost pohybu. Klávesy WASD nebo šipky posouvají kameru, Ctrl/Shift mění výšku a Home obnoví výchozí kameru. Rozhraní nabízí ovladač rychlosti, změnu převýšení a u terénu volbu sezony, barevného režimu a okružní silnice; městská scéna má přepnutí technického/přírodního stylu, budoucích staveb a názvů ulic. Vstup používá Pointer Events, proto obslouží i dotykové ukazatele.

## Výkonová místa a bezpečný další krok

Terén překresluje šest dlaždic a při změně sezony nebo převýšení znovu generuje výškové buffery; počasí běží přes 'requestAnimationFrame'. Larpington při změně převýšení přestavuje více skupin městské geometrie, zatímco přírodní vrstvu sestavuje při prvním použití a ukládá ji do bufferů. Rozumné další ověření je zaznamenat čas vykreslení a dobu změny převýšení na jednom desktopu a jednom mobilním zařízení, potom případně oddělit opakované buffer uploady od změn kamery. Bez profilování není vhodné přidávat detailnější stíny, větší výškovou mřížku ani nový renderer.

Ohraničený další úkol: samostatný profilovací průchod se dvěma referenčními zařízeními, bez úpravy souřadnic či topologie; změny pouze po srovnání snímkové frekvence, času obnovy scény a paměti GPU.

Ověření zachování: čtyři zdrojové 3D datové soubory se přesně shodují s veřejnými kopiemi podle SHA-256; zdrojové HTML obou 3D scén je shodné s výchozím stavem.
