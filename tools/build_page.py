import json,sys,datetime
import os,glob
# usage: build_page.py <page.html> <data_dir with <dataset_id>.json> <asof YYYY-MM-DD> <out.html>
PAGE,DATA,ASOF,OUT=sys.argv[1:5]
data={os.path.basename(f)[:-5]:json.load(open(f)) for f in glob.glob(os.path.join(DATA,'*.json'))}
page=open(PAGE).read().replace('<p class="he-note" id="asof">Updated daily from Zoho CRM and Zoho Books. Hippie Energy only.</p>','<p class="he-note" id="asof">Updated every morning from Zoho CRM, Zoho Books and Shopline. Hippie Energy, plus Hippie Brew in the revenue totals.</p>')
d3js=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'vendor','d3.min.js')).read()
asof=ASOF
css='''<style>
:root{--font-anthropic-sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,Helvetica,Arial,sans-serif;--font-anthropic-serif:Georgia,"Iowan Old Style","Times New Roman",serif;
--color-bg:#f7f6f2;--color-panel:#ffffff;--color-fg:#1f1e1c;--color-fg-muted:#6b6963;--color-border-line:#e4e1d8;--color-accent:#c96442;--color-ok:#3f8f5a;--color-warn:#c8902e;--color-bad:#c4483e;
--cds-chart-grid:#ece9e1;--cds-chart-muted:#d9d4c7;--cds-text-secondary:#6b6963;--cds-surface-popover:#ffffff;--cds-shadow-popover:0 4px 16px rgba(0,0,0,.12);--cds-border:#e4e1d8;
--cds-gap-xs:4px;--cds-gap-sm:8px;--cds-gap-md:16px;--cds-gap-lg:24px;--cds-gap-xl:32px;--cds-pad-xs:4px;--cds-pad-sm:8px;--cds-pad-lg:20px;--cds-radius:10px;
--cds-font-size-caption:12px;--cds-font-size-body:15px;--cds-font-size-heading:16px;--cds-font-size-title:26px;--cds-font-weight-medium:600;--cds-dur-slow:.3s;color-scheme:light}
@media (prefers-color-scheme: dark){:root{--color-bg:#1b1a18;--color-panel:#252421;--color-fg:#ecebe6;--color-fg-muted:#a3a097;--color-border-line:#3a3833;--cds-chart-grid:#33312c;--cds-chart-muted:#55524a;--cds-text-secondary:#a3a097;--cds-surface-popover:#2c2b27;--cds-border:#3a3833;color-scheme:dark}}
html,body{margin:0;background:var(--color-bg);color:var(--color-fg)}
#dash-root{padding:24px clamp(16px,3vw,40px) 48px}
.export-note{max-width:1200px;margin:0 auto 12px;font:12px var(--font-anthropic-sans);color:var(--color-fg-muted)}
.he-tip{position:absolute;z-index:10;pointer-events:none;background:var(--cds-surface-popover);box-shadow:var(--cds-shadow-popover);border:1px solid var(--cds-border);border-radius:8px;padding:6px 10px;font:12px var(--font-anthropic-sans);color:var(--color-fg)}
.dash-skeleton{opacity:.5}
</style>'''
shim='''<script>
(function(){
const RAW=%s;
const C=['#c96442','#3b82a0','#8a6bbf','#5c9e6e','#d4a04c','#b85c8a','#6b7fb3','#a0794d'];
const L={},CALC={},D={},cbs=[];
window.dash={colors:C,loader:(i,o)=>{L[i]=o},calc:(i,o)=>{CALC[i]=o},data:(i)=>D[i]?{status:'ok',data:D[i],refreshing:false,meta:[]}:{status:'loading',data:[]},onData:(f)=>{cbs.push(f)},refresh:()=>{},params:()=>({}),setParams:()=>{},resetParams:()=>{},setLink:()=>{}};
window.addEventListener('DOMContentLoaded',()=>{
  for(const k in RAW){const r=RAW[k];D[k]=Array.isArray(r)?r:(r.rows||r.data||r.results||r);}
  let go=true;while(go){go=false;for(const k in CALC){if(D[k])continue;if(CALC[k].inputs.every(i=>D[i])){try{D[k]=CALC[k].fn(...CALC[k].inputs.map(i=>D[i]));}catch(e){console.error(k,e);D[k]=[];}go=true;}}}
  document.querySelectorAll('[data-source][data-field][data-row]').forEach(e=>{const d=D[e.dataset.source];if(d&&d[+e.dataset.row]!=null){const v=d[+e.dataset.row][e.dataset.field];if(v!=null){e.textContent=typeof v==='number'?v.toLocaleString('en-US'):v;e.classList.remove('dash-skeleton');}}});
  cbs.forEach(f=>{try{f()}catch(e){console.error(e)}});
});
})();
</script>'''%json.dumps(data,separators=(',',':'))
note='<p class="export-note">Data as of %s · Prepared from Zoho CRM, Zoho Books and Shopline data. Hover any chart for details.</p>'%datetime.date.fromisoformat(asof).strftime('%B %-d, %Y')
html='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Hippie Energy Sales</title>'+css+'<script>'+d3js+'</script>'+shim+'</head><body><div id="dash-root">'+note+page+'</div></body></html>'
out=OUT
open(out,'w').write(html); print(out,len(html))
