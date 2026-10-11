"""Bounded, parent-connected directory data and one unified file inventory."""
import heapq
import json


def compact_directories(nodes, root, limit=3000):
    by_path = {n['path']: n for n in nodes}
    children = {}
    for n in nodes:
        children.setdefault(n.get('parent'), []).append(n)
    pending = [(-by_path[root]['bytes'], root)] if root in by_path else []
    selected = {}
    while pending and len(selected) < limit:
        _, path = heapq.heappop(pending)
        selected[path] = dict(by_path[path])
        for child in children.get(path, []):
            heapq.heappush(pending, (-child['bytes'], child['path']))
    for path, node in selected.items():
        omitted = [c for c in children.get(path, []) if c['path'] not in selected]
        node['omitted_count'] = node.get('omitted_count', 0) + len(omitted)
        node['omitted_bytes'] = node.get('omitted_bytes', 0) + sum(c['bytes'] for c in omitted)
    return list(selected.values())


def interactive_section(result):
    from file_records import file_records
    from report_dashboard import TEMPLATE
    data = {key: result.get(key, []) for key in ('directory_map', 'cleanup_candidates', 'largest_files')}
    data['root'] = result['root']
    data['directory_count'] = result.get('directories', len(data['directory_map']))
    data['directory_map'] = compact_directories(data['directory_map'], data['root'])
    data['ai_findings'] = result.get('ai_findings', [])
    data['files'] = file_records(result)
    data['summary'] = {k: v for k, v in result.items() if k not in {'directory_map', 'cleanup_candidates', 'largest_files', 'ai_findings'}}
    payload = json.dumps(data, ensure_ascii=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    return '<script type="application/json" id="scan-data">' + payload + '</script>' + TEMPLATE
