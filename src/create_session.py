"""Interactive setup; credentials are prompted for, never passed on the command line."""
from terminal_ui import prompt as input, choose, step, secret, login_logs, clear_login_screen
import argparse
from urllib.parse import unquote

from instagrapi.exceptions import (
    TwoFactorRequired, ClientThrottledError, PleaseWaitFewMinutes,
    BadPassword, ChallengeRequired, LoginRequired,
)
from session_utils import SESSION_FILE, make_client, parse_session, save_session


class SetupError(Exception):
    """A safe, user-facing setup error."""


def verification_code(*_args, **_kwargs):
    return secret('Instagram verification code').strip()


RATE_LIMIT_MESSAGE = (
    'Instagram temporarily blocked this request (HTTP 429 / rate limit).\n'
    'This does not prove your password is wrong. No automatic retry was made.\n'
    'Stop login attempts for now; check Instagram for any verification prompts.\n'
    'Wait before trying again on your usual network. Instagram does not provide a guaranteed cooldown.\n'
    'After the restriction clears, you can try option 3 with a trusted saved session, or option 2 '    'with a browser session. Neither bypasses a rate limit.\n'
    'Your previous saved session has not been overwritten.'
)


def disable_login_retries(client):
    # Loaded settings can restore retry values, so also apply this after set_settings.
    client.set_retry_config(session_retry_total=0, public_request_retries_count=0)


def authenticate(client):
    disable_login_retries(client)
    try:
        with login_logs():
            _authenticate(client)
    except (ClientThrottledError, PleaseWaitFewMinutes):
        raise SetupError(RATE_LIMIT_MESSAGE) from None
    except BadPassword:
        raise SetupError('Instagram rejected the login. Verify your details in the official app. '
                         'A correct password can also be rejected because of login/network restrictions. '
                         'Do not repeatedly retry.') from None
    except ChallengeRequired:
        raise SetupError('Instagram requires verification. Complete the prompt in the official app, '
                         'then retry setup. No new session was saved.') from None
    except LoginRequired:
        raise SetupError('Instagram rejected or expired this session. Resolve any prompts in the app, '
                         'then create a new session. No new session was saved.') from None
    except Exception as exc:
        response = getattr(exc, 'response', None)
        if getattr(response, 'status_code', None) == 429:
            raise SetupError(RATE_LIMIT_MESSAGE) from None
        raise


def _authenticate(client):
    client.challenge_code_handler = verification_code
    choice = choose('Choose a login method:', [
        ('1', 'Username and password'), ('2', 'Browser session'),
        ('3', 'Reuse a trusted local session (no password login)'), ('0', 'Exit')],
        '1', 'Enter a number [1]: ')
    if choice == '0':
        raise SystemExit(0)
    if choice == '1':
        username = input('Instagram username: ').strip()
        password = secret('Instagram password')
        if not username or not password:
            raise SetupError('Username and password are required.')
        try:
            logged_in = client.login(username, password)
        except TwoFactorRequired:
            logged_in = client.login(username, password, verification_code=verification_code())
        if not logged_in:
            raise SetupError('Instagram did not confirm the login.')
    elif choice == '2':
        print('Browser sessions may pass login checks but fail profile changes. Password login is preferred for automation.')
        print('In your browser: instagram.com → developer tools → Application/Storage → Cookies → sessionid.')
        token = unquote(secret('Paste sessionid').strip())
        if not token:
            raise SetupError('A session ID is required.')
        client.login_by_sessionid(token)
    elif choice == '3':
        try:
            settings = parse_session(SESSION_FILE.read_text())
        except (OSError, ValueError):
            raise SetupError('No usable local session. Choose option 1 or 2 on your next setup attempt.') from None
        print('Use this only for a session you trust. Revoke sessions exposed in Git history.')
        client.set_settings(settings)
        disable_login_retries(client)
    else:
        raise SetupError('Choose 0, 1, 2, or 3, then run setup again.')
    client.account_info()


def configure_github():
    from github_setup import configure_github as configure
    configure(SESSION_FILE)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--github-only', action='store_true', help='Retry GitHub setup using the existing local session')
    args = parser.parse_args(argv)
    if args.github_only:
        try:
            parse_session(SESSION_FILE.read_text())
        except (OSError, ValueError):
            raise SystemExit('No usable local session. Run python setup.py without --github-only first.') from None
        try:
            configure_github()
        except (KeyboardInterrupt, EOFError):
            raise SystemExit('GitHub setup cancelled; your local session is saved.') from None
        return
    from terminal_ui import banner
    banner()
    step('1 / 3', 'Instagram')
    try:
        client = make_client()
        authenticate(client)
        save_session(client, SESSION_FILE)
        clear_login_screen()
        print('Login validated. Your private session is saved locally.')
        configure_github()
    except (KeyboardInterrupt, EOFError):
        raise SystemExit('\nSetup cancelled.') from None
    except SetupError as exc:
        raise SystemExit(str(exc)) from None
    except Exception:
        raise SystemExit('Setup failed. Check your network and login details; open Instagram to resolve '
                         'any verification prompts, then retry. No unvalidated session was saved.') from None


if __name__ == '__main__':
    main()
