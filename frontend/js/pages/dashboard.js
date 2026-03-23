/* ─── Bridge – Dashboard Page ──────────────────────────────────────── */

async function rDash(el){
el.innerHTML=`<div class="fi"><div class="ph1"><h1>Bridge</h1><p>Independent MPS research and oversight for UK financial adviser firms</p></div>
<div class="grid g2" style="margin-bottom:28px">
<div class="card hp-card" style="cursor:pointer;position:relative" onclick="nav('analysis')" onmouseenter="showTip(this)" onmouseleave="hideTip(this)">
<div class="card-b" style="text-align:center;padding:32px 22px">
<div style="width:48px;height:48px;border-radius:12px;background:var(--accent-g);display:flex;align-items:center;justify-content:center;margin:0 auto 16px">
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="2"><rect x="2" y="4" width="20" height="4" rx="1"/><rect x="2" y="10" width="20" height="4" rx="1"/><rect x="2" y="16" width="20" height="4" rx="1"/></svg></div>
<div style="font-size:16px;font-weight:600;margin-bottom:6px">MPS Analysis</div>
<div style="font-size:13px;color:var(--text-s);line-height:1.5">Explore detailed, independent analysis of individual MPS ranges.</div>
</div>
<div class="hp-tip" style="display:none;position:absolute;bottom:100%;left:50%;transform:translateX(-50%);background:var(--bg-card);border:1px solid var(--accent);border-radius:var(--rs);padding:10px 14px;font-size:12px;color:var(--text-s);white-space:nowrap;z-index:10;margin-bottom:8px">Explore our MPS Analysis tool, providing comprehensive, independent research on managed portfolio services.</div>
</div>
<div class="card" style="cursor:pointer" onclick="nav('selection')">
<div class="card-b" style="text-align:center;padding:32px 22px">
<div style="width:48px;height:48px;border-radius:12px;background:var(--green-bg);display:flex;align-items:center;justify-content:center;margin:0 auto 16px">
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2"><polygon points="22,3 2,3 10,12.46 10,19 14,21 14,12.46"/></svg></div>
<div style="font-size:16px;font-weight:600;margin-bottom:6px">MPS Selection</div>
<div style="font-size:13px;color:var(--text-s);line-height:1.5">Filter the MPS universe by risk profiling tool, platform availability and investment style.</div>
</div></div>
</div>
<div id="hp-subs"></div>
<div id="hp-ins"></div>
<div style="border:1px solid var(--border);border-radius:var(--r);overflow:hidden">
<div class="exp-row" onclick="togExp(this)" style="display:flex;align-items:center;justify-content:space-between;padding:14px 20px;cursor:pointer;border-bottom:1px solid var(--border)">
<span style="font-size:13.5px;font-weight:500">Submit feedback</span>
<span class="exp-arr" style="color:var(--text-m);font-size:12px;transition:transform .2s">▸</span></div>
<div class="exp-body" style="display:none;padding:20px;border-bottom:1px solid var(--border)">
<div style="display:flex;flex-direction:column;gap:12px">
<div class="fg"><span class="fl">Subject</span><input type="text" id="fb-subj" placeholder="e.g. Feature request, Bug report..." style="width:100%"></div>
<div class="fg"><span class="fl">Message</span><textarea id="fb-msg" rows="4" placeholder="Your feedback..." style="background:var(--bg-card);border:1px solid var(--border);border-radius:var(--rs);padding:10px 12px;font-size:13px;color:var(--text);font-family:inherit;outline:none;resize:vertical;width:100%;transition:border-color .15s" onfocus="this.style.borderColor='var(--accent)'" onblur="this.style.borderColor='var(--border)'"></textarea></div>
<div style="display:flex;gap:10px;align-items:center"><button class="btn btn-p" onclick="sendFb()">Send Feedback</button><span id="fb-status" style="font-size:12px;color:var(--text-m)"></span></div>
</div></div>
<div class="exp-row" onclick="togExp(this)" style="display:flex;align-items:center;justify-content:space-between;padding:14px 20px;cursor:pointer">
<span style="font-size:13.5px;font-weight:500">How to use the tool</span>
<span class="exp-arr" style="color:var(--text-m);font-size:12px;transition:transform .2s">▸</span></div>
<div class="exp-body" style="display:none;padding:16px 20px;font-size:13px;color:var(--text-s);line-height:1.6">
Use <strong>MPS Analysis</strong> to explore provider-level research across 8 structured tabs. Use <strong>MPS Selection</strong> to filter the universe by platform, fund selection approach, risk rating provider, and risk level. Use <strong>Insights</strong> to access weekly commentary and thematic analysis.</div>
</div></div>`;
const ins=await F('/api/insights');if(ins&&ins.insights.length){
const hpi=document.getElementById('hp-ins');if(hpi)hpi.innerHTML=`
<div class="card" style="margin-bottom:28px"><div class="card-h"><span class="card-t">Latest Insights</span><button class="btn btn-g btn-sm" onclick="nav('insights')">View All →</button></div>
<div class="card-b"><div class="grid g3">
${ins.insights.slice(0,3).map(i=>`<div class="insight-card" onclick="nav('insight',{id:'${i.id}'})">
<div class="im"><span class="badge ${catB(i.category)}">${i.category}</span><span>${i.date}</span><span>${i.read_time_minutes} min</span></div>
<div class="it">${i.title}</div><div class="is">${i.summary.slice(0,120)}...</div></div>`).join('')}
</div></div></div>`}
// Subscribed MPS ranges widget
try{const sr=await fetch('/api/subscriptions');if(sr.ok){const sd=await sr.json();
const hps=document.getElementById('hp-subs');if(hps&&sd.subscriptions.length){hps.innerHTML=`
<div class="card" style="margin-bottom:28px"><div class="card-h"><span class="card-t">📌 Your Subscribed MPS Ranges</span><button class="btn btn-g btn-sm" onclick="nav('account')">Manage →</button></div>
<div class="card-b"><div style="display:flex;gap:10px;flex-wrap:wrap">${sd.subscriptions.map(s=>`<div style="padding:10px 16px;background:var(--accent-g);border:1px solid rgba(37,99,235,.15);border-radius:var(--rs);cursor:pointer;transition:all .15s" onclick="nav('provider',{id:'${s.provider_id}'})" onmouseover="this.style.borderColor='var(--accent)'" onmouseout="this.style.borderColor='rgba(37,99,235,.15)'"><div style="font-size:13px;font-weight:600;color:var(--accent)">${s.provider_name}</div><div style="font-size:11px;color:var(--text-m);margin-top:2px">Subscribed · Click to view</div></div>`).join('')}</div></div></div>`}}}catch(e){}}

function showTip(el){const t=el.querySelector('.hp-tip');if(t)t.style.display='block'}
function hideTip(el){const t=el.querySelector('.hp-tip');if(t)t.style.display='none'}
function togExp(row){const body=row.nextElementSibling;const arr=row.querySelector('.exp-arr');
if(body.style.display==='none'){body.style.display='block';arr.textContent='▾'}
else{body.style.display='none';arr.textContent='▸'}
const st=document.getElementById('fb-status');if(st)st.textContent=''}
async function sendFb(){
const subj=$('fb-subj').value.trim(),msg=$('fb-msg').value.trim(),st=$('fb-status');
if(!subj||!msg){st.style.color='var(--red)';st.textContent='Please fill in both fields.';return}
st.style.color='var(--text-m)';st.textContent='Sending...';
try{const r=await fetch('/api/feedback',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({subject:subj,message:msg})});
if(r.ok){st.style.color='var(--green)';st.textContent='Feedback sent successfully.';$('fb-subj').value='';$('fb-msg').value=''}
else{const d=await r.json();st.style.color='var(--red)';st.textContent=d.detail||'Failed to send.'}}
catch(e){st.style.color='var(--red)';st.textContent='Failed to send. Please try again.'}}
