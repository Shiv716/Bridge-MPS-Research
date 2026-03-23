/* ─── Bridge – Chart Helpers ───────────────────────────────────────── */

const hoverLine={id:'hoverLine',beforeDatasetsDraw(chart){const{ctx,chartArea:{left,right,top,bottom}}=chart;const active=chart.tooltip?.getActiveElements();if(active&&active.length){const x=active[0].element.x;ctx.save();ctx.beginPath();ctx.moveTo(x,top);ctx.lineTo(x,bottom);ctx.lineWidth=1;ctx.strokeStyle='rgba(107,114,128,.3)';ctx.setLineDash([4,3]);ctx.stroke();ctx.restore()}}};
const ttOpts={mode:'index',intersect:false,callbacks:{label:ctx=>`${ctx.dataset.label}: ${ctx.parsed.y!=null?ctx.parsed.y.toFixed(1)+'%':'–'}`}};

function renderHistoricalCharts(h){
if(h.asset_allocation){
const aa=h.asset_allocation;
const labels=aa.map(d=>d.Date);
CH.haa=new Chart($('haa'),{type:'line',data:{labels,datasets:[
{label:'Equity',data:aa.map(d=>d.Equity),backgroundColor:'rgba(59,130,246,.4)',borderColor:'rgba(59,130,246,.8)',fill:true,tension:.3,pointRadius:0},
{label:'Fixed Income',data:aa.map(d=>d['Fixed Income']),backgroundColor:'rgba(139,92,246,.4)',borderColor:'rgba(139,92,246,.8)',fill:true,tension:.3,pointRadius:0},
{label:'Alternative',data:aa.map(d=>d.Alternative),backgroundColor:'rgba(16,185,129,.4)',borderColor:'rgba(16,185,129,.8)',fill:true,tension:.3,pointRadius:0},
{label:'Cash',data:aa.map(d=>d.Cash),backgroundColor:'rgba(245,158,11,.4)',borderColor:'rgba(245,158,11,.8)',fill:true,tension:.3,pointRadius:0}
]},plugins:[hoverLine],options:{responsive:true,maintainAspectRatio:false,interaction:{mode:'index',intersect:false},plugins:{legend:{labels:{color:'#4b5563',font:{size:11}}},tooltip:ttOpts},scales:{x:{ticks:{color:'#6b7280',maxTicksLimit:12,font:{size:10}},grid:{display:false}},y:{stacked:true,min:0,max:100,ticks:{color:'#6b7280'},grid:{color:'#e5e7eb'}}}}})
}
if(h.equity_region){
const eq=h.equity_region;const labels=eq.map(d=>d.Date);
const keys=Object.keys(eq[0]).filter(k=>k!=='Date');
const colors=['rgba(59,130,246,.5)','rgba(16,185,129,.5)','rgba(245,158,11,.5)','rgba(239,68,68,.5)','rgba(139,92,246,.5)','rgba(6,182,212,.5)','rgba(168,85,247,.5)'];
CH.heq=new Chart($('heq'),{type:'line',data:{labels,datasets:keys.map((k,i)=>({label:k,data:eq.map(d=>d[k]||0),backgroundColor:colors[i%7],borderColor:colors[i%7].replace('.5','.8'),fill:true,tension:.3,pointRadius:0}))},plugins:[hoverLine],options:{responsive:true,maintainAspectRatio:false,interaction:{mode:'index',intersect:false},plugins:{legend:{labels:{color:'#4b5563',font:{size:10}}},tooltip:ttOpts},scales:{x:{ticks:{color:'#6b7280',maxTicksLimit:10,font:{size:9}},grid:{display:false}},y:{stacked:true,ticks:{color:'#6b7280'},grid:{color:'#e5e7eb'}}}}})
}
if(h.fixed_income){
const fi=h.fixed_income;const labels=fi.map(d=>d.Date);
const keys=Object.keys(fi[0]).filter(k=>k!=='Date');
const colors=['rgba(59,130,246,.5)','rgba(139,92,246,.5)','rgba(16,185,129,.5)','rgba(239,68,68,.5)','rgba(245,158,11,.5)','rgba(6,182,212,.5)','rgba(168,85,247,.5)'];
CH.hfi=new Chart($('hfi'),{type:'line',data:{labels,datasets:keys.map((k,i)=>({label:k,data:fi.map(d=>d[k]||0),backgroundColor:colors[i%7],borderColor:colors[i%7].replace('.5','.8'),fill:true,tension:.3,pointRadius:0}))},plugins:[hoverLine],options:{responsive:true,maintainAspectRatio:false,interaction:{mode:'index',intersect:false},plugins:{legend:{labels:{color:'#4b5563',font:{size:10}}},tooltip:ttOpts},scales:{x:{ticks:{color:'#6b7280',maxTicksLimit:10,font:{size:9}},grid:{display:false}},y:{stacked:true,ticks:{color:'#6b7280'},grid:{color:'#e5e7eb'}}}}})
}
}

function updateRvR(){
const ctx=$('rvr');if(!ctx)return;if(CH.rvr)CH.rvr.destroy();
const period=$('rrPeriod')?$('rrPeriod').value:(S._rrData.length?S._rrData[0].period:'3 Year');
const filtered=S._rrData.filter(d=>d.period===period);
const quilter=filtered.filter(d=>d.portfolio.startsWith('Quilter'));
const benchmarks=filtered.filter(d=>!d.portfolio.startsWith('Quilter'));
// Show date range
const drEl=$('rrDateRange');if(drEl){const now=new Date();const end='31/12/'+now.getFullYear();let start='';const match=period.match(/(\d+)/);if(match){const yrs=parseInt(match[1]);start='31/12/'+(now.getFullYear()-yrs)}else if(period.toLowerCase().includes('inception')){start='24/02/2014'}else{start='31/12/'+(now.getFullYear()-3)}drEl.textContent=`Period: ${start} – ${end}`}
CH.rvr=new Chart(ctx,{type:'scatter',data:{datasets:[
{label:'Quilter Portfolios',data:quilter.map(d=>({x:d.risk,y:d.return})),backgroundColor:'rgba(59,130,246,.8)',pointRadius:8,pointHoverRadius:10},
{label:'IA Sectors',data:benchmarks.map(d=>({x:d.risk,y:d.return})),backgroundColor:'rgba(245,158,11,.7)',pointRadius:7,pointHoverRadius:9,pointStyle:'triangle'}
]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{labels:{color:'#4b5563',font:{size:11}}},tooltip:{callbacks:{label:ctx2=>{const i=ctx2.dataIndex;const src=ctx2.datasetIndex===0?quilter:benchmarks;const d=src[i];if(!d)return'';const name=d.portfolio.replace('Quilter WealthSelect Active Managed ','Portfolio ');return`${name}: Risk ${d.risk.toFixed(1)}%, Return ${d.return.toFixed(1)}%`}}}},scales:{x:{title:{display:true,text:'Annualised Risk (%)',color:'#6b7280'},ticks:{color:'#6b7280'},grid:{color:'#e5e7eb'}},y:{title:{display:true,text:'Annualised Return (%)',color:'#6b7280'},ticks:{color:'#6b7280'},grid:{color:'#e5e7eb'}}}}})}
