"""
Run this ONCE from your local machine / home network to create a session.
Instagram sees your home IP → trusts the login → saves the session.
GitHub Actions then reuses this session without triggering a fresh login.

Usage:
    cd src
    pip install instagrapi
    python create_session.py
"""

import getpass
from pathlib import Path
from instagrapi import Client

SESSION_FILE = Path(__file__).parent.parent / "data" / "session.json"


def main():
    print("=== Instagram Session Creator ===\n")
    print("This logs in from YOUR network so Instagram trusts the session.")
    print("The saved session.json will be reused by GitHub Actions.\n")

    username = input("Instagram username: ").strip()
    password = getpass.getpass("Instagram password: ")

    if not username or not password:
        raise SystemExit("Username and password are required.")

    SESSION_FILE.parent.mkdir(exist_ok=True)

    cl = Client()

    # If an old session exists, try to reuse it first
    if SESSION_FILE.exists():
        print("\nFound existing session, validating...")
        cl.load_settings(str(SESSION_FILE))
        cl.login(username, password)
        try:
            cl.get_timeline_feed()
            print("Existing session is still valid!")
            cl.dump_settings(str(SESSION_FILE))
            print(f"\nSession saved to: {SESSION_FILE}")
            return
        except Exception:
            print("Session expired, creating a fresh one...")
            cl = Client()

    # Fresh login from local network
    print("\nLogging in (this creates a trusted session from your IP)...")
    cl.login(username, password)
    cl.get_timeline_feed()  # validate
    cl.dump_settings(str(SESSION_FILE))

    print(f"\nSession saved to: {SESSION_FILE}")
    print("\nNext steps:")
    print("  1. git add data/session.json")
    print("  2. git commit -m 'add session'")
    print("  3. git push")
    print("\nGitHub Actions will now reuse this session instead of logging in fresh.")


if __name__ == "__main__":
    main()
