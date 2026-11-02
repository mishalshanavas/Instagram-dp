# Instagram DP

Rotate your Instagram profile picture through a collection of photos, with a guided terminal setup and GitHub Actions.

Works on **Windows, macOS, and Linux**. Your computer is only needed for setup; GitHub runs the scheduled changes afterward.

![Instagram DP demo](https://github.com/user-attachments/assets/83b23108-116a-4a98-9d53-658ad9dec2a6)

*Demo at 10× speed. Real rotations give your followers time to recover.*

It focuses on:

- **Simple setup:** arrow-key menus, masked passwords, and automatic dependency installation.
- **Your own copy:** repository discovery or automatic private template creation.
- **Easy photo replacement:** upload a folder; validation and numbering are handled for you.
- **Visible progress:** login diagnostics and workflow results in the terminal.
- **Cloud scheduling:** random 2–5 hour intervals, checked hourly, with times in your timezone.

> **This repository is the template. Actions are disabled here.** Setup configures automation in your own copy.

## Prerequisites

- An Instagram account and access to its verification codes.
- A [GitHub account](https://github.com/signup).
- [Python 3.11 or newer](https://www.python.org/downloads/).
- An internet connection and permission to install GitHub CLI if needed.

## Get started

Choose your system for a complete walkthrough, including how to download the ZIP, open a terminal in the correct folder, and launch setup:

- **[Windows installation](docs/Windows.md)**
- **[macOS installation](docs/macOS.md)**
- **[Linux / VM installation](docs/Linux.md)**

Then follow **[First setup: every prompt explained](docs/First-setup.md)**.

Already have Python and the extracted project folder? Open a terminal in the folder containing `setup.py`:

```powershell
# Windows
py setup.py
```

```sh
# macOS / Linux
python3 setup.py
```

Setup connects your accounts, selects a repository, asks for your timezone, and recommends replacing the placeholder photos. It then checks setup and requests the first rotation automatically. A successful read-only check does not guarantee Instagram will allow a profile change.

## Must-know tips

- Use **↑ / ↓** to move, **Enter** to select, and **Ctrl+C** to cancel.
- [Replace the complete photo set](docs/Photos.md); local originals stay untouched.
- [Timezone selection](docs/Scheduling.md) changes displayed times, not the random interval.
- Your computer can be off after setup. [Disable the workflow](docs/Scheduling.md#pause-or-resume-from-your-terminal) to pause scheduled changes.
- Never share `data/session.json`. [Session and privacy details](docs/Account-safety.md).

## Usage examples

Open the project folder's terminal first. Windows users can replace `python3` with `py`.

```sh
# Full setup: Instagram login, GitHub setup, photos, check, first rotation
python3 setup.py

# Reuse the saved local Instagram session and run setup again
python3 setup.py --github-only

# Open photo/settings/workflow controls instead of automatic rotation
python3 setup.py --github-only --manage
```

The management menu includes photo replacement, timezone changes, read-only checks, and immediate rotation. An expired Instagram session requires full setup again.

## User documentation

Each guide explains the prerequisites, steps, expected result, and what to do next.

| Guide | What it covers |
| --- | --- |
| [Documentation home](docs/Home.md) | Where to start and the recommended reading order |
| [Windows](docs/Windows.md) | Python, ZIP extraction, PowerShell, launching setup |
| [macOS](docs/macOS.md) | Python, Finder, Terminal, launching setup |
| [Linux and VMs](docs/Linux.md) | Python/venv, terminal setup, headless browser authorization |
| [First setup](docs/First-setup.md) | Instagram, GitHub, repository choice, timezone, secret storage, first run |
| [Photos](docs/Photos.md) | Folder paths, ordering, automatic names, replacement behavior |
| [Scheduling](docs/Scheduling.md) | Random intervals, hourly checks, timezone, pause/resume |
| [Troubleshooting](docs/Troubleshooting.md) | Installation, authentication, upload, and workflow failures |
| [Account safety](docs/Account-safety.md) | Credentials, photo privacy, session renewal, proxies |
| [Development](docs/Development.md) | Running tests and understanding the source files |

The guides live in this repository so they travel with ZIP downloads and template copies. [Wiki publishing instructions](docs/Wiki-publishing.md) include the prepared export and sidebar. The original demo URL is backed up in [docs/demo-url.txt](docs/demo-url.txt).

## Support

Read [Troubleshooting](docs/Troubleshooting.md) before opening an issue. Include your OS, Python version, GitHub CLI version, and sanitized error text. Never include passwords, cookies, session files, or verification codes.

This uses an unofficial Instagram API. Verification prompts, expired sessions, and account/network restrictions can interrupt automation.

## License

[MIT](LICENSE). Built with [instagrapi](https://github.com/subzeroid/instagrapi) and GitHub Actions.
