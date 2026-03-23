/* ─── Bridge – Demo Requests (Admin) ───────────────────────────────── */

async function adminDemoRequests(el){
el.innerHTML='<div class="loading"><div class="spinner"></div>Loading...</div>';
let requests=[];
try{const r=await fetch('/api/admin/demo-requests');if(r.ok){const d=await r.json();requests=d.requests}}catch(e){}
const pending=requests.filter(r=>r.status==='pending');
const reviewed=requests.filter(r=>r.status!=='pending');
el.innerHTML=`
${pending.length?`<div class="card" style="margin-bottom:24px"><div class="card-h"><span class="card-t">Pending Requests</span><span class="badge b-amber">${pending.length} pending</span></div>
<div class="card-b" style="padding:0"><div class="table-wrap"><table><thead><tr><th>Name</th><th>Email</th><th>Firm</th><th>I am</th><th>Firm Size</th><th>Submitted</th><th></th></tr></thead>
<tbody>${pending.map(r=>`<tr>
<td class="nc">${r.name}</td>
<td>${r.email}</td>
<td>${r.firm||'–'}</td>
<td style="font-size:12px">${r.persona||'–'}</td>
<td style="font-size:12px">${r.tier||'–'}</td>
<td style="font-size:12px">${r.created_at?new Date(r.created_at).toLocaleDateString('en-GB'):'–'}</td>
<td style="white-space:nowrap">
<button class="btn btn-p btn-sm" onclick="approveDemoReq('${r.id}','${r.email}')">Approve</button>
<button class="btn btn-g btn-sm" style="margin-left:4px" onclick="rejectDemoReq('${r.id}','${r.email}')">Reject</button>
</td></tr>`).join('')}</tbody></table></div></div>`
:`<div class="card" style="margin-bottom:24px"><div class="card-h"><span class="card-t">Pending Requests</span></div>
<div class="card-b"><p style="color:var(--text-m);font-size:13px">No pending demo requests.</p></div></div>`}

${reviewed.length?`<div class="card"><div class="card-h"><span class="card-t">Reviewed</span><span style="font-size:12px;color:var(--text-m)">${reviewed.length} total</span></div>
<div class="card-b" style="padding:0"><div class="table-wrap"><table><thead><tr><th>Name</th><th>Email</th><th>Firm</th><th>Status</th><th>Submitted</th><th>Reviewed</th></tr></thead>
<tbody>${reviewed.map(r=>`<tr>
<td class="nc">${r.name}</td>
<td>${r.email}</td>
<td>${r.firm||'–'}</td>
<td><span class="badge ${r.status==='approved'?'b-green':'b-red'}">${r.status}</span></td>
<td style="font-size:12px">${r.created_at?new Date(r.created_at).toLocaleDateString('en-GB'):'–'}</td>
<td style="font-size:12px">${r.reviewed_at?new Date(r.reviewed_at).toLocaleDateString('en-GB'):'–'}</td>
</tr>`).join('')}</tbody></table></div></div>`:''}
`}

async function approveDemoReq(id,email){
if(!confirm(`Approve ${email}? This will create their account and send an invite email.`))return;
try{const r=await fetch(`/api/admin/demo-requests/${id}/approve`,{method:'POST'});
if(r.ok){const d=await r.json();alert(`Approved. Invite sent to ${email}`);adminTab('requests')}
else{const d=await r.json();alert(d.detail||'Failed to approve')}}
catch(e){alert('Connection error')}}

async function rejectDemoReq(id,email){
if(!confirm(`Reject ${email}'s demo request?`))return;
try{const r=await fetch(`/api/admin/demo-requests/${id}/reject`,{method:'POST'});
if(r.ok)adminTab('requests');
else{const d=await r.json();alert(d.detail||'Failed')}}
catch(e){alert('Connection error')}}
