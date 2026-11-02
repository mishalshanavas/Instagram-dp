<div align="center">

# Instagram DP

**Fresh profile pictures. Less manual labor.**

A guided setup that rotates your Instagram profile picture using GitHub Actions.

![Instagram DP demo](https://github.com/user-attachments/assets/83b23108-116a-4a98-9d53-658ad9dec2a6)

*Demo at 10× speed. The bot itself has boundaries.*

**Windows · macOS · Linux** · **Python 3.11+** · **MIT licensed**

</div>

---

## What you get

- A terminal wizard with arrow-key menus and masked passwords.
- Your own repository, created automatically if you don't have a copy.
- Photo uploads from a local folder, with automatic numbering.
- A timezone picker and readable rotation times.
- Automatic setup checks and a first rotation, watched from your terminal.
- Cloud scheduling—your computer can be off afterward.

> This repository is a **template**. Actions are disabled here. The wizard sets up automation in **your own copy**.

## Start here

You'll need an **Instagram account**, a [GitHub account](https://github.com/signup), and [Python 3.11 or newer](https://www.python.org/downloads/).

On Windows, enable **Add Python to PATH** when installing Python.

### 1. Download and extract

Click **Code → Download ZIP** at the top of this page. Extract it and open the folder containing `setup.py`.

### 2. Open a terminal and run setup

| Computer | Open a terminal in the extracted folder | Command |
| --- | --- | --- |
| Windows | Type `powershell` in File Explorer's address bar and press Enter. | `py setup.py` |
| macOS | Open Terminal, type `cd `, drag the folder into Terminal, then press Enter. | `python3 setup.py` |
| Linux | Right-click inside the folder → **Open in Terminal**. | `python3 setup.py` |

If Windows doesn't recognize `py`, try `python setup.py`. Reopen the terminal after installing Python.

Setup installs the required packages and GitHub CLI. You may need to approve an OS permission prompt or enter your administrator password.

**Use ↑ / ↓ to move, Enter to select, and Ctrl+C to cancel.** Basic terminals show numbered choices instead.

### 3. Connect your accounts

**Instagram:** select **Username and password**. Enter your details and any verification code requested. Your password appears as asterisks. Login activity clears when validation succeeds.

Already set up on this computer? **Reuse a trusted local session** avoids another password login. Browser-session login is also available, but may fail on operations that password-based sessions can perform.

**GitHub:** follow the browser sign-in instructions. On a VM without a browser, open the displayed device-login URL on another device and enter the displayed code.

The wizard then:

1. Finds your existing copies and lets you choose one.
2. Creates a **private template copy automatically** if none exist, choosing an available name.
3. Asks for your **timezone**, such as `Asia/Kolkata`.
4. Saves your Instagram session as the `INSTA_SESSION` repository secret.

Expired GitHub authentication triggers browser sign-in and one discovery retry automatically.

### 4. Add your photos

Select **Add my photos from a folder (recommended)**.

Put all the pictures you want in one folder, then paste its full path:

```text
Windows   C:\Users\You\Pictures\Instagram
macOS     /Users/you/Pictures/Instagram
Linux     /home/you/Pictures/Instagram
```

Review the list and confirm replacement. Setup validates the files, uploads them in one commit, and restarts rotation from the first image.

| Supported files | Upload limits | Automatic names |
| --- | --- | --- |
| PNG, JPG, JPEG | 1–100 photos, up to 20 MB each | `1.png`, `2.jpg`, `3.png`… |

Files are sorted by numeric filename first, then alphabetically. Extensions are preserved, and your local originals stay untouched.

**This replaces the whole photo set.** Include every photo you want to keep. Cancelling or failing the upload stops setup before a rotation is requested.

You can explicitly choose the existing repository images instead. New copies contain **11 solid-color, 320 × 320 placeholders**. A bold color is a look; accidentally choosing it is less of one.

### 5. Let setup finish

Setup automatically enables the workflow, runs a login-and-image check, and watches its progress. If the check passes, it requests the first profile-picture change and watches that too.

**No visit to the GitHub Actions page needed.** Refresh progress appears every three seconds.

A successful read-only check doesn't guarantee Instagram will allow a profile update. If a run fails, setup shows recovery guidance and stops rather than repeatedly retrying.

## How the schedule works

After each successful rotation, the bot picks a random **2–5 hour interval**. GitHub checks hourly at **minute 17 UTC**, rotating when that interval is due. Scheduled runs can be delayed.

The wizard and workflow summaries show the next due time and first hourly check in your chosen timezone. Timezone selection changes the displayed times, not the interval or GitHub's UTC cron.

Images rotate in order and loop back to the start. Once enabled, scheduled rotations run independently of the setup terminal.

## Change photos or settings later

Open the project folder's terminal:

**Windows:**

```powershell
py setup.py --github-only --manage
```

**macOS / Linux:**

```sh
python3 setup.py --github-only --manage
```

Choose your repository to replace photos, change timezone, check setup, or rotate manually. Your saved local session is required; an expired Instagram session needs full setup again.

Omit `--manage` to use the automatic flow again: choose photos, check setup, then rotate.

## Pause or resume

Replace `YOUR-NAME/YOUR-REPO` with the repository selected during setup.

```sh
# Pause scheduled rotations
gh workflow disable change-dp.yml --repo YOUR-NAME/YOUR-REPO

# Resume scheduled rotations
gh workflow enable change-dp.yml --repo YOUR-NAME/YOUR-REPO

# See recent runs
gh run list --repo YOUR-NAME/YOUR-REPO --workflow change-dp.yml --limit 5
```

## If something goes wrong

| Problem | Next step |
| --- | --- |
| Python isn't recognized | Install Python 3.11+, reopen the terminal, and use the command for your system. |
| Virtual environment cannot be created | On Linux, install your distribution's Python venv package. On Windows/macOS, repair Python with pip support. |
| GitHub browser won't open | Open the displayed device-login URL elsewhere and enter its code. Wait for authentication to complete. |
| GitHub still returns HTTP 401 | Complete browser authorization. If recovery fails, run `gh auth login`, then resume setup with `--github-only`. |
| Instagram returns HTTP 429 | Stop repeated attempts, check for prompts in the Instagram app, and wait before retrying. There is no guaranteed cooldown. |
| Login works but rotation returns HTTP 403 | Check account restrictions in the official app. If you used a browser session, try full setup with username/password and replace the secret. The exact cause may be account- or network-related. |
| Workflow differs from setup | Update the project files in your copy's default branch, then resume setup. |
| Upload fails | Check file types, file sizes, repository permissions, and branch rules. |

## A few things to keep private

**Never upload or share `data/session.json`.** It contains your login session. Your Instagram password stays on your computer; GitHub receives the session secret.

Photos in a public repository are public. Replaced photos can remain in Git history. If an older version committed your session, revoke it and create a fresh one.

Instagram can expire sessions or require verification. This project uses an unofficial API; uninterrupted automation isn't guaranteed. Session secrets aren't renewed automatically.

<details>
<summary><strong>Advanced: proxy</strong></summary>

Set `PROXY_URL` as a repository Actions secret if you use a stable proxy. Set the same environment variable locally before login. A configured proxy failure stops the request rather than silently switching networks.

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

Tests use fake clients. Workflow shell tests require Bash. Actions are disabled on the template; user copies contain the workflows. The setup has been exercised on Windows and Linux; macOS has not been verified on a physical machine.

</details>

---

<div align="center">

Built with [instagrapi](https://github.com/subzeroid/instagrapi) · Powered by GitHub Actions · [MIT license](LICENSE)

*Your profile gets variety. You get your time back.*

</div>
