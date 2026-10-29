"""Plán hlavního města (F7): samostatný HTML prohlížeč (SVG + registr objektů CP-*): hledání, vrstvy, jazyky, režim stavů, záznam s foto/video vodítkem."""
from __future__ import annotations

import json

import cp_data as C

CSS = """
:root{--bg:#f6f4ee;--ink:#1f2a33;--soft:#5a6670;--line:#d9d3c3;--acc:#8a3f6e;--card:#fffdf8;--ok:#2a8a4a;--warn:#d9741a;--bad:#c0392b}
@media (prefers-color-scheme:dark){:root{--bg:#141a1f;--ink:#e8e6df;--soft:#9aa6ae;--line:#2c353c;--acc:#e0a0c8;--card:#1b2227}}
*{box-sizing:border-box}html,body{height:100%;margin:0}body{background:var(--bg);color:var(--ink);font:14px/1.45 'Segoe UI',system-ui,sans-serif;display:grid;grid-template-columns:310px 1fr 350px;grid-template-rows:auto 1fr auto}
header{grid-column:1/-1;display:flex;gap:14px;align-items:center;padding:8px 14px;border-bottom:1px solid var(--line);background:var(--card)}header h1{font-size:1.05rem;margin:0}.badge{background:var(--acc);color:#fff;border-radius:999px;padding:1px 10px;font-size:.75rem}
aside{overflow:auto;padding:10px 12px;border-right:1px solid var(--line)}aside.r{border-right:0;border-left:1px solid var(--line)}h2{font-size:.8rem;text-transform:uppercase;letter-spacing:.05em;color:var(--soft);margin:12px 0 6px}
#map{position:relative;overflow:hidden;background:#d3e6f0;cursor:grab;touch-action:none}#map.drag{cursor:grabbing}#map svg{width:100%;height:100%;display:block}
label.row{display:flex;gap:8px;align-items:center;padding:2px 0;cursor:pointer}input[type=search]{width:100%;padding:7px 9px;border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--ink)}
.seg{display:flex;border:1px solid var(--line);border-radius:8px;overflow:hidden}.seg button{flex:1;padding:5px;border:0;background:var(--card);color:var(--ink);cursor:pointer}.seg button[aria-pressed=true]{background:var(--ink);color:var(--bg)}
#results{max-height:230px;overflow:auto;margin-top:6px}#results div{padding:4px 6px;border-radius:6px;cursor:pointer;display:flex;justify-content:space-between;gap:8px}#results div:hover{background:var(--line)}
.st{display:inline-block;border-radius:999px;padding:0 8px;font-size:.72rem;color:#fff}.st.approved{background:var(--ok)}.st.proposed{background:var(--warn)}.st.needs_decision{background:var(--bad)}
dl{margin:6px 0}dt{color:var(--soft);font-size:.75rem;margin-top:6px}dd{margin:0}footer{grid-column:1/-1;padding:4px 14px;border-top:1px solid var(--line);color:var(--soft);font-size:.8rem;display:flex;justify-content:space-between;background:var(--card)}
button.small{font:inherit;padding:3px 10px;border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--ink);cursor:pointer}
@media (max-width:980px){body{grid-template-columns:1fr;grid-template-rows:auto 62vh auto auto auto}#map{order:1}aside{border:0;order:2;max-height:none}aside.r{order:3}footer{order:4}}
"""

JS = r"""
const svg=document.querySelector('#map svg');const REG=JSON.parse(document.getElementById('reg').textContent);const BYID=Object.fromEntries(REG.objects.map(o=>[o.id,o]));
const vb0=svg.viewBox.baseVal;const FULL=[vb0.x,vb0.y,vb0.width,vb0.height];let vb=[...FULL];svg.removeAttribute('width');svg.removeAttribute('height');
const X0=REG.meta.origin_atlas_km.x,Y0=REG.meta.origin_atlas_km.y;function setVB(){svg.setAttribute('viewBox',vb.join(' '))}
const map=document.getElementById('map');
function clientToSvg(ev){const r=svg.getBoundingClientRect();const k=Math.max(vb[2]/r.width,vb[3]/r.height);const cx=r.left+r.width/2,cy=r.top+r.height/2;return [vb[0]+vb[2]/2+(ev.clientX-cx)*k,vb[1]+vb[3]/2+(ev.clientY-cy)*k]}
map.addEventListener('wheel',e=>{e.preventDefault();const [sx,sy]=clientToSvg(e);const f=e.deltaY<0?0.8:1.25;const nw=Math.min(FULL[2],vb[2]*f),nh=nw*vb[3]/vb[2];vb=[sx-(sx-vb[0])*nw/vb[2],sy-(sy-vb[1])*nh/vb[3],nw,nh];setVB()},{passive:false});
let drag=null;map.addEventListener('pointerdown',e=>{drag={x:e.clientX,y:e.clientY,vb:[...vb],moved:false};map.setPointerCapture(e.pointerId)});
map.addEventListener('pointermove',e=>{const [sx,sy]=clientToSvg(e);document.getElementById('coord').textContent=`u ${sx.toFixed(0)} m · v ${sy.toFixed(0)} m · atlas x ${(X0+sx/1000).toFixed(3)} km, y ${(Y0+sy/1000).toFixed(3)} km`;
 if(drag){const r=svg.getBoundingClientRect();const k=Math.max(vb[2]/r.width,vb[3]/r.height);if(Math.abs(e.clientX-drag.x)+Math.abs(e.clientY-drag.y)>4){drag.moved=true;map.classList.add('drag')}vb=[drag.vb[0]-(e.clientX-drag.x)*k,drag.vb[1]-(e.clientY-drag.y)*k,vb[2],vb[3]];setVB()}});
map.addEventListener('pointerup',e=>{const was=drag&&drag.moved;drag=null;map.classList.remove('drag');if(!was){const t=e.target.closest('[data-id]');if(t)show(t.getAttribute('data-id'))}});
function zoomTo(o,w=700){const r=svg.getBoundingClientRect();const h=w*r.height/r.width;vb=[o.u-w/2,o.v-h/2,w,h];setVB()}
let hlEl=[];function highlight(id){hlEl.forEach(e=>e.classList.remove('hl'));hlEl=[...svg.querySelectorAll(`[data-id="${CSS.escape(id)}"]`)].filter(e=>!e.closest('#labels-cs,#labels-ja,#labels-en'));hlEl.forEach(e=>e.classList.add('hl'))}
function esc(s){return String(s??'').replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]))}
function stBadge(k,v){return `<span class="st ${esc(v)}" title="${esc(k)}">${esc(k)}: ${esc(v)}</span>`}
function show(id){const o=BYID[id];const box=document.getElementById('info');if(!o){box.innerHTML=`<p>Objekt <b>${esc(id)}</b> není v registru plánu (atlasový objekt viz atlas.html).</p>`;return}highlight(id);const g=o.photo_guide;
 let h=`<h3 style="margin:.2em 0">${esc(o.id)} · ${esc(o.name_cs)}</h3><div style="color:var(--soft)">${esc(o.name_en||'')}${o.name_ja?' · '+esc(o.name_ja):''}</div>`;
 h+=`<p>${stBadge('existence',o.exist_status)} ${stBadge('jméno',o.name_status)} ${stBadge('poloha',o.pos_status)}</p><dl>`;
 h+=`<dt>Typ</dt><dd>${esc(o.type)} / ${esc(o.subtype||'')}${o.district?' · čtvrť '+esc(o.district):''}</dd>`;
 h+=`<dt>Poloha</dt><dd>u ${o.u} m, v ${o.v} m (plán) · atlas x ${o.x_km} km, y ${o.y_km} km</dd>`;
 if(o.area_m2)h+=`<dt>Plocha</dt><dd>${o.area_m2.toLocaleString('cs')} m²</dd>`;if(o.length_m)h+=`<dt>Délka</dt><dd>${o.length_m} m</dd>`;
 if(o.land_use)h+=`<dt>Využití</dt><dd>${esc(o.land_use_text||o.land_use)}</dd>`;if(o.lines)h+=`<dt>Linky</dt><dd>${o.lines.join(', ')}</dd>`;
 if(o.atlas_ref)h+=`<dt>Odkaz do atlasu</dt><dd>${esc(o.atlas_ref)}</dd>`;if(o.bible_ref)h+=`<dt>Bible / zadání</dt><dd>${esc(o.bible_ref)}</dd>`;if(o.notes)h+=`<dt>Poznámka</dt><dd>${esc(o.notes)}</dd>`;
 if(g){h+=`<h2>Foto / video vodítko</h2><dl><dt>Pohled kam</dt><dd>${esc(g.view_toward)}${g.sea_direction?` · moře: ${esc(g.sea_direction)}`:''}</dd><dt>Blízké body</dt><dd>${esc((g.near_ids||[]).join(', ')||'–')}</dd>`+
  `<dt>Vzdálené viditelné</dt><dd>${esc((g.far_visible||[]).map(v=>`${v.id} (${v.dir}, ${v.dist_km} km)`).join('; ')||'–')}</dd><dt>Styl</dt><dd>${esc(g.styles)}</dd><dt>Roční doba</dt><dd>${esc(g.season)}</dd><dt>Vyhnout se</dt><dd>${esc(g.avoid)}</dd></dl>`}
 box.innerHTML=h+'</dl><p><button class="small" onclick="zoomTo(BYID[\''+o.id+'\'])">Přiblížit</button></p>'}
const layers=[...svg.querySelectorAll(':scope > g[id]')].filter(g=>g.getAttribute('inkscape:groupmode')==='layer');const lp=document.getElementById('layers');
const groups={'Základ':['bg-sea','land','contours','beaches','grid'],'Město':['green-wedges','districts','blocks','spaces','harbor'],'Doprava':['streets','rail-surface','rail-L3','stations','access-route'],'Objekty':['houses','buildings-key','poi'],'Popisky':['labels-cs','labels-en','labels-ja'],'Okraje':['marginalia']};
for(const [gname,ids] of Object.entries(groups)){const present=ids.filter(i=>svg.getElementById(i));if(!present.length)continue;lp.insertAdjacentHTML('beforeend',`<h2>${gname}</h2>`);
 present.forEach(i=>{const el=svg.getElementById(i);const lab=el.getAttribute('inkscape:label')||i;const on=!(i.startsWith('labels-')&&i!=='labels-cs')&&i!=='contours';el.style.display=on?'':'none';
 lp.insertAdjacentHTML('beforeend',`<label class="row"><input type="checkbox" data-l="${i}" ${on?'checked':''}> ${esc(lab)}</label>`)})}
lp.addEventListener('change',e=>{const i=e.target.dataset.l;if(i)svg.getElementById(i).style.display=e.target.checked?'':'none'});
document.querySelectorAll('[data-lang]').forEach(b=>b.onclick=()=>{document.querySelectorAll('[data-lang]').forEach(x=>x.setAttribute('aria-pressed',x===b));['cs','ja','en'].forEach(l=>{const el=svg.getElementById('labels-'+l);if(el)el.style.display=(l===b.dataset.lang)?'':'none';const cb=lp.querySelector(`[data-l="labels-${l}"]`);if(cb)cb.checked=(l===b.dataset.lang)})});
document.getElementById('status').onchange=e=>svg.classList.toggle('status-mode',e.target.checked);
document.getElementById('reset').onclick=()=>{vb=[...FULL];setVB()};
const q=document.getElementById('q'),res=document.getElementById('results');
function search(){const t=q.value.trim().toLowerCase();if(!t){res.innerHTML='';return}
 const hits=REG.objects.filter(o=>o.u!=null&&((o.id+' '+o.name_cs+' '+(o.name_en||'')+' '+(o.name_ja||'')).toLowerCase().includes(t))).slice(0,40);
 res.innerHTML=hits.map(o=>`<div data-id="${esc(o.id)}"><span>${esc(o.id)} · ${esc(o.name_cs)}</span><span class="st ${esc(o.exist_status)}">${esc(o.exist_status)}</span></div>`).join('')}
q.addEventListener('input',search);res.addEventListener('click',e=>{const d=e.target.closest('[data-id]');if(d){const o=BYID[d.dataset.id];zoomTo(o);show(o.id)}});
document.getElementById('count').textContent=REG.objects.length+' objektů v registru plánu';
"""


def viewer_html(svg_text: str, objs: list, meta: dict) -> str:
    svg_inline = svg_text.split("?>", 1)[1].strip()
    slim = []
    for o in objs:
        d = {k: v for k, v in o.items() if k not in ("poly", "plan_geometry")}
        slim.append(d)
    reg = json.dumps({"meta": meta, "objects": slim}, ensure_ascii=False)
    return f"""<!doctype html><html lang="cs"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Larpington – podklad plánu města</title><style>{CSS}</style></head><body>
<header><h1>Larpington – podklad plánu hlavního města (CP-01)</h1><span class="badge">NÁVRH · v{meta['atlas_version']}</span><span style="color:var(--soft)">A2 · 1 : 10 000 · kolečko = přiblížení, tažení = posun, klik = záznam</span></header>
<aside><h2>Hledání</h2><input id="q" type="search" placeholder="ID nebo název (např. CP-B01, parlament, tržnice)"><div id="results"></div>
<h2>Jazyk popisků</h2><div class="seg"><button data-lang="cs" aria-pressed="true">CS</button><button data-lang="ja" aria-pressed="false">JA</button><button data-lang="en" aria-pressed="false">EN</button></div>
<h2>Režim</h2><label class="row"><input type="checkbox" id="status"> Obrysy podle stavu (schváleno × návrh)</label><button class="small" id="reset">Celý plán</button>
<div id="layers"></div></aside>
<div id="map">{svg_inline}</div>
<aside class="r"><h2>Záznam</h2><div id="info"><p style="color:var(--soft)">Klikněte na objekt v plánu nebo ho vyhledejte. Zobrazí se stav, poloha v metrech plánu i v km atlasu a foto/video vodítko.</p></div></aside>
<footer><span id="coord">–</span><span id="count"></span></footer>
<script id="reg" type="application/json">{reg}</script><script>{JS}</script></body></html>"""
