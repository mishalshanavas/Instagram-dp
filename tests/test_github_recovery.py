import contextlib
import io
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import Mock, patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import github_setup as gh


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        redirect = contextlib.redirect_stdout(io.StringIO())
        redirect.__enter__()
        self.addCleanup(redirect.__exit__, None, None, None)

    def test_expired_discovery_recovers_and_creates_copy(self):
        with patch.object(gh, 'discover_repositories', side_effect=[gh.GitHubAuthenticationExpired(), ('me', [])]) as discover, patch.object(gh, 'recover_github_login', return_value=True) as login, patch.object(gh, 'create_repository', return_value='me/new') as create:
            self.assertEqual(gh.select_repository(), 'me/new')
        self.assertEqual(discover.call_count, 2)
        login.assert_called_once()
        create.assert_called_once_with('me', automatic=True)

    def test_no_infinite_auth_loop(self):
        with patch.object(gh, 'discover_repositories', side_effect=gh.GitHubAuthenticationExpired()) as discover, patch.object(gh, 'recover_github_login', return_value=True) as login, patch.object(gh, 'create_repository') as create:
            self.assertIsNone(gh.select_repository())
        self.assertEqual(discover.call_count, 2)
        login.assert_called_once()
        create.assert_not_called()

    def test_cancelled_login_preserves_no_creation(self):
        with patch.object(gh, 'discover_repositories', side_effect=gh.GitHubAuthenticationExpired()), patch.object(gh, 'recover_github_login', return_value=False), patch.object(gh, 'create_repository') as create:
            self.assertIsNone(gh.select_repository())
        create.assert_not_called()

    def test_overriding_tokens_removed_only_in_child(self):
        with patch.dict(os.environ, {'GH_TOKEN': 'private', 'GITHUB_TOKEN': 'private2'}), patch.object(gh, 'USE_SAVED_GITHUB_LOGIN', True), patch.object(gh.subprocess, 'run') as run:
            gh.run_gh(['api', 'user'])
            self.assertEqual(os.environ['GH_TOKEN'], 'private')
        self.assertNotIn('GH_TOKEN', run.call_args.kwargs['env'])
        self.assertNotIn('GITHUB_TOKEN', run.call_args.kwargs['env'])

    def test_401_is_distinct_from_network_failure(self):
        with patch.object(gh, 'run_gh', return_value=Mock(returncode=1, stderr='HTTP 401: private-token')):
            with self.assertRaises(gh.GitHubAuthenticationExpired):
                gh.api_json('user')
