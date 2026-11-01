import contextlib
import io
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import create_session
import main
import session_utils
from instagrapi.exceptions import TwoFactorRequired
from PIL import Image

SESSION = {'authorization_data': {'sessionid': 'fake-test-session', 'ds_user_id': '123'}}


class AppTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.session = self.root / 'session.json'
        self.index = self.root / 'index.txt'
        self.images = self.root / 'images'
        self.images.mkdir()
        for name in ['10.png', '2.png', '1.png']:
            Image.new('RGB', (10, 10)).save(self.images / name)
        for target, value in [('IMAGE_FOLDER', self.images), ('INDEX_FILE', self.index), ('SESSION_FILE', self.session)]:
            p = patch.object(main, target, value)
            p.start()
            self.addCleanup(p.stop)
        p = patch.dict(os.environ, {}, clear=True)
        p.start()
        self.addCleanup(p.stop)
        self.client = Mock()
        self.client.get_settings.return_value = SESSION

    def test_invalid_sessions_have_actionable_errors(self):
        for raw in ['broken', 'null', '[]', '{}', '{"cookies": []}', '{"authorization_data": "bad"}']:
            with self.subTest(raw=raw), self.assertRaisesRegex(ValueError, 'setup.py'):
                session_utils.parse_session(raw)

    def test_ci_requires_secret_even_with_local_file(self):
        self.session.write_text(json.dumps(SESSION))
        os.environ['GITHUB_ACTIONS'] = 'true'
        with self.assertRaisesRegex(SystemExit, 'Missing INSTA_SESSION'):
            main.login_user()

    def test_secret_authentication_never_uses_password(self):
        os.environ['INSTA_SESSION'] = json.dumps(SESSION)
        with patch.object(main, 'make_client', return_value=self.client):
            self.assertIs(main.login_user(), self.client)
        self.client.set_settings.assert_called_once_with(SESSION)
        self.client.account_info.assert_called_once()
        self.client.login.assert_not_called()

    def test_expired_session_does_not_leak_api_error(self):
        os.environ['INSTA_SESSION'] = json.dumps(SESSION)
        self.client.account_info.side_effect = RuntimeError('SECRET-TOKEN')
        with patch.object(main, 'make_client', return_value=self.client):
            with self.assertRaises(SystemExit) as exc:
                main.login_user()
        self.assertIn('replace the INSTA_SESSION', str(exc.exception))
        self.assertNotIn('SECRET-TOKEN', str(exc.exception))

    def test_local_session_supported(self):
        self.session.write_text(json.dumps(SESSION))
        with patch.object(main, 'make_client', return_value=self.client):
            main.login_user()
        self.client.account_info.assert_called_once()

    def test_invalid_local_json(self):
        self.session.write_text('invalid')
        with self.assertRaisesRegex(SystemExit, 'not valid JSON'):
            main.login_user()

    def test_check_does_not_mutate(self):
        self.index.write_text('1')
        with patch.object(main, 'login_user', return_value=self.client):
            main.main(['--check'])
        self.client.account_change_picture.assert_not_called()
        self.assertEqual(self.index.read_text(), '1')
        self.assertFalse(self.session.exists())

    def test_rotation_wraps_and_ci_does_not_save_session(self):
        self.index.write_text('2')
        os.environ['GITHUB_ACTIONS'] = 'true'
        with patch.object(main, 'login_user', return_value=self.client):
            main.main([])
        self.client.account_change_picture.assert_called_once_with(str(self.images / '10.png'))
        self.assertEqual(self.index.read_text(), '0')
        self.assertFalse(self.session.exists())

    def test_failed_update_preserves_position(self):
        self.index.write_text('1')
        for outcome in [False, RuntimeError('private error')]:
            self.client.account_change_picture.side_effect = outcome if isinstance(outcome, Exception) else None
            self.client.account_change_picture.return_value = False
            with patch.object(main, 'login_user', return_value=self.client):
                with self.assertRaisesRegex(SystemExit, 'not confirmed|did not confirm'):
                    main.main([])
            self.assertEqual(self.index.read_text(), '1')

    def test_bad_image_fails_before_login(self):
        (self.images / 'bad.png').write_text('not an image')
        with patch.object(main, 'login_user') as login:
            with self.assertRaisesRegex(SystemExit, 'Cannot read image'):
                main.main(['--check'])
        login.assert_not_called()

    def test_missing_and_empty_image_folder(self):
        for image in self.images.iterdir():
            image.unlink()
        with self.assertRaisesRegex(SystemExit, 'No pictures'):
            main.main([])
        self.images.rmdir()
        with self.assertRaisesRegex(SystemExit, 'Missing assets/images'):
            main.main([])

    def test_sort_and_index_recovery(self):
        self.assertEqual(main.get_images(), ['1.png', '2.png', '10.png'])
        for value in ['', 'abc', '-1']:
            self.index.write_text(value)
            self.assertEqual(main.read_index(), 0)
        self.index.unlink()
        self.assertEqual(main.read_index(), 0)

    def test_session_save_is_private_and_validated(self):
        session_utils.save_session(self.client, self.session)
        self.assertEqual(json.loads(self.session.read_text()), SESSION)
        if os.name == 'posix':
            self.assertEqual(stat.S_IMODE(self.session.stat().st_mode), 0o600)
        self.client.get_settings.return_value = {}
        with self.assertRaises(ValueError):
            session_utils.save_session(self.client, self.session)
        self.assertEqual(json.loads(self.session.read_text()), SESSION)

    def test_password_and_two_factor_flow(self):
        self.client.login.side_effect = [TwoFactorRequired(), True]
        with patch('builtins.input', side_effect=['1', 'tester']), patch('getpass.getpass', side_effect=['password', '123456']):
            create_session.authenticate(self.client)
        self.assertEqual(self.client.login.call_args.kwargs, {'verification_code': '123456'})
        self.client.account_info.assert_called_once()

    def test_browser_cookie_is_decoded_and_validated(self):
        with patch('builtins.input', return_value='2'), patch('getpass.getpass', return_value='123%3Atest'):
            create_session.authenticate(self.client)
        self.client.login_by_sessionid.assert_called_once_with('123:test')
        self.client.account_info.assert_called_once()

    def test_failed_setup_preserves_previous_session(self):
        self.session.write_text('previous-session')
        self.client.account_info.side_effect = RuntimeError('SECRET-TOKEN')
        with patch.object(create_session, 'SESSION_FILE', self.session), patch.object(create_session, 'make_client', return_value=self.client), patch('builtins.input', side_effect=['1', 'tester']), patch('getpass.getpass', return_value='password'), contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit) as exc:
                create_session.main([])
        self.assertNotIn('SECRET-TOKEN', str(exc.exception))
        self.assertEqual(self.session.read_text(), 'previous-session')



if __name__ == '__main__':
    unittest.main()
