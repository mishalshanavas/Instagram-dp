import contextlib
import io
from pathlib import Path
import sys
import unittest
from unittest.mock import Mock, patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import github_setup as gh


class FinishSetupTests(unittest.TestCase):
    def setUp(self):
        self.output = io.StringIO()
        redirect = contextlib.redirect_stdout(self.output)
        redirect.__enter__()
        self.addCleanup(redirect.__exit__, None, None, None)

    def test_successful_run_watched_by_exact_dispatch_id(self):
        dispatched = Mock(returncode=0, stdout='https://github.com/me/repo/actions/runs/123\n')
        with patch.object(gh, 'run_gh', side_effect=[dispatched, Mock(returncode=0)]) as run:
            self.assertTrue(gh.run_workflow('me/repo', 'rotate'))
        self.assertIn('mode=rotate', run.call_args_list[0].args[0])
        self.assertEqual(run.call_args_list[1].args[0][:3], ['run', 'watch', '123'])
        self.assertIn('picture was updated', self.output.getvalue())

    def test_failed_remote_run_not_reported_as_success(self):
        with patch.object(gh, 'run_gh', side_effect=[Mock(returncode=0, stdout='https://github.com/me/repo/actions/runs/123'), Mock(returncode=1), Mock(returncode=1)]):
            self.assertFalse(gh.run_workflow('me/repo', 'rotate'))
        self.assertNotIn('picture was updated', self.output.getvalue())
        self.assertIn('--log-failed', self.output.getvalue())

    def test_check_can_be_followed_by_explicit_rotation(self):
        with patch('builtins.input', side_effect=['1', 'y']), patch.object(gh, 'prepare_workflow', return_value=True), patch.object(gh, 'run_workflow', return_value=True) as run:
            gh.finish_setup('me/repo')
        self.assertEqual([call.args for call in run.call_args_list], [('me/repo', 'check'), ('me/repo', 'rotate')])

    def test_failed_check_never_offers_rotation(self):
        with patch('builtins.input', return_value='1') as prompt, patch.object(gh, 'prepare_workflow', return_value=True), patch.object(gh, 'run_workflow', return_value=False) as run:
            gh.finish_setup('me/repo')
        self.assertEqual(prompt.call_count, 1)
        run.assert_called_once_with('me/repo', 'check')

    def test_exit_does_not_enable_or_dispatch(self):
        with patch('builtins.input', return_value='0'), patch.object(gh, 'prepare_workflow') as prepare, patch.object(gh, 'run_workflow') as run:
            gh.finish_setup('me/repo')
        prepare.assert_not_called()
        run.assert_not_called()

    def test_automatic_setup_checks_then_rotates_without_prompt(self):
        with patch.object(gh, 'prepare_workflow', return_value=True), patch.object(gh, 'run_workflow', return_value=True) as run, patch('builtins.input') as prompt:
            self.assertTrue(gh.automatic_setup('me/repo'))
        self.assertEqual([call.args for call in run.call_args_list], [('me/repo', 'check'), ('me/repo', 'rotate')])
        prompt.assert_not_called()

    def test_automatic_setup_never_rotates_after_failed_check(self):
        with patch.object(gh, 'prepare_workflow', return_value=True), patch.object(gh, 'run_workflow', return_value=False) as run:
            self.assertFalse(gh.automatic_setup('me/repo'))
        run.assert_called_once_with('me/repo', 'check')

    def test_automatic_setup_respects_template_guard(self):
        with patch.object(gh, 'prepare_workflow', return_value=False), patch.object(gh, 'run_workflow') as run:
            self.assertFalse(gh.automatic_setup(gh.SOURCE_REPO))
        run.assert_not_called()
