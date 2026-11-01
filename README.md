# Instagram Profile Picture Changer

Rotate your Instagram profile picture through a folder of photos using GitHub Actions.

**Works on Windows, macOS, and Linux.** You need a GitHub account and Python 3.11 or newer on your computer. No Git commands required.

Your computer is needed for setup and session renewal. The scheduled bot runs on GitHub Actions, so you can turn your computer off afterward.

 Instagram may ask you to verify a login or renew your session; this is unofficial automation, not a guarantee of uninterrupted updates.

## 1. Make your own copy and add photos

Click **Use this template → Create a new repository** if available, or **Fork**. Choose a private repository when creating from a template if you do not want your photos public. A fork may inherit the source repository's visibility.

In your copy, open **assets/images → Add file → Upload files**. Upload PNG or JPG pictures named `1.png`, `2.png`, `3.png`, etc., then click **Commit changes**. Delete the sample pictures you do not want in the rotation using GitHub's file menu. Numeric names run first in numerical order, followed by other names alphabetically.

## 2. Run guided setup on your computer

In **your copy**, click **Code → Download ZIP** and extract it. Install [Python 3.11+](https://www.python.org/downloads/) if needed (on Windows, enable **Add Python to PATH**).

Open a terminal in the extracted folder containing `setup.py` (not inside `src`):

- **Windows:** open the folder in File Explorer, type `powershell` in the address bar, and press Enter.
- **macOS:** open Terminal, type `cd ` (with a trailing space), drag the extracted folder into Terminal, and press Enter.
- **Linux:** open the folder in your file manager and choose **Open in Terminal**, or use `cd` to enter it.

Run the command for your computer:

| Computer | Command |
| --- | --- |
| Windows | `py setup.py` |
| macOS | `python3 setup.py` |
| Linux | `python3 setup.py` |

If Windows cannot find `py`, try `python setup.py`. Reopen the terminal after installing Python. You do not need WSL, Docker, or a Linux computer.

The wizard installs its dependencies, clears the screen after a successful installation in an interactive terminal, then shows:

```text
1. Username and password
2. Browser session
3. Reuse a trusted local session (no password login)
0. Exit
```

Option 3 validates the existing local session without another password login. Never reuse a session that was exposed in Git history. Installation errors stay visible, and redirected logs are not cleared.

The wizard asks for your Instagram login and validates it. Passwords and verification codes are hidden while you type. It supports password login, a two-factor code prompt, supported email/SMS challenges, and a browser-session option. Some Instagram challenges must be completed in the Instagram app before retrying.

After Instagram login, the wizard handles GitHub setup:

1. Detects **GitHub CLI (`gh`)** and offers to install it if a supported package manager is available (see below). You do not need GitHub CLI installed before starting.
2. Starts [GitHub browser sign-in](https://cli.github.com/manual/gh_auth_login) if needed. Follow the displayed device code instructions.
3. Lists forks and template-created copies of `mishal-scet/Instagram-dp` owned by your signed-in account in a numbered picker. Select a copy by number, or press **Enter** to choose the first non-archived copy marked `[default]`. Choose **N** to create a new copy even when others exist, **M** to enter a repository manually, or **0** to exit. When no usable copies exist, Enter opens the creation flow; creation still asks for the required choices before creating anything. The source repository is also listed if you own it. Archived copies are shown but cannot be selected.
   Discovery checks all repository pages and GitHub provenance metadata; renamed copies are supported. Copies made by manually uploading files may not have provenance and must be selected manually.
   New copies use GitHub templates with a choice of private/public visibility. If the source is not marked as a template, the wizard explains that and offers a fork instead. It never changes the source repository settings. Repository admin access is checked before saving secrets.
4. Shows the target repository and saves **INSTA_SESSION** after you confirm. No copying JSON into GitHub required.
5. Offers to start the workflow in **check** mode and gives you the results link. A dispatched check is not a passed check—read its result.

GitHub CLI installation options:

| System | Installer used by the wizard | If the installer is unavailable |
| --- | --- | --- |
| Windows | Winget | Install GitHub CLI from [its official site](https://cli.github.com/), then reopen PowerShell. |
| macOS | Homebrew, if already installed | Follow the [official GitHub CLI installation instructions](https://cli.github.com/), then reopen Terminal. |
| Linux | apt, dnf, or pacman, if available | Follow the [official GitHub CLI installation instructions](https://cli.github.com/) for your distribution. |

The wizard does not install the package manager itself. Installation may request administrator access; if it fails, use the official instructions or the manual secret steps printed by the wizard.

If GitHub setup is interrupted, resume without another Instagram login:

| System | Retry command |
| --- | --- |
| Windows | `py setup.py --github-only` |
| macOS / Linux | `python3 setup.py --github-only` |

Manual secret instructions remain available if you skip CLI installation or cannot sign in.

**Never upload or commit `data/session.json`.** It contains login credentials. The file is ignored by Git, and your Instagram password is not needed in GitHub Secrets.

## 3. Check setup, then start

Open **Actions** in your repository. Enable workflows if prompted.

If the wizard already started a check, open its results link. Otherwise, choose **Update Instagram DP → Run workflow → mode: check → Run workflow**. Open that run and read its summary. A successful check validates login and images without changing your picture.

Then run again with **mode: rotate** for your first picture change. Scheduled runs also rotate automatically: once Actions is enabled, they can run before your manual check. To pause automation, use **Update Instagram DP → … → Disable workflow**.

Actions checks hourly, at minute 17, and changes the picture when the next randomized 2–5 hour interval is due. Hourly checks round this up and GitHub can delay runs. There is no exact-time guarantee. Workflows run on the repository's default branch.

## When something fails

| Message / problem | What to do |
| --- | --- |
| Python command not found | Install Python; on Windows try `py`, on macOS/Linux try `python3`. |
| Python cannot create a virtual environment | On Linux, install your distribution's Python venv package. On Windows/macOS, repair or reinstall Python with pip support. Then rerun setup. |
| Missing INSTA_SESSION | Complete step 2 in the same repository where Actions is running. |
| HTTP 429 / Too many requests | Stop login attempts and wait; check Instagram for verification prompts. Setup disables transport retries and preserves the previous session. See the rate-limit notes below. |
| Login/session cannot be validated | Open Instagram, resolve prompts, then rerun setup and replace the secret. |
| Verification is not supported | Complete it in Instagram and retry; the browser-session option may also work. |
| No pictures / unreadable image | Upload valid PNG/JPG files to `assets/images`, removing broken files. |
| GitHub CLI cannot save secret | Confirm admin access to your own repository, then use the GitHub retry command for your system above. |
| Update succeeds but Git push fails | Check branch rules and Actions write permissions; the image may already have changed, and the next run may repeat it. |
| Scheduled run does not appear | Confirm workflows are enabled on the default branch; inspect the latest run summary. GitHub may delay or disable inactive schedules. |

### HTTP 429 during login

The specific fresh-login failure in [instagrapi issue #2852](https://github.com/subzeroid/instagrapi/issues/2852) was fixed in **3.0.21** by requiring TLS 1.3 in the default private curl transport ([upstream fix](https://github.com/subzeroid/instagrapi/pull/2862)). This project now pins **instagrapi 3.2.2** and **Pillow 13.0.0**. Rerun the setup command for your platform to install the updated dependencies; no custom TLS patch or extra transport package is needed.

This fixes a known cause, not every possible HTTP 429. If it continues after updating, stop repeated attempts, check Instagram for verification prompts, and follow [instagrapi's rate-limit guidance](https://subzeroid.github.io/instagrapi/latest/usage-guide/best-practices/). Use a consistent network and device identity; there is no guaranteed cooldown. A trusted saved session may avoid a fresh password login, but browser cookies are not guaranteed to work with Instagram's private mobile API.

The wizard stops on rate limits instead of automatically switching login methods. Failed validation never overwrites your saved session. If you already have a validated local session and only need to configure GitHub, use the `--github-only` command above.

### How sessions are renewed

The workflow reads `INSTA_SESSION` into memory and never commits it, caches it, or uploads it as an artifact. Each run starts from that saved secret. It intentionally does **not** update GitHub secrets automatically: when Instagram expires or rejects the session, rerun the local wizard to replace it. Local rotations save refreshed settings to the ignored local file.

If you used an older version that committed `data/session.json`, **revoke that Instagram session and create a new one**. Untracking the file does not erase credentials from earlier commits or forks. Old `INSTA_USER` and `INSTA_PASS` repository secrets are no longer used and can be removed.

### Optional advanced setup: proxy

Set `PROXY_URL` as an Actions secret if you need a stable proxy, for example `http://user:password@host:port`. Use the same proxy locally by setting the `PROXY_URL` environment variable before setup. The client uses the configured proxy for its authenticated validation and update. A failed proxy stops the run; it does not silently switch networks. Proxy URLs are never printed by project code.

### Development and tests

These commands are for contributors; normal setup only needs the wizard above.

**Windows (PowerShell):**

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

**macOS / Linux:**

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m unittest discover -s tests -v
```

No virtual-environment activation is required. Tests use fake clients; they never log into Instagram or change a profile. The workflow shell tests require Bash and are intended for Linux/CI; use `-p 'test_app.py'` instead of `-v` to run just the core application tests on a Windows machine without Bash.

For a real authenticated check without changing your picture:

| System | Command |
| --- | --- |
| Windows | `.\.venv\Scripts\python.exe src/main.py --check` |
| macOS / Linux | `.venv/bin/python src/main.py --check` |

A valid session is required. Automated CI currently runs on Ubuntu; Windows and macOS setup paths have not been verified on physical machines.

| File | Purpose |
| --- | --- |
| `setup.py` | One-command dependency installation and wizard launcher |
| `src/create_session.py` | Interactive login and GitHub secret setup |
| `src/main.py` | Validate setup or rotate pictures |
| `src/github_setup.py` | GitHub CLI installation, browser sign-in, secret upload, and workflow check |
| `src/session_utils.py` | Shared client and private local session handling |
| `data/index.txt` | Next image position |
| `data/next_run.txt` | Next due time; generated after a successful scheduled/manual rotation |

Built with [instagrapi](https://github.com/subzeroid/instagrapi). MIT license.
