/* ─── Bridge – Account / Preferences Page ──────────────────────────── */

async function rAcct(el){
let subs=[];try{const r=await fetch('/api/subscriptions');if(r.ok){const d=await r.json();subs=d.subscriptions}}catch(e){}
let prefs={display:{default_risk_level:7,dark_mode:false},notifications:{frequency:'instant'},subscription_alerts:{}};
try{const r=await fetch('/api/preferences');if(r.ok){const d=await r.json();prefs=d.preferences}}catch(e){}
el.innerHTML=`<div class="fi"><div class="ph1"><h1>Preferences</h1><p>Manage your account settings, display options, notifications and MPS subscriptions</p></div>

<div class="card" style="margin-bottom:24px"><div class="card-h"><span class="card-t">Account Details</span></div>
<div class="card-b" style="padding:0"><table>
<tr><td class="nc" style="width:160px">Name</td><td>${S.user.name}</td></tr>
<tr><td class="nc">Email</td><td>${S.user.email}</td></tr>
<tr><td class="nc">Firm</td><td>${S.user.firm}</td></tr>
<tr><td class="nc">Role</td><td style="text-transform:capitalize">${S.user.role}</td></tr>
</table></div></div>

<div class="card" style="margin-bottom:24px"><div class="card-h"><span class="card-t">Display Preferences</span></div>
<div class="card-b">
<div style="display:flex;flex-direction:column;gap:16px">
<div style="display:flex;align-items:center;justify-content:space-between">
<div><div style="font-size:13.5px;font-weight:500">Default Risk Level</div><div style="font-size:12px;color:var(--text-m)">Pre-select this risk level when viewing provider dashboards</div></div>
<select id="prefRisk" onchange="savePref()" style="min-width:80px">${[3,4,5,6,7,8,9,10].map(r=>`<option value="${r}" ${prefs.display.default_risk_level===r?'selected':''}>${r}</option>`).join('')}</select>
</div>
<div style="display:flex;align-items:center;justify-content:space-between">
<div><div style="font-size:13.5px;font-weight:500">Dark Mode</div><div style="font-size:12px;color:var(--text-m)">Switch to a dark colour scheme</div></div>
<label class="toggle">
<input type="checkbox" id="prefDark" ${prefs.display.dark_mode?'checked':''} onchange="savePref()">
<span class="track"></span>
<span class="knob"></span>
</label>
</div>
</div></div></div>

<div class="card" style="margin-bottom:24px"><div class="card-h"><span class="card-t">Notification Settings</span></div>
<div class="card-b">
<div style="display:flex;align-items:center;justify-content:space-between">
<div><div style="font-size:13.5px;font-weight:500">Email Notification Frequency</div><div style="font-size:12px;color:var(--text-m)">How often you receive email alerts for subscribed MPS updates</div></div>
<select id="prefFreq" onchange="savePref()" style="min-width:120px">
<option value="instant" ${prefs.notifications.frequency==='instant'?'selected':''}>Instant</option>
<option value="daily" ${prefs.notifications.frequency==='daily'?'selected':''}>Daily Digest</option>
<option value="weekly" ${prefs.notifications.frequency==='weekly'?'selected':''}>Weekly Digest</option>
</select>
</div>
</div></div>

<div class="card"><div class="card-h"><span class="card-t">MPS Subscriptions</span><span style="font-size:12px;color:var(--text-m)">${subs.length} active</span></div>
${subs.length?`<div class="card-b" style="padding:0"><table><thead><tr><th>MPS Range</th><th>Subscribed</th><th>Email Alerts</th><th></th></tr></thead>
<tbody>${subs.map(s=>{const alertOn=prefs.subscription_alerts[s.provider_id]!==false;return`<tr><td class="nc" style="cursor:pointer" onclick="nav('provider',{id:'${s.provider_id}'})">${s.provider_name}</td>
<td>${new Date(s.created_at*1000).toLocaleDateString('en-GB')}</td>
<td><label class="toggle toggle-sm toggle-green">
<input type="checkbox" ${alertOn?'checked':''} onchange="togSubAlert('${s.provider_id}',this.checked)">
<span class="track"></span>
<span class="knob"></span>
</label></td>
<td><button class="btn btn-g btn-sm" onclick="unsubProv('${s.provider_id}')">Unsubscribe</button></td></tr>`}).join('')}</tbody></table></div>`
:`<div class="card-b"><p style="color:var(--text-m);font-size:13px">No active subscriptions. Subscribe to MPS ranges from the MPS Analysis dashboards to receive email alerts when data is updated.</p></div>`}
</div></div>`}

async function savePref(){
const body={display:{default_risk_level:parseInt($('prefRisk').value),dark_mode:$('prefDark').checked},notifications:{frequency:$('prefFreq').value}};
try{await fetch('/api/preferences',{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)})}catch(e){}
savePrefApplyDark(body.display.dark_mode)}

async function togSubAlert(providerId,enabled){
try{await fetch('/api/preferences/subscription-alert',{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify({provider_id:providerId,enabled})})}catch(e){}}
