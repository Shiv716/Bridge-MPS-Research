/* ─── Bridge – Insights Pages ──────────────────────────────────────── */

async function rIns(el){
const d=await F('/api/insights');if(!d){el.innerHTML='<p>Failed</p>';return}
const pinned=d.insights.filter(i=>i.pinned);
const regular=d.insights.filter(i=>!i.pinned);
el.innerHTML=`<div class="fi"><div class="ph1"><h1>Insights</h1><p>Expert insights from Buckingham Research — market theme analysis and ad-hoc thought pieces</p></div>
${pinned.length?`<div class="card" style="margin-bottom:24px;border-color:rgba(37,99,235,.25)"><div class="card-h" style="background:var(--accent-g)"><span class="card-t" style="display:flex;align-items:center;gap:8px"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="2"><path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/></svg> Latest Weekly Market Update</span><span style="font-size:12px;color:var(--text-m)">Updated ${pinned[0].date}</span></div>
<div class="card-b" style="cursor:pointer" onclick="nav('insight',{id:'${pinned[0].id}'})">
<div class="it" style="margin-bottom:6px">${pinned[0].title}</div>
<div class="is">${pinned[0].summary}</div>
<div style="margin-top:10px;font-size:12px;color:var(--accent);font-weight:500">Read full update →</div>
</div></div>`:''}
<div class="filter-bar" style="margin-bottom:24px">
<div class="fg"><span class="fl">Category</span><select id="ic" onchange="fIns()"><option value="">All</option>${d.categories.map(c=>`<option>${c}</option>`).join('')}</select></div>
</div>
<div class="grid g2" id="il">${insCards(regular)}</div></div>`}

function insCards(ins){return ins.map(i=>`<div class="insight-card" onclick="nav('insight',{id:'${i.id}'})">
<div class="im"><span class="badge ${catB(i.category)}">${i.category}</span><span>${i.date}</span><span>${i.read_time_minutes} min read</span></div>
<div class="it">${i.title}</div><div class="is">${i.summary}</div></div>`).join('')}

async function fIns(){const c=$('ic').value;let u='/api/insights';if(c)u+=`?category=${encodeURIComponent(c)}`;delete S.c[u];const d=await F(u);if(d){const regular=d.insights.filter(i=>!i.pinned);$('il').innerHTML=insCards(regular)}}

// ─── Insight Detail ──────────────────────────────────────────────────

async function rInsD(el){
const id=S.pr?.id;if(!id){nav('insights');return}
const d=await F(`/api/insights/${id}`);if(!d){el.innerHTML='<p>Not found</p>';return}
const i=d.insight;
el.innerHTML=`<div class="fi"><div class="back" onclick="nav('insights')">← Back to Insights</div>
<div style="margin-bottom:24px"><div class="im"><span class="badge ${catB(i.category)}">${i.category}</span><span>${i.date}</span><span>${i.read_time_minutes} min read</span><span>By ${i.author}</span></div>
<h1 style="font-family:'DM Sans',sans-serif;font-size:26px;font-weight:700;letter-spacing:-.5px;line-height:1.3;margin-bottom:8px">${i.title}</h1>
<p style="font-size:15px;color:var(--text-s);line-height:1.5">${i.summary}</p></div>
<div class="article">${i.content.split('\n\n').map(p=>{
if(p.startsWith('**')&&p.endsWith('**'))return`<h3>${p.replace(/\*\*/g,'')}</h3>`;
return`<p>${p.replace(/\*\*(.*?)\*\*/g,'<strong>$1</strong>')}</p>`}).join('')}</div>
<div style="margin-top:24px;display:flex;gap:8px;flex-wrap:wrap">${i.tags.map(t=>`<span class="badge b-blue">${t}</span>`).join('')}</div></div>`}
