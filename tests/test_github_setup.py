import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import github_setup as gh
import create_session


def result(code=0, data=None):
    return Mock(returncode=code, stdout=json.dumps(data or {}))


class GitHubSetupTests(unittest.TestCase):
    def setUp(self):
        snapshot = patch.object(gh, 'workflow_run_ids', return_value=set())
        snapshot.start()
        self.addCleanup(snapshot.stop)
        lookup = patch.object(gh, 'find_dispatched_run', return_value=None)
        lookup.start()
        self.addCleanup(lookup.stop)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.session = Path(self.temp.name) / 'session.json'
        self.session.write_text('{"authorization_data":{"sessionid":"PRIVATE-TEST-TOKEN"}}')
        self.output = io.StringIO()
        p = contextlib.redirect_stdout(self.output)
        p.__enter__()
        self.addCleanup(p.__exit__, None, None, None)

    def configure(self, replies, results):
        with patch.object(gh, 'prepare_workflow', return_value=True), patch.object(gh, 'discover_repositories', side_effect=ValueError('offline')), patch.object(gh, 'ensure_gh', return_value=True), patch('builtins.input', side_effect=replies), patch.object(gh, 'run_gh', side_effect=results) as run:
            gh.configure_github(self.session)
        self.assertNotIn('PRIVATE-TEST-TOKEN', self.output.getvalue())
        return run

    def test_full_flow_logs_in_uploads_stdin_and_dispatches_check(self):
        run = self.configure(['https://github.com/owner/repo.git', '', ''], [result(1), result(), result(data={'nameWithOwner': 'owner/repo', 'viewerPermission': 'ADMIN'}), result(), result()])
        self.assertIn('--web', run.call_args_list[1].args[0])
        upload = run.call_args_list[3]
        self.assertEqual(upload.args[0], ['secret', 'set', 'INSTA_SESSION', '--repo', 'github.com/owner/repo'])
        self.assertIn('stdin', upload.kwargs)
        self.assertIn('mode=check', run.call_args_list[4].args[0])
        self.assertIn('does not mean the check passed', self.output.getvalue())

    def test_existing_login_automatically_dispatches_check(self):
        run = self.configure(['owner/repo'], [result(), result(data={'nameWithOwner': 'owner/repo', 'viewerPermission': 'ADMIN'}), result(), result()])
        self.assertEqual(run.call_count, 4)
        self.assertNotIn('auth login', str(run.call_args_list))

    def test_auth_failure_does_not_upload(self):
        run = self.configure([], [result(1), result(1)])
        self.assertEqual(run.call_count, 2)
        self.assertIn('sign-in did not finish', self.output.getvalue())

    def test_missing_repo_does_not_upload(self):
        run = self.configure(['owner/missing'], [result(), result(1)])
        self.assertEqual(run.call_count, 2)
        self.assertIn('Cannot access', self.output.getvalue())

    def test_no_admin_access_does_not_upload(self):
        run = self.configure(['owner/repo'], [result(), result(data={'viewerPermission': 'READ'})])
        self.assertEqual(run.call_count, 2)
        self.assertIn('admin access', self.output.getvalue())

    def test_upload_is_automatic(self):
        run = self.configure(['owner/repo'], [result(), result(data={'viewerPermission': 'ADMIN', 'nameWithOwner': 'owner/repo'}), result(), result()])
        self.assertEqual(run.call_count, 4)
        self.assertIn('secret', run.call_args_list[2].args[0])

    def test_upload_failure_never_dispatches(self):
        run = self.configure(['owner/repo', ''], [result(), result(data={'viewerPermission': 'ADMIN', 'nameWithOwner': 'owner/repo'}), result(1)])
        self.assertEqual(run.call_count, 3)
        self.assertIn('Secret upload failed', self.output.getvalue())

    def test_dispatch_failure_preserves_uploaded_secret(self):
        self.configure(['owner/repo', '', ''], [result(), result(data={'viewerPermission': 'ADMIN', 'nameWithOwner': 'owner/repo'}), result(), result(1)])
        self.assertIn('INSTA_SESSION saved', self.output.getvalue())
        self.assertIn('Could not start', self.output.getvalue())

    def test_bad_repo_input_reprompts_and_manual_exit(self):
        run = self.configure(['https://evil.example/repo', ''], [result()])
        self.assertEqual(run.call_count, 1)
        self.assertIn('Manual setup', self.output.getvalue())

    def test_existing_cli_needs_no_install(self):
        with patch.object(gh.shutil, 'which', return_value='/bin/gh'), patch.object(gh.subprocess, 'run') as run:
            self.assertTrue(gh.ensure_gh())
        run.assert_not_called()

    def test_missing_cli_linux_install(self):
        def which(name):
            return None if name == 'gh' else '/usr/bin/' + name
        with patch.object(gh.sys, 'platform', 'linux'), patch.object(gh.os, 'geteuid', return_value=1000, create=True), patch.object(gh.shutil, 'which', side_effect=which), patch('builtins.input', return_value=''), patch.object(gh.subprocess, 'run', return_value=result()) as run:
            self.assertFalse(gh.ensure_gh())
        self.assertEqual(run.call_args.args[0], ['sudo', 'apt-get', 'install', '-y', 'gh'])
        self.assertIn('reopen your terminal', self.output.getvalue())

    def test_missing_cli_installs_without_confirmation(self):
        with patch.object(gh.sys, 'platform', 'darwin'), patch.object(gh.shutil, 'which', side_effect=lambda name: '/bin/brew' if name == 'brew' else None), patch('builtins.input', return_value='n'), patch.object(gh.subprocess, 'run') as run:
            self.assertFalse(gh.ensure_gh())
        run.assert_called_once_with(['brew', 'install', 'gh'])

    def test_github_only_does_not_authenticate_instagram(self):
        with patch.object(create_session, 'SESSION_FILE', self.session), patch.object(create_session, 'authenticate') as login, patch.object(create_session, 'configure_github') as configure:
            create_session.main(['--github-only'])
        login.assert_not_called()
        configure.assert_called_once()

    def test_github_only_requires_valid_local_session(self):
        self.session.write_text('broken')
        with patch.object(create_session, 'SESSION_FILE', self.session), self.assertRaisesRegex(SystemExit, 'No usable local session'):
            create_session.main(['--github-only'])


if __name__ == '__main__':
    unittest.main()
