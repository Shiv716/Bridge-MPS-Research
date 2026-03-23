/* ─── Bridge – Messages Page ───────────────────────────────────────── */

async function rMsg(el){
let d;try{const r=await fetch('/api/messages');d=await r.json()}catch(e){el.innerHTML='<p>Failed to load</p>';return}
el.innerHTML=`<div class="fi"><div class="ph1"><h1>Messages</h1><p>Your conversations with the Bridge Research team</p></div>
<div class="card" style="margin-bottom:24px"><div class="card-h"><span class="card-t">New Message</span></div>
<div class="card-b"><div class="msg-form">
<input type="text" id="msgSubj" placeholder="Subject">
<textarea id="msgBody" placeholder="Your message to Bridge Research..."></textarea>
<div style="display:flex;gap:10px;align-items:center"><button class="btn btn-p" onclick="sendMsg()">Send Message</button><span id="msgStatus" style="font-size:12px;color:var(--text-m)"></span></div>
</div></div></div>
<div class="card"><div class="card-h"><span class="card-t">Message History</span><span style="font-size:12px;color:var(--text-m)">${d.count} message${d.count!==1?'s':''}</span></div>
${d.messages.length?d.messages.map(m=>`<div class="msg-item" style="cursor:pointer" onclick="openThread('${m.id}')">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">
<span style="font-size:13px;font-weight:600">${m.subject}</span>
<span style="font-size:11px;color:var(--text-m)">${new Date(m.created_at*1000).toLocaleDateString('en-GB')}</span></div>
<div style="font-size:12.5px;color:var(--text-s);line-height:1.5">${m.body.slice(0,120)}${m.body.length>120?'...':''}</div>
${m.provider_name?`<div style="margin-top:4px"><span class="badge b-blue" style="font-size:10px">${m.provider_name}</span></div>`:''}
<div style="display:flex;align-items:center;gap:8px;margin-top:6px"><span class="badge ${m.reply?'b-green':'b-amber'}" style="font-size:10px">${m.reply?'Replied':'Awaiting reply'}</span>${m.replies&&m.replies.length?`<span style="font-size:11px;color:var(--text-m)">${m.replies.length} repl${m.replies.length===1?'y':'ies'}</span>`:''}</div>
</div>`).join(''):`<div style="padding:40px;text-align:center;color:var(--text-m);font-size:13px">No messages yet</div>`}
</div>
<div id="msgThread" style="display:none"></div>
</div>`}

async function openThread(msgId){
let d;try{const r=await fetch(`/api/messages/${msgId}`);d=await r.json()}catch(e){return}
const m=d.message;const th=$('msgThread');if(!th)return;
const replies=m.replies||[];
th.style.display='block';
th.innerHTML=`<div class="card" style="margin-top:20px"><div class="card-h"><span class="card-t">${m.subject}</span><span style="font-size:11px;color:var(--text-m);cursor:pointer" onclick="$('msgThread').style.display='none'">✕ Close</span></div>
<div class="card-b" style="padding:0">
<div style="padding:16px;border-bottom:1px solid var(--border)">
<div style="display:flex;justify-content:space-between;margin-bottom:8px"><span style="font-size:12px;font-weight:600;color:var(--accent)">You</span><span style="font-size:11px;color:var(--text-m)">${new Date(m.created_at*1000).toLocaleString('en-GB')}</span></div>
<div style="font-size:13px;color:var(--text-s);line-height:1.6;white-space:pre-wrap">${m.body}</div>
${m.provider_name?`<div style="margin-top:8px"><span class="badge b-blue" style="font-size:10px">${m.provider_name}</span></div>`:''}
</div>
${replies.map(r=>`<div style="padding:16px;border-bottom:1px solid var(--border);background:var(--accent-g)">
<div style="display:flex;justify-content:space-between;margin-bottom:8px"><span style="font-size:12px;font-weight:600;color:var(--green)">Bridge Research</span><span style="font-size:11px;color:var(--text-m)">${new Date(r.created_at*1000).toLocaleString('en-GB')}</span></div>
<div style="font-size:13px;color:var(--text-s);line-height:1.6;white-space:pre-wrap">${r.body}</div>
</div>`).join('')}
${!replies.length?`<div style="padding:24px;text-align:center;color:var(--text-m);font-size:12.5px">Awaiting reply from Bridge Research</div>`:''}
</div></div>`;
th.scrollIntoView({behavior:'smooth'})}

async function sendMsg(){
const subj=$('msgSubj').value.trim(),body=$('msgBody').value.trim(),st=$('msgStatus');
if(!subj||!body){st.style.color='var(--red)';st.textContent='Please fill in both fields';return}
st.style.color='var(--text-m)';st.textContent='Sending...';
try{const r=await fetch('/api/messages',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({subject:subj,message:body})});
if(r.ok){st.style.color='var(--green)';st.textContent='Message sent';$('msgSubj').value='';$('msgBody').value='';setTimeout(()=>nav('messages'),1000)}
else{const d=await r.json();st.style.color='var(--red)';st.textContent=d.detail||'Failed'}}
catch(e){st.style.color='var(--red)';st.textContent='Failed to send'}}
