# Instagram Profile Picture Changer

<div align="center">

![Demo: Instagram profile pictures rotating](https://github.com/user-attachments/assets/83b23108-116a-4a98-9d53-658ad9dec2a6)

*Demo at 10× speed*

</div>

Pick your photos, run the setup wizard, and let GitHub change your Instagram profile picture automatically.

**Windows, macOS, and Linux supported.** Your computer only needs to be on during setup. Afterward, GitHub runs the bot for you.

**This repository is the template. Actions are disabled here.** Setup creates or selects your own copy, where the bot runs. Workflow files are included so your copy can use them.

## Before you start

You need:

- An Instagram account you can log into.
- A free [GitHub account](https://github.com/signup).
- [Python 3.11 or newer](https://www.python.org/downloads/). On Windows, enable **Add Python to PATH** during installation.

You don't need to install Python packages or GitHub CLI yourself—the wizard handles packages and offers to install GitHub CLI.

The wizard has arrow-key menus: use **↑ / ↓** to move and **Enter** to select. Press **Ctrl+C** to cancel. You can choose Instagram login, your repository, photo replacement, and workflow runs from the terminal. Terminals without interactive support show numbered prompts instead.

## 1. Download the project

At the top of this repository, click **Code → Download ZIP**. Extract the ZIP into a folder you can find easily, such as your Desktop.

Open the extracted folder. You should see **setup.py**, **README.md**, and the **src** folder.

## 2. Open a terminal in that folder

| Your computer | How to open the terminal |
| --- | --- |
| Windows | In File Explorer, open the extracted folder. Type `powershell` in its address bar and press Enter. |
| macOS | Open Terminal. Type `cd ` with a space, drag the extracted folder into Terminal, then press Enter. |
| Linux | Right-click inside the extracted folder and choose **Open in Terminal**. |

Run **one** command:

**Windows:**

```powershell
py setup.py
```

**macOS / Linux:**

```sh
python3 setup.py
```

If Windows doesn't recognize `py`, try `python setup.py`. Keep the terminal open while packages install. Once installation finishes, the login menu appears.

## 3. Log into Instagram

```text
1. Username and password
2. Browser session
3. Reuse a trusted local session (no password login)
0. Exit
```

For your first setup, select **Username and password** and press Enter (or type **1** in plain mode). Enter your username and password. **Nothing appears while you type your password—that is normal.** Press Enter when finished.

Enter a verification code if asked. If Instagram requires approval in its app, complete that prompt before trying again.

Wait for **“Login validated. Your private session is saved locally.”**

Already completed Instagram setup on this computer? Choose **3** to reuse your saved session. Option **2** is an advanced alternative using your browser's `sessionid` cookie; it is not guaranteed to work with Instagram's mobile API.

## 4. Let the wizard set up GitHub

Follow the prompts in the same terminal:

1. **Install GitHub CLI:** accept the installation offer if it appears. It uses Winget on Windows, Homebrew on macOS, or apt/dnf/pacman on supported Linux systems. If none is available, follow the printed installation link, reopen your terminal, and resume using the command below.
2. **Sign in:** follow GitHub's browser/device-code instructions. This browser sign-in may be required once; you won't need the GitHub website to start the bot afterward.
3. **Choose your repository:** select an existing copy by number. For a first setup, choose **N** to create one. The wizard uses a template when available, or asks whether to create a fork. Review the repository name before continuing.
4. **Save your session:** press Enter at **“Save/replace INSTA_SESSION…”**. The wizard uploads it securely as a GitHub Actions secret.

Your Instagram password is not uploaded. **Never upload or share `data/session.json`**, which contains your private login session.

## 5. Add your own pictures

At the final setup menu, select **Replace photos from a folder** (or type **3** in plain mode).

1. Put the photos you want in one folder on your computer. PNG and JPG files are supported.
2. Paste that folder's full path into the terminal. For example, `C:\Users\You\Pictures\Instagram` on Windows or `/Users/you/Pictures/Instagram` on macOS.
3. Review the displayed photo list. Type **y** to upload it.

The wizard checks the files, numbers them automatically, replaces the repository's old PNG/JPG photos, and restarts the rotation at the first picture. Files are ordered by numeric filename first, then alphabetically. Your originals stay on your computer. Files uploaded through this wizard are renamed automatically to `1.png`, `2.jpg`, and so on, preserving their file extensions. Files uploaded manually through GitHub are not automatically renamed.

**No Git commands or GitHub upload page needed.** Uploading replaces the complete photo set, so include every photo you want to keep. The default is **No** until you confirm. Old photos remain in Git history, and pictures uploaded to a public repository are public.

The included placeholders are 11 distinct solid-color PNGs, each 320 × 320 pixels (1:1 square).

You can upload 1–100 images, each up to 20 MB. After uploading, choose **1** to check setup or **2** to change your picture now. If you skip this step, the sample photos remain in the rotation.

## 6. Start the bot from your terminal

At the end of setup, the wizard shows:

```text
1. Check login and photos without changing your picture (recommended)
2. Change your profile picture now
3. Replace photos from a folder on this computer
0. Finish without running a workflow
```

Select **Check login and photos** and press **Enter**. The wizard enables the workflow if needed, starts it through GitHub CLI, and displays progress in your terminal. Enabling it also activates scheduled rotations.

When the check passes, type **y** at **“Change your profile picture now?”** to run your first rotation. Wait for the success message. **No trip to the GitHub Actions page needed.**

The next change is scheduled 2–5 hours later. GitHub checks hourly, so actual timing can be later. You can now close the terminal and turn off your computer.

### Already closed setup? Resume here

This skips another Instagram login and takes you through repository selection and the final run menu:

| System | Command |
| --- | --- |
| Windows | `py setup.py --github-only` |
| macOS / Linux | `python3 setup.py --github-only` |

### Run or pause later with GitHub CLI

Replace `YOUR-NAME/YOUR-REPO` with the repository selected in setup.

**Change your picture now:**

```sh
gh workflow run change-dp.yml --repo YOUR-NAME/YOUR-REPO -f mode=rotate
```

**See recent results:**

```sh
gh run list --repo YOUR-NAME/YOUR-REPO --workflow change-dp.yml --limit 5
```

**Pause automatic changes:**

```sh
gh workflow disable change-dp.yml --repo YOUR-NAME/YOUR-REPO
```

**Resume automatic changes:**

```sh
gh workflow enable change-dp.yml --repo YOUR-NAME/YOUR-REPO
```

## Stuck?

| What you see | What to do |
| --- | --- |
| Python command not found | Install Python 3.11+, reopen the terminal, and retry the command for your computer. |
| Cannot create a virtual environment | On Linux, install your distribution's Python venv package. On Windows/macOS, repair Python with pip support. |
| HTTP 429 / Too many requests | Stop repeated attempts. Check Instagram for prompts and wait before retrying on your usual network. There is no guaranteed cooldown. |
| Session expired or login rejected | Open Instagram to resolve prompts, then run full setup again and save the new secret. |
| No repositories listed | Choose **N** to create one, or **M** to enter an existing repository manually. |
| Secret upload failed | Confirm that you own/administer the selected repository and signed into the correct GitHub account. Retry with `--github-only`. |
| Workflow missing or differs from setup | The selected repository has older code. Update its project files on the default branch, then retry with `--github-only`. |
| Workflow failed | Use the `gh run view … --log-failed` command printed by setup to read the failed step. |
| No images or unreadable image | Upload valid PNG/JPG pictures to your repository's `assets/images` folder. |

Instagram can expire sessions or require verification. This uses an unofficial API, so uninterrupted automation is not guaranteed. Existing sessions are reused until rejected; the workflow does not automatically replace your GitHub secret.

<details>
<summary>Advanced: proxy and older installations</summary>

Set `PROXY_URL` as a GitHub Actions secret if you use a stable proxy. Set the same environment variable locally before login. A failed configured proxy stops the run rather than silently switching networks.

This project pins instagrapi 3.2.2 and Pillow 13.0.0. The specific older TLS-related login failure was fixed upstream in [instagrapi 3.0.21](https://github.com/subzeroid/instagrapi/issues/2852); that does not fix every HTTP 429.

If you previously committed a session file, revoke that session and create a new one. Removing the file doesn't erase it from Git history. The old `INSTA_USER` and `INSTA_PASS` secrets are no longer used.

</details>

<details>
<summary>For developers: run tests</summary>

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

Tests use fake clients. Workflow shell tests require Bash; CI runs on Ubuntu. Windows and macOS setup paths have not been tested on physical machines.

</details>

Built with [instagrapi](https://github.com/subzeroid/instagrapi). MIT license.
