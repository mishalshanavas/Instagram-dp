import os
import time
import logging
from pathlib import Path
from instagrapi import Client
from instagrapi.exceptions import LoginRequired
from time_manager import TimeManager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

# Get repository root (parent of src/)
REPO_ROOT = Path(__file__).parent.parent
IMAGE_FOLDER = REPO_ROOT / "assets" / "images"
DATA_FOLDER = REPO_ROOT / "data"
INDEX_FILE = DATA_FOLDER / "index.txt"
SESSION_FILE = DATA_FOLDER / "session.json"


def ensure_data_directory():
    DATA_FOLDER.mkdir(exist_ok=True)


def login_user() -> Client:
    """
    Login following instagrapi best practices:
    https://subzeroid.github.io/instagrapi/usage-guide/best-practices.html
    
    - Reuse session to avoid repeated logins (Instagram flags fresh logins)
    - Preserve device UUIDs across relogins (so Instagram sees the same device)
    - Add delay_range for human-like request spacing
    """
    cl = Client()
    cl.delay_range = [1, 3]

    login_via_session = False
    login_via_pw = False

    if SESSION_FILE.exists():
        logger.info("Loading existing session...")
        session = cl.load_settings(str(SESSION_FILE))

        if session:
            try:
                cl.set_settings(session)
                cl.login(USERNAME, PASSWORD)

                # Check if session is still valid
                try:
                    cl.get_timeline_feed()
                except LoginRequired:
                    logger.info("Session expired, re-logging with same device UUIDs...")

                    old_session = cl.get_settings()

                    # Preserve device UUIDs so Instagram sees the same device
                    cl.set_settings({})
                    cl.set_uuids(old_session["uuids"])

                    cl.login(USERNAME, PASSWORD)

                login_via_session = True
                logger.info("Logged in via session")
            except Exception as e:
                logger.warning(f"Session login failed: {e}")

    if not login_via_session:
        try:
            logger.info("Logging in via username and password...")
            if cl.login(USERNAME, PASSWORD):
                login_via_pw = True
                logger.info("Logged in via password")
        except Exception as e:
            logger.error(f"Password login failed: {e}")

    if not login_via_session and not login_via_pw:
        raise Exception("Could not login with either session or password")

    cl.dump_settings(str(SESSION_FILE))
    return cl


def read_current_index() -> int:
    if INDEX_FILE.exists():
        try:
            with open(INDEX_FILE, "r") as f:
                return int(f.read().strip())
        except (ValueError, IOError) as e:
            logger.warning(f"Error reading index file: {e}, starting from 0")
    return 0


def write_current_index(index: int) -> None:
    try:
        with open(INDEX_FILE, "w") as f:
            f.write(str(index))
        logger.info(f"Updated index to: {index}")
    except IOError as e:
        logger.error(f"Error writing index file: {e}")


def get_available_images() -> list[str]:
    if not IMAGE_FOLDER.exists():
        logger.error(f"Image folder not found: {IMAGE_FOLDER}")
        return []
    
    image_extensions = {'.png', '.jpg', '.jpeg'}
    images = []
    
    for file in IMAGE_FOLDER.iterdir():
        if file.suffix.lower() in image_extensions and file.is_file():
            images.append(file.name)
    
    try:
        images.sort(key=lambda x: int(x.split('.')[0]))
    except ValueError:
        images.sort()
    
    logger.info(f"Found {len(images)} images: {images}")
    return images


def change_profile_picture(client: Client, index: int) -> int:
    images = get_available_images()
    
    if not images:
        raise FileNotFoundError("No images found in assets/images folder")
    
    current_image = images[index]
    image_path = IMAGE_FOLDER / current_image
    
    logger.info(f"Changing profile picture to: {current_image}")
    
    for attempt in range(2):
        try:
            client.account_change_picture(str(image_path))
            logger.info(f"Successfully changed profile picture to: {current_image}")
            break
        except Exception as e:
            if attempt == 0:
                logger.warning(f"Attempt 1 failed: {e}, retrying in 10s...")
                time.sleep(10)
            else:
                logger.error(f"Failed to change profile picture after 2 attempts: {e}")
                raise
    
    next_index = (index + 1) % len(images)
    return next_index


def main():
    logger.info("Starting Instagram Profile Picture Changer...")
    
    # Get force_run flag from environment (set by workflow)
    force_run = os.getenv("FORCE_RUN", "false").lower() == "true"
    
    try:
        if not USERNAME or not PASSWORD:
            raise ValueError("USERNAME and PASSWORD environment variables must be set")
        
        ensure_data_directory()
        
        # Initialize time manager
        time_mgr = TimeManager()
        
        # Log current schedule info
        schedule_info = time_mgr.get_schedule_info()
        logger.info("=" * 60)
        logger.info("SCHEDULE INFORMATION")
        logger.info("=" * 60)
        for key, value in schedule_info.items():
            if isinstance(value, dict):
                logger.info(f"{key}:")
                for k, v in value.items():
                    logger.info(f"  {k}: {v}")
            else:
                logger.info(f"{key}: {value}")
        logger.info("=" * 60)
        
        # Check if we should run now
        should_run, reason, details = time_mgr.should_run_now(force=force_run)
        
        if not should_run:
            logger.info(f"⏸️  SKIPPING: {reason}")
            logger.info("Run will be skipped this cycle")
            return
        
        logger.info(f"✅ PROCEEDING: {reason}")
        
        # Proceed with DP change
        client = login_user()
        current_index = read_current_index()
        next_index = change_profile_picture(client, current_index)
        write_current_index(next_index)
        
        # Record successful run and schedule next
        next_scheduled = time_mgr.record_successful_run()
        
        logger.info("=" * 60)
        logger.info("✅ Profile picture change completed successfully!")
        logger.info(f"📅 Next run scheduled for: {next_scheduled.strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"❌ Error in main execution: {e}")
        raise


if __name__ == "__main__":
    main()