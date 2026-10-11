"""A single inventory with a persistent detail panel, exported as HTML."""
TEMPLATE = r'''
<style>
body{max-width:1480px;background:#edf1f7;margin:24px auto;font-family:Segoe UI,Microsoft YaHei,sans-serif}
header{padding:24px;background:#13233e;color:white}header p{font-size:13px;color:#cedaef}header .stats{color:#7dd3fc}
button,select,input{font:inherit;border:1px solid #d4ddea;border-radius:8px;padding:9px 12px;background:white;color:#253751}
button{cursor:pointer}button:disabled{opacity:.5;cursor:default}input{min-width:240px}
.toolbar{display:flex;gap:10px;flex-wrap:wrap;align-items:center}.workbench{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(300px,1fr);gap:20px}
.list-wrap{max-height:490px;overflow:auto;border:1px solid #e5eaf2;border-radius:10px}#candidates tr{cursor:pointer}#candidates tr:hover{background:#edf5ff}#candidates tr.active{background:#dbeafe}
#candidates td{max-width:230px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}#candidates td:last-child{max-width:150px}
#detail{background:#f7faff;border:1px solid #e0e8f2;border-radius:14px;padding:20px;max-height:610px;overflow:auto}
#detail h3{margin-top:0;font-size:20px}#detail p{overflow-wrap:anywhere;font-size:14px}#detail .field-label{color:#4c6384;font-weight:600;font-size:12px;margin-bottom:4px}
.badge{display:inline-block;padding:3px 9px;background:#e0eafc;color:#254879;border-radius:20px;font-size:12px}
.pager{display:flex;gap:12px;align-items:center;margin-top:14px}#space-map{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;max-height:260px;overflow:auto}
#space-map button{text-align:left;min-height:58px;overflow-wrap:anywhere;position:relative;background:#eff5ff}
@media(max-width:900px){.workbench{grid-template-columns:1fr}#space-map{grid-template-columns:repeat(2,minmax(0,1fr))}body{padding:0 12px}}
</style>
<section><h2>文件清单 · AI 解释就在同一条记录里</h2><p id="coverage"></p>
<div class="toolbar"><input id="search" placeholder="搜索名称、软件或路径">
<select id="kind"><option value="all">全部状态</option><option value="analyzed">AI 已分析</option><option value="pending">AI 未分析</option><option value="review">规则：可考虑清理</option><option value="confirm">规则：需确认</option><option value="keep">规则：保留 / 未知</option></select></div>
<p id="candidate-count"></p><div class="workbench"><div><div class="list-wrap"><table><thead><tr><th>名称</th><th>大小</th><th>AI 状态</th><th>本地规则</th></tr></thead><tbody id="candidates"></tbody></table></div>
<div class="pager"><button id="prev">上一页</button><span id="page"></span><button id="next">下一页</button></div></div>
<aside id="detail"><h3>选择文件查看解释</h3></aside></div>
<p>本地规则和 AI 意见分别标明；不一致时先保留并核实。未检测文件是否在使用、是否有备份或是否可恢复。本报告不执行删除。</p></section>
<section><details><summary><strong>空间分布 · 点击展开</strong></summary><div class="toolbar" style="margin:16px 0"><button id="up">上一级</button><button id="home">根目录</button></div><p id="location"></p><div id="space-map"></div><div class="pager"><button id="map-prev">上一页</button><span id="map-page"></span><button id="map-next">下一页</button></div><p id="map-limit"></p></details></section>
<script>
(()=>{
const data=JSON.parse(document.getElementById('scan-data').textContent);
const records=data.files||[],size=n=>{let i=0;const u=['B','KiB','MiB','GiB','TiB'];while(n>=1024&&i<4){n/=1024;i++;}return n.toFixed(1)+' '+u[i];},name=p=>p.split(/[\\/]/).filter(Boolean).pop()||p;
const analyzed=records.filter(n=>n.ai).length;
document.getElementById('coverage').textContent='清单 '+records.length+' 项 · AI 已分析 '+analyzed+' 项 · 未分析 '+(records.length-analyzed)+' 项。清单由大文件和候选组成；AI 不再是另一份清单。';
let page=0,chosen=null;
function field(panel,label,value){const heading=document.createElement('p');heading.className='field-label';heading.textContent=label;const p=document.createElement('p');p.textContent=value||'未知';panel.append(heading,p);}
function details(n){chosen=n.path;const panel=document.getElementById('detail');panel.replaceChildren();const h=document.createElement('h3');h.textContent=n.ai?n.ai.name:name(n.path);panel.append(h);
field(panel,'路径与逻辑大小',n.path+' · '+size(n.bytes));field(panel,'本地规则提示',n.label+'：'+n.reason);
if(!n.ai){field(panel,'尚未分析','此项还没有发给 AI。在客户端选择这项并分析，结果会更新到同一条记录。');field(panel,'潜在影响',n.impact);return;}
const a=n.ai;for(const [label,value] of [['是什么',a.description],['所属软件',a.owner],['AI 建议（非删除许可）',a.decision],['处理影响',a.impact],['推荐方式',a.method],['证据状态',a.evidence_status]])field(panel,label,value);
for(const source of a.sources||[]){if(!/^https?:\/\//i.test(source.url))continue;const link=document.createElement('a');link.href=source.url;link.textContent=source.title||source.url;link.target='_blank';link.rel='noopener noreferrer';panel.append(link,document.createElement('br'));}}
function show(){const q=document.getElementById('search').value.toLowerCase(),kind=document.getElementById('kind').value;
const rows=records.filter(n=>(kind==='all'||(kind==='analyzed'&&n.ai)||(kind==='pending'&&!n.ai)||n.level===kind)&&
(n.path+' '+(n.ai?n.ai.name+' '+n.ai.owner:'')).toLowerCase().includes(q));
const pages=Math.max(1,Math.ceil(rows.length/15));page=Math.min(page,pages-1);document.getElementById('page').textContent=(page+1)+' / '+pages;document.getElementById('prev').disabled=page===0;document.getElementById('next').disabled=page===pages-1;
document.getElementById('candidate-count').textContent='当前筛选 '+rows.length+' 项；点击一行在右侧查看用途和影响。';
const tbody=document.getElementById('candidates');tbody.replaceChildren();const visible=rows.slice(page*15,(page+1)*15);
for(const n of visible){const tr=document.createElement('tr');tr.className=chosen===n.path?'active':'';for(const value of [n.ai?n.ai.name:name(n.path),size(n.bytes),n.ai?'已分析':'未分析',n.label]){const td=document.createElement('td');td.textContent=value;td.title=n.path;tr.append(td);}tr.onclick=()=>{details(n);show();};tbody.append(tr);}
if(visible.length&&!rows.some(n=>n.path===chosen)){details(visible[0]);}if(!visible.length){document.getElementById('detail').textContent='当前筛选没有匹配文件。';}}
document.getElementById('prev').onclick=()=>{page--;show();};document.getElementById('next').onclick=()=>{page++;show();};document.getElementById('kind').onchange=()=>{page=0;chosen=null;show();};document.getElementById('search').oninput=()=>{page=0;chosen=null;show();};show();
const nodes=new Map(data.directory_map.map(n=>[n.path,n])),children=new Map();for(const n of data.directory_map){if(n.parent){if(!children.has(n.parent))children.set(n.parent,[]);children.get(n.parent).push(n);}}
let current=data.root,mapPage=0;
function map(){const node=nodes.get(current),box=document.getElementById('space-map');box.replaceChildren();document.getElementById('location').textContent=current;document.getElementById('up').disabled=!node||!node.parent;
if(!node){box.textContent='没有目录明细。';return;}const items=[...(children.get(current)||[])].sort((a,b)=>b.bytes-a.bytes);if(node.direct_bytes)items.push({path:'直接文件合计',bytes:node.direct_bytes,leaf:true});if(node.omitted_count)items.push({path:'折叠 '+node.omitted_count+' 个子目录',bytes:node.omitted_bytes,leaf:true});
const pages=Math.max(1,Math.ceil(items.length/24));mapPage=Math.min(mapPage,pages-1);document.getElementById('map-page').textContent=(mapPage+1)+' / '+pages;document.getElementById('map-prev').disabled=mapPage===0;document.getElementById('map-next').disabled=mapPage===pages-1;
for(const item of items.slice(mapPage*24,(mapPage+1)*24)){const b=document.createElement('button');b.textContent=name(item.path)+' · '+size(item.bytes)+' · '+(item.bytes/Math.max(node.bytes,1)*100).toFixed(1)+'%';b.title=item.path;b.disabled=!!item.leaf;if(!item.leaf)b.onclick=()=>{current=item.path;mapPage=0;map();};box.append(b);}}
document.getElementById('up').onclick=()=>{current=nodes.get(current).parent;mapPage=0;map();};document.getElementById('home').onclick=()=>{current=data.root;mapPage=0;map();};document.getElementById('map-prev').onclick=()=>{mapPage--;map();};document.getElementById('map-next').onclick=()=>{mapPage++;map();};
document.getElementById('map-limit').textContent='目录明细 '+data.directory_map.length+' / '+data.directory_count+' 个，优先展示大目录。父目录包含子目录，不可相加；折叠或未扫描不等于没有占用。';map();
})();
</script>
'''
