import os
import time
import random
from instagrapi import Client
from instagrapi.exceptions import LoginRequired

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
IMAGE_FOLDER = ""

def login_user():
    cl = Client()
    session_path = "session.json"
    if os.path.exists(session_path):
        cl.load_settings(session_path)
    try:
        cl.login(USERNAME, PASSWORD)
        cl.get_timeline_feed()
    except LoginRequired:
        cl.set_settings({})
        cl.login(USERNAME, PASSWORD)
    cl.dump_settings(session_path)
    return cl

def change_profile_pic(cl):
    images = [f"{i}.png" for i in range(1, 12)]
    if not hasattr(change_profile_pic, "current_index"):
        change_profile_pic.current_index = 0
    image_path = os.path.join(IMAGE_FOLDER, images[change_profile_pic.current_index])
    cl.account_change_picture(image_path)
    change_profile_pic.current_index = (change_profile_pic.current_index + 1) % len(images)

if __name__ == "__main__":
    cl = login_user()
    while True:
        current_index = getattr(change_profile_pic, "current_index", 0)
        print(f"Changing profile picture to {current_index + 1}.png")
        change_profile_pic(cl)
        delay = random.randint(1700, 1900)
        for remaining in range(delay, 0, -1):
            print(f"Next change in: {remaining} seconds", end="\r")
            time.sleep(1)
        print()