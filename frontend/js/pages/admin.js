/* ─── Bridge – Admin Page ──────────────────────────────────────────── */

async function rAdmin(el){
if(!S.user||S.user.role!=='admin'){el.innerHTML='<div class="fi"><p style="color:var(--red)">Admin access required.</p></div>';return}
let users=[];
try{const r=await fetch('/api/admin/users');if(r.ok){const d=await r.json();users=d.users}}catch(e){}
el.innerHTML=`<div class="fi"><div class="ph1"><h1>Admin</h1><p>Manage users and send invitations</p></div>

<div class="card" style="margin-bottom:24px"><div class="card-h"><span class="card-t">Invite New User</span></div>
<div class="card-b">
<div style="display:flex;flex-direction:column;gap:12px;max-width:480px">
<div class="fg"><span class="fl">Email</span><input type="email" id="invEmail" placeholder="adviser@firm.co.uk" style="width:100%"></div>
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
</div></div>`}

async function doInvite(){
const email=$('invEmail').value.trim(),name=$('invName').value.trim(),firm=$('invFirm').value.trim(),role=$('invRole').value,st=$('invStatus');
st.textContent='';st.style.color='var(--text-m)';
if(!email||!name||!firm){st.style.color='var(--red)';st.textContent='Email, name and firm are required';return}
st.textContent='Sending invite...';
try{const r=await fetch('/api/admin/invite',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email,name,firm,role})});
if(r.ok){const d=await r.json();st.style.color='var(--green)';st.textContent='Invite sent to '+email;
$('invEmail').value='';$('invName').value='';$('invFirm').value='';
setTimeout(()=>nav('admin'),1500)}
else{const d=await r.json();st.style.color='var(--red)';st.textContent=d.detail||'Failed to send invite'}}
catch(e){st.style.color='var(--red)';st.textContent='Connection error'}}

async function doDeleteUser(userId,email){
if(!confirm(`Remove ${email}? This cannot be undone.`))return;
try{const r=await fetch(`/api/admin/users/${userId}`,{method:'DELETE'});
if(r.ok)nav('admin');
else{const d=await r.json();alert(d.detail||'Failed')}}catch(e){alert('Connection error')}}
