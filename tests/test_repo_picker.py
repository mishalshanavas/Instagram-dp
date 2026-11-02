import contextlib
import io
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import Mock, patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import github_setup as gh


class PickerTests(unittest.TestCase):
    def setUp(self):
        redirect = contextlib.redirect_stdout(io.StringIO())
        redirect.__enter__()
        self.addCleanup(redirect.__exit__, None, None, None)

    def test_provenance_not_repo_name_and_pagination(self):
        first = [{'full_name': f'me/repo{i}', 'owner': {'login': 'me'}} for i in range(100)]
        last = [{'full_name': 'me/renamed', 'owner': {'login': 'me'}}]
        def api(endpoint):
            if endpoint == 'user': return {'login': 'me'}
            if endpoint.endswith('&page=1'): return first
            if endpoint.endswith('&page=2'): return last
            name = endpoint.removeprefix('repos/')
            data = {'full_name': name}
            if name == 'me/repo0': data['source'] = {'full_name': gh.SOURCE_REPO}
            if name == 'me/renamed': data['template_repository'] = {'full_name': gh.SOURCE_REPO}
            return data
        with patch.object(gh, 'api_json', side_effect=api):
            user, matches = gh.discover_repositories()
        self.assertEqual(user, 'me')
        self.assertEqual(matches, [('me/renamed', 'template copy', False), ('me/repo0', 'fork', False)])

    def test_pick_existing(self):
        with patch.object(gh, 'discover_repositories', return_value=('me', [('me/a', 'fork', False), ('me/b', 'template copy', False)])), patch('builtins.input', return_value='2'):
            self.assertEqual(gh.select_repository(), 'me/b')

    def test_empty_account_can_create(self):
        with patch.object(gh, 'discover_repositories', return_value=('me', [])), patch('builtins.input', return_value='n'), patch.object(gh, 'create_repository', return_value='me/new') as create:
            self.assertEqual(gh.select_repository(), 'me/new')
        create.assert_called_once_with('me', automatic=True)

    def test_archived_not_selected(self):
        with patch.object(gh, 'discover_repositories', return_value=('me', [('me/a', 'fork', True)])), patch('builtins.input', side_effect=['1', '0']):
            self.assertIsNone(gh.select_repository())

    def test_private_template_creation(self):
        with patch.object(gh, 'api_json', return_value={'is_template': True}), patch('builtins.input', side_effect=['new', '', '']), patch.object(gh, 'run_gh', return_value=Mock(returncode=0)) as run:
            self.assertEqual(gh.create_repository('me'), 'me/new')
        self.assertEqual(run.call_args.args[0], ['repo', 'create', 'me/new', '--template', 'github.com/' + gh.SOURCE_REPO, '--private'])

    def test_non_template_requires_explicit_fork_choice(self):
        with patch.object(gh, 'api_json', return_value={'is_template': False}), patch('builtins.input', return_value='n'), patch.object(gh, 'run_gh') as run:
            self.assertIsNone(gh.create_repository('me'))
        run.assert_not_called()

    def test_fork_fallback(self):
        with patch.object(gh, 'api_json', return_value={'is_template': False}), patch('builtins.input', return_value='y'), patch.object(gh, 'run_gh', return_value=Mock(returncode=0)) as run:
            self.assertEqual(gh.create_repository('me'), 'me/Instagram-dp')
        self.assertIn('--clone=false', run.call_args.args[0])

    def test_failed_creation_not_returned_as_success(self):
        with patch.object(gh, 'api_json', return_value={'is_template': True}), patch('builtins.input', side_effect=['new', '2', '']), patch.object(gh, 'run_gh', return_value=Mock(returncode=1)):
            self.assertIsNone(gh.create_repository('me'))

    def test_discovery_failure_does_not_create(self):
        with patch.object(gh, 'discover_repositories', side_effect=ValueError('denied')), patch('builtins.input', side_effect=['n', '0']), patch.object(gh, 'create_repository') as create:
            self.assertIsNone(gh.select_repository())
        create.assert_not_called()

    def test_enter_selects_first_usable_copy_without_creation(self):
        matches = [('me/archived', 'fork', True), ('me/first', 'template copy', False), ('me/second', 'fork', False)]
        with patch.object(gh, 'discover_repositories', return_value=('me', matches)), patch('builtins.input', return_value='') as prompt, patch.object(gh, 'create_repository') as create:
            self.assertEqual(gh.select_repository(), 'me/first')
        prompt.assert_called_once_with('Choose an option [2]: ')
        create.assert_not_called()

    def test_enter_offers_creation_when_no_copies_exist(self):
        with patch.object(gh, 'discover_repositories', return_value=('me', [])), patch('builtins.input', return_value=''), patch.object(gh, 'create_repository', return_value='me/new') as create:
            self.assertEqual(gh.select_repository(), 'me/new')
        create.assert_called_once_with('me', automatic=True)

    def test_create_remains_available_with_multiple_copies(self):
        with patch.object(gh, 'discover_repositories', return_value=('me', [('me/a', 'fork', False), ('me/b', 'template copy', False)])), patch('builtins.input', return_value='N'), patch.object(gh, 'create_repository', return_value='me/new'):
            self.assertEqual(gh.select_repository(), 'me/new')

    def test_old_workflow_never_enabled(self):
        with patch.object(gh, 'run_gh', return_value=Mock(returncode=0, stdout='old workflow')) as run, patch.object(gh, 'api_json') as api:
            self.assertFalse(gh.prepare_workflow('me/repo'))
        self.assertEqual(run.call_count, 1)
        api.assert_not_called()

    def test_disabled_current_workflow_can_be_enabled(self):
        workflow = (Path(gh.__file__).resolve().parent.parent / '.github/workflows/change-dp.yml').read_text()
        with patch.object(gh, 'run_gh', side_effect=[Mock(returncode=0, stdout=workflow), Mock(returncode=0)]) as run, patch.object(gh, 'api_json', return_value={'state': 'disabled_manually'}), patch('builtins.input', return_value=''):
            self.assertTrue(gh.prepare_workflow('me/repo'))
        self.assertIn('enable', run.call_args.args[0])

    def test_auto_creation_uses_private_available_name_without_prompt(self):
        responses = [Mock(returncode=0, stderr=''), Mock(returncode=1, stderr='HTTP 404: Not Found'), Mock(returncode=0)]
        with patch.object(gh, 'api_json', return_value={'is_template': True}), patch.object(gh, 'run_gh', side_effect=responses) as run, patch('builtins.input') as prompt:
            self.assertEqual(gh.create_repository('me', automatic=True), 'me/Instagram-dp-2')
        prompt.assert_not_called()
        self.assertIn('--private', run.call_args.args[0])

    def test_auto_creation_does_not_treat_permission_failure_as_free_name(self):
        with patch.object(gh, 'api_json', return_value={'is_template': True}), patch.object(gh, 'run_gh', return_value=Mock(returncode=1, stderr='HTTP 403')) as run:
            self.assertIsNone(gh.create_repository('me', automatic=True))
        self.assertEqual(run.call_count, 1)
