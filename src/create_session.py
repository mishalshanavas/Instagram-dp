"""
Run this ONCE from your local machine / home network to create a session.
Instagram sees your home IP → trusts the login → saves the session.
GitHub Actions then reuses this session without triggering a fresh login.

Usage:
    # Option 1: Login with session ID from browser (recommended)
    python create_session.py --sessionid <sessionid>

    # Option 2: Login with username/password
    python create_session.py <username> <password>

To get your session ID:
    1. Log in to instagram.com in your browser
    2. F12 → Application → Cookies → instagram.com
    3. Copy the value of the 'sessionid' cookie
"""

import sys
from pathlib import Path
from instagrapi import Client

SESSION_FILE = Path(__file__).parent.parent / "data" / "session.json"


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python create_session.py --sessionid <sessionid>")
        print("  python create_session.py <username> <password>")
        raise SystemExit(1)

    SESSION_FILE.parent.mkdir(exist_ok=True)
    cl = Client()

    if sys.argv[1] == "--sessionid":
        if len(sys.argv) != 3:
            print("Usage: python create_session.py --sessionid <sessionid>")
            raise SystemExit(1)

        session_id = sys.argv[2]
        # URL-decode if needed
        if "%3A" in session_id:
            from urllib.parse import unquote
            session_id = unquote(session_id)

        print("=== Instagram Session Creator (via browser session) ===\n")

        # Try full login first, fall back to manual session save
        try:
            print("Logging in with session ID...")
            cl.login_by_sessionid(session_id)
        except Exception as e:
            print(f"API login failed ({e.__class__.__name__}), saving session manually...")
            # Manually build session — GitHub Actions will use it from a clean IP
            cl.set_settings({
                "authorization_data": {
                    "ds_user_id": session_id.split(":")[0],
                    "sessionid": session_id,
                },
                "cookies": {
                    "sessionid": session_id,
                    "ds_user_id": session_id.split(":")[0],
                },
                "uuids": {},
            })
            cl.dump_settings(str(SESSION_FILE))
            print(f"\nSession saved to: {SESSION_FILE}")
            print("(Session was saved without validation — GitHub Actions will validate it from a clean IP)")
            print("\n  git add data/session.json && git commit -m 'add session' && git push")
            return

    else:
        if len(sys.argv) != 3:
            print("Usage: python create_session.py <username> <password>")
            raise SystemExit(1)

        username, password = sys.argv[1], sys.argv[2]
        print(f"=== Instagram Session Creator ===")
        print(f"User: {username}\n")
        print("Logging in with credentials...")
        cl.login(username, password)

    # Validate the session
    cl.get_timeline_feed()
    print("Login successful!")

    cl.dump_settings(str(SESSION_FILE))
    print(f"\nSession saved to: {SESSION_FILE}")
    print("\nNext steps:")
    print("  git add data/session.json && git commit -m 'add session' && git push")


if __name__ == "__main__":
    main()
