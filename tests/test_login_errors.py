import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import create_session as wizard
from instagrapi.exceptions import ClientThrottledError, PleaseWaitFewMinutes, BadPassword, ChallengeRequired


class LoginErrorTests(unittest.TestCase):
    def test_rate_limit_stops_without_retry_or_cookie_fallback(self):
        for error in (ClientThrottledError(), PleaseWaitFewMinutes()):
            client = Mock()
            client.login.side_effect = error
            with patch('builtins.input', side_effect=['1', 'tester']), patch('getpass.getpass', return_value='private'), contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaisesRegex(wizard.SetupError, 'HTTP 429'):
                    wizard.authenticate(client)
            client.login.assert_called_once()
            client.login_by_sessionid.assert_not_called()
            client.account_info.assert_not_called()
            client.set_retry_config.assert_called_once_with(session_retry_total=0, public_request_retries_count=0)

    def test_wrapped_http_429_is_detected_without_printing_response(self):
        error = RuntimeError('PRIVATE RESPONSE')
        error.response = Mock(status_code=429)
        client = Mock()
        client.login_by_sessionid.side_effect = error
        with patch('builtins.input', return_value='2'), patch('getpass.getpass', return_value='123:secret'), contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(wizard.SetupError) as caught:
                wizard.authenticate(client)
        self.assertIn('HTTP 429', str(caught.exception))
        self.assertNotIn('PRIVATE RESPONSE', str(caught.exception))

    def test_validation_throttle_never_saves_session(self):
        client = Mock()
        client.account_info.side_effect = ClientThrottledError()
        with patch.object(wizard, 'make_client', return_value=client), patch.object(wizard, 'save_session') as save, patch('builtins.input', side_effect=['1', 'tester']), patch('getpass.getpass', return_value='private'), contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(SystemExit, 'HTTP 429'):
                wizard.main([])
        save.assert_not_called()

    def test_saved_session_disables_restored_retries_and_avoids_login(self):
        with tempfile.TemporaryDirectory() as folder:
            session = Path(folder) / 'session.json'
            session.write_text(json.dumps({'authorization_data': {'sessionid': 'fake'}, 'session_retry_total': 5}))
            client = Mock()
            with patch.object(wizard, 'SESSION_FILE', session), patch('builtins.input', return_value='3'), contextlib.redirect_stdout(io.StringIO()):
                wizard.authenticate(client)
            client.set_settings.assert_called_once()
            self.assertEqual(client.set_retry_config.call_count, 2)
            client.login.assert_not_called()
            client.account_info.assert_called_once()

    def test_menu_is_vertical_and_exit_makes_no_login(self):
        output = io.StringIO()
        client = Mock()
        with patch('builtins.input', return_value='0'), contextlib.redirect_stdout(output):
            with self.assertRaises(SystemExit) as caught:
                wizard.authenticate(client)
        self.assertEqual(caught.exception.code, 0)
        self.assertIn('  1. Username and password\n  2. Browser session\n  3.', output.getvalue())
        client.login.assert_not_called()

    def test_specific_auth_errors(self):
        for error, expected in [(BadPassword(), 'rejected the login'), (ChallengeRequired(), 'requires verification')]:
            client = Mock()
            client.login.side_effect = error
            with patch('builtins.input', side_effect=['1', 'tester']), patch('getpass.getpass', return_value='private'), contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaisesRegex(wizard.SetupError, expected):
                    wizard.authenticate(client)
