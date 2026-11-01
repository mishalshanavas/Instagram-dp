import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import Mock, patch

spec = importlib.util.spec_from_file_location('setup_launcher', Path(__file__).resolve().parents[1] / 'setup.py')
launcher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(launcher)


class LauncherTests(unittest.TestCase):
    def setUp(self):
        terminal = patch.object(launcher.sys.stdout, 'isatty', return_value=False)
        terminal.start()
        self.addCleanup(terminal.stop)
        p = patch.object(launcher.sys, 'argv', ['setup.py'])
        p.start()
        self.addCleanup(p.stop)

    def test_creates_environment_installs_then_launches(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            with patch.object(launcher, '__file__', str(root / 'setup.py')), patch.object(launcher.venv, 'EnvBuilder') as builder, patch.object(launcher.subprocess, 'run') as run:
                launcher.main()
            builder.return_value.create.assert_called_once_with(root / '.venv')
            self.assertEqual(len(run.call_args_list), 2)
            self.assertIn('pip', run.call_args_list[0].args[0])
            self.assertEqual(run.call_args_list[1].args[0][-1], str(root / 'src/create_session.py'))

    def test_install_failure_does_not_launch_wizard(self):
        with patch.object(launcher.venv, 'EnvBuilder'), patch.object(launcher.subprocess, 'run', side_effect=subprocess.CalledProcessError(1, 'pip')) as run:
            with self.assertRaisesRegex(SystemExit, 'Setup did not finish'):
                launcher.main()
        self.assertEqual(run.call_count, 1)

    def test_old_python_has_clear_message(self):
        with patch.object(launcher.sys, 'version_info', (3, 10)):
            with self.assertRaisesRegex(SystemExit, 'Python 3.11'):
                launcher.main()

    def test_wizard_failure_preserves_exit_code_without_duplicate_message(self):
        with patch.object(launcher.venv, 'EnvBuilder'), patch.object(launcher.subprocess, 'run', side_effect=[Mock(), subprocess.CalledProcessError(1, 'wizard')]):
            with self.assertRaises(SystemExit) as caught:
                launcher.main()
        self.assertEqual(caught.exception.code, 1)

    def test_clear_only_after_successful_install(self):
        with patch.object(launcher.venv, 'EnvBuilder'), patch.object(launcher.subprocess, 'run', side_effect=subprocess.CalledProcessError(1, 'pip')), patch.object(launcher, 'clear_screen') as clear:
            with self.assertRaises(SystemExit):
                launcher.main()
        clear.assert_not_called()

    def test_redirected_output_not_cleared(self):
        with patch.object(launcher.subprocess, 'run') as run:
            launcher.clear_screen()
        run.assert_not_called()

    def test_windows_terminal_clear(self):
        with patch.object(launcher.sys.stdout, 'isatty', return_value=True), patch.object(launcher.sys, 'platform', 'win32'), patch.dict(launcher.os.environ, {'TERM': 'xterm'}), patch.object(launcher.subprocess, 'run') as run:
            launcher.clear_screen()
        run.assert_called_once_with(['cmd', '/c', 'cls'], check=False)

    def test_posix_terminal_clear(self):
        with patch.object(launcher.sys.stdout, 'isatty', return_value=True), patch.object(launcher.sys, 'platform', 'linux'), patch.dict(launcher.os.environ, {'TERM': 'xterm'}), patch('builtins.print') as output:
            launcher.clear_screen()
        output.assert_called_once_with('\033[2J\033[H', end='', flush=True)
