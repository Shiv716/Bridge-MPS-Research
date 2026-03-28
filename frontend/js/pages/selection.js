/* ─── Bridge – MPS Selection Page ──────────────────────────────────── */

async function rSel(el){
const f=await F('/api/selection/filters'),d=await F('/api/selection/mps?risk_min=1&risk_max=10');
if(!f||!d){el.innerHTML='<p>Failed to load</p>';return}
el.innerHTML=`<div class="fi"><div class="ph1"><h1>MPS Selection</h1><p>Filter the MPS universe to find solutions relevant for your firm</p></div>
<div class="filter-bar">
<div class="fg"><span class="fl">Platform</span><div class="ms-wrap" id="ms-plat"><button class="ms-btn" onclick="togMS('ms-plat')">All Platforms</button><div class="ms-dd">${f.platforms.map(p=>`<label class="ms-opt"><input type="checkbox" value="${p}" onchange="updMS('ms-plat');flt()"> ${p}</label>`).join('')}</div></div></div>
<div class="fg"><span class="fl">Fund Selection</span><div class="ms-wrap" id="ms-fs"><button class="ms-btn" onclick="togMS('ms-fs')">All</button><div class="ms-dd">${(f.investment_styles||[]).map(s=>`<label class="ms-opt"><input type="radio" name="fs" value="${s}" onchange="updFS();flt()"> ${s}</label>`).join('')}</div></div></div>
<div class="fg"><span class="fl">Risk Rating Provider</span><div class="ms-wrap" id="ms-rrp"><button class="ms-btn" onclick="togMS('ms-rrp')">All Providers</button><div class="ms-dd">${(f.risk_rating_providers||[]).map(r=>`<label class="ms-opt"><input type="checkbox" value="${r}" onchange="updMS('ms-rrp');flt()"> ${r}</label>`).join('')}</div></div></div>
<div class="fg" style="align-self:flex-end"><button class="btn btn-g btn-sm" onclick="rflt()">Reset</button></div>
</div>
<div class="card"><div class="card-h"><span class="card-t" id="mc">${grpRanges(d.mps).length} MPS Ranges</span></div>
<div style="padding:0"><div class="table-wrap"><table><thead><tr><th>MPS Range</th><th>Fund Selection</th><th>Risk Levels</th><th>All in Fee</th><th>Platforms</th></tr></thead>
<tbody id="mt">${mRows(d.mps)}</tbody></table></div></div></div></div>`}

function grpRanges(mps){const g={};mps.forEach(m=>{const rn=m.name.replace(/\s+\d+$/,'');if(!g[rn])g[rn]={name:rn,provider:m.provider,risks:[],ocfs:[],platforms:m.platforms||[],style:''};g[rn].risks.push(m.risk_rating);g[rn].ocfs.push(m.ocf)});return Object.values(g).map(r=>{r.risks.sort((a,b)=>a-b);return r})}
function mRows(mps){return grpRanges(mps).map(r=>`<tr class="cr" onclick="nav('provider',{id:'${pId(r.provider)}'})">
<td class="nc">${r.name}</td><td><span class="badge b-blue">Active</span></td>
<td>${r.risks[0]}-${r.risks[r.risks.length-1]}</td>
<td>${Math.min(...r.ocfs).toFixed(2)}% - ${Math.max(...r.ocfs).toFixed(2)}%</td>
<td style="font-size:11px;max-width:180px;overflow:hidden;text-overflow:ellipsis">${r.platforms.join(', ')}</td></tr>`).join('')}

async function flt(){
let u='/api/selection/mps?risk_min=1&risk_max=10';
const selPlats=getMS('ms-plat');
if(selPlats.length)u+=`&platforms=${selPlats.join(',')}`;
delete S.c[u];const d=await F(u);if(!d)return;
let filtered=d.mps;
const fsWrap=document.getElementById('ms-fs');const fsSel=fsWrap?fsWrap.querySelector('input:checked'):null;const fs=fsSel?fsSel.value:'';
if(fs){const provs=await F('/api/providers');if(provs){const matchProvs=provs.providers.filter(p=>p.investment_style===fs).map(p=>p.name);filtered=filtered.filter(m=>matchProvs.includes(m.provider))}}
const selRRP=getMS('ms-rrp');
if(selRRP.length){const provs=await F('/api/providers');if(provs){const matchProvs=provs.providers.filter(p=>(p.risk_rating_providers||[]).some(r=>selRRP.includes(r))).map(p=>p.name);filtered=filtered.filter(m=>matchProvs.includes(m.provider))}}
const ranges=grpRanges(filtered);
$('mc').textContent=`${ranges.length} MPS Ranges`;$('mt').innerHTML=mRows(filtered)}

function rflt(){const fsWrap=document.getElementById('ms-fs');if(fsWrap)fsWrap.querySelectorAll('input').forEach(i=>i.checked=false);updFS();clearMS('ms-plat');clearMS('ms-rrp');flt()}

// ─── Multi-Select Helpers ────────────────────────────────────────────

function togMS(id){const wrap=document.getElementById(id);if(!wrap)return;const dd=wrap.querySelector('.ms-dd');dd.classList.toggle('open');if(dd.classList.contains('open')){const close=e=>{if(!wrap.contains(e.target)){dd.classList.remove('open');document.removeEventListener('click',close)}};setTimeout(()=>document.addEventListener('click',close),0)}}
function getMS(id){const wrap=document.getElementById(id);if(!wrap)return[];return[...wrap.querySelectorAll('input:checked')].map(i=>i.value)}
function updMS(id){const wrap=document.getElementById(id);if(!wrap)return;const sel=getMS(id);const btn=wrap.querySelector('.ms-btn');const label=id==='ms-plat'?'Platforms':'Providers';btn.textContent=sel.length?`${sel.length} ${label} selected`:`All ${label}`}
function clearMS(id){const wrap=document.getElementById(id);if(!wrap)return;wrap.querySelectorAll('input').forEach(i=>i.checked=false);updMS(id)}
function updFS(){const wrap=document.getElementById('ms-fs');if(!wrap)return;const sel=wrap.querySelector('input:checked');const btn=wrap.querySelector('.ms-btn');btn.textContent=sel?sel.value:'All'}