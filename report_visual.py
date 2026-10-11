"""Self-contained interactive report; no CDN or network access."""
import json


def interactive_section(result):
    data = {key: result.get(key, []) for key in ('directory_map', 'cleanup_candidates', 'largest_files')}
    data['root'] = result['root']
    # Prevent filenames from closing the script element.
    payload = json.dumps(data, ensure_ascii=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    return '<script type="application/json" id="scan-data">' + payload + '</script>' + TEMPLATE


TEMPLATE = r'''
<section><h2>空间分布 · 点击目录逐层查看</h2>
<button id="up">上一级</button> <button id="home">回到根目录</button>
<p id="location" style="overflow-wrap:anywhere"></p><div id="space-map" style="display:flex;flex-wrap:wrap;gap:6px;min-height:100px"></div>
<p>块大小表示当前层已统计字节占比；直接文件合并展示。零字节、未扫描和被跳过位置不代表没有文件。</p></section>
<section><h2>哪些值得检查？</h2><p>这是一份候选清单，不是可删文件白名单。缓存需确认所属软件；个人文件需你决定。回收站、备份、实际可释放空间均未核实。</p>
<label>类别 <select id="kind"><option value="all">全部</option><option value="review">可考虑清理（有条件）</option><option value="confirm">需要你确认</option><option value="keep">建议保留 / 用途未知</option></select></label>
<label> 搜索路径 <input id="search" placeholder="输入文件名或目录"></label>
<p id="candidate-count"></p><div style="overflow:auto"><table><thead><tr><th>文件</th><th>大小</th><th>判断</th><th>依据 / 可能影响</th></tr></thead><tbody id="candidates"></tbody></table></div>
<p>保留最大的 200 个非保留类候选，另展示大文件榜中的未知/保留项；不是全盘所有候选文件。数字是逻辑大小，不是预计可释放空间。</p></section>
<script>
(()=>{
const data=JSON.parse(document.getElementById('scan-data').textContent);
const nodes=new Map(data.directory_map.map(n=>[n.path,n]));
const children=new Map(); for(const n of data.directory_map){if(n.parent){if(!children.has(n.parent))children.set(n.parent,[]);children.get(n.parent).push(n);}}
const fmt=n=>{let i=0;const u=['B','KiB','MiB','GiB','TiB'];while(n>=1024&&i<4){n/=1024;i++;}return n.toFixed(1)+' '+u[i];};
const name=p=>p.split(/[\\/]/).filter(Boolean).pop()||p;
let current=data.root;
function draw(){
const node=nodes.get(current);document.getElementById('location').textContent=current;
const box=document.getElementById('space-map');box.replaceChildren();
document.getElementById('up').disabled=!node||!node.parent;
if(!node){box.textContent='旧报告缺少目录明细，请重新扫描。';return;}
const items=[...(children.get(current)||[])].sort((a,b)=>b.bytes-a.bytes);
if(node.direct_bytes)items.push({path:'直接文件（合计）',bytes:node.direct_bytes,leaf:true});
if(!items.length)box.textContent='没有已统计的子目录或文件。';
for(const item of items){const b=document.createElement('button');b.textContent=name(item.path)+' · '+fmt(item.bytes);b.title=item.path;
b.style.cssText='min-height:70px;min-width:130px;border:0;border-radius:10px;padding:12px;color:white;background:'+(item.leaf?'#64748b':'#275abe')+';flex:'+Math.max(item.bytes/Math.max(node.bytes,1)*100,1)+' 1 130px';
if(item.leaf)b.disabled=true;else b.onclick=()=>{current=item.path;draw();};box.append(b);}}
document.getElementById('up').onclick=()=>{current=nodes.get(current).parent;draw();};
document.getElementById('home').onclick=()=>{current=data.root;draw();};draw();
const rows=[...data.cleanup_candidates];const seen=new Set(rows.map(n=>n.path));
for(const f of data.largest_files){if(!seen.has(f.path))rows.push({...f,level:'keep',label:'建议保留 / 用途未知',reason:'不在清理候选规则中。',impact:'先核实用途，无法判断可恢复性。'});}
function filter(){const kind=document.getElementById('kind').value;const query=document.getElementById('search').value.toLowerCase();
const selected=rows.filter(n=>(kind==='all'||n.level===kind)&&n.path.toLowerCase().includes(query)).sort((a,b)=>b.bytes-a.bytes);
document.getElementById('candidate-count').textContent='显示 '+selected.length+' 项 · 逻辑大小合计 '+fmt(selected.reduce((sum,n)=>sum+n.bytes,0));
const tbody=document.getElementById('candidates');tbody.replaceChildren();
for(const n of selected){const tr=document.createElement('tr');for(const value of [n.path,fmt(n.bytes),n.label,n.reason+' '+n.impact]){const td=document.createElement('td');td.textContent=value;tr.append(td);}tbody.append(tr);}}
document.getElementById('kind').onchange=filter;document.getElementById('search').oninput=filter;filter();
})();
</script>
'''
