"""Plán hlavního města (F7): samostatný HTML prohlížeč (SVG + registr objektů CP-*): hledání, vrstvy, jazyky, režim stavů, záznam s foto/video vodítkem."""
from __future__ import annotations

import json

import cp_data as C

CSS = """
:root{--bg:#f6f4ee;--ink:#1f2a33;--soft:#5a6670;--line:#d9d3c3;--acc:#8a3f6e;--card:#fffdf8;--ok:#2a8a4a;--warn:#d9741a;--bad:#c0392b}
@media (prefers-color-scheme:dark){:root{--bg:#141a1f;--ink:#e8e6df;--soft:#9aa6ae;--line:#2c353c;--acc:#e0a0c8;--card:#1b2227}}
*{box-sizing:border-box}html,body{height:100%;margin:0}body{background:var(--bg);color:var(--ink);font:15px/1.5 'Segoe UI',system-ui,sans-serif;display:grid;grid-template-columns:300px minmax(0,1fr) 350px;grid-template-rows:auto 1fr auto}
header{grid-column:1/-1;display:flex;gap:14px;align-items:center;padding:10px 15px;border-bottom:1px solid var(--line);background:var(--card)}header h1{font-size:1.18rem;margin:0;font-weight:750}.badge{background:var(--acc);color:#fff;border-radius:999px;padding:2px 10px;font-size:.8rem;font-weight:750}
.city3d-link{margin-left:auto;color:var(--acc);font-size:.86rem;font-weight:750;white-space:nowrap}
aside{overflow:auto;padding:13px 14px;border-right:1px solid var(--line)}aside.r{border-right:0;border-left:1px solid var(--line)}h2{font-size:.9rem;text-transform:uppercase;letter-spacing:.05em;color:var(--soft);margin:13px 0 7px;font-weight:750}
#map{position:relative;overflow:hidden;background:#d3e6f0;cursor:grab;touch-action:none}#map.drag{cursor:grabbing}#map svg{width:100%;height:100%;display:block}#map svg [data-id]{cursor:pointer;transition:filter .12s ease}#map svg [data-id]:hover{filter:drop-shadow(0 0 7px rgba(255,177,71,.95))}
label.row{display:flex;gap:8px;align-items:center;padding:2px 0;cursor:pointer}input[type=search]{width:100%;padding:7px 9px;border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--ink)}
.seg{display:flex;border:1px solid var(--line);border-radius:8px;overflow:hidden}.seg button{flex:1;padding:5px;border:0;background:var(--card);color:var(--ink);cursor:pointer}.seg button[aria-pressed=true]{background:var(--ink);color:var(--bg)}
#results{max-height:230px;overflow:auto;margin-top:6px}#results div{padding:5px 7px;border-radius:6px;cursor:pointer;display:flex;justify-content:space-between;gap:8px;font-weight:550}#results div:hover{background:var(--line)}
.st{display:inline-block;border-radius:999px;padding:0 8px;font-size:.72rem;color:#fff}.st.approved{background:var(--ok)}.st.proposed{background:var(--warn)}.st.needs_decision{background:var(--bad)}
dl{margin:7px 0}dt{color:var(--soft);font-size:.82rem;margin-top:7px;font-weight:650}dd{margin:1px 0;font-size:.92rem;font-weight:520}footer{grid-column:1/-1;padding:6px 14px;border-top:1px solid var(--line);color:var(--soft);font-size:.84rem;font-weight:600;display:flex;justify-content:space-between;background:var(--card)}
button.small{font:inherit;padding:3px 10px;border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--ink);cursor:pointer}
@media (max-width:980px){body{grid-template-columns:1fr;grid-template-rows:auto 62vh auto auto auto}#map{order:1}aside{border:0;order:2;max-height:none}aside.r{order:3}footer{order:4}}
"""

JS = r"""
const svg=document.querySelector('#map svg');const REG=JSON.parse(document.getElementById('reg').textContent);const BYID=Object.fromEntries(REG.objects.map(o=>[o.id,o]));
const vb0=svg.viewBox.baseVal;const FULL=[vb0.x,vb0.y,vb0.width,vb0.height];let vb=[...FULL];svg.removeAttribute('width');svg.removeAttribute('height');
const X0=REG.meta.origin_atlas_km.x,Y0=REG.meta.origin_atlas_km.y;let numberFrame=0;function setVB(){svg.setAttribute('viewBox',vb.join(' '));if(numberFrame)return;numberFrame=requestAnimationFrame(updateHouseNumbers)}
const map=document.getElementById('map');
function updateHouseNumbers(){numberFrame=0;const layer=svg.getElementById('house-numbers'),toggle=document.getElementById('house-numbers-toggle');if(!layer)return;const enabled=!!toggle?.checked&&vb[2]<=1100;layer.style.display=enabled?'':'none';if(!enabled)return;const rect=svg.getBoundingClientRect(),matrix=svg.getScreenCTM(),labels=[...layer.querySelectorAll('text')],font=Math.max(5,Math.min(18,vb[2]/Math.max(1,rect.width)*11));const occupied=new Set(),cell=24;for(const el of labels){el.style.fontSize=font+'px';const x=Number(el.getAttribute('x')),y=Number(el.getAttribute('y'));if(x<vb[0]||x>vb[0]+vb[2]||y<vb[1]||y>vb[1]+vb[3]){el.style.display='none';continue}const pt=svg.createSVGPoint();pt.x=x;pt.y=y;const p=pt.matrixTransform(matrix),key=Math.floor(p.x/cell)+','+Math.floor(p.y/cell);if(occupied.has(key)){el.style.display='none';continue}occupied.add(key);el.style.display=''} }
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
function addFutureDevelopment(){if(svg.getElementById('future-development'))return;const layer=document.createElementNS('http://www.w3.org/2000/svg','g');layer.setAttribute('id','future-development');layer.setAttribute('inkscape:groupmode','layer');layer.setAttribute('inkscape:label','Návrh budoucí zástavby v rezervě');layer.setAttribute('aria-label','Schematické budoucí domy v dosud nezastavěných blocích');layer.style.pointerEvents='none';const blockPaths=[...svg.querySelectorAll('#blocks path[data-id]')],houses=[...svg.querySelectorAll('#houses path')],bins=new Map(),binSize=100,key=(x,y)=>`${x},${y}`;function bin(box,item){const x0=Math.floor(box.x/binSize),y0=Math.floor(box.y/binSize),x1=Math.floor((box.x+box.width)/binSize),y1=Math.floor((box.y+box.height)/binSize);for(let y=y0;y<=y1;y++)for(let x=x0;x<=x1;x++){const k=key(x,y);if(!bins.has(k))bins.set(k,[]);bins.get(k).push(item)}}houses.forEach(el=>{try{const b=el.getBBox();bin(b,b)}catch{}});const colors={residential_low:'#b69b79',residential_mid:'#b88368',old_town_mixed:'#b9775b',promenade_retail:'#c28b69',retail_main:'#c49a70',transit_mixed:'#ad856d',new_waterfront:'#aaa9b4'};let made=0;for(const path of blockPaths){const o=BYID[path.getAttribute('data-id')];if(!o||!['reserve','partial'].includes(o.build_state))continue;const box=path.getBBox(),use=o.land_use||'residential_mid',wanted=o.build_state==='partial'?2:use==='residential_low'?3:use==='new_waterfront'?4:5,remaining=Math.max(0,wanted-(o.houses||0));if(!remaining||box.width<14||box.height<12)continue;const cols=Math.max(1,Math.ceil(Math.sqrt(wanted*box.width/box.height))),rows=Math.max(1,Math.ceil(wanted/cols)),w=Math.min(13,box.width/(cols+1)*.48),h=Math.min(9,box.height/(rows+1)*.48),seed=[...o.id].reduce((a,c)=>(a*31+c.charCodeAt(0))>>>0,7);let placed=0;for(let n=0;n<cols*rows&&placed<remaining;n++){const idx=(n+seed)%(cols*rows),col=idx%cols,row=Math.floor(idx/cols),cx=box.x+(col+1)*box.width/(cols+1),cy=box.y+(row+1)*box.height/(rows+1),pts=[[cx-w/2,cy-h/2],[cx+w/2,cy-h/2],[cx+w/2,cy+h/2],[cx-w/2,cy+h/2]];const p=svg.createSVGPoint();if(!pts.every(([x,y])=>{p.x=x;p.y=y;return path.isPointInFill(p)}))continue;const test={x:cx-w/2,y:cy-h/2,width:w,height:h},bx0=Math.floor(test.x/binSize),by0=Math.floor(test.y/binSize),bx1=Math.floor((test.x+w)/binSize),by1=Math.floor((test.y+h)/binSize);let overlap=false;for(let yy=by0;yy<=by1&&!overlap;yy++)for(let xx=bx0;xx<=bx1&&!overlap;xx++)for(const old of bins.get(key(xx,yy))||[])if(!(test.x+test.width<old.x||test.x>old.x+old.width||test.y+test.height<old.y||test.y>old.y+old.height)){overlap=true;break}if(overlap)continue;const node=document.createElementNS('http://www.w3.org/2000/svg','path');node.setAttribute('d',`M${pts.map(q=>q.join(',')).join(' L')} Z`);node.setAttribute('fill',colors[use]||'#b88368');node.setAttribute('fill-opacity','.8');node.setAttribute('stroke','#5f5146');node.setAttribute('stroke-width','1.3');node.setAttribute('stroke-dasharray','3 2');node.setAttribute('data-id',`future-${o.id}-${placed+1}`);node.setAttribute('data-proposed','true');layer.appendChild(node);bin(test,test);placed++;made++}}const labels=svg.getElementById('labels-cs');svg.insertBefore(layer,labels||null);layer.setAttribute('data-count',String(made))}
let activeLang='cs';function declutterLabels(){const all=[...svg.querySelectorAll('#labels-cs text,#labels-en text,#labels-ja text')];all.forEach(el=>{if(el.dataset.collisionHidden){el.style.removeProperty('display');delete el.dataset.collisionHidden}});const layer=svg.getElementById('labels-'+activeLang);if(!layer||layer.style.display==='none')return;const labels=[...layer.querySelectorAll('text')].map(el=>{let box;try{box=el.getBBox()}catch{return null}const size=parseFloat(el.getAttribute('font-size'))||16,isDistrict=Number(el.getAttribute('opacity'))<.5&&size>50,isRoad=!!el.querySelector('textPath'),weight=Number(el.getAttribute('font-weight'))||400;const priority=isDistrict?5:isRoad?35:size>=25&&weight>=650?85:size>=18?70:size>=13?55:40;return{el,box,size,priority}}).filter(x=>x&&x.box.width>0&&x.box.height>0).sort((a,b)=>b.priority-a.priority||b.size-a.size);const kept=[];for(const item of labels){const pad=Math.max(3,item.size*.18),b=item.box,clash=kept.some(k=>!(b.x+b.width+pad<k.x||b.x-pad>k.x+k.width||b.y+b.height+pad<k.y||b.y-pad>k.y+k.height));if(clash){item.el.style.display='none';item.el.dataset.collisionHidden='true'}else kept.push({x:b.x-pad,y:b.y-pad,width:b.width+pad*2,height:b.height+pad*2})}}
addFutureDevelopment();
const layers=[...svg.querySelectorAll(':scope > g[id]')].filter(g=>g.getAttribute('inkscape:groupmode')==='layer');const lp=document.getElementById('layers');
const groups={'Základ':['bg-sea','land','contours','beaches','grid'],'Město':['green-wedges','districts','blocks','spaces','harbor'],'Doprava':['streets','rail-surface','rail-L3','stations','access-route'],'Objekty':['houses','buildings-key','poi'],'Rozvoj':['future-development'],'Popisky':['labels-cs','labels-en','labels-ja'],'Okraje':['marginalia']};
for(const [gname,ids] of Object.entries(groups)){const present=ids.filter(i=>svg.getElementById(i));if(!present.length)continue;lp.insertAdjacentHTML('beforeend',`<h2>${gname}</h2>`);
 present.forEach(i=>{const el=svg.getElementById(i);const lab=el.getAttribute('inkscape:label')||i;const on=!(i.startsWith('labels-')&&i!=='labels-cs')&&i!=='contours';el.style.display=on?'':'none';
 lp.insertAdjacentHTML('beforeend',`<label class="row"><input type="checkbox" data-l="${i}" ${on?'checked':''}> ${esc(lab)}</label>`)})}
lp.addEventListener('change',e=>{const i=e.target.dataset.l;if(i)svg.getElementById(i).style.display=e.target.checked?'':'none'});
document.querySelectorAll('[data-lang]').forEach(b=>b.onclick=()=>{activeLang=b.dataset.lang;document.querySelectorAll('[data-lang]').forEach(x=>x.setAttribute('aria-pressed',x===b));['cs','ja','en'].forEach(l=>{const el=svg.getElementById('labels-'+l);if(el)el.style.display=(l===activeLang)?'':'none';const cb=lp.querySelector(`[data-l="labels-${l}"]`);if(cb)cb.checked=(l===activeLang)});requestAnimationFrame(()=>requestAnimationFrame(declutterLabels))});
requestAnimationFrame(()=>requestAnimationFrame(declutterLabels));
document.getElementById('status').onchange=e=>svg.classList.toggle('status-mode',e.target.checked);
document.getElementById('house-numbers-toggle').onchange=()=>{if(numberFrame)cancelAnimationFrame(numberFrame);numberFrame=requestAnimationFrame(updateHouseNumbers)};
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
<header><h1>Larpington – podklad plánu hlavního města (CP-01)</h1><span class="badge">NÁVRH · v{meta['atlas_version']}</span><span style="color:var(--soft)">A2 · 1 : 10 000 · kolečko = přiblížení, tažení = posun, klik = záznam</span><a class="city3d-link" href="capital-3d.html" target="_blank" rel="noopener">Otevřít 3D Larpington ↗</a></header>
<aside><h2>Hledání</h2><input id="q" type="search" placeholder="ID nebo název (např. CP-B01, parlament, tržnice)"><div id="results"></div>
<h2>Jazyk popisků</h2><div class="seg"><button data-lang="cs" aria-pressed="true">CS</button><button data-lang="ja" aria-pressed="false">JA</button><button data-lang="en" aria-pressed="false">EN</button></div>
<h2>Režim</h2><label class="row"><input type="checkbox" id="status"> Obrysy podle stavu (schváleno × návrh)</label><label class="row"><input type="checkbox" id="house-numbers-toggle"> Čísla domů při přiblížení</label><button class="small" id="reset">Celý plán</button>
<div id="layers"></div></aside>
<div id="map">{svg_inline}</div>
<aside class="r"><h2>Záznam</h2><div id="info"><p style="color:var(--soft)">Klikněte na objekt v plánu nebo ho vyhledejte. Zobrazí se stav, poloha v metrech plánu i v km atlasu a foto/video vodítko.</p></div></aside>
<footer><span id="coord">–</span><span id="count"></span></footer>
<script id="reg" type="application/json">{reg}</script><script>{JS}</script></body></html>"""
