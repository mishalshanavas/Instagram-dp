import os
import logging
from pathlib import Path
from instagrapi import Client
from instagrapi.exceptions import LoginRequired

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

REPO_ROOT = Path(__file__).parent.parent
IMAGE_FOLDER = REPO_ROOT / "assets" / "images"
DATA_FOLDER = REPO_ROOT / "data"
INDEX_FILE = DATA_FOLDER / "index.txt"
SESSION_FILE = DATA_FOLDER / "session.json"

# Instagram v410 user-agent — required since Feb 2026 (#2369)
# Old versions get "unsupported_version" / checkpoint_required
USER_AGENT = (
    "Instagram 410.0.0.0.96 Android (33/13; 480dpi; 1080x2400; "
    "xiaomi; M2007J20CG; surya; qcom; en_US; 641123490)"
)


def _make_client() -> Client:
    """Create a Client with best-practice settings."""
    cl = Client()
    cl.set_user_agent(USER_AGENT)
    cl.delay_range = [1, 3]  # mimic human pacing between API calls
    return cl


def login_user() -> Client:
    """
    Best-practice login flow from instagrapi docs:
    1. Load saved session → set_settings → login (reuses session, no fresh auth)
    2. Validate with get_timeline_feed()
    3. If session expired: preserve device UUIDs, re-login with credentials
    4. If no session at all: full credential login
    """
    cl = _make_client()

    session = None
    if SESSION_FILE.exists():
        session = cl.load_settings(str(SESSION_FILE))

    login_via_session = False
    login_via_pw = False

    if session:
        try:
            cl.set_settings(session)
            cl.set_user_agent(USER_AGENT)  # re-apply after set_settings
            cl.login(USERNAME, PASSWORD)   # reuses session — no actual HTTP login

            # validate session is alive
            try:
                cl.get_timeline_feed()
            except LoginRequired:
                logger.warning("Session expired — re-logging with same device UUIDs")
                old_session = cl.get_settings()

                # preserve device fingerprint across logins (anti-detection)
                cl.set_settings({})
                cl.set_uuids(old_session["uuids"])
                cl.set_user_agent(USER_AGENT)

                cl.login(USERNAME, PASSWORD)

            login_via_session = True
        except Exception as e:
            logger.warning(f"Session login failed: {e}")

    if not login_via_session:
        try:
            if not USERNAME or not PASSWORD:
                raise SystemExit(
                    "No valid session and no credentials — "
                    "run create_session.py locally first"
                )
            logger.info("Logging in with credentials (no session)...")
            if cl.login(USERNAME, PASSWORD):
                login_via_pw = True
        except SystemExit:
            raise
        except Exception as e:
            logger.error(f"Credential login failed: {e}")

    if not login_via_session and not login_via_pw:
        raise SystemExit("Could not login via session or credentials")

    logger.info("Logged in successfully")
    return cl


def get_images() -> list[str]:
    """Return sorted list of image filenames in assets/images/."""
    exts = {".png", ".jpg", ".jpeg"}
    images = [f.name for f in IMAGE_FOLDER.iterdir()
              if f.is_file() and f.suffix.lower() in exts]

    try:
        images.sort(key=lambda x: int(x.split(".")[0]))
    except ValueError:
        images.sort()

    return images


def read_index() -> int:
    try:
        return int(INDEX_FILE.read_text().strip())
    except (FileNotFoundError, ValueError):
        return 0


def write_index(index: int) -> None:
    INDEX_FILE.write_text(str(index))


def main():
    DATA_FOLDER.mkdir(exist_ok=True)

    images = get_images()
    if not images:
        raise SystemExit(f"No images found in {IMAGE_FOLDER}")

    index = read_index() % len(images)
    image_path = IMAGE_FOLDER / images[index]

    logger.info(f"Changing DP to {images[index]} ({index + 1}/{len(images)})")

    client = login_user()
    client.account_change_picture(str(image_path))

    # Re-save session to keep it fresh for next run
    client.dump_settings(str(SESSION_FILE))

    next_index = (index + 1) % len(images)
    write_index(next_index)

    logger.info(f"Done — next run will use {images[next_index]}")


if __name__ == "__main__":
    main()