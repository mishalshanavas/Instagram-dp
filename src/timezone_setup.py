"""Timezone selection and schedule display. Scheduling remains epoch-based."""
import os
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def valid_timezone(name):
    try:
        ZoneInfo(name)
        return True
    except (ZoneInfoNotFoundError, ValueError):
        return False


def format_schedule(timestamp, name):
    if not valid_timezone(name):
        name = 'UTC'
    due = datetime.fromtimestamp(timestamp, timezone.utc)
    check = due.replace(minute=17, second=0, microsecond=0)
    if check < due:
        from datetime import timedelta
        check += timedelta(hours=1)
    zone = ZoneInfo(name)
    display = '%d %b %Y, %I:%M %p %Z (UTC%z)'
    return (f'Next rotation due: {due.astimezone(zone).strftime(display)} [{name}]\n'
            f'First hourly check after due time: {check.astimezone(zone).strftime(display)}\n'
            'GitHub may delay scheduled runs.')


def configure_timezone(repo):
    from github_setup import run_gh
    from terminal_ui import choose, prompt
    options = [('UTC', 'UTC'), ('Asia/Kolkata', 'India — Asia/Kolkata'),
               ('America/New_York', 'US Eastern — America/New_York'),
               ('America/Los_Angeles', 'US Pacific — America/Los_Angeles'),
               ('Europe/London', 'United Kingdom — Europe/London'),
               ('Europe/Berlin', 'Central Europe — Europe/Berlin'),
               ('Asia/Dubai', 'UAE — Asia/Dubai'), ('Asia/Singapore', 'Singapore'),
               ('Australia/Sydney', 'Australia — Australia/Sydney'), ('custom', 'Another timezone')]
    stored = run_gh(['variable', 'get', 'TIMEZONE', '--repo', 'github.com/' + repo], capture_output=True, text=True)
    current = stored.stdout.strip() if stored.returncode == 0 and isinstance(stored.stdout, str) else 'UTC'
    if not valid_timezone(current):
        current = 'UTC'
    if current not in dict(options):
        options.insert(0, (current, current + ' (saved)'))
    while True:
        selected = choose('Timezone for rotation times', options, current, f'Timezone [{current}]: ')
        if selected == 'custom':
            selected = prompt('Timezone name, e.g. Asia/Kolkata: ').strip()
        if valid_timezone(selected):
            break
        print('Unknown timezone. Use an IANA name such as Asia/Kolkata or Europe/London.')
    saved = run_gh(['variable', 'set', 'TIMEZONE', '--repo', 'github.com/' + repo, '--body', selected], capture_output=True)
    if saved.returncode:
        print('Could not save timezone. Check repository permissions before continuing.')
        return False
    print(f'Times will use {selected}; daylight-saving changes are handled automatically.')
    return True


def show_remote_schedule(repo):
    import base64
    from github_setup import api_json, run_gh
    try:
        variable = run_gh(['variable', 'get', 'TIMEZONE', '--repo', 'github.com/' + repo], capture_output=True, text=True)
        name = variable.stdout.strip() if variable.returncode == 0 else 'UTC'
        content = api_json(f'repos/{repo}/contents/data/next_run.txt')['content']
        timestamp = int(base64.b64decode(content).decode().strip())
        print(format_schedule(timestamp, name))
    except (ValueError, KeyError, TypeError, OSError):
        print('Schedule details are not available yet; see the workflow summary.')


def write_summary():
    path = Path('data/next_run.txt')
    if not path.exists():
        return
    try:
        text = format_schedule(int(path.read_text().strip()), os.getenv('TIMEZONE', 'UTC'))
    except (ValueError, OverflowError, OSError):
        return
    print(text)
    summary = os.getenv('GITHUB_STEP_SUMMARY')
    if summary:
        with open(summary, 'a') as output:
            output.write('\n' + text.replace('\n', '  \n') + '\n')


if __name__ == '__main__':
    write_summary()
