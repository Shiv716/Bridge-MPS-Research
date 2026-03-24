/* ─── Bridge – Admin Page ──────────────────────────────────────────── */

async function rAdmin(el){
if(!S.user||S.user.role!=='admin'){el.innerHTML='<div class="fi"><p style="color:var(--red)">Admin access required.</p></div>';return}
el.innerHTML=`<div class="fi"><div class="ph1"><h1>Admin</h1><p>Manage users, send invitations, and view platform activity</p></div>
<div class="tabs" id="adminTabs">
<div class="tab active" onclick="adminTab('users')">Users</div>
<div class="tab" onclick="adminTab('activity')">Activity</div>
<div class="tab" onclick="adminTab('stats')">Stats</div>
<div class="tab" onclick="adminTab('messages')">Messages</div>
</div>
<div id="adminContent"></div></div>`;
adminTab('users')}

function adminTab(tab){
document.querySelectorAll('#adminTabs .tab').forEach(t=>t.classList.remove('active'));
const tabs=document.querySelectorAll('#adminTabs .tab');
const map=['users','activity','stats','messages'];
const idx=map.indexOf(tab);if(idx>=0&&tabs[idx])tabs[idx].classList.add('active');
const el=$('adminContent');if(!el)return;
switch(tab){
case'users':adminUsers(el);break;
case'activity':adminActivity(el);break;
case'stats':adminStats(el);break;
case'messages':adminMessages(el);break;
}}

// ─── Users Tab ───────────────────────────────────────────────────────

async function adminUsers(el){
el.innerHTML='<div class="loading"><div class="spinner"></div>Loading...</div>';
let users=[];
try{const r=await fetch('/api/admin/users');if(r.ok){const d=await r.json();users=d.users}}catch(e){}
el.innerHTML=`<div class="card" style="margin-bottom:24px"><div class="card-h"><span class="card-t">Invite New User</span></div>
<div class="card-b">
<div style="display:flex;flex-direction:column;gap:12px;max-width:480px">
<div class="fg"><span class="fl">Email</span><input type="text" id="invEmail" placeholder="adviser@firm.co.uk" style="width:100%"></div>
<div class="fg"><span class="fl">Full Name</span><input type="text" id="invName" placeholder="Jane Smith" style="width:100%"></div>
<div class="fg"><span class="fl">Firm</span><input type="text" id="invFirm" placeholder="Smith & Partners" style="width:100%"></div>
<div class="fg"><span class="fl">Role</span><select id="invRole" style="min-width:160px"><option value="adviser">Adviser</option><option value="admin">Admin</option></select></div>
<div style="display:flex;gap:10px;align-items:center"><button class="btn btn-p" onclick="doInvite()">Send Invite</button><span id="invStatus" style="font-size:12px;color:var(--text-m)"></span></div>
</div>
</div></div>

<div class="card"><div class="card-h"><span class="card-t">Users</span><span style="font-size:12px;color:var(--text-m)">${users.length} total</span></div>
${users.length?`<div class="card-b" style="padding:0"><div class="table-wrap"><table><thead><tr><th>Name</th><th>Email</th><th>Firm</th><th>Role</th><th>Verified</th><th>Created</th><th></th></tr></thead>
<tbody>${users.map(u=>`<tr>
<td class="nc">${u.name||'–'}</td>
<td>${u.email}</td>
<td>${u.firm||'–'}</td>
<td><span class="badge ${u.role==='admin'?'b-purple':'b-blue'}">${u.role}</span></td>
<td>${u.email_verified?'<span class="badge b-green">Yes</span>':'<span class="badge b-amber">Pending</span>'}</td>
<td>${u.created_at?new Date(u.created_at).toLocaleDateString('en-GB'):'–'}</td>
<td>${u.id!==S.user.id?`<button class="btn btn-g btn-sm" onclick="doDeleteUser('${u.id}','${u.email}')">Remove</button>`:''}</td>
</tr>`).join('')}</tbody></table></div></div>`
:`<div class="card-b"><p style="color:var(--text-m);font-size:13px">No users yet.</p></div>`}
</div>`}

async function doInvite(){
const email=$('invEmail').value.trim(),name=$('invName').value.trim(),firm=$('invFirm').value.trim(),role=$('invRole').value,st=$('invStatus');
st.textContent='';st.style.color='var(--text-m)';
if(!email||!name||!firm){st.style.color='var(--red)';st.textContent='Email, name and firm are required';return}
st.textContent='Sending invite...';
try{const r=await fetch('/api/admin/invite',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email,name,firm,role})});
if(r.ok){const d=await r.json();st.style.color='var(--green)';st.textContent='Invite sent to '+email;
$('invEmail').value='';$('invName').value='';$('invFirm').value='';
setTimeout(()=>adminTab('users'),1500)}
else{const d=await r.json();st.style.color='var(--red)';st.textContent=d.detail||'Failed to send invite'}}
catch(e){st.style.color='var(--red)';st.textContent='Connection error'}}

async function doDeleteUser(userId,email){
if(!confirm(`Remove ${email}? This cannot be undone.`))return;
try{const r=await fetch(`/api/admin/users/${userId}`,{method:'DELETE'});
if(r.ok)adminTab('users');
else{const d=await r.json();alert(d.detail||'Failed')}}catch(e){alert('Connection error')}}

// ─── Activity Tab ────────────────────────────────────────────────────

async function adminActivity(el){
el.innerHTML='<div class="loading"><div class="spinner"></div>Loading...</div>';
let activity=[];
try{const r=await fetch('/api/admin/activity');if(r.ok){const d=await r.json();activity=d.activity}}catch(e){}
const typeLabel={'login':'🔑 Login','page_view':'📄 Page View','export':'📥 Export','subscribe':'🔔 Subscribe','unsubscribe':'🔕 Unsubscribe','message_sent':'💬 Message','session_heartbeat':'💓 Active'};
const typeBadge={'login':'b-green','page_view':'b-blue','export':'b-purple','subscribe':'b-green','unsubscribe':'b-amber','message_sent':'b-blue','session_heartbeat':'b-amber'};
const filtered=activity.filter(a=>a.event_type!=='session_heartbeat');
el.innerHTML=`<div class="card"><div class="card-h"><span class="card-t">Recent Activity</span>
<div style="display:flex;gap:8px;align-items:center">
<label style="font-size:12px;color:var(--text-m);display:flex;align-items:center;gap:4px"><input type="checkbox" id="showHeartbeats" onchange="toggleHeartbeats()"> Show heartbeats</label>
<span style="font-size:12px;color:var(--text-m)">${activity.length} events</span></div></div>
${filtered.length?`<div class="card-b" style="padding:0"><div class="table-wrap"><table><thead><tr><th>Time</th><th>User</th><th>Firm</th><th>Event</th><th>Page</th><th>Details</th></tr></thead>
<tbody id="activityRows">${activityRows(filtered,typeLabel,typeBadge)}</tbody></table></div></div>`
:`<div class="card-b"><p style="color:var(--text-m);font-size:13px">No activity recorded yet.</p></div>`}
</div>`;
S._activityData=activity;S._typeLabel=typeLabel;S._typeBadge=typeBadge}

function activityRows(items,typeLabel,typeBadge){
return items.map(a=>{
const time=a.created_at?new Date(a.created_at).toLocaleString('en-GB',{day:'2-digit',month:'short',hour:'2-digit',minute:'2-digit'}):'–';
const label=typeLabel[a.event_type]||a.event_type;
const badge=typeBadge[a.event_type]||'b-blue';
let details='';
let ed=a.event_data;
if(typeof ed==='string'){try{ed=JSON.parse(ed)}catch(e){ed={}}}
if(ed&&typeof ed==='object'){
const d=ed;
if(d.provider_name)details=d.provider_name+(d.tab?' — '+d.tab:'');
else if(d.subject)details=d.subject;
else if(d.type)details=d.type;
else if(d.method)details=d.method;
}
return`<tr>
<td style="font-size:12px">${time}</td>
<td class="nc">${a.name||'–'}</td>
<td style="font-size:12px">${a.firm||'–'}</td>
<td><span class="badge ${badge}" style="font-size:10px">${label}</span></td>
<td style="font-size:12px">${a.page||'–'}</td>
<td style="font-size:12px;color:var(--text-m);max-width:160px;overflow:hidden;text-overflow:ellipsis">${details}</td>
</tr>`}).join('')}

function toggleHeartbeats(){
const show=$('showHeartbeats').checked;
const items=show?S._activityData:S._activityData.filter(a=>a.event_type!=='session_heartbeat');
const tbody=$('activityRows');
if(tbody)tbody.innerHTML=activityRows(items,S._typeLabel,S._typeBadge)}

// ─── Stats Tab ───────────────────────────────────────────────────────

async function adminStats(el){
el.innerHTML='<div class="loading"><div class="spinner"></div>Loading...</div>';
let stats={};
try{const r=await fetch('/api/admin/activity/stats');if(r.ok){const d=await r.json();stats=d.stats}}catch(e){}
el.innerHTML=`
<div class="grid g3" style="margin-bottom:24px">
<div class="stat-card"><div class="stat-l">Active Users (7d)</div><div class="stat-v">${stats.active_users_7d||0}</div></div>
<div class="stat-card"><div class="stat-l">Logins (30d)</div><div class="stat-v">${stats.logins_30d||0}</div></div>
<div class="stat-card"><div class="stat-l">Page Views (30d)</div><div class="stat-v">${stats.page_views_30d||0}</div></div>
</div>
<div class="grid g2">
<div class="card"><div class="card-h"><span class="card-t">Top Pages (30d)</span></div>
${stats.top_pages&&stats.top_pages.length?`<div class="card-b" style="padding:0"><table><thead><tr><th>Page</th><th>Views</th></tr></thead>
<tbody>${stats.top_pages.map(p=>`<tr><td class="nc">${p.page}</td><td>${p.count}</td></tr>`).join('')}</tbody></table></div>`
:`<div class="card-b"><p style="color:var(--text-m);font-size:13px">No data yet</p></div>`}
</div>
<div class="card"><div class="card-h"><span class="card-t">Feature Usage (30d)</span></div>
${stats.feature_usage&&stats.feature_usage.length?`<div class="card-b" style="padding:0"><table><thead><tr><th>Feature</th><th>Count</th></tr></thead>
<tbody>${stats.feature_usage.map(f=>`<tr><td class="nc">${f.event_type}</td><td>${f.count}</td></tr>`).join('')}</tbody></table></div>`
:`<div class="card-b"><p style="color:var(--text-m);font-size:13px">No data yet</p></div>`}
</div>
</div>`}

// ─── Messages Tab ────────────────────────────────────────────────────

async function adminMessages(el){
el.innerHTML='<div class="loading"><div class="spinner"></div>Loading...</div>';
let msgs=[];
try{const r=await fetch('/api/admin/messages');if(r.ok){const d=await r.json();msgs=d.messages}}catch(e){}
el.innerHTML=`<div class="card"><div class="card-h"><span class="card-t">All Messages</span><span style="font-size:12px;color:var(--text-m)">${msgs.length} total</span></div>
${msgs.length?msgs.map(m=>`<div style="padding:16px 22px;border-bottom:1px solid var(--border)">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
<div><span style="font-size:13px;font-weight:600">${m.subject}</span>
${m.provider_name?` <span class="badge b-blue" style="font-size:10px">${m.provider_name}</span>`:''}</div>
<span class="badge ${m.status==='replied'?'b-green':'b-amber'}" style="font-size:10px">${m.status==='replied'?'Replied':'Awaiting reply'}</span></div>
<div style="font-size:12px;color:var(--text-m);margin-bottom:8px">From: <strong>${m.name||'–'}</strong> (${m.email||'–'}) · ${m.firm||'–'} · ${m.created_at?new Date(m.created_at).toLocaleDateString('en-GB'):''}</div>
<div style="font-size:13px;color:var(--text-s);line-height:1.6;margin-bottom:10px;white-space:pre-wrap">${m.body}</div>
${m.replies&&m.replies.length?m.replies.map(r=>`<div style="margin-left:20px;padding:10px 14px;background:var(--accent-g);border-radius:var(--rs);margin-bottom:6px">
<div style="font-size:11px;color:var(--green);font-weight:600;margin-bottom:4px">Bridge Research · ${r.created_at?new Date(r.created_at).toLocaleDateString('en-GB'):''}</div>
<div style="font-size:13px;color:var(--text-s);line-height:1.5;white-space:pre-wrap">${r.body}</div></div>`).join(''):''}
<div style="margin-top:8px;display:flex;gap:8px;align-items:flex-start" id="reply-${m.id}">
<textarea style="flex:1;background:var(--bg-card);border:1px solid var(--border);border-radius:var(--rs);padding:8px 10px;font-size:12px;color:var(--text);font-family:inherit;outline:none;resize:vertical;min-height:36px;transition:border-color .15s" onfocus="this.style.borderColor='var(--accent)'" onblur="this.style.borderColor='var(--border)'" placeholder="Type your reply..." id="rt-${m.id}"></textarea>
<button class="btn btn-p btn-sm" onclick="adminReply('${m.id}')">Reply</button>
</div>
</div>`).join(''):`<div class="card-b"><p style="color:var(--text-m);font-size:13px">No messages yet.</p></div>`}
</div>`}

async function adminReply(msgId){
const textarea=$('rt-'+msgId);
const reply=textarea.value.trim();
if(!reply){return}
textarea.disabled=true;
try{const r=await fetch(`/api/admin/messages/${msgId}/reply`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({reply})});
if(r.ok){adminTab('messages')}
else{const d=await r.json();alert(d.detail||'Failed');textarea.disabled=false}}
catch(e){alert('Connection error');textarea.disabled=false}}