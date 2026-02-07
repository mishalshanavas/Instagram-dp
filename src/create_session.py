"""
SIMPLE SESSION GENERATOR

This creates a session WITHOUT instagrapi (since it requires old Python).
Creates a base64 string to paste into GitHub Secrets that contains your 
Instagram username and password.

The main script will use this to login directly with instagrapi on GitHub Actions.

Usage:
    python create_session.py
"""

import base64
import json
import getpass
import os


def main():
    print("=" * 50)
    print("Instagram Session Generator (Simple)")
    print("=" * 50)
    print()
    print("This creates a session secret for GitHub Actions.")
    print("Your credentials are base64-encoded (NOT encrypted).")
    print()

    # Check for environment variables first
    username = os.getenv("INSTA_USER")
    password = os.getenv("INSTA_PASS")
    
    # If not found in env vars, prompt interactively
    if not username:
        username = input("Instagram username: ").strip()
    if not password:
        password = getpass.getpass("Instagram password: ")

    if not username or not password:
        print("Username and password are required.")
        return

    # Create a minimal session data structure
    session_data = {
        "username": username,
        "password": password,
        "created_at": "local_machine"
    }

    session_json = json.dumps(session_data)
    session_b64 = base64.b64encode(session_json.encode()).decode()

    print()
    print("=" * 50)
    print("Copy the value below and add it as a GitHub Secret:")
    print()
    print("  Secret name:  INSTA_SESSION")
    print("  Secret value: (below)")
    print("=" * 50)
    print()
    print(session_b64)
    print()
    print("=" * 50)
    print("Go to: Settings → Secrets → Actions → New secret")
    print("Name:  INSTA_SESSION")
    print("Value: paste the base64 string above")
    print("=" * 50)
    print()
    print("Note: This just encodes your username/password.")
    print("The main script will use instagrapi to login properly.")


if __name__ == "__main__":
    main()
