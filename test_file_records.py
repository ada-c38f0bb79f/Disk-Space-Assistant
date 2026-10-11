import unittest
from unittest.mock import patch
from file_records import file_records
from cloud_analysis import analyze_selected


class InventoryTests(unittest.TestCase):
    def test_disjoint_ai_and_candidates_are_joined(self):
        result = {'cleanup_candidates': [{'path': 'D:/a.zip', 'bytes': 1}],
                  'largest_files': [{'path': 'C:/Windows/x.dll', 'bytes': 10}],
                  'ai_findings': [{'path': 'C:/Windows/x.dll', 'name': 'library'}]}
        rows = file_records(result)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]['analysis_status'], '已分析')
        self.assertEqual(rows[0]['level'], 'keep')
        self.assertEqual(rows[1]['analysis_status'], '未分析')

    def test_explicit_selection_and_batch_progress(self):
        selected = [{'path': f'D:/f{i}.zip', 'bytes': i} for i in range(7)]
        result = {'ai_findings': [{'path': 'D:/previous.zip', 'name': 'previous'}]}
        updates = []
        def fake(subset, *args, **kwargs):
            return [{'path': n['path'], 'name': 'identified'} for n in subset['largest_files']]
        with patch('cloud_analysis.analyze', side_effect=fake) as call:
            done = analyze_selected(result, selected, 'https://example.com', 'model', 'secret', 'chat',
                                    progress=lambda n, total, stage: updates.append(n))
        self.assertEqual(done, 7)
        self.assertEqual(call.call_count, 2)
        self.assertEqual(updates, [0, 5, 5, 7])
        self.assertEqual(len(result['ai_findings']), 8)

    def test_partial_results_survive_later_failure(self):
        selected = [{'path': f'D:/f{i}.zip', 'bytes': i} for i in range(7)]
        result = {}
        with patch('cloud_analysis.analyze', side_effect=[
                [{'path': n['path']} for n in selected[:5]], ValueError('failed')]):
            with self.assertRaises(ValueError):
                analyze_selected(result, selected, 'https://example.com', 'm', 'k', 'chat')
        self.assertEqual(len(result['ai_findings']), 5)


if __name__ == '__main__':
    unittest.main()
