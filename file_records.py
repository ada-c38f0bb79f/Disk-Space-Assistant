"""One file inventory shared by the desktop and exported report."""
from disk_assistant import cleanup_assessment


def file_records(result):
    records = {}
    for field in ('cleanup_candidates', 'largest_files'):
        for item in result.get(field, []):
            records.setdefault(item['path'], {}).update(item)
    for finding in result.get('ai_findings', []):
        records.setdefault(finding['path'], {'path': finding['path'], 'bytes': 0})['ai'] = finding
    for path, item in records.items():
        item.update(cleanup_assessment(path))
        item['analysis_status'] = '已分析' if 'ai' in item else '未分析'
    return sorted(records.values(), key=lambda item: item.get('bytes', 0), reverse=True)


def merge_findings(existing, new):
    merged = {item['path']: item for item in existing}
    merged.update({item['path']: item for item in new})
    return list(merged.values())
