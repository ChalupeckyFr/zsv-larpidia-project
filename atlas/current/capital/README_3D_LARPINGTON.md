# 3D Larpington

## Zdroj a generování

- `capital-3d.html` vykresluje město v atlasovém i přírodním režimu.
- `capital-3d-nature.js` přidává materiály, okna, zahrady, ploty a vegetaci.
- `capital-3d-data.js` se generuje z aktuálních `cp_*.geojson` skriptem `atlas/scripts/build_capital_3d_data.mjs`.
- Geometrii města vytváří `atlas/scripts/build_capital.py` z modulů `cp_*.py`.

## Ovládání

- **Pravé tlačítko + tažení myší:** otáčení pohledu. Na dotykové obrazovce otáčejte jedním prstem.
- **W/A/S/D nebo šipky:** pohyb vpřed, vlevo, vzad a vpravo.
- **Ctrl:** pohyb kamery nahoru. **Shift:** pohyb dolů.
- **Kolečko nebo posuvník rychlosti:** nastavení pohybu od 0,25× do 5×; kolečko nemění přiblížení.
- **Home** nebo tlačítko **Výchozí pohled:** návrat k výchozí pozici.

## Radnice a veřejná prostranství

Radnice a sídlo parlamentu stojí uprostřed Radničního náměstí a Náměstí čtyř. Její světlá neorenesanční fasáda, strmá střecha, věž s hodinami a menší nárožní věžičky jsou volně inspirované libereckou radnicí. Jde o návrh pro Larpington, ne kopii skutečné stavby. Obě náměstí mají dlážděný povrch a procedurální stromy ani uliční stromořadí do jejich hranic nezasahují.

## Přístav

Molo je dlouhé 230 m a navazuje na dlážděný předprostor. Jeho tvar se bere z objektu `CP-PI01`, takže data plánu a 3D model sdílejí stejnou geometrii. Samostatný trajektový terminál byl odstraněn. Hladina vnějšího moře navazuje na pobřežní vodní buňky terénu; přístavní voda, molo, vlnolamy a vybrané pláže zůstávají součástí obou 3D režimů.

## Omezení

Město, budovy, zeleň i výšky jsou vizualizační návrh. Nejde o geodetický plán ani skutečné stavby. Přírodní detaily jsou procedurální a jejich hustota se může lišit podle výkonu zařízení.