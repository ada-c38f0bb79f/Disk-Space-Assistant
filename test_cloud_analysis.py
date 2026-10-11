import json
import unittest
from unittest.mock import patch
from cloud_analysis import prepare_items, analyze, validate_settings
from report_visual import compact_directories


class CloudTests(unittest.TestCase):
    def sample(self):
        return {'cleanup_candidates': [], 'largest_files': [
            {'path': 'C:/Users/Alice/AppData/Local/pip/cache/item.body', 'bytes': 123}]}

    def test_account_redaction(self):
        _, public = prepare_items(self.sample())
        self.assertNotIn('Alice', json.dumps(public))
        self.assertNotIn('C:', json.dumps(public))

    def test_chinese_or_whitespace_key_rejected_locally(self):
        for key in ('secret与文字', 'secret text', 'secret\ntext'):
            with self.assertRaises(ValueError) as caught:
                validate_settings('https://api.deepseek.com/chat/completions', 'model', key, 'chat')
            self.assertNotIn(key, str(caught.exception))

    def test_directory_compaction_preserves_omitted_size(self):
        nodes = [{'path': 'r', 'parent': None, 'bytes': 10, 'direct_bytes': 0},
                 {'path': 'a', 'parent': 'r', 'bytes': 7, 'direct_bytes': 7},
                 {'path': 'b', 'parent': 'r', 'bytes': 3, 'direct_bytes': 3}]
        compact = compact_directories(nodes, 'r', 2)
        root = next(n for n in compact if n['path'] == 'r')
        self.assertEqual(root['omitted_bytes'], 3)
        self.assertEqual(root['omitted_count'], 1)
        again = compact_directories(compact, 'r', 2)
        self.assertEqual(next(n for n in again if n['path'] == 'r')['omitted_bytes'], 3)

    def response(self, answer):
        raw = {'output': [{'type': 'web_search_call'}, {'type': 'message', 'content': [
            {'type': 'output_text', 'text': json.dumps({'items': [answer]}),
             'annotations': [{'type': 'url_citation', 'url': 'https://example.com/docs', 'title': 'Docs'}]}]}]}
        handle = unittest.mock.MagicMock()
        handle.__enter__.return_value.read.return_value = json.dumps(raw).encode()
        return handle

    def test_only_actual_citations_are_accepted(self):
        answer = {'id': 0, 'name': '缓存', 'source_urls': ['https://invented.example', 'https://example.com/docs']}
        with patch('cloud_analysis.request.build_opener') as opener:
            opener.return_value.open.return_value = self.response(answer)
            output = analyze(self.sample(), 'https://api.example/v1/responses', 'model', 'secret')
        self.assertEqual(len(output[0]['sources']), 1)
        self.assertNotIn('secret', json.dumps(output))

    def test_wrong_id_rejected(self):
        with patch('cloud_analysis.request.build_opener') as opener:
            opener.return_value.open.return_value = self.response({'id': 5})
            with self.assertRaises(ValueError):
                analyze(self.sample(), 'https://api.example/v1/responses', 'model', 'secret')

    def test_no_http_api(self):
        with self.assertRaises(ValueError):
            analyze(self.sample(), 'http://example.com', 'model', 'secret')

    def test_deepseek_base_url_and_json_mode(self):
        handle = unittest.mock.MagicMock()
        handle.__enter__.return_value.read.return_value = json.dumps({'choices': [{'message': {
            'content': json.dumps({'items': [{'id': 0, 'name': 'test', 'source_urls': []}]})}}]}).encode()
        with patch('cloud_analysis.request.build_opener') as opener:
            opener.return_value.open.return_value = handle
            analyze(self.sample(), 'https://api.deepseek.com/v1', 'account-model', 'secret', 'chat')
            req = opener.return_value.open.call_args.args[0]
            self.assertEqual(req.full_url, 'https://api.deepseek.com/v1/chat/completions')
            self.assertEqual(json.loads(req.data)['response_format']['type'], 'json_object')

    def test_deepseek_search_rejected_before_request(self):
        with patch('cloud_analysis.request.build_opener') as opener:
            with self.assertRaises(ValueError):
                analyze(self.sample(), 'https://api.deepseek.com', 'model', 'secret', 'search')
            opener.assert_not_called()


if __name__ == '__main__':
    unittest.main()
