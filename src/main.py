import os
import logging
from pathlib import Path
from instagrapi import Client
from instagrapi.exceptions import LoginRequired

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
IMAGE_FOLDER = Path("assets/images")
DATA_FOLDER = Path("data")
INDEX_FILE = DATA_FOLDER / "index.txt"
SESSION_FILE = DATA_FOLDER / "session.json"


def ensure_data_directory():
    DATA_FOLDER.mkdir(exist_ok=True)


def login_user() -> Client:
    logger.info("Initializing Instagram client...")
    cl = Client()
    
    if SESSION_FILE.exists():
        logger.info("Loading existing session...")
        cl.load_settings(str(SESSION_FILE))
    
    try:
        cl.login(USERNAME, PASSWORD)
        cl.get_timeline_feed()
        logger.info("Successfully logged in to Instagram")
    except LoginRequired:
        logger.warning("Session expired, creating new session...")
        cl.set_settings({})
        cl.login(USERNAME, PASSWORD)
        logger.info("Created new session and logged in")
    
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
    
    try:
        client.account_change_picture(str(image_path))
        logger.info(f"Successfully changed profile picture to: {current_image}")
    except Exception as e:
        logger.error(f"Failed to change profile picture: {e}")
        raise
    
    next_index = (index + 1) % len(images)
    return next_index


def main():
    logger.info("Starting Instagram Profile Picture Changer...")
    
    try:
        if not USERNAME or not PASSWORD:
            raise ValueError("USERNAME and PASSWORD environment variables must be set")
        
        ensure_data_directory()
        client = login_user()
        current_index = read_current_index()
        next_index = change_profile_picture(client, current_index)
        write_current_index(next_index)
        
        logger.info("Profile picture change completed successfully!")
        
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
        raise


if __name__ == "__main__":
    main()