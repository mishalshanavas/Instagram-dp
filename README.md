# Instagram DP

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Platforms](https://img.shields.io/badge/platforms-Windows%20%7C%20macOS%20%7C%20Linux-555)](#get-started)
[![GitHub Actions](https://img.shields.io/badge/runs%20on-GitHub%20Actions-2088FF?logo=githubactions&logoColor=white)](Wiki/Scheduling.md)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Automatically rotate your Instagram profile picture through a folder of photos.
Setup runs on your computer; scheduled changes run in your own GitHub repository.
Your computer can stay off afterward.

![Instagram profile picture rotation demo](https://github.com/user-attachments/assets/83b23108-116a-4a98-9d53-658ad9dec2a6)

*Demo at 10× speed. Actual rotations happen hours apart.*

The setup wizard handles:

- Instagram login and verification, with masked password entry.
- GitHub sign-in and creation of a private copy of this project.
- Photo uploads, automatic numbering, and replacement of old collections.
- Timezone selection, a setup check, and the first profile-picture change.
- Workflow progress and results directly in your terminal.

> [!NOTE]
> This uses an unofficial Instagram API. Instagram may require verification,
> expire your session, or refuse automated changes. A successful login check
> does not guarantee that a picture update will succeed.

## Get started

You need **Python 3.11+**, a **GitHub account**, and an **Instagram account**.
No Git commands or manual secret setup are required.

**Choose your installation guide:**

- **[Windows](Wiki/Windows.md)**
- **[macOS](Wiki/macOS.md)**
- **[Linux / headless VM](Wiki/Linux.md)**

Already have Python? Download **Code → Download ZIP**, extract it, and open a
terminal in the folder containing `setup.py`:

```sh
# Windows
py setup.py

# macOS / Linux
python3 setup.py
```

Then follow **[First setup](Wiki/First-setup.md)** for each prompt and its expected
result. Dependencies and GitHub CLI install automatically where supported.

> [!IMPORTANT]
> Add your own photos during setup. The included images are solid-color
> placeholders. Once the check passes, setup requests the first picture change
> automatically—there is no separate visit to GitHub Actions.

## Everyday use

To replace photos, change timezone, check your session, or rotate immediately,
open the management menu:

```sh
# Windows
py setup.py --github-only --manage

# macOS / Linux
python3 setup.py --github-only --manage
```

- **[Replace your photos](Wiki/Photos.md):** upload a complete collection; originals stay unchanged.
- **[Understand the schedule](Wiki/Scheduling.md):** random 2–5 hour intervals, checked hourly. Timing is approximate.
- **[Renew an expired session](Wiki/Account-safety.md):** run full setup again to reconnect Instagram.

## Documentation

The walkthrough lives in separate pages so this README stays short.

| Guide | Covers |
| --- | --- |
| [Start here](Wiki/Home.md) | Recommended reading order |
| [First setup](Wiki/First-setup.md) | Accounts, repository, timezone, photos, and first run |
| [Photos](Wiki/Photos.md) | Formats, ordering, folder paths, and replacement |
| [Scheduling](Wiki/Scheduling.md) | Due times, timezones, manual runs, and pausing |
| [Troubleshooting](Wiki/Troubleshooting.md) | Login errors, failed updates, and GitHub access |
| [Account safety](Wiki/Account-safety.md) | Sessions, credentials, and photo privacy |
| [Configuration](Wiki/Configuration.md) | Commands, secrets, environment, and state |
| [Architecture](Wiki/Architecture.md) | Components and data flow |
| [Development](Wiki/Development.md) | Project layout and tests |

These guides are included in ZIP downloads and template copies. The GitHub wiki
is awaiting initial publication; the links above work now.

## Before opening an issue

Check [Troubleshooting](Wiki/Troubleshooting.md), then include your operating
system, Python version, and the failed step. Never include passwords, verification
codes, cookies, or `data/session.json`.

This repository is the **source template**, with Actions disabled. Automation
runs in the copy created under your account.

## License

[MIT](LICENSE)
