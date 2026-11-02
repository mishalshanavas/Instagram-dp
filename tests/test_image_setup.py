import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch
from PIL import Image
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import image_setup
import github_setup as gh


class PhotoTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        Image.new('RGB', (10, 10)).save(self.folder / 'holiday.png')
        redirect = contextlib.redirect_stdout(io.StringIO())
        redirect.__enter__()
        self.addCleanup(redirect.__exit__, None, None, None)

    def test_decline_and_invalid_images_never_call_github(self):
        with patch('builtins.input', side_effect=[str(self.folder), 'n']), patch.object(gh, 'run_gh') as run:
            self.assertFalse(image_setup.replace_photos('me/repo'))
        run.assert_not_called()
        (self.folder / 'broken.jpg').write_text('broken')
        with patch('builtins.input', return_value=str(self.folder)), patch.object(gh, 'run_gh') as run:
            self.assertFalse(image_setup.replace_photos('me/repo'))
        run.assert_not_called()

    def upload(self, fail_update=False):
        existing = [
            {'path': 'assets/images/old.png', 'type': 'blob', 'mode': '100644'},
            {'path': 'assets/images/notes.txt', 'type': 'blob', 'mode': '100644'},
            {'path': 'src/main.py', 'type': 'blob', 'mode': '100644'},
        ]
        calls = []
        def request(args, **kwargs):
            body = json.loads(kwargs['input'])
            calls.append((args, body))
            if args[args.index('--method') + 1] == 'PATCH' and fail_update:
                return Mock(returncode=1)
            return Mock(returncode=0, stdout=json.dumps({'sha': 'new-object'}))
        with patch('builtins.input', side_effect=[str(self.folder), 'y']), patch.object(gh, 'api_json', side_effect=[{'default_branch': 'main'}, {'object': {'sha': 'old-head'}}, {'tree': {'sha': 'old-tree'}}, {'tree': existing}]), patch.object(gh, 'run_gh', side_effect=request):
            success = image_setup.replace_photos('me/repo')
        return success, calls

    def test_atomic_replacement_preserves_unrelated_files(self):
        success, calls = self.upload()
        self.assertTrue(success)
        tree = calls[1][1]
        self.assertEqual(tree['base_tree'], 'old-tree')
        paths = {item['path']: item for item in tree['tree']}
        self.assertIsNone(paths['assets/images/old.png']['sha'])
        self.assertIn('assets/images/1.png', paths)
        self.assertEqual(paths['data/index.txt']['content'], '0')
        self.assertNotIn('src/main.py', paths)
        self.assertNotIn('assets/images/notes.txt', paths)
        self.assertEqual(calls[2][1]['parents'], ['old-head'])
        self.assertFalse(calls[-1][1]['force'])

    def test_concurrent_branch_change_reports_failure(self):
        success, calls = self.upload(fail_update=True)
        self.assertFalse(success)
        self.assertEqual(len(calls), 4)

    def test_menu_returns_after_upload_without_running_workflow(self):
        with patch('builtins.input', side_effect=['3', '0']), patch.object(image_setup, 'replace_photos') as upload, patch.object(gh, 'run_workflow') as run:
            gh.finish_setup('me/repo')
        upload.assert_called_once_with('me/repo')
        run.assert_not_called()
