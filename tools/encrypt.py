import sys,os,base64,json
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
# usage: PAGE_PASSWORD=... encrypt.py <in.html> <out.html>
src,out=sys.argv[1],sys.argv[2]
pw=os.environ['PAGE_PASSWORD']
ITER=600000
salt=os.urandom(16); iv=os.urandom(12)
key=PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=salt,iterations=ITER).derive(pw.encode())
ct=AESGCM(key).encrypt(iv,open(src,'rb').read(),None)
b=lambda x: base64.b64encode(x).decode()
payload=json.dumps({'s':b(salt),'i':b(iv),'n':ITER,'c':b(ct)})
html='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>Hippie Energy Sales</title>
<style>
:root{--bg:#f7f6f2;--panel:#fff;--fg:#1f1e1c;--muted:#6b6963;--line:#e4e1d8;--accent:#c96442;color-scheme:light}
@media (prefers-color-scheme:dark){:root{--bg:#1b1a18;--panel:#252421;--fg:#ecebe6;--muted:#a3a097;--line:#3a3833;color-scheme:dark}}
html,body{margin:0;height:100%;background:var(--bg);color:var(--fg);font:15px -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,Helvetica,Arial,sans-serif}
main{min-height:100%;display:grid;place-items:center;padding:16px;box-sizing:border-box}
form{width:min(100%,360px);background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:28px;display:grid;gap:14px}
h1{font:400 26px Georgia,"Times New Roman",serif;margin:0}
p{margin:0;color:var(--muted);font-size:14px}
label{font-size:13px;color:var(--muted)}
input{font:inherit;padding:10px 12px;border:1px solid var(--line);border-radius:8px;background:var(--bg);color:var(--fg)}
input:focus{outline:2px solid var(--accent);outline-offset:1px}
button{font:inherit;font-weight:600;padding:10px 12px;border:0;border-radius:8px;background:var(--accent);color:#fff;cursor:pointer}
button:disabled{opacity:.6;cursor:default}
#err{color:#c4483e;font-size:13px;min-height:1em}
</style></head><body><main>
<form id="f" autocomplete="off">
<h1>Hippie Energy Sales</h1>
<p>This dashboard is password protected.</p>
<label for="pw">Password</label>
<input id="pw" type="password" autofocus required>
<button id="go" type="submit">Open dashboard</button>
<div id="err" role="alert"></div>
</form></main>
<script>
const P=__PAYLOAD__;
const u=(s)=>Uint8Array.from(atob(s),c=>c.charCodeAt(0));
async function open_(pw){
  const base=await crypto.subtle.importKey('raw',new TextEncoder().encode(pw),'PBKDF2',false,['deriveKey']);
  const key=await crypto.subtle.deriveKey({name:'PBKDF2',salt:u(P.s),iterations:P.n,hash:'SHA-256'},base,{name:'AES-GCM',length:256},false,['decrypt']);
  const pt=await crypto.subtle.decrypt({name:'AES-GCM',iv:u(P.i)},key,u(P.c));
  return new TextDecoder().decode(pt);
}
async function show(pw){
  const html=await open_(pw);
  try{sessionStorage.setItem('he_pw',pw)}catch(e){}
  document.open();document.write(html);document.close();
}
document.getElementById('f').addEventListener('submit',async(e)=>{
  e.preventDefault();const b=document.getElementById('go'),er=document.getElementById('err');
  b.disabled=true;b.textContent='Opening…';er.textContent='';
  try{await show(document.getElementById('pw').value)}catch(x){er.textContent='That password didn\\u2019t work. Try again.';b.disabled=false;b.textContent='Open dashboard';}
});
(async()=>{let s=null;try{s=sessionStorage.getItem('he_pw')}catch(e){}if(s){try{await show(s)}catch(e){}}})();
</script></body></html>'''.replace('__PAYLOAD__',payload)
open(out,'w').write(html); print(out,len(html))
