/* ─── Bridge – Provider Detail Page (9-tab layout) ────────────────── */

async function rProv(el){
const id=S.pr?.id;if(!id){nav('analysis');return}
const d=await F(`/api/providers/${id}`);if(!d){el.innerHTML='<p>Not found</p>';return}
const p=d.provider,pts=d.portfolios;
S._provData=d;S._provTab='overview';
el.innerHTML=`<div class="fi"><div class="back" onclick="nav('analysis')">← Back to Providers</div>
<div class="ph"><div style="display:flex;justify-content:space-between;align-items:flex-start"><div><div class="pn">${p.full_name||p.name}</div>
<div style="color:var(--text-s);font-size:14px;margin-bottom:8px">${p.name} · ${p.investment_style}</div></div>
<button class="sub-btn unsubscribed" id="subBtn" onclick="togSub('${p.id}','${(p.full_name||p.name).replace(/'/g,"\\'")}')">🔔 Subscribe</button></div></div>
<div class="tabs" id="ptabs">
<div class="tab active" onclick="pTab('overview')">Overview</div>
<div class="tab" onclick="pTab('investment')">Investment Process</div>
<div class="tab" onclick="pTab('current')">Current Exposure</div>
<div class="tab" onclick="pTab('historical')">Historical Exposure</div>
<div class="tab" onclick="pTab('performance')">Performance</div>
<div class="tab" onclick="pTab('cost')">Cost</div>
<div class="tab" onclick="pTab('adviser')">Adviser Support</div>
<div class="tab" onclick="pTab('quarterly')">Quarterly Review</div>
<div class="tab" onclick="pTab('consumer_duty')">Consumer Duty</div>
</div>
<div id="tc"></div></div>`;
try{const sr=await fetch(`/api/subscriptions/check/${p.id}`);if(sr.ok){const sd=await sr.json();
const btn=$('subBtn');if(btn&&sd.subscribed){btn.className='sub-btn subscribed';btn.innerHTML='✓ Subscribed'}}}catch(e){}
trackEvent('page_view',{provider_name:p.full_name||p.name,provider_id:p.id,tab:'overview'});
pTab('overview')}

function pTab(tab){
S._provTab=tab;DC();removeBV();
document.querySelectorAll('#ptabs .tab').forEach(t=>t.classList.remove('active'));
const tabs=document.querySelectorAll('#ptabs .tab');
const tabMap=['overview','investment','current','historical','performance','cost','adviser','quarterly','consumer_duty'];
const idx=tabMap.indexOf(tab);if(idx>=0&&tabs[idx])tabs[idx].classList.add('active');
const tc=$('tc'),d=S._provData;if(!tc||!d)return;
const p2=d.provider;trackEvent('page_view',{provider_name:p2.full_name||p2.name,provider_id:p2.id,tab:tab});
const p=d.provider,pts=d.portfolios;
switch(tab){
case'overview':tabOverview(tc,p,pts);break;
case'investment':tabInvestment(tc,p);break;
case'current':tabCurrent(tc,pts);break;
case'historical':tabHistorical(tc);break;
case'performance':tabPerformance(tc,pts,p);break;
case'cost':tabCost(tc,pts);break;
case'adviser':tabAdviser(tc,p);break;
case'quarterly':tabQuarterly(tc,p);break;
case'consumer_duty':tabConsumerDuty(tc,p,pts);break;
}}

// ─── Overview Tab ────────────────────────────────────────────────────

function tabOverview(tc,p,pts){
const rrp=p.risk_rating_providers||[];
tc.innerHTML=`
<div class="grid g2" style="margin-bottom:20px">
<div class="stat-card"><div class="stat-l">Risk Levels</div><div class="stat-v">${pts.length}</div></div>
<div class="stat-card"><div class="stat-l">All in Fee</div><div class="stat-v">${Math.min(...pts.map(m=>m.ocf)).toFixed(2)}% – ${Math.max(...pts.map(m=>m.ocf)).toFixed(2)}%</div></div>
</div>
<div class="card" style="margin-bottom:20px"><div class="card-h"><span class="card-t">Provider Details</span></div>
<div class="card-b" style="padding:0"><table><thead><tr><th>Firm</th><th>Fund Selection</th><th>Management Fee</th>${p.established?'<th>Established</th>':''}${p.regulatory_status?'<th>Status</th>':''}</tr></thead>
<tbody><tr><td class="nc">${p.name}</td><td>${p.investment_style||'–'}</td><td>0.15%</td>${p.established?`<td>${p.established}</td>`:''}${p.regulatory_status?`<td>${p.regulatory_status}</td>`:''}</tr></tbody></table></div></div>
${p.description?`<div class="card" style="margin-bottom:20px"><div class="card-h"><span class="card-t">Description</span></div><div class="card-b"><div class="article"><p>${p.description}</p></div></div></div>`:''}
<div class="card" style="margin-bottom:20px"><div class="card-h"><span class="card-t">Model Range</span></div>
<div class="card-b" style="padding:0"><table><thead><tr><th>Model</th><th>Inception</th></tr></thead>
<tbody>${pts.map(m=>`<tr><td class="nc">${m.name}</td><td>${m.inception_date?new Date(m.inception_date).toLocaleDateString('en-GB'):'–'}</td></tr>`).join('')}</tbody></table></div></div>
<div class="grid g2">
<div class="card"><div class="card-h"><span class="card-t">Platform Availability</span></div>
<div class="card-b"><ul class="slist">${pts[0].platforms.map(pl=>`<li>${pl}</li>`).join('')}</ul></div></div>
${rrp.length?`<div class="card"><div class="card-h"><span class="card-t">Risk Rating Providers</span></div>
<div class="card-b"><ul class="slist">${rrp.map(r=>`<li>${r}</li>`).join('')}</ul></div></div>`:''}
</div>
${p.strengths&&p.strengths.length?`<div class="grid g2" style="margin-top:20px"><div class="card"><div class="card-h"><span class="card-t">Strengths</span></div><div class="card-b"><ul class="slist">${p.strengths.map(s=>`<li>${s}</li>`).join('')}</ul></div></div>
${p.considerations&&p.considerations.length?`<div class="card"><div class="card-h"><span class="card-t">Considerations</span></div><div class="card-b"><ul class="clist">${p.considerations.map(c=>`<li>${c}</li>`).join('')}</ul></div></div>`:''}</div>`:''}
<div class="card" style="margin-top:20px"><div class="card-h"><span class="card-t">💬 Have a Question?</span></div>
<div class="card-b"><p style="font-size:13.5px;color:var(--text-s);margin-bottom:14px">Ask the Bridge Research team about this MPS provider, we typically respond within 1 business day.</p>
<div class="msg-form" id="askForm">
<input type="text" id="askSubj" placeholder="Subject, e.g. 'Question about rebalancing approach'">
<textarea id="askMsg" placeholder="Your question..."></textarea>
<div style="display:flex;gap:10px;align-items:center"><button class="btn btn-p" onclick="sendAsk()">Send Question</button><span id="askStatus" style="font-size:12px;color:var(--text-m)"></span></div>
</div></div></div>`}

// ─── Investment Process Tab ──────────────────────────────────────────

function tabInvestment(tc,p){
const ip=p.investment_process||{};
const sections=[
{title:'Investment Team',key:'investment_team'},
{title:'Strategic Asset Allocation',key:'strategic_aa'},
{title:'Tactical Asset Allocation',key:'tactical_aa'},
{title:'Fund Selection',key:'fund_selection'},
{title:'Portfolio Construction',key:'portfolio_construction'},
{title:'Rebalancing & Trading',key:'rebalancing'}
];
tc.innerHTML=sections.map(s=>`<div class="card" style="margin-bottom:20px"><div class="card-h"><span class="card-t">${s.title}</span></div>
<div class="card-b"><div class="article">${fmtArticle(ip[s.key])}</div></div></div>`).join('');
renderBV(`<p><strong>Bridge View: Investment Process</strong></p><p>Quilter's investment process is comprehensive, built around a centralised Manager Research Hub with dedicated teams for quantitative analysis, operational due diligence, and responsible investment.</p><p>The use of WTW capital market assumptions for SAA adds rigour, while quarterly TAA reviews allow tactical flexibility within defined risk guardrails.</p><p>The sub-advised fund structure is a notable feature — it provides continuity and tax efficiency that many competitors lack.</p><p>Areas to monitor: the breadth of the investment team relative to the number of portfolios managed, and whether TAA decisions are consistently adding value over SAA alone.</p>`)}

// ─── Current Exposure Tab ────────────────────────────────────────────

function tabCurrent(tc,pts){
const defPort=pts[0];
tc.innerHTML=`
<div class="card" style="margin-bottom:20px"><div class="card-h"><span class="card-t">Current Holdings</span>
<div style="display:flex;gap:8px;align-items:center"><span style="font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.8px;color:var(--text-m)">Risk Level</span><div class="fg"><select id="hp" onchange="chPort()">${pts.map((m,i)=>`<option value="${i}">${shortName(m.name)}</option>`).join('')}</select></div></div></div>
<div class="card-b" style="padding:0"><div class="table-wrap"><table><thead><tr><th>Fund Name</th><th>ISIN</th><th>Portfolio Weighting (%)</th><th>Asset Class</th><th>Sub Asset Class</th></tr></thead>
<tbody id="ht">${holdRows(defPort,true)}</tbody></table></div>
<div id="holdToggle" style="padding:12px 14px;text-align:center;border-top:1px solid var(--border)"><a href="#" onclick="expandHold(event)" id="holdBtn" style="color:var(--accent);font-size:12px;font-weight:500;text-decoration:none">Show all ${defPort.underlying_funds?defPort.underlying_funds.length:0} holdings ▾</a></div></div></div>
<div class="card" style="margin-bottom:20px"><div class="card-h"><span class="card-t">Asset Allocation</span></div>
<div class="card-b" style="padding:0"><div class="table-wrap"><table><thead><tr><th>Asset Class</th>${pts.map(m=>`<th>${shortName(m.name)}</th>`).join('')}</tr></thead>
<tbody id="aat">${aaRows(pts)}</tbody></table></div></div></div>
<div class="grid g2">
<div class="card"><div class="card-h"><span class="card-t">Equity Exposure</span>
<div class="fg"><select id="eqMode" onchange="chEqMode()" style="min-width:110px"><option value="abs">Absolute</option><option value="prop">Proportion</option></select></div></div>
<div class="card-b" style="padding:0"><div class="table-wrap"><table><thead><tr><th>Region</th>${pts.map(m=>`<th>${shortName(m.name)}</th>`).join('')}</tr></thead>
<tbody id="eqt">${eqRows(pts,'abs')}</tbody></table></div></div></div>
<div class="card"><div class="card-h"><span class="card-t">Fixed Income Exposure</span>
<div class="fg"><select id="fiMode" onchange="chFiMode()" style="min-width:110px"><option value="abs">Absolute</option><option value="prop">Proportion</option></select></div></div>
<div class="card-b" style="padding:0"><div class="table-wrap"><table><thead><tr><th>Type</th>${pts.map(m=>`<th>${shortName(m.name)}</th>`).join('')}</tr></thead>
<tbody id="fit">${fiRows(pts,'abs')}</tbody></table></div></div></div>
</div>`;
S._holdExpanded=false;
renderBV(`<p><strong>Bridge View: Current Exposure</strong></p><p>The current holdings reveal Quilter's active approach to portfolio construction, with a blend of sub-advised mandates and third-party funds.</p><p>Equity exposure tilts towards global developed markets, with a meaningful UK allocation that provides domestic anchoring. The fixed income allocation favours investment-grade sterling credit with selective duration management.</p><p>Key observations: diversification across managers reduces single-manager risk, and the use of sub-advised structures provides operational efficiency advantages.</p>`)}

function holdRows(m,limit){
if(!m.underlying_funds||!m.underlying_funds.length)return'<tr><td colspan="5">No holdings data</td></tr>';
const funds=limit&&!S._holdExpanded?m.underlying_funds.slice(0,10):m.underlying_funds;
return funds.map(f=>{const subBadge=f.sub_type?`<span class="badge ${f.type==='Equity'?'b-blue':f.type==='Fixed Income'?'b-green':f.type==='Alternative'?'b-purple':'b-amber'}" style="opacity:.7">${f.sub_type}</span>`:'–';return`<tr><td class="nc">${f.name}</td><td>${f.isin||'–'}</td><td>${f.weight}</td>
<td><span class="badge ${f.type==='Equity'?'b-blue':f.type==='Fixed Income'?'b-green':f.type==='Alternative'?'b-purple':'b-amber'}">${f.type}</span></td>
<td>${subBadge}</td></tr>`}).join('')}

function expandHold(e){e.preventDefault();S._holdExpanded=!S._holdExpanded;const idx=$('hp').value;const m=S._provData.portfolios[idx];$('ht').innerHTML=holdRows(m,true);const btn=$('holdBtn');if(btn)btn.innerHTML=S._holdExpanded?'Show top 10 ▴':`Show all ${m.underlying_funds?m.underlying_funds.length:0} holdings ▾`}

function chPort(){
S._holdExpanded=false;const idx=$('hp').value;const m=S._provData.portfolios[idx];
$('ht').innerHTML=holdRows(m,true);const btn=$('holdBtn');if(btn)btn.innerHTML=`Show all ${m.underlying_funds?m.underlying_funds.length:0} holdings ▾`}

function eqRows(pts,mode){
const regions=new Set();
pts.forEach(m=>{if(m.geographic_allocation)Object.keys(m.geographic_allocation).forEach(k=>regions.add(k))});
return[...regions].map(r=>{
const vals=pts.map(m=>m.geographic_allocation&&m.geographic_allocation[r]!=null?m.geographic_allocation[r]:0);
if(mode==='prop'){const totals=pts.map(m=>{if(!m.geographic_allocation)return 1;return Object.values(m.geographic_allocation).reduce((s,v)=>s+(v||0),0)||1});
return`<tr><td class="nc">${r.replace(/_/g,' ').replace(/\b\w/g,l=>l.toUpperCase())}</td>${pts.map((m,i)=>`<td>${vals[i]>0?(vals[i]/totals[i]*100).toFixed(1)+'%':'–'}</td>`).join('')}</tr>`}
return`<tr><td class="nc">${r.replace(/_/g,' ').replace(/\b\w/g,l=>l.toUpperCase())}</td>${vals.map(v=>`<td>${v>0?v.toFixed(2):'–'}</td>`).join('')}</tr>`}).join('')}

function fiRows(pts,mode){
const types=new Set();
pts.forEach(m=>{if(m.fixed_income_breakdown)Object.keys(m.fixed_income_breakdown).forEach(k=>types.add(k))});
return[...types].map(t=>{
const vals=pts.map(m=>m.fixed_income_breakdown&&m.fixed_income_breakdown[t]!=null?m.fixed_income_breakdown[t]:0);
if(mode==='prop'){const totals=pts.map(m=>{if(!m.fixed_income_breakdown)return 1;return Object.values(m.fixed_income_breakdown).reduce((s,v)=>s+(v||0),0)||1});
return`<tr><td class="nc">${t.replace(/_/g,' ').replace(/\b\w/g,l=>l.toUpperCase())}</td>${pts.map((m,i)=>`<td>${vals[i]>0?(vals[i]/totals[i]*100).toFixed(1)+'%':'–'}</td>`).join('')}</tr>`}
return`<tr><td class="nc">${t.replace(/_/g,' ').replace(/\b\w/g,l=>l.toUpperCase())}</td>${vals.map(v=>`<td>${v>0?v.toFixed(2):'–'}</td>`).join('')}</tr>`}).join('')}

function chEqMode(){$('eqt').innerHTML=eqRows(S._provData.portfolios,$('eqMode').value)}
function chFiMode(){$('fit').innerHTML=fiRows(S._provData.portfolios,$('fiMode').value)}

function aaRows(pts){
const classes=['Equity','Fixed Income','Alternative','Cash'];
const colors={'Equity':'b-blue','Fixed Income':'b-green','Alternative':'b-purple','Cash':'b-amber'};
return classes.map(ac=>{
const vals=pts.map(m=>{
if(!m.underlying_funds)return 0;
return m.underlying_funds.filter(f=>f.type===ac).reduce((s,f)=>s+(f.weight||0),0)});
const total=vals.reduce((s,v)=>s+v,0);
if(total===0)return'';
return`<tr><td class="nc"><span class="badge ${colors[ac]||'b-blue'}">${ac}</span></td>${vals.map(v=>`<td>${v>0?v.toFixed(1)+'%':'–'}</td>`).join('')}</tr>`}).join('')}

// ─── Historical Exposure Tab ─────────────────────────────────────────

//async function tabHistorical(tc){
//const h=await F('/api/historical/portfolio_7');
//tc.innerHTML=`
//<div style="margin-bottom:16px;padding:12px 16px;background:var(--accent-g);border-radius:var(--rs);font-size:13px;color:var(--accent);font-weight:500">📊 Showing historical data for <strong>Risk Level 7</strong> (Balanced)</div>
//<div class="card" style="margin-bottom:20px"><div class="card-h"><span class="card-t">Asset Allocation – Risk Level 7</span></div>
//<div class="card-b"><div class="cc" style="height:320px"><canvas id="haa"></canvas></div></div></div>
//<div class="grid g2">
//<div class="card"><div class="card-h"><span class="card-t">Equity Exposure – Risk Level 7</span></div>
//<div class="card-b"><div class="cc" style="height:280px"><canvas id="heq"></canvas></div></div></div>
//<div class="card"><div class="card-h"><span class="card-t">Fixed Income Exposure – Risk Level 7</span></div>
//<div class="card-b"><div class="cc" style="height:280px"><canvas id="hfi"></canvas></div></div></div>
//</div>`;
//renderBV(`<p><strong>Bridge View: Historical Exposure</strong></p><p>Historical asset allocation data shows how the portfolio has evolved over time. Gradual shifts in equity/bond weighting reflect both strategic reviews and tactical positioning.</p><p>The equity regional breakdown shows any geographic rotation decisions, while the fixed income history highlights duration and credit quality positioning through different rate environments.</p><p>Look for consistency between the stated investment approach and the actual changes observed — significant deviations may warrant further investigation.</p>`);
//if(!h)return;
//setTimeout(()=>{renderHistoricalCharts(h)},100)}

async function tabHistorical(tc){
const pts=S._provData.portfolios;
const riskLevels=pts.map(m=>m.risk_rating).sort((a,b)=>a-b);
const defaultRL=riskLevels.includes(7)?7:riskLevels[0];
S._histRL=defaultRL;
const h=await F(`/api/historical/portfolio_${defaultRL}`);
tc.innerHTML=`
<div style="margin-bottom:16px;display:flex;align-items:center;gap:12px">
<div style="padding:12px 16px;background:var(--accent-g);border-radius:var(--rs);font-size:13px;color:var(--accent);font-weight:500;flex:1">📊 Showing historical data for <strong>Risk Level <span id="histRLLabel">${defaultRL}</span></strong></div>
<div class="fg"><span class="fl">Risk Level</span><select id="histRL" onchange="changeHistRL()" style="min-width:100px">${riskLevels.map(r=>`<option value="${r}" ${r===defaultRL?'selected':''}>${r}</option>`).join('')}</select></div>
</div>
<div class="card" style="margin-bottom:20px"><div class="card-h"><span class="card-t">Asset Allocation – Risk Level <span class="histRLTitle">${defaultRL}</span></span></div>
<div class="card-b"><div class="cc" style="height:320px"><canvas id="haa"></canvas></div></div></div>
<div class="grid g2">
<div class="card"><div class="card-h"><span class="card-t">Equity Exposure – Risk Level <span class="histRLTitle">${defaultRL}</span></span></div>
<div class="card-b"><div class="cc" style="height:280px"><canvas id="heq"></canvas></div></div></div>
<div class="card"><div class="card-h"><span class="card-t">Fixed Income Exposure – Risk Level <span class="histRLTitle">${defaultRL}</span></span></div>
<div class="card-b"><div class="cc" style="height:280px"><canvas id="hfi"></canvas></div></div></div>
</div>`;
renderBV(`<p><strong>Bridge View: Historical Exposure</strong></p><p>Historical asset allocation data shows how the portfolio has evolved over time. Gradual shifts in equity/bond weighting reflect both strategic reviews and tactical positioning.</p><p>The equity regional breakdown shows any geographic rotation decisions, while the fixed income history highlights duration and credit quality positioning through different rate environments.</p><p>Look for consistency between the stated investment approach and the actual changes observed — significant deviations may warrant further investigation.</p>`);
if(!h)return;
setTimeout(()=>{renderHistoricalCharts(h)},100)}

async function changeHistRL(){
const rl=$('histRL').value;
S._histRL=rl;
$('histRLLabel').textContent=rl;
document.querySelectorAll('.histRLTitle').forEach(el=>el.textContent=rl);
DC();
const h=await F(`/api/historical/portfolio_${rl}`);
if(!h)return;
setTimeout(()=>{renderHistoricalCharts(h)},100)}

// ─── Performance Tab ─────────────────────────────────────────────────

function tabPerformance(tc,pts,p){
const years=['YTD','2025','2024','2023','2022','2021','2020','2019','2018','2017','2016'];
const rrData=p.risk_return_data||[];
const periods=[...new Set(rrData.map(d=>d.period))];
tc.innerHTML=`
<div class="card" style="margin-bottom:20px"><div class="card-h"><span class="card-t">Calendar Year Returns (%)</span></div>
<div class="card-b" style="padding:0"><div class="table-wrap"><table><thead><tr><th>Model</th>${years.map(y=>`<th>${y}</th>`).join('')}</tr></thead>
<tbody>${pts.map(m=>{const cr=m.calendar_returns||{};return`<tr><td class="nc">${m.name}</td>${years.map(y=>{const val=cr[y];return`<td style="color:${val!=null&&val<0?'var(--red)':'var(--text-s)'}">${val!=null?val+'%':'–'}</td>`}).join('')}</tr>`}).join('')}</tbody></table></div></div></div>
<div class="card" style="margin-bottom:20px"><div class="card-h"><span class="card-t">Trailing Returns (%)</span></div>
<div class="card-b" style="padding:0"><div class="table-wrap"><table><thead><tr><th>Model</th><th>1M</th><th>3M</th><th>6M</th><th>YTD</th><th>1Y</th><th>3Y</th><th>5Y</th><th>10Y</th></tr></thead>
<tbody>${pts.map(m=>{const tr=m.trailing_returns||{};return`<tr><td class="nc">${m.name}</td><td>${v(tr['1M'])}</td><td>${v(tr['3M'])}</td><td>${v(tr['6M'])}</td><td>${v(tr['YTD'])}</td><td>${v(tr['1Y'])}</td><td>${v(tr['3Y'])}</td><td>${v(tr['5Y'])}</td><td>${v(tr['10Y'])}</td></tr>`}).join('')}</tbody></table></div></div></div>
<div class="card"><div class="card-h"><span class="card-t">Risk vs Return</span>
${periods.length?`<div class="fg"><select id="rrPeriod" onchange="updateRvR()" style="min-width:140px">${periods.map((p,i)=>`<option value="${p}" ${i===0?'selected':''}>${p}</option>`).join('')}</select></div>`:''}</div>
<div class="card-b"><div id="rrDateRange" style="font-size:12px;color:var(--text-m);margin-bottom:8px;font-weight:500"></div><div class="cc" style="height:340px"><canvas id="rvr"></canvas></div></div></div>`;
S._rrData=rrData;
renderBV(`<p><strong>Bridge View: Performance</strong></p><p>Calendar year returns show the portfolio's behaviour through different market environments. Pay attention to 2022 (a challenging year for multi-asset) and subsequent recovery.</p><p>The risk/return scatter chart plots annualised risk against annualised return, with IA sector benchmarks for context. Portfolios above and to the left of the benchmark line are delivering superior risk-adjusted returns.</p><p>Quilter's active portfolios have generally clustered above the IA sector line, suggesting the active management approach has added value on a risk-adjusted basis over these periods.</p>`);
setTimeout(()=>{updateRvR()},100)}

// ─── Cost Tab ────────────────────────────────────────────────────────

function tabCost(tc,pts){
tc.innerHTML=`
<div class="card"><div class="card-h"><span class="card-t">Cost Breakdown</span></div>
<div class="card-b" style="padding:0"><div class="table-wrap"><table><thead><tr><th>Model</th><th>DFM</th><th>Underlying</th><th>All In</th></tr></thead>
<tbody>${pts.map(m=>{const c=m.cost_breakdown||{};return`<tr><td class="nc">${m.name}</td><td>${c.dfm!=null?c.dfm.toFixed(2):'–'}</td><td>${c.underlying!=null?c.underlying.toFixed(2):'–'}</td><td><strong>${c.all_in!=null?c.all_in.toFixed(2):'–'}</strong></td></tr>`}).join('')}</tbody></table></div></div></div>`;
renderBV(`<p><strong>Bridge View: Costs</strong></p><p>The management fee of 0.15% is competitive within the active MPS space. The all-in fee range of 0.60% to 0.83% reflects the varying underlying fund costs across different risk levels.</p><p>Higher risk portfolios (8-10) carry slightly higher underlying fund costs due to greater use of actively managed equity funds, while lower risk portfolios benefit from more cost-efficient fixed income allocations.</p><p>When comparing costs, consider the total cost to the client inclusive of platform charges and adviser fees, not the MPS cost in isolation.</p>`)}

// ─── Consumer Duty Tab ───────────────────────────────────────────────

function tabConsumerDuty(tc,p,pts){
const provName=p.full_name||p.name;
const today=new Date().toLocaleDateString('en-GB',{day:'numeric',month:'long',year:'numeric'});
tc.innerHTML=`
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px">
<div><div style="font-size:16px;font-weight:600">Consumer Duty Oversight Report</div>
<div style="font-size:13px;color:var(--text-m)">Editable template — click any section to customise before exporting</div></div>
<button class="btn btn-p" onclick="exportCD()">Export Report</button>
</div>
<div class="card" style="margin-bottom:16px"><div class="card-h"><span class="card-t">📋 Report Details</span></div>
<div class="card-b" style="padding:0"><table>
<tr><td class="nc" style="width:180px">Provider</td><td>${provName}</td></tr>
<tr><td class="nc">Date</td><td>${today}</td></tr>
<tr><td class="nc">Risk Levels Covered</td><td>${pts.map(m=>m.risk_rating).join(', ')}</td></tr>
<tr><td class="nc">All-in Fee Range</td><td>${Math.min(...pts.map(m=>m.ocf)).toFixed(2)}% – ${Math.max(...pts.map(m=>m.ocf)).toFixed(2)}%</td></tr>
</table></div></div>
<div class="card" style="margin-bottom:16px"><div class="card-h"><span class="card-t">1. Selection Rationale</span></div>
<div class="cd-editable" contenteditable="true" data-placeholder="Document why this MPS was selected for your firm's approved list...">${provName} was selected following an independent assessment of the investment process, cost structure, platform availability, and alignment with our client segments. The proposition offers a comprehensive active managed solution across risk levels ${pts[0].risk_rating} to ${pts[pts.length-1].risk_rating}, available on ${pts[0].platforms.length} platforms.</div></div>
<div class="card" style="margin-bottom:16px"><div class="card-h"><span class="card-t">2. Target Market & Suitability</span></div>
<div class="cd-editable" contenteditable="true" data-placeholder="Define which client segments this MPS is suitable for...">This MPS range is suitable for clients seeking a professionally managed, diversified multi-asset portfolio with active fund selection. The range spans risk levels ${pts[0].risk_rating} to ${pts[pts.length-1].risk_rating}, making it appropriate for clients across cautious to adventurous risk profiles with a medium to long-term investment horizon.</div></div>
<div class="card" style="margin-bottom:16px"><div class="card-h"><span class="card-t">3. Fair Value Assessment</span></div>
<div class="cd-editable" contenteditable="true" data-placeholder="Assess whether the costs represent fair value for clients...">The all-in fee range of ${Math.min(...pts.map(m=>m.ocf)).toFixed(2)}% to ${Math.max(...pts.map(m=>m.ocf)).toFixed(2)}% is assessed as representing fair value given the depth of the investment process, breadth of manager research, and the active management approach. The management fee of 0.15% is competitive within the active MPS universe.</div></div>
<div class="card" style="margin-bottom:16px"><div class="card-h"><span class="card-t">4. Ongoing Monitoring Summary</span></div>
<div class="cd-editable" contenteditable="true" data-placeholder="Summarise monitoring activity and findings...">Portfolios have been monitored on a quarterly basis. Performance has been reviewed against relevant IA sector benchmarks and peer groups. Asset allocation changes and fund selection decisions have been assessed for consistency with the stated investment approach.</div></div>
<div class="card" style="margin-bottom:16px"><div class="card-h"><span class="card-t">5. Actions & Conclusions</span></div>
<div class="cd-editable" contenteditable="true" data-placeholder="Record any actions taken or conclusions reached...">Based on the current review, ${provName} remains appropriate for the target client segments identified above. No changes to the approved list are recommended at this time. Next review scheduled in accordance with our quarterly monitoring cadence.</div></div>
`}

async function exportCD(){
const btn=event.target;btn.textContent='Generating...';btn.disabled=true;
try{
const rows=document.querySelectorAll('.card-b table tr');
const details={};
rows.forEach(r=>{const cells=r.querySelectorAll('td');if(cells.length===2)details[cells[0].innerText.trim()]=cells[1].innerText.trim()});
const sections=[];
document.querySelectorAll('.cd-editable').forEach(el=>{
const card=el.closest('.card');
const title=card?card.querySelector('.card-t')?.innerText.trim():'';
sections.push({title,content:el.innerText.trim()})});
const d=S._provData;if(d){const p=d.provider,pts=d.portfolios;
const ip=p.investment_process||{};const as=p.adviser_support||{};
sections.push({title:'Overview',content:`Provider: ${p.full_name||p.name}\nInvestment Style: ${p.investment_style||''}\nRisk Levels: ${pts.map(m=>m.risk_rating).join(', ')}\nPlatforms: ${pts[0]?.platforms?.join(', ')||''}\nRisk Rating Providers: ${(p.risk_rating_providers||[]).join(', ')}\nInception: ${pts[0]?.inception_date||''}`});
sections.push({title:'Investment Process',content:[ip.investment_team,ip.strategic_aa,ip.tactical_aa,ip.fund_selection,ip.portfolio_construction,ip.rebalancing].filter(Boolean).join('\n\n')});
sections.push({title:'Performance Summary',content:pts.map(m=>`${m.name}: 1Y ${m.return_1yr||'-'}% | 3Y ${m.return_3yr||'-'}% | 5Y ${m.return_5yr||'-'}%`).join('\n')});
sections.push({title:'Cost Breakdown',content:pts.map(m=>`${m.name}: DFM ${m.cost_breakdown?.dfm}% + Underlying ${m.cost_breakdown?.underlying}% = All-in ${m.ocf}%`).join('\n')});
sections.push({title:'Adviser Support',content:[as.onboarding,as.ongoing_communication,as.review_meetings,as.investment_commentary,as.digital_tools].filter(Boolean).join('\n\n')});}
const res=await fetch('/api/export/consumer-duty',{method:'POST',headers:{'Content-Type':'application/json'},
body:JSON.stringify({details,sections})});
if(!res.ok)throw new Error('Export failed');
const blob=await res.blob();
const a=document.createElement('a');a.href=URL.createObjectURL(blob);
a.download='Consumer_Duty_Oversight_Report.docx';a.click();
}catch(e){alert('Export failed: '+e.message)}
finally{btn.textContent='Export Report';btn.disabled=false}}

// ─── Adviser Support Tab ─────────────────────────────────────────────

function tabAdviser(tc,p){
const as=p.adviser_support||{};
const websiteUrl=p.website||'';
const sections=[
{title:'Onboarding & Training',key:'onboarding'},
{title:'Ongoing Portfolio Communication',key:'ongoing_communication'},
{title:'Review Meetings & Ongoing Engagement',key:'review_meetings'},
{title:'Investment Commentary & Market Insight',key:'investment_commentary'},
{title:'Digital Tools & Support Infrastructure',key:'digital_tools'}
];
tc.innerHTML=`${websiteUrl?`<div class="card" style="margin-bottom:20px"><div class="card-h"><span class="card-t">Provider Website</span></div>
<div class="card-b"><a href="${websiteUrl}" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;gap:8px;color:var(--accent);font-size:14px;font-weight:500;text-decoration:none">🔗 ${p.full_name||p.name} <span style="font-size:12px;color:var(--text-m)">↗ Opens in new tab</span></a></div></div>`:''}`+sections.map(s=>`<div class="card" style="margin-bottom:20px"><div class="card-h"><span class="card-t">${s.title}</span></div>
<div class="card-b"><div class="article">${fmtArticle(as[s.key])}</div></div></div>`).join('');
renderBV(`<p><strong>Bridge View: Adviser Support</strong></p><p>Quilter provides a comprehensive support offering spanning onboarding, ongoing communication, and digital infrastructure. The breadth of support is above average for the MPS market.</p><p>Quarterly rebalance documentation and post-trade rationale are particularly valuable for Consumer Duty evidence requirements. The availability of both virtual and in-person training adds flexibility.</p><p>Consider: how responsive is the Quilter team to ad-hoc queries? Adviser firms should test the support model during the evaluation phase rather than relying solely on the documented offering.</p>`)}

// ─── Quarterly Review Tab ────────────────────────────────────────────

function tabQuarterly(tc,p){
const qr=p.quarterly_review||{};
tc.innerHTML=`
<div class="card" style="margin-bottom:20px"><div class="card-h"><span class="card-t">Asset Allocation Changes</span></div>
<div class="card-b"><div class="article">${fmtArticle(qr.aa_changes)}</div></div></div>
<div class="card" style="margin-bottom:20px"><div class="card-h"><span class="card-t">Fund Selection Changes</span></div>
<div class="card-b"><div class="article">${fmtArticle(qr.fund_changes)}</div></div></div>
<div class="card"><div class="card-h"><span class="card-t">Performance Review</span></div>
<div class="card-b"><div class="article">${fmtArticle(qr.performance_review)}</div></div></div>`}

// ─── Ask Question (from Overview tab) ────────────────────────────────

async function sendAsk(){
const subj=$('askSubj').value.trim(),body=$('askMsg').value.trim(),st=$('askStatus');
if(!subj||!body){st.style.color='var(--red)';st.textContent='Please fill in both fields';return}
const p=S._provData?.provider;
st.style.color='var(--text-m)';st.textContent='Sending...';
try{const r=await fetch('/api/messages',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({subject:subj,message:body,provider_id:p?.id,provider_name:p?.full_name||p?.name})});
if(r.ok){st.style.color='var(--green)';st.textContent='Question sent — we\'ll reply within 1 business day';$('askSubj').value='';$('askMsg').value=''}
else{const d=await r.json();st.style.color='var(--red)';st.textContent=d.detail||'Failed'}}
catch(e){st.style.color='var(--red)';st.textContent='Failed to send'}}

// ─── Subscription Toggle ─────────────────────────────────────────────

async function togSub(providerId,providerName){
const btn=$('subBtn');if(!btn)return;
const isSub=btn.classList.contains('subscribed');
try{if(isSub){const r=await fetch(`/api/subscriptions/${providerId}`,{method:'DELETE'});
if(r.ok){btn.className='sub-btn unsubscribed';btn.innerHTML='🔔 Subscribe'}}
else{const r=await fetch('/api/subscriptions',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({provider_id:providerId,provider_name:providerName})});
if(r.ok){btn.className='sub-btn subscribed';btn.innerHTML='✓ Subscribed'}}}catch(e){}}

async function unsubProv(providerId){
try{const r=await fetch(`/api/subscriptions/${providerId}`,{method:'DELETE'});
if(r.ok)nav('account')}catch(e){}}
