"""Small terminal UI with accessible plain-text fallback."""
import builtins
import os
import sys


def interactive():
    return sys.stdin.isatty() and sys.stdout.isatty() and os.getenv('TERM') != 'dumb' and not os.getenv('DP_PLAIN')


def style():
    import questionary
    return questionary.Style([
        ('qmark', 'fg:#5fd7d7 bold'), ('question', 'bold'),
        ('answer', 'fg:#5fd7d7'), ('pointer', 'fg:#5fd7d7 bold'),
        ('highlighted', 'fg:#5fd7d7 bold'), ('instruction', 'fg:#808080'),
    ])


def choose(title, options, default, fallback_prompt):
    """Options are stable values and human-readable labels."""
    if not interactive():
        print(title + '\n')
        for value, label in options:
            print(f'  {value}. {label}')
        print()
        return builtins.input(fallback_prompt).strip() or default
    import questionary
    answer = questionary.select(title, choices=[questionary.Choice(label, value=value) for value, label in options],
                                default=default, style=style(), qmark='›', pointer='❯',
                                instruction='↑/↓ move · Enter select · Ctrl+C cancel').unsafe_ask()
    if answer is None:
        raise KeyboardInterrupt
    return answer


def prompt(message):
    if not interactive():
        return builtins.input(message)
    import questionary
    if '[Y/n]' in message or '[y/N]' in message:
        default = '[Y/n]' in message
        label = message.replace('[Y/n]', '').replace('[y/N]', '').strip(' :')
        value = questionary.confirm(label, default=default, style=style(), qmark='›').unsafe_ask()
        if value is None:
            raise KeyboardInterrupt
        return 'y' if value else 'n'
    value = questionary.text(message.rstrip(' :'), style=style(), qmark='›').unsafe_ask()
    if value is None:
        raise KeyboardInterrupt
    return value


def banner():
    if not interactive():
        print('\nInstagram DP setup — your password stays on this computer.\n')
        return
    from rich.console import Console
    from rich.panel import Panel
    Console().print(Panel('[bold]Instagram DP[/bold]  [dim] / setup[/dim]\n\n'
                          'Connect Instagram → Choose a repository → Add photos → Run\n'
                          '[dim]Your password stays on this computer. Ctrl+C to exit.[/dim]',
                          border_style='cyan', padding=(1, 2), expand=False))


def step(number, label):
    if interactive():
        from rich.console import Console
        Console().rule(f'[cyan]{number}[/cyan] · {label}', align='left')


def secret(message):
    """Show asterisks in interactive terminals; retain secure no-echo fallback."""
    if not interactive():
        import getpass
        return getpass.getpass(message + ' (hidden): ')
    import questionary
    value = questionary.password(message, style=style(), qmark='›').unsafe_ask()
    if value is None:
        raise KeyboardInterrupt
    return value


def clear_login_screen():
    if interactive():
        from rich.console import Console
        Console().clear()
        banner()


from contextlib import contextmanager


@contextmanager
def login_logs():
    """Display only allowlisted request metadata, never raw library log text."""
    import logging
    import re
    class SafeHandler(logging.Handler):
        def emit(self, record):
            message = record.getMessage()
            response = re.search(r'\[(\d{3})\]\s+(GET|POST|PUT|DELETE)', message)
            endpoint = re.search(r'https://[^\s]+', message)
            if not endpoint:
                return
            url = endpoint.group()
            if 'instagram.com' not in url:
                return
            stage = 'Instagram request'
            for token, label in [('current_user', 'Validate session'), ('login', 'Login'),
                                 ('challenge', 'Verification'), ('two_factor', 'Two-factor verification'),
                                 ('bloks', 'Authentication flow')]:
                if token in url:
                    stage = label
                    break
            detail = f'{response.group(2)} · HTTP {response.group(1)}' if response else 'Sending request'
            print(f'  {stage}: {detail}', flush=True)
    logger = logging.getLogger('instagrapi')
    previous = logger.handlers[:], logger.level, logger.propagate
    logger.handlers = [SafeHandler()]
    logger.setLevel(logging.INFO)
    logger.propagate = False
    try:
        yield
    finally:
        logger.handlers, logger.level, logger.propagate = previous
