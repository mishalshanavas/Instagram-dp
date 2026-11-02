"""Rotate the profile picture using a previously validated session."""
import argparse
import logging
import os
from pathlib import Path

from failure_help import instagram_failure
from session_utils import RECOVERY, SESSION_FILE, make_client, parse_session, save_session

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)
ROOT = Path(__file__).resolve().parent.parent
IMAGE_FOLDER = ROOT / 'assets' / 'images'
INDEX_FILE = ROOT / 'data' / 'index.txt'


def login_user():
    raw = os.getenv('INSTA_SESSION')
    if not raw:
        # CI must never silently pick up an old tracked credential.
        if os.getenv('GITHUB_ACTIONS') == 'true' or not SESSION_FILE.exists():
            raise SystemExit('Missing INSTA_SESSION. ' + RECOVERY)
        raw = SESSION_FILE.read_text()
    try:
        settings = parse_session(raw)
    except ValueError as exc:
        raise SystemExit(str(exc)) from None
    try:
        client = make_client()
        client.set_settings(settings)
        # An authenticated read validates the saved authorization without a password login.
        client.account_info()
    except Exception:
        raise SystemExit('Instagram could not validate the session. Check your connection/proxy, '
                         'resolve any prompts in Instagram, then retry. ' + RECOVERY) from None
    return client


def get_images():
    if not IMAGE_FOLDER.is_dir():
        raise SystemExit('Missing assets/images folder. Upload your PNG or JPG pictures there.')
    images = [p.name for p in IMAGE_FOLDER.iterdir()
              if p.is_file() and p.suffix.lower() in {'.png', '.jpg', '.jpeg'}]
    # Natural numeric ordering, with predictable ordering for other filenames.
    return sorted(images, key=lambda name: (0, int(Path(name).stem), name)
                  if Path(name).stem.isdigit() else (1, name.casefold(), name))


def read_index():
    try:
        return max(0, int(INDEX_FILE.read_text().strip()))
    except (FileNotFoundError, ValueError):
        return 0


def write_index(index):
    INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    temporary = INDEX_FILE.with_suffix('.tmp')
    temporary.write_text(str(index))
    temporary.replace(INDEX_FILE)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Validate images and login without changing your picture')
    args = parser.parse_args(argv)
    images = get_images()
    if not images:
        raise SystemExit('No pictures found. Upload PNG or JPG files into assets/images/.')
    # Validate all files before making any Instagram requests.
    from PIL import Image
    for name in images:
        try:
            with Image.open(IMAGE_FOLDER / name) as image:
                image.verify()
        except Exception:
            raise SystemExit(f'Cannot read image {name}. Replace it with a valid PNG or JPG.') from None
    index = read_index() % len(images)
    client = login_user()
    if args.check:
        logger.info('Setup works: login validated; %s images ready. No profile change made. This read-only check does not test permission to change your picture.', len(images))
        return
    try:
        result = client.account_change_picture(str(IMAGE_FOLDER / images[index]))
        if not result:
            raise RuntimeError('No success response')
    except Exception as exc:
        raise SystemExit('DP_ERROR: ' + instagram_failure(exc) + ' Index was not advanced.') from None
    write_index((index + 1) % len(images))
    # Local runs retain refreshed settings. CI intentionally reuses its secret until renewal.
    if os.getenv('GITHUB_ACTIONS') != 'true':
        save_session(client, SESSION_FILE)
    logger.info('Profile updated to %s.', images[index])


if __name__ == '__main__':
    main()
