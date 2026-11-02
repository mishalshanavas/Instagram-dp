import contextlib
from datetime import datetime, timezone
import io
from pathlib import Path
import sys
import unittest
from unittest.mock import Mock, patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import timezone_setup as tz
import github_setup as gh


class TimezoneTests(unittest.TestCase):
    def test_india_half_hour_offset_and_hourly_check(self):
        timestamp = int(datetime(2026, 11, 2, 11, 0, 2, tzinfo=timezone.utc).timestamp())
        result = tz.format_schedule(timestamp, 'Asia/Kolkata')
        self.assertIn('04:30 PM', result)
        self.assertIn('04:47 PM', result)
        self.assertIn('+0530', result)

    def test_daylight_saving_is_date_sensitive(self):
        summer = datetime(2026, 7, 1, 12, tzinfo=timezone.utc).timestamp()
        winter = datetime(2026, 12, 1, 12, tzinfo=timezone.utc).timestamp()
        self.assertIn('-0400', tz.format_schedule(summer, 'America/New_York'))
        self.assertIn('-0500', tz.format_schedule(winter, 'America/New_York'))

    def test_invalid_zone_falls_back_to_utc(self):
        self.assertFalse(tz.valid_timezone('invalid/zone'))
        self.assertIn('[UTC]', tz.format_schedule(0, 'invalid/zone'))

    def test_custom_zone_validated_before_saving(self):
        with patch('terminal_ui.choose', side_effect=['custom', 'Asia/Kolkata']), patch('terminal_ui.prompt', return_value='invalid'), patch.object(gh, 'run_gh', side_effect=[Mock(returncode=1), Mock(returncode=0)]) as run, contextlib.redirect_stdout(io.StringIO()):
            self.assertTrue(tz.configure_timezone('me/repo'))
        self.assertEqual(run.call_args.args[0][-2:], ['--body', 'Asia/Kolkata'])
