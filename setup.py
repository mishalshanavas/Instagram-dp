"""Run with Python 3.11+ to install dependencies and launch guided setup."""
import argparse
import os
import pathlib
import subprocess
import sys
import venv


def clear_screen():
    """Clear an interactive terminal, leaving redirected output and errors intact."""
    if not sys.stdout.isatty() or os.environ.get('TERM') == 'dumb':
        return
    if sys.platform == 'win32':
        subprocess.run(['cmd', '/c', 'cls'], check=False)
    else:
        print('\033[2J\033[H', end='', flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--github-only', action='store_true', help='Retry GitHub setup without another Instagram login')
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
        print('Installing required packages...', flush=True)
        subprocess.run([str(python), '-m', 'pip', 'install', '-r', str(root / 'src/requirements.txt')], check=True)
        clear_screen()
        command = [str(python), str(root / 'src/create_session.py')]
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
