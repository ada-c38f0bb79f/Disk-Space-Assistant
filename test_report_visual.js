// Lightweight DOM contract checks; no network or personal report input.
const fs = require('fs');
const vm = require('vm');
const assert = require('assert');
class Element {
  constructor() { this.children = []; this.style = {}; this.value = ''; }
  append(...nodes) { this.children.push(...nodes); }
  replaceChildren(...nodes) { this.children = nodes; }
  after() {}
}
const nodes = new Map();
function get(id) { if (!nodes.has(id)) nodes.set(id, new Element()); return nodes.get(id); }
const data = {
  root: 'root', directory_count: 51,
  directory_map: [{path: 'root', parent: null, bytes: 50, direct_bytes: 0},
    ...Array.from({length: 50}, (_, i) => ({path: `root/dir${i}`, parent: 'root', bytes: 1, direct_bytes: 1}))],
  cleanup_candidates: Array.from({length: 40}, (_, i) => ({path: `file${i}.zip`, bytes: i,
    level: 'confirm', label: 'confirm', reason: 'reason', impact: 'impact'})),
  largest_files: [], ai_findings: [],
};
data.files = data.cleanup_candidates.map(n => ({...n, analysis_status: '未分析'}));
data.files[0].ai = {name: '测试用途', description: '测试描述', owner: '测试软件', decision: '需确认',
  impact: '未知', method: '先核实', evidence_status: '未联网', sources: []};
get('scan-data').textContent = JSON.stringify(data);
get('kind').value = 'all';
const script = fs.readFileSync('report_dashboard.py', 'utf8').split('<script>')[1].split('</script>')[0];
vm.runInNewContext(script, {document: {getElementById: get,
  createElement: () => new Element(), querySelector: () => new Element()}});
assert.equal(get('space-map').children.length, 24);
assert.equal(get('candidates').children.length, 15);
get('next').onclick();
assert.equal(get('page').textContent, '2 / 3');
get('map-next').onclick();
assert.equal(get('map-page').textContent, '2 / 3');
get('search').value = 'file39'; get('search').oninput();
assert.equal(get('candidates').children.length, 1);
assert.equal(get('page').textContent, '1 / 1');
get('search').value = ''; get('search').oninput();
get('kind').value = 'analyzed'; get('kind').onchange();
assert.equal(get('candidates').children.length, 1);
assert.equal(get('candidates').children[0].children[0].textContent, '测试用途');
get('candidates').children[0].onclick();
assert(get('detail').children.some(n => n.textContent === '测试描述'));
console.log('Directory pagination, candidate pagination and search checks passed.');
