# Instagram DP

Automatically rotate your Instagram profile picture through a folder of photos. Setup runs on your computer; scheduled changes run in your own GitHub repository using GitHub Actions.

Supports Windows, macOS, and Linux. Requires Python 3.11 or newer.

![Instagram profile picture rotation demo](https://github.com/user-attachments/assets/83b23108-116a-4a98-9d53-658ad9dec2a6)

*Demo at 10× speed.*

## Before you start

You need:

- An Instagram account and access to any login verification codes.
- A [GitHub account](https://github.com/signup).
- [Python 3.11+](https://www.python.org/downloads/). On Windows, select **Add Python to PATH** if the installer offers it.
- An internet connection and permission to install GitHub CLI.

This repository is a template. Actions are disabled here. Setup creates or selects a copy under your GitHub account and configures the bot there.

## Installation

1. Click **Code → Download ZIP** on this page.
2. Extract the ZIP.
3. Open a terminal in the extracted folder containing `setup.py`.
4. Run the command for your system:

| Windows | macOS / Linux |
| --- | --- |
| `py setup.py` | `python3 setup.py` |

If Windows cannot find `py`, try `python setup.py`.

For instructions on installing Python and opening the terminal, follow the guide for your system:

- [Windows](docs/Windows.md)
- [macOS](docs/macOS.md)
- [Linux and headless VMs](docs/Linux.md)

## First setup

Use **↑ / ↓** to move between choices and **Enter** to select. Press **Ctrl+C** to cancel. Terminals without interactive support show numbered prompts.

Setup will:

1. Install dependencies and GitHub CLI where a supported package manager is available. Your OS may request administrator approval.
2. Ask you to log into Instagram and complete verification. Passwords are masked.
3. Sign into GitHub through browser authorization. On a headless VM, open the displayed URL on another device and enter its code.
4. List your existing project copies. If none exist, create a private copy with an available name.
5. Ask for your timezone and save your Instagram session as the `INSTA_SESSION` repository secret.
6. Recommend uploading your own photos. You must explicitly choose to keep existing images, including the template's solid-color placeholders.
7. Run a read-only check, then request the first profile-picture change if the check passes.

The terminal displays workflow progress and the next rotation time. Once setup completes, your computer can be turned off.

**[Full setup guide: each prompt and expected result](docs/First-setup.md)**

## Photos

Choose a folder containing **1–100 PNG/JPG files**, each up to **20 MB**. Setup validates them and shows the proposed upload before asking you to confirm.

Uploads are renamed to `1.png`, `2.jpg`, and so on, preserving extensions. The complete repository photo set is replaced and rotation restarts at the first image. Your local originals are untouched. Manual GitHub uploads are not automatically renamed.

Include every photo you want to keep. Replaced files can remain in Git history, and photos in public repositories are public.

[Photo ordering, folder paths, and replacement instructions](docs/Photos.md)

## Schedule

After each successful change, the bot chooses a random interval of **2–5 hours**. GitHub checks hourly at **minute 17 UTC** and rotates when the stored due time has passed. Actual timing may be later because of hourly checks or GitHub delays.

Your selected timezone controls how times are displayed. It does not change the interval. Scheduled runs remain active after you close the terminal.

[Timezone settings, manual runs, and pause/resume commands](docs/Scheduling.md)

## Change settings or photos

Open the project folder's terminal and run:

| Windows | macOS / Linux |
| --- | --- |
| `py setup.py --github-only --manage` | `python3 setup.py --github-only --manage` |

Select your repository. The menu provides photo replacement, timezone selection, read-only checks, and immediate rotation.

`--github-only` reuses the saved local Instagram session. If that session expires, run full setup again. Omitting `--manage` uses the automatic flow: choose photos, check setup, then rotate.

## Limitations and credentials

This project uses [instagrapi](https://github.com/subzeroid/instagrapi), an unofficial Instagram API client. Instagram may require verification, expire a session, or refuse automated changes. A successful read-only check does not prove that a profile update will succeed.

Your Instagram password is not uploaded to GitHub. **Do not share or commit `data/session.json`: it contains login credentials.** Workflow runs reuse the session secret; they do not renew it automatically.

[Session storage, photo privacy, and renewal](docs/Account-safety.md)

## Documentation and support

- [Documentation index](docs/Home.md)
- [Troubleshooting](docs/Troubleshooting.md)
- [Development and tests](docs/Development.md)

Before opening an issue, check the troubleshooting guide. Include your OS, Python version, `gh --version`, and the failed step. Remove passwords, cookies, session data, and verification codes from logs.

The guides are stored in `docs/` so they are included in downloads and template copies. [Wiki publishing instructions](docs/Wiki-publishing.md) are available for maintainers.

## License

[MIT](LICENSE).
