# First setup: follow the prompts

Start with your platform's guide: [Windows](Windows.md), [macOS](macOS.md), or [Linux](Linux.md).

## 1. Connect Instagram

Select **Username and password** for your first login. Enter your username, then password. Asterisks appear instead of the password. In basic terminal mode, entry may be completely invisible.

If asked, enter your verification code. Keep the official Instagram app open so you can approve any login or account-review prompt. Request details shown during login are cleared after success.

**Expected result:** `Login validated. Your private session is saved locally.`

Other choices:

- **Reuse a trusted local session:** for a later setup on this computer. It validates the existing `data/session.json` without a new password login.
- **Browser session:** an advanced cookie-based alternative. It may pass read-only checks while Instagram refuses profile changes. Never paste session cookies into a chat or issue.

If login fails, use [Troubleshooting](Troubleshooting.md). Repeatedly pressing retry is not a rate-limit strategy.

## 2. Connect GitHub

GitHub CLI installs automatically when a supported package manager exists. Complete OS administrator prompts if needed. Then follow browser/device authorization and wait until the terminal says authentication is complete.

If authorization expires later, setup opens sign-in and retries discovery once. During recovery it ignores overriding `GH_TOKEN`/`GITHUB_TOKEN` values in its child processes without changing your shell.

## 3. Choose your repository

Setup searches repositories owned by the signed-in account for copies of this template.

- **Copies exist:** select the one you want. Review the account and repository name.
- **No copies exist:** setup creates a private template copy automatically. If `Instagram-dp` is taken, it tries a numbered name.
- **Discovery failed:** setup will not treat this as an empty account. Read the error and fix access/network issues.
- **Manual copy:** if you uploaded files yourself rather than using a template/fork, select the manual repository option.

A repository is your copy of the project on GitHub. Its files, pictures, workflow runs, and session secret belong there—not in the source template.

## 4. Choose your timezone

Select a listed region or choose **Another timezone**, then enter a name such as `Asia/Kolkata`. Setup validates the timezone and saves it as the repository variable `TIMEZONE`.

This affects displayed times. The underlying random interval is unchanged.

## 5. Save the session

Setup automatically saves `INSTA_SESSION` in the selected repository. The Instagram password is not uploaded. Repository admin access is required.

**Expected result:** `INSTA_SESSION saved. Your Instagram password was not uploaded.`

## 6. Choose your pictures

Select **Add my photos from a folder (recommended)**. Follow [Photos](Photos.md) to select and confirm a complete collection. Cancelling or failing the upload stops setup before requesting a rotation.

Only select **Use the photos already in this repository** if you intend to keep them. A new copy contains solid-color placeholders.

## 7. Watch the check and first rotation

Setup enables the workflow if necessary, runs a read-only login/image check, and displays GitHub Actions progress every three seconds. Older GitHub CLI versions are supported even if dispatch does not return a run URL.

If the check succeeds, setup requests the first rotation automatically. A successful check does not guarantee write permission: Instagram may still refuse a profile change.

**Expected result:** `Your profile picture was updated and the next rotation was scheduled.` Due times appear in your chosen timezone. Scheduled runs are now enabled; your computer can be turned off.

If any run fails, setup stops and provides a safe error summary. It does not automatically retry the profile update.

## Return to settings later

Windows:

```powershell
py setup.py --github-only --manage
```

macOS/Linux:

```sh
python3 setup.py --github-only --manage
```

Choose your repository. The menu lets you replace photos, change timezone, check setup, or rotate manually. If Instagram's session has expired, run full setup without `--github-only` and save a new session.

Omitting `--manage` uses the automatic flow again: photo selection, check, then rotation.


---
[Documentation home](Home.md) · [Project README](../README.md)
