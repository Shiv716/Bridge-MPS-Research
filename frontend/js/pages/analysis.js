/* ─── Bridge – MPS Analysis Page (Provider List) ──────────────────── */

async function rAna(el){
const d=await F('/api/providers');if(!d){el.innerHTML='<p>Failed</p>';return}
el.innerHTML=`<div class="fi"><div class="ph1"><h1>MPS Analysis</h1><p>Structured analytical dashboards for each approved MPS provider</p></div>
<div class="grid g2">${d.providers.map(p=>`<div class="card" style="cursor:pointer" onclick="nav('provider',{id:'${p.id}'})">
<div class="card-b"><div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:14px">
<div><div style="font-size:18px;font-weight:700;font-family:'DM Sans',sans-serif;margin-bottom:2px">${p.name}</div>
<div style="font-size:13px;color:var(--text-s)">${p.full_name}</div></div>
<span class="badge b-blue">${p.investment_style}</span></div>
<div style="font-size:13px;color:var(--text-s);line-height:1.6;margin-bottom:16px">${p.description.slice(0,160)}...</div>
<div style="display:flex;gap:20px;font-size:12px">
<div><span style="color:var(--text-m)">Risk Levels </span><strong>${p.portfolio_count}</strong></div>
<div><span style="color:var(--text-m)">Risk </span><strong>${p.risk_range}</strong></div>
<div><span style="color:var(--text-m)">All in Fee </span><strong>${p.ocf_range}</strong></div>
</div></div></div>`).join('')}</div></div>`}
