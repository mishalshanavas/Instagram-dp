# Instagram DP

Rotate your Instagram profile picture through your own collection of photos.
Set it up once from your computer; GitHub Actions handles subsequent changes,
even when your computer is off.

![Profile pictures rotating on Instagram — demo shown at 10× speed](https://github.com/user-attachments/assets/83b23108-116a-4a98-9d53-658ad9dec2a6)

*Demo shown at 10× speed. Actual changes are scheduled hours apart.*

[Get started](#get-started) · [Replace photos](#replace-your-photos) · [Schedule](#how-the-schedule-works) · [Troubleshooting](docs/Troubleshooting.md)

Uses [instagrapi](https://github.com/subzeroid/instagrapi), an unofficial Instagram client. Instagram can require verification or reject automated updates; this project cannot guarantee uninterrupted rotation.

## Get started

You need an Instagram account, a [GitHub account](https://github.com/signup),
and **Python 3.11 or newer**. Setup supports Windows, macOS, and Linux.
No Git commands are required.

### 1. Download and open the project

Select **Code → Download ZIP** at the top of this repository, then extract the
ZIP. Open the extracted folder containing `setup.py`—there may be another
folder inside the first one.

You do not need to create a GitHub repository yourself. Setup will create a
private copy under your account, or let you select an existing copy.

### 2. Start setup

Follow the instructions for your computer:

<details open>
<summary><strong>Windows</strong></summary>

1. Install [Python](https://www.python.org/downloads/windows/) if you do not have it. Select **Add Python to PATH** if the installer offers it.
2. In the extracted project folder, click File Explorer's address bar, type `powershell`, and press **Enter**.
3. Paste this command into the window and press **Enter**:

```powershell
py setup.py
```

If `py` is not found, try `python setup.py`. If neither works, follow the
[Windows installation guide](docs/Windows.md).

</details>

<details>
<summary><strong>macOS</strong></summary>

1. Install [Python 3.11 or newer](https://www.python.org/downloads/macos/) if needed.
2. Open **Terminal** using Spotlight (**Command + Space**).
3. Type `cd ` with a space, drag the extracted project folder into Terminal, then press **Enter**.
4. Run:

```sh
python3 setup.py
```

[Detailed macOS instructions](docs/macOS.md). The macOS setup path has not yet
been verified on a physical Mac.

</details>

<details>
<summary><strong>Linux</strong></summary>

Open a terminal in the extracted project folder and run:

```sh
python3 setup.py
```

Python must be version 3.11 or newer, with pip and venv available.
See the [Linux guide](docs/Linux.md) for installation commands and headless VM setup.

</details>

Keep the terminal open while dependencies install. Setup also installs GitHub
CLI when a supported package manager is available; your system may ask for
administrator approval. If automatic installation is unavailable, setup shows
what to install.

### 3. Connect your accounts

Use **↑ / ↓** to choose an option and **Enter** to select it. Basic terminals
show numbered choices instead.

1. **Instagram:** choose **Username and password**, then enter your login details. Complete verification if prompted. Your password is masked and is not uploaded to GitHub.
2. **GitHub:** follow the terminal's browser sign-in instructions. If a browser cannot open, visit the displayed URL on another device and enter the displayed code.
3. **Repository:** select your existing copy, or let setup create a private one if none exists. A repository is where GitHub stores the project and your photos.
4. **Timezone:** choose your region so scheduled times are displayed correctly.

Setup saves your Instagram session in your chosen repository's `INSTA_SESSION`
secret automatically. You do not need to copy credentials into GitHub settings.

### 4. Add your photos

Put the photos you want to rotate through in one folder:

- **1–100 images**, in PNG, JPG, or JPEG format.
- **20 MB or less per image.** Subfolders are not included.
- Square photos work well with Instagram's circular profile crop.

Choose **Add my photos from a folder (recommended)** and paste that folder's
full path. On Windows, copy the path from File Explorer's address bar.

Setup shows how files will be numbered—for example, `portrait.jpg → 1.jpg`.
Review the list and confirm the upload. Your original files stay unchanged.

> The included images are solid-color placeholders. If you choose to keep them,
> your Instagram profile picture will become one of those colors.

### 5. Wait for the first change

**Setup checks your login and photos, then automatically changes your profile
picture if the check passes.** Choose your photos before continuing.

Both runs are shown in the terminal; you do not need to open GitHub Actions.
Progress refreshes every three seconds. A successful rotation ends with:

```text
Your profile picture was updated and the next rotation was scheduled.
```

The terminal also shows the schedule in your selected timezone. You can now
close it and turn off your computer.

If the check passes but the change fails, setup is **not** complete: Instagram
can allow account reads while blocking profile updates. Follow the error shown
in the terminal or the [troubleshooting guide](docs/Troubleshooting.md).

[See every setup prompt and expected result →](docs/First-setup.md)

## Replace your photos

Prepare a folder containing the **complete collection** you want to use,
including any old photos you want to keep. Open a terminal in the project
folder again and run:

**Windows**

```powershell
py setup.py --github-only --manage
```

**macOS / Linux**

```sh
python3 setup.py --github-only --manage
```

Select your repository, choose **Replace photos from a folder**, and follow the
upload prompts. This replaces the repository's current photo collection and
restarts the sequence at the first image. Local originals are untouched.

The next scheduled rotation uses the new collection. To use it immediately,
choose **Change your profile picture now** from the menu.

Files uploaded through setup are numbered automatically, preserving their
extensions. Files uploaded directly on GitHub keep their filenames.
[Photo ordering and replacement details →](docs/Photos.md)

## How the schedule works

After each successful change, a random **2–5 hour** interval sets the next due
time. GitHub checks once an hour, at **17 minutes past the hour UTC**, and
changes the picture when that time has passed.

For example, if a picture is due at **14:40 UTC**, the next scheduled check is
**15:17 UTC**. GitHub may delay that run further. This is an approximate
schedule, not an exact timer.

Photos are used in sequence; after the last one, rotation starts again at the
first. Your timezone changes the displayed times, not the rotation interval.

Use the same management command above to change your timezone, check setup,
or request a rotation. [Schedule details and how to pause rotation →](docs/Scheduling.md)

## Your account and photos

- Your Instagram password stays on your computer. The saved **session is also a credential**: never share or commit `data/session.json`.
- Setup uploads the session to a GitHub Actions secret so the workflow can sign in. If Instagram expires it, run `setup.py` again to renew it.
- Photos in a public repository are public. Replacing photos does not remove their old versions from Git history.
- Automation runs in **your copy**. Actions are disabled in this source template.

[Session storage and account safety →](docs/Account-safety.md)

## Help and documentation

| What you need | Guide |
| --- | --- |
| Installation, step by step | [Windows](docs/Windows.md) · [macOS](docs/macOS.md) · [Linux](docs/Linux.md) |
| Help with a setup prompt | [First setup](docs/First-setup.md) |
| Image formats, ordering, and replacement | [Photos](docs/Photos.md) |
| Timezones, manual runs, and pausing | [Scheduling](docs/Scheduling.md) |
| Login errors or a failed workflow | [Troubleshooting](docs/Troubleshooting.md) |
| Running tests or contributing code | [Development](docs/Development.md) |

If you open an issue, include your operating system, Python version, and the
failed step. Remove passwords, verification codes, cookies, and session data
from anything you share.

## License

[MIT](LICENSE)
