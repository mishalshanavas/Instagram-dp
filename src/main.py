"""
Instagram Profile Picture Changer - Main Module

This module handles automated Instagram profile picture rotation
optimized for serverless execution (GitHub Actions).
"""

import os
import logging
from pathlib import Path
from instagrapi import Client
from instagrapi.exceptions import LoginRequired

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
IMAGE_FOLDER = Path("assets/images")
DATA_FOLDER = Path("data")
INDEX_FILE = DATA_FOLDER / "index.txt"
SESSION_FILE = DATA_FOLDER / "session.json"


def ensure_data_directory():
    """Ensure data directory exists."""
    DATA_FOLDER.mkdir(exist_ok=True)


def login_user() -> Client:
    """
    Login to Instagram using saved session or credentials.
    
    Returns:
        Client: Authenticated Instagram client
    """
    logger.info("Initializing Instagram client...")
    cl = Client()
    
    if SESSION_FILE.exists():
        logger.info("Loading existing session...")
        cl.load_settings(str(SESSION_FILE))
    
    try:
        cl.login(USERNAME, PASSWORD)
        cl.get_timeline_feed()  # Test connection
        logger.info("Successfully logged in to Instagram")
    except LoginRequired:
        logger.warning("Session expired, creating new session...")
        cl.set_settings({})
        cl.login(USERNAME, PASSWORD)
        logger.info("Created new session and logged in")
    
    # Save session for next run
    cl.dump_settings(str(SESSION_FILE))
    return cl


def read_current_index() -> int:
    """
    Read the current image index from file.
    
    Returns:
        int: Current index (0-based)
    """
    if INDEX_FILE.exists():
        try:
            with open(INDEX_FILE, "r") as f:
                return int(f.read().strip())
        except (ValueError, IOError) as e:
            logger.warning(f"Error reading index file: {e}, starting from 0")
    return 0


def write_current_index(index: int) -> None:
    """
    Write the current image index to file.
    
    Args:
        index: Index to save
    """
    try:
        with open(INDEX_FILE, "w") as f:
            f.write(str(index))
        logger.info(f"Updated index to: {index}")
    except IOError as e:
        logger.error(f"Error writing index file: {e}")


def get_available_images() -> list[str]:
    """
    Get list of available image files.
    
    Returns:
        list: List of image filenames
    """
    if not IMAGE_FOLDER.exists():
        logger.error(f"Image folder not found: {IMAGE_FOLDER}")
        return []
    
    # Support multiple image formats
    image_extensions = {'.png', '.jpg', '.jpeg'}
    images = []
    
    for file in IMAGE_FOLDER.iterdir():
        if file.suffix.lower() in image_extensions and file.is_file():
            images.append(file.name)
    
    # Sort numerically if they follow the pattern 1.png, 2.png, etc.
    try:
        images.sort(key=lambda x: int(x.split('.')[0]))
    except ValueError:
        images.sort()  # Fallback to alphabetical sort
    
    logger.info(f"Found {len(images)} images: {images}")
    return images


def change_profile_picture(client: Client, index: int) -> int:
    """
    Change Instagram profile picture to the specified index.
    
    Args:
        client: Authenticated Instagram client
        index: Current image index
        
    Returns:
        int: Next index to use
    """
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
    
    # Calculate next index (cycle through images)
    next_index = (index + 1) % len(images)
    return next_index


def main():
    """Main execution function."""
    logger.info("Starting Instagram Profile Picture Changer...")
    
    try:
        # Validate environment variables
        if not USERNAME or not PASSWORD:
            raise ValueError("USERNAME and PASSWORD environment variables must be set")
        
        # Ensure data directory exists
        ensure_data_directory()
        
        # Login to Instagram
        client = login_user()
        
        # Get current index and change profile picture
        current_index = read_current_index()
        next_index = change_profile_picture(client, current_index)
        
        # Save next index for future runs
        write_current_index(next_index)
        
        logger.info("Profile picture change completed successfully!")
        
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
        raise


if __name__ == "__main__":
    main()