# Instagram Auto Profile Picture Changer

![Auto PFP Changer](https://github.com/user-attachments/assets/83b23108-116a-4a98-9d53-658ad9dec2a6)

A Python script that automatically changes your Instagram profile picture at regular intervals using the [`instagrapi`](https://github.com/adw0rd/instagrapi) library.

---

## Features

- Logs in using session handling with `instagrapi`
- Rotates between a set of profile images from a local folder
- Randomized delay between profile picture changes
- Automatic retry mechanism with wait period on failure

---

## Requirements

- Python 3.7 or higher
- `instagrapi` library
- Valid Instagram account credentials

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/instagram-pfp-changer.git
   cd instagram-pfp-changer
   ```

2. **Install the required packages**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**

   Create a `.env` file in the root directory or set environment variables directly:

   ```env
   USERNAME=your_instagram_username
   PASSWORD=your_instagram_password
   ```

   Then include the following in your script:

   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

4. **Add your images**

   Store your profile images (`1.png`, `2.png`, ..., `11.png`) in a designated folder, and update the `IMAGE_FOLDER` variable in your script to point to it.

---

## Usage

To start the script, run:

```bash
python main.py
```

The script will:
- Log in to Instagram
- Change the profile picture to the next image in sequence
- Wait for a random interval between changes (e.g., 1700–1900 seconds)
- Continue the process indefinitely

---

## Project Structure

```
.
├── main.py
├── session.json
├── .env
├── images/
│   ├── 1.png
│   ├── 2.png
│   └── ...
├── requirements.txt
└── README.md
```

---

## Disclaimer

This script is intended for educational and personal use only. Automated interactions with Instagram may violate their Terms of Service. Use at your own discretion. Repeated or excessive profile changes may result in account restrictions or temporary bans.

---

## License

This project is licensed under the [MIT License](LICENSE).
