import io
import contextlib
from pathlib import Path
import sys
import unittest
from unittest.mock import Mock, patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from failure_help import instagram_failure
import github_setup as gh


class FailureTests(unittest.TestCase):
    def test_403_recovery_does_not_expose_response_body(self):
        error = RuntimeError('PRIVATE-TOKEN')
        error.response = Mock(status_code=403)
        message = instagram_failure(error)
        self.assertIn('HTTP 403', message)
        self.assertIn('does not grant write access', message)
        self.assertNotIn('PRIVATE-TOKEN', message)

    def test_rate_limit_does_not_recommend_repeated_logins(self):
        error = RuntimeError()
        error.response = Mock(status_code=429)
        self.assertIn('Stop retries', instagram_failure(error))

    def test_legacy_logs_get_safe_summary(self):
        output = io.StringIO()
        logs = 'PRIVATE-TOKEN\\nINFO: None [403] POST https://i.instagram.com/api/v1/accounts/change_profile_picture/'
        with patch.object(gh, 'run_gh', return_value=Mock(returncode=0, stdout=logs)), contextlib.redirect_stdout(output):
            gh.show_run_failure('me/repo', '123')
        self.assertIn('HTTP 403', output.getvalue())
        self.assertNotIn('PRIVATE-TOKEN', output.getvalue())
