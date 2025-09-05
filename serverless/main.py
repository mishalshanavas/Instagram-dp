import os
from instagrapi import Client
from instagrapi.exceptions import LoginRequired

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
IMAGE_FOLDER = "assets"
INDEX_FILE = os.path.join("serverless", "index.txt")
SESSION_FILE = os.path.join("serverless", "session.json")


def login_user():
    cl = Client()
    if os.path.exists(SESSION_FILE):
        cl.load_settings(SESSION_FILE)
    try:
        cl.login(USERNAME, PASSWORD)
        cl.get_timeline_feed()
    except LoginRequired:
        cl.set_settings({})
        cl.login(USERNAME, PASSWORD)
    cl.dump_settings(SESSION_FILE)
    return cl


def read_index():
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "r") as f:
            return int(f.read().strip())
    return 0


def write_index(index):
    with open(INDEX_FILE, "w") as f:
        f.write(str(index))


def change_profile_pic(cl, index):
    images = [f"{i}.png" for i in range(1, 12)]
    image_path = os.path.join(IMAGE_FOLDER, images[index])
    cl.account_change_picture(image_path)
    return (index + 1) % len(images)


if __name__ == "__main__":
    cl = login_user()
    index = read_index()
    print(f"Changing DP to {index + 1}.png")
    next_index = change_profile_pic(cl, index)
    write_index(next_index)
