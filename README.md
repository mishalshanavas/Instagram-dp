<div align="center">

# Instagram DP

### A fresh profile picture. Without the daily decision.

Choose your photos. Set up once. Let the rotation run.

![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat-square)
![Windows, macOS, Linux](https://img.shields.io/badge/Windows%20%C2%B7%20macOS%20%C2%B7%20Linux-334155?style=flat-square)
[![MIT license](https://img.shields.io/badge/License-MIT-14B8A6?style=flat-square)](LICENSE)

[**Start here**](#get-started) · [Documentation](docs/Home.md) · [Troubleshooting](docs/Troubleshooting.md)

![Instagram profile picture rotation demo](https://github.com/user-attachments/assets/83b23108-116a-4a98-9d53-658ad9dec2a6)

*Demo at 10× speed. Your profile does not need that much caffeine.*

</div>

---

Instagram DP rotates your Instagram profile picture through a collection of your photos. A guided terminal wizard connects your accounts, uploads your pictures, and starts the automation in your own GitHub repository.

**Your computer handles setup. GitHub handles the schedule.** Close the terminal and switch off your computer once setup is complete.

## What it does

| Feature | What that means for you |
| --- | --- |
| Guided setup | Arrow-key menus, masked passwords, and automatic dependency installation |
| Your own repository | Select an existing copy or let setup create a private one |
| Folder-to-profile uploads | Choose photos locally; validation and numbering are automatic |
| Automatic rotation | Random 2–5 hour intervals, checked hourly by GitHub Actions |
| Local time displays | Choose your timezone and see when the next change is due |
| Terminal controls | Check, rotate, replace photos, and change settings without opening Actions |

> [!NOTE]
> **This repository is the template.** Actions are disabled here. Your copy runs the bot; the template supplies the code and solid-color sample images.

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

The wizard walks you through:

1. **Connect Instagram** — sign in and complete verification if requested.
2. **Connect GitHub** — choose your copy, select a timezone, and save the session secret.
3. **Choose your photos** — upload a folder or explicitly keep the existing images.
4. **Start rotating** — setup checks the configuration, then requests the first picture change.

If an upload or check fails, setup stops before requesting a rotation. A successful read-only check does not guarantee Instagram will allow the write. [See every prompt explained →](docs/First-setup.md)

## Your photos, your controls

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

## When something needs attention

Read [Troubleshooting](docs/Troubleshooting.md) before opening an issue. Include your OS, Python version, GitHub CLI version, and sanitized error text. Never include passwords, cookies, session files, or verification codes.

> [!IMPORTANT]
> This uses an unofficial Instagram API. Verification prompts, expired sessions, and account/network restrictions can interrupt automation. Scheduled runs may be delayed; this is not an exact-time scheduler.

## License

[MIT](LICENSE). Built with [instagrapi](https://github.com/subzeroid/instagrapi) and GitHub Actions.
