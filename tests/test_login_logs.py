import contextlib
import io
import logging
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from terminal_ui import login_logs


class LoginLogsTests(unittest.TestCase):
    def test_safe_metadata_only_and_logger_restored(self):
        logger = logging.getLogger('instagrapi')
        before = logger.handlers[:], logger.level, logger.propagate
        output = io.StringIO()
        with contextlib.redirect_stdout(output), login_logs():
            logger.info('PRIVATE_USERNAME [403] POST https://i.instagram.com/api/v1/accounts/login/?token=SECRET_TOKEN')
            logger.info('password=SECRET_PASSWORD cookies=SECRET_COOKIE')
        self.assertIn('Login: POST · HTTP 403', output.getvalue())
        self.assertNotIn('PRIVATE_USERNAME', output.getvalue())
        self.assertNotIn('SECRET', output.getvalue())
        self.assertEqual(before, (logger.handlers, logger.level, logger.propagate))

    def test_logger_restored_after_error(self):
        logger = logging.getLogger('instagrapi')
        before = logger.handlers[:], logger.level, logger.propagate
        with self.assertRaises(RuntimeError), login_logs():
            raise RuntimeError('failed')
        self.assertEqual(before, (logger.handlers, logger.level, logger.propagate))
