"""Shared session handling. Never log credentials or raw API errors."""
import json
import os
from pathlib import Path

from instagrapi import Client

ROOT = Path(__file__).resolve().parent.parent
SESSION_FILE = ROOT / 'data' / 'session.json'
RECOVERY = 'Run python setup.py locally, then replace the INSTA_SESSION repository secret.'


def make_client():
    client = Client()
    client.delay_range = [1, 3]
    proxy = os.getenv('PROXY_URL', '').strip()
    if proxy:
        client.set_proxy(proxy)
    return client


def parse_session(raw):
    try:
        settings = json.loads(raw)
    except (ValueError, TypeError):
        raise ValueError('Session is not valid JSON. ' + RECOVERY) from None
    if not isinstance(settings, dict):
        raise ValueError('Session must be a JSON object. ' + RECOVERY)
    auth = settings.get('authorization_data') or {}
    cookies = settings.get('cookies') or {}
    if not isinstance(auth, dict) or not isinstance(cookies, dict) or not (
        auth.get('sessionid') or cookies.get('sessionid')
    ):
        raise ValueError('Session has no login token. ' + RECOVERY)
    return settings


def save_session(client, path=SESSION_FILE):
    """Save validated settings atomically, with owner-only access on POSIX."""
    payload = json.dumps(client.get_settings(), indent=2)
    parse_session(payload)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix('.json.tmp')
    fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    try:
        with os.fdopen(fd, 'w') as stream:
            stream.write(payload)
        temporary.chmod(0o600)
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)
