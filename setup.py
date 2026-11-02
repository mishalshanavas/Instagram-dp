"""Run with Python 3.11+ to install dependencies and launch guided setup."""
import argparse
import os
import pathlib
import subprocess
import sys
import venv
import threading
import itertools
from contextlib import contextmanager


def clear_screen():
    """Clear an interactive terminal, leaving redirected output and errors intact."""
    if not sys.stdout.isatty() or os.environ.get('TERM') == 'dumb':
        return
    if sys.platform == 'win32':
        subprocess.run(['cmd', '/c', 'cls'], check=False)
    else:
        print('\033[2J\033[H', end='', flush=True)


@contextmanager
def install_progress():
    """Indeterminate bar: pip has no reliable overall completion percentage."""
    stop = threading.Event()
    enabled = sys.stdout.isatty() and os.environ.get('TERM') != 'dumb'
    def animate():
        for position in itertools.cycle(range(18)):
            if stop.is_set():
                break
            bar = ' ' * position + '====' + ' ' * (17 - position)
            print('\r  [' + bar + '] Installing dependencies', end='', flush=True)
            if stop.wait(0.12):
                break
    worker = threading.Thread(target=animate, daemon=True)
    if enabled:
        worker.start()
    else:
        print('Installing dependencies...', flush=True)
    try:
        yield
    finally:
        stop.set()
        if enabled:
            worker.join()
            print('\r' + ' ' * 70 + '\r', end='', flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--github-only', action='store_true', help='Retry GitHub setup without another Instagram login')
    parser.add_argument('--manage', action='store_true', help='Open the photo/workflow menu instead of automatic rotation')
    args = parser.parse_args()
    if sys.version_info < (3, 11):
        raise SystemExit('Install Python 3.11 or newer from https://www.python.org/downloads/, then retry.')
    root = pathlib.Path(__file__).resolve().parent
    environment = root / '.venv'
    python = environment / ('Scripts/python.exe' if sys.platform == 'win32' else 'bin/python')
    try:
        if not python.exists():
            print('Creating a private Python environment...', flush=True)
            venv.EnvBuilder(with_pip=True).create(environment)
        try:
            with install_progress():
                subprocess.run([str(python), '-m', 'pip', 'install', '--disable-pip-version-check',
                                '-r', str(root / 'src/requirements.txt')],
                               check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as exc:
            print('Dependency installation failed. Installer details:', file=sys.stderr)
            if isinstance(exc.stdout, str):
                print(exc.stdout, file=sys.stderr)
            if isinstance(exc.stderr, str):
                print(exc.stderr, file=sys.stderr)
            raise
        print('Dependencies ready.', flush=True)
        clear_screen()
        command = [str(python), str(root / 'src/create_session.py')]
        if args.manage:
            command.append('--manage')
        if args.github_only:
            command.append('--github-only')
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as exc:
            # The wizard already explained its failure. Preserve its exit status without a second error.
            raise SystemExit(exc.returncode) from None
    except subprocess.CalledProcessError:
        raise SystemExit('Setup did not finish. Fix the error shown above and run this command again.') from None
    except (OSError, KeyboardInterrupt):
        raise SystemExit('Setup stopped. Check Python/venv is installed and this folder is writable, then retry.') from None


if __name__ == '__main__':
    main()
