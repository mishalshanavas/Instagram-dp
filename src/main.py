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


def login_user() -> Client:
    """Reuse the local session if valid; only fall back to password login."""
    cl = Client()

    # Try saved session first (created from your home IP)
    if SESSION_FILE.exists():
        logger.info("Loading saved session...")
        cl.load_settings(str(SESSION_FILE))
        try:
            cl.get_timeline_feed()  # test if session is still alive
            logger.info("Session is valid — no fresh login needed")
            return cl
        except LoginRequired:
            logger.warning("Saved session expired")
        except Exception as e:
            logger.warning(f"Session check failed: {e}")

    # Fallback: full login (will use cloud IP — may trigger verification)
    logger.info("Logging in with credentials...")
    if not USERNAME or not PASSWORD:
        raise SystemExit("No valid session and no credentials — run create_session.py locally first")
    cl = Client()
    cl.login(USERNAME, PASSWORD)
    cl.dump_settings(str(SESSION_FILE))
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