<div align="center">

# Instagram DP

### Your photos. A fresh profile picture. On autopilot.

Rotate your Instagram profile picture with a guided terminal setup and GitHub Actions.

![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Platforms: Windows, macOS, Linux](https://img.shields.io/badge/Platforms-Windows%20%C2%B7%20macOS%20%C2%B7%20Linux-334155?style=flat-square)
[![License: MIT](https://img.shields.io/badge/License-MIT-14B8A6?style=flat-square)](LICENSE)

![Instagram DP rotation demo](https://github.com/user-attachments/assets/83b23108-116a-4a98-9d53-658ad9dec2a6)

*Demo at 10× speed. Your actual profile gets a more reasonable schedule.*

[Get started](#get-started) · [Replace photos](#3-add-your-photos) · [Run it again](#run-it-again) · [Troubleshooting](#troubleshooting)

</div>

---

Choose some photos, follow the wizard, and let GitHub handle the rotation. Once setup is complete, your computer can be switched off. Your profile has a schedule now. Very employed of it.

| Guided setup | Your own photos | Runs in the cloud |
| --- | --- | --- |
| Arrow-key menus, hidden passwords, and clear prompts | Upload a folder; files are validated and numbered for you | Start, check, and watch runs from your terminal |

> [!NOTE]
> **This is the template repository. Actions are disabled here.** The wizard creates or selects your own copy, where automation runs. Keep the workflow files—they power your copy.

## Get started

Have these ready:

- **Instagram:** an account you can log into, including access to verification codes.
- **GitHub:** a [free account](https://github.com/signup).
- **Python 3.11+:** [download Python](https://www.python.org/downloads/). On Windows, select **Add Python to PATH** during installation.

The wizard installs Python dependencies and installs GitHub CLI when a supported package manager is available. No Git commands required.

### 1. Download and launch

Click **Code → Download ZIP** at the top of this page, then extract the ZIP. Open the extracted folder—you should see `setup.py`, `README.md`, and `src`.

Open a terminal **in that folder**:

| System | Open the terminal | Run this command |
| --- | --- | --- |
| Windows | In File Explorer, type `powershell` into the folder's address bar and press Enter. | `py setup.py` |
| macOS | Open Terminal, type `cd ` with a space, drag the extracted folder into it, then press Enter. | `python3 setup.py` |
| Linux | Right-click inside the folder and choose **Open in Terminal**. | `python3 setup.py` |

On Windows, try `python setup.py` if `py` is not recognized. Reopen your terminal after installing Python.

Package installation shows a compact animated progress bar instead of pip logs. If installation fails, the installer details stay visible. Once it finishes, the wizard clears the screen and opens the setup menu.

**Controls:** **↑ / ↓** to move · **Enter** to select · **Ctrl+C** to cancel. Basic terminals show numbered choices instead.

### 2. Connect your accounts

**Instagram**

Select **Username and password** for your first login. Enter your details and any verification code requested.

Your password appears as `*****` while you type—visible progress, private characters. Basic terminals fall back to invisible entry.

During login, the terminal shows request stages and HTTP status codes, without passwords, cookies, or raw response bodies. These details are cleared after a successful login; failures remain visible.

Wait for **“Login validated. Your private session is saved locally.”** If Instagram asks you to approve a login in its app, complete that prompt before trying again.

For later setups, **Reuse a trusted local session** avoids another password login. **Browser session** is an advanced alternative and may be rejected by Instagram's mobile API.

**GitHub**

Follow the prompts in the same terminal:

1. **GitHub CLI installs automatically** if missing. The wizard uses Winget, Homebrew, or a supported Linux package manager. If none is available, follow the installation link it prints.
2. **Sign in** using GitHub's browser/device-code instructions. This browser authorization may be needed once.
3. **Select your repository.** Choose an existing copy. If none are found, setup automatically creates a private template copy with an available name. Choose private visibility if you don't want your photos public. If template creation is unavailable, the wizard offers a fork instead.
4. **Session saved automatically.** The wizard shows the destination and saves `INSTA_SESSION` as a repository secret.

> [!IMPORTANT]
> **Never upload or share `data/session.json`.** It contains your Instagram login session. Your Instagram password is not uploaded to GitHub.

### 3. Add your photos

In the final menu, select **Replace photos from a folder**.

1. Put **every photo you want in the rotation** into one folder on your computer.
2. Paste that folder's full path when asked. Examples:
   - Windows: `C:\Users\You\Pictures\Instagram`
   - macOS: `/Users/you/Pictures/Instagram`
   - Linux: `/home/you/Pictures/Instagram`
3. Review the list and confirm the upload.

The wizard does the housekeeping:

| You provide | The wizard handles |
| --- | --- |
| 1–100 PNG/JPG photos, each up to 20 MB | Checks that each image is readable |
| Your original filenames | Renames uploads to `1.png`, `2.jpg`, etc., preserving extensions |
| One complete photo collection | Replaces the old set in one commit and restarts at the first photo |

Photos are ordered by numeric filename first, then alphabetically. Your local originals are untouched. Files uploaded manually through GitHub keep their original names.

**Replacing means replacing:** include photos you want to keep. Old images remain in Git history; images in a public repository are public.

The template includes **11 solid-color placeholders at 320 × 320 pixels (1:1)**. Replace them before rotating unless your current aesthetic is “a very confident square.”

### 4. Check it, then start

From the same menu:

```text
Check login and photos (recommended)
Change your profile picture now
Replace photos from a folder
Finish
```

Select **Check login and photos**. The wizard checks the remote workflow, enables it if disabled, and watches the run in your terminal.

The check validates login and images only; Instagram can still refuse a profile update. If a run fails, the wizard fetches a safe error summary automatically.

After the check passes, answer **yes** to **“Change your profile picture now?”** Wait for the success message. You don't need to open the GitHub Actions page.

**What happens next:** each successful rotation schedules the next change 2–5 hours later. GitHub checks hourly, so actual timing may be later. Enabling the workflow also enables scheduled rotations, which can run independently of your manual check.

You can now close the terminal and switch off your computer.

## Run it again

Want to replace photos or trigger another run? Open the project folder's terminal and resume GitHub setup without another Instagram login:

| Windows | macOS / Linux |
| --- | --- |
| `py setup.py --github-only` | `python3 setup.py --github-only` |

Select your repository and use the final menu. If the Instagram session itself has expired, run full setup again to create and save a new one.

<details>
<summary><strong>Prefer direct GitHub CLI commands?</strong></summary>

Replace `YOUR-NAME/YOUR-REPO` with your copy's repository name.

```sh
# Change your profile picture now
gh workflow run change-dp.yml --repo YOUR-NAME/YOUR-REPO -f mode=rotate

# Check setup without changing the picture
gh workflow run change-dp.yml --repo YOUR-NAME/YOUR-REPO -f mode=check

# Show recent runs
gh run list --repo YOUR-NAME/YOUR-REPO --workflow change-dp.yml --limit 5

# Pause scheduled changes
gh workflow disable change-dp.yml --repo YOUR-NAME/YOUR-REPO

# Resume scheduled changes
gh workflow enable change-dp.yml --repo YOUR-NAME/YOUR-REPO
```

</details>

## Troubleshooting

| What happened | What to do |
| --- | --- |
| Python command not found | Install Python 3.11+, reopen the terminal, and use the command for your system above. |
| Cannot create a virtual environment | On Linux, install your distribution's Python venv package. On Windows/macOS, repair Python with pip support. |
| HTTP 403 on profile change | Login may work while writes are refused. Check the official app for restrictions; if using browser-session login, try full setup with username/password and replace the secret. No automatic retry is made. |
| HTTP 429 / Too many requests | Stop repeated attempts. Check Instagram for prompts and wait before retrying on your usual network. There is no guaranteed cooldown. |
| Session expired or login rejected | Resolve prompts in Instagram, then run full setup and save the new session secret. |
| No repositories listed | Choose **Create a new repository**, or enter an existing repository manually. |
| Secret upload failed | Check the selected GitHub account and repository admin permissions. Resume with `--github-only`. |
| Workflow missing or differs from setup | Update the selected repository's project files on its default branch, then resume with `--github-only`. |
| Workflow failed | Run the `gh run view … --log-failed` command printed by the wizard to see the failed step. |
| Photos cannot be uploaded | Use readable PNG/JPG files within the limits above. Check repository permissions and branch rules. |

Instagram can expire sessions or require verification. This project uses an unofficial API, so uninterrupted automation isn't guaranteed. Sessions are reused until rejected; GitHub secrets are not refreshed automatically.

<details>
<summary><strong>Advanced: proxy and migration from older versions</strong></summary>

Set `PROXY_URL` as a GitHub Actions secret if you use a stable proxy. Set the same environment variable locally before login. A failed configured proxy stops the run rather than silently changing networks.

The project pins instagrapi 3.2.2 and Pillow 13.0.0. An older TLS-related login failure was fixed upstream in [instagrapi 3.0.21](https://github.com/subzeroid/instagrapi/issues/2852); that does not resolve every HTTP 429.

If you previously committed a session file, revoke that session and create a new one. Removing the file doesn't erase it from Git history. The old `INSTA_USER` and `INSTA_PASS` secrets are no longer used.

</details>

<details>
<summary><strong>Development and tests</strong></summary>

**Windows:**

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -p test_app.py -v
```

**macOS / Linux:**

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m unittest discover -s tests -v
```

Tests use fake clients. Workflow shell tests require Bash. CI runs on Ubuntu in user copies; Actions are disabled on the template. Windows and macOS setup paths have not been tested on physical machines.

</details>

---

<div align="center">

Built with [instagrapi](https://github.com/subzeroid/instagrapi) · Powered by GitHub Actions · [MIT license](LICENSE)

*Automate the rotation. Keep the questionable selfies a manual decision.*

</div>
