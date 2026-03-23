/* ─── Bridge – App Core ────────────────────────────────────────────── */
/* State, auth, router, utilities                                       */

const $=id=>document.getElementById(id);
let S={p:'dashboard',c:{},pr:{},bvOpen:true,user:null},CH={};

// ─── Auth ────────────────────────────────────────────────────────────

async function checkAuth(){
try{const r=await fetch('/api/auth/me');const d=await r.json();
if(d.authenticated){S.user=d.user;showApp();return true}}catch(e){}
showLogin();return false}

function showLogin(){$('loginOverlay').style.display='flex';$('appShell').style.display='none';$('loginEmail').value='';$('loginPass').value='';$('loginErr').textContent=''}
function showApp(){$('loginOverlay').style.display='none';$('appShell').style.display='flex';
$('userAvatar').textContent=S.user.name.split(' ').map(w=>w[0]).join('');
$('userName').textContent=S.user.name;
fetch('/api/preferences').then(r=>r.json()).then(d=>{if(d.preferences?.display?.dark_mode)savePrefApplyDark(true)}).catch(()=>{});
render()}

async function doLogin(){
const email=$('loginEmail').value.trim(),pass=$('loginPass').value;
$('loginErr').textContent='';
if(!email||!pass){$('loginErr').textContent='Please enter email and password';return}
try{const r=await fetch('/api/auth/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email,password:pass})});
if(r.ok){const d=await r.json();S.user=d.user;showApp()}
else{const d=await r.json();$('loginErr').textContent=d.detail||'Login failed'}}
catch(e){$('loginErr').textContent='Connection error'}}

async function doLogout(){
try{await fetch('/api/auth/logout',{method:'POST'})}catch(e){}
S.user=null;S.c={};showLogin()}

function toggleUserMenu(){
const existing=document.getElementById('userMenu');
if(existing){existing.remove();return}
const pill=$('userPill');const rect=pill.getBoundingClientRect();
const menu=document.createElement('div');menu.id='userMenu';
menu.style.cssText=`position:fixed;top:${rect.bottom+4}px;right:${window.innerWidth-rect.right}px;background:var(--bg);border:1px solid var(--border);border-radius:var(--rs);box-shadow:0 4px 12px rgba(0,0,0,.1);z-index:200;min-width:180px;overflow:hidden`;
menu.innerHTML=`<div style="padding:12px 16px;border-bottom:1px solid var(--border)"><div style="font-size:13px;font-weight:600">${S.user.name}</div><div style="font-size:11px;color:var(--text-m)">${S.user.firm}</div></div>
<div style="padding:4px"><div style="padding:8px 12px;font-size:13px;cursor:pointer;border-radius:4px;color:var(--text-s)" onmouseover="this.style.background='var(--bg-hover)'" onmouseout="this.style.background=''" onclick="document.getElementById('userMenu').remove();nav('account')">Preferences</div>
<div style="padding:8px 12px;font-size:13px;cursor:pointer;border-radius:4px;color:var(--text-s)" onmouseover="this.style.background='var(--bg-hover)'" onmouseout="this.style.background=''" onclick="document.getElementById('userMenu').remove();nav('messages')">Messages</div>
<div style="padding:8px 12px;font-size:13px;cursor:pointer;border-radius:4px;color:var(--red)" onmouseover="this.style.background='var(--red-bg)'" onmouseout="this.style.background=''" onclick="document.getElementById('userMenu').remove();doLogout()">Sign Out</div></div>`;
document.body.appendChild(menu);
setTimeout(()=>{const close=e=>{if(!menu.contains(e.target)&&!pill.contains(e.target)){menu.remove();document.removeEventListener('click',close)}};document.addEventListener('click',close)},0)}

// ─── Dark Mode ───────────────────────────────────────────────────────

function savePrefApplyDark(dark){
const root=document.documentElement;
const loginLogo=document.querySelector('.login-box .logo img');
if(dark){root.style.setProperty('--bg','#0f1117');root.style.setProperty('--bg-card','#1a1d2e');root.style.setProperty('--bg-hover','#242736');root.style.setProperty('--bg-surface','#1a1d2e');root.style.setProperty('--border','#2a2d3e');root.style.setProperty('--border-a','#3a3d4e');root.style.setProperty('--text','#e2e8f0');root.style.setProperty('--text-s','#94a3b8');root.style.setProperty('--text-m','#64748b');if(loginLogo)loginLogo.src='bridge-logo-dark.png'}
else{root.style.setProperty('--bg','#ffffff');root.style.setProperty('--bg-card','#f8f9fb');root.style.setProperty('--bg-hover','#f1f3f7');root.style.setProperty('--bg-surface','#f3f4f6');root.style.setProperty('--border','#e2e5ea');root.style.setProperty('--border-a','#cbd0d8');root.style.setProperty('--text','#1a1f2e');root.style.setProperty('--text-s','#4b5563');root.style.setProperty('--text-m','#6b7280');if(loginLogo)loginLogo.src='bridge-logo-nav.png'}}

// ─── Router ──────────────────────────────────────────────────────────

function nav(p,pr={}){S.p=p;S.pr=pr;document.querySelectorAll('.nav-item').forEach(n=>n.classList.remove('active'));const e=document.querySelector(`.nav-item[data-page="${p}"]`);if(e)e.classList.add('active');render()}

async function render(){
const el=$('app'),tt=$('tt');DC();removeBV();el.innerHTML='<div class="loading"><div class="spinner"></div>Loading...</div>';
switch(S.p){
case'dashboard':tt.textContent='Homepage';await rDash(el);break;
case'selection':tt.textContent='MPS Selection';await rSel(el);break;
case'analysis':tt.textContent='MPS Analysis';await rAna(el);break;
case'provider':tt.textContent='MPS Analysis';await rProv(el);break;
case'insights':tt.textContent='Insights';await rIns(el);break;
case'insight':tt.textContent='Insight';await rInsD(el);break;
case'messages':tt.textContent='Messages';await rMsg(el);break;
case'account':tt.textContent='Preferences';await rAcct(el);break;
default:tt.textContent='Homepage';await rDash(el);
}}

// ─── Utilities ───────────────────────────────────────────────────────

async function F(u){if(S.c[u])return S.c[u];try{const r=await fetch(u);const d=await r.json();S.c[u]=d;return d}catch(e){console.error(e);return null}}
function DC(){Object.values(CH).forEach(c=>c.destroy&&c.destroy());CH={}}
function v(x,suf='%'){return x!=null?x+suf:'–'}
function catB(c){return c==='Weekly Commentary'?'b-green':c==='Regulatory'?'b-amber':'b-blue'}
function riskB(r){return r<=3?'b-green':r<=5?'b-blue':r<=7?'b-amber':'b-red'}
function pId(n){return n.toLowerCase().replace(/ investors/,'').replace(/ /g,'-')}
function shortName(n){return n.replace('Quilter WealthSelect Active ','').replace('Managed ','')}

// ─── Bridge View ─────────────────────────────────────────────────────

function removeBV(){const el=document.getElementById('bv-inline');if(el)el.remove()}
function toggleBV(){}
function renderBV(content){removeBV();if(!content)return;const tc=$('tc');if(!tc)return;const div=document.createElement('div');div.id='bv-inline';div.className='bv-inline';div.innerHTML=`<div class="bv-inline-header">💡 Bridge View</div><div class="bv-inline-content">${content}</div>`;tc.prepend(div)}

// ─── Article Formatter ───────────────────────────────────────────────

function fmtArticle(t){if(!t)return'<p style="color:var(--text-m)">Content to be added.</p>';return t.split('\n\n').map(p=>{p=p.trim();if(!p)return'';if(p.startsWith('**')&&p.endsWith('**'))return`<h3>${p.replace(/\*\*/g,'')}</h3>`;let h=p.replace(/\*\*(.*?)\*\*/g,'<strong>$1</strong>');const lines=h.split('\n');const hasList=lines.some(l=>{const tr=l.trim();return tr.startsWith('•')||tr.match(/^\d+\.\t/)||tr.match(/^\d+\. /)||tr.startsWith('o\t')||tr.startsWith('o ')||tr.startsWith('\uf0a7')});if(hasList){let out='',inUl=false,inOl=false,inSub=false;lines.forEach(l=>{const tr=l.trim();if(!tr)return;const isBullet=tr.startsWith('•')||tr.startsWith('\u2022');const isNum=tr.match(/^(\d+)\.\t/)||tr.match(/^(\d+)\.\s/);const isSub=tr.startsWith('o\t')||tr.startsWith('o ')||tr.startsWith('\uf0a7');const isSubSub=tr.startsWith('\uf0a7')||tr.startsWith(' \uf0a7');if(isBullet){if(inSub){out+='</ul></li>';inSub=false}if(inOl){out+='</li></ol>';inOl=false}if(!inUl){out+='<ul>';inUl=true}else{out+='</li>'}out+=`<li>${tr.slice(1).trim()}`}else if(isNum){if(inSub){out+='</ul></li>';inSub=false}if(inUl){out+='</li></ul>';inUl=false}if(!inOl){out+='<ol>';inOl=true}else{out+='</li>'}const txt=tr.replace(/^\d+\.\s*/,'');out+=`<li>${txt}`}else if(isSub&&(inUl||inOl)){if(!inSub){out+='<ul style="margin-left:20px;margin-top:4px">';inSub=true}const txt=tr.startsWith('\uf0a7')?tr.slice(1).trim():tr.slice(1).trim();out+=`<li>${txt}</li>`}else if(isSubSub&&inSub){const txt=tr.startsWith('\uf0a7')?tr.slice(1).trim():tr.replace(/^\s*/,'');out+=`<li style="margin-left:20px">${txt}</li>`}else{if(inSub){out+='</ul>';inSub=false}if(inUl){out+='</li></ul>';inUl=false}if(inOl){out+='</li></ol>';inOl=false}out+=`<p>${tr}</p>`}});if(inSub)out+='</ul></li>';if(inUl)out+='</ul>';if(inOl)out+='</ol>';return out}return`<p>${h.replace(/\n/g,'<br>')}</p>`}).join('')}

// ─── Init ────────────────────────────────────────────────────────────

checkAuth();
