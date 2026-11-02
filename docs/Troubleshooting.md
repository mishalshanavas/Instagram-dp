# Troubleshooting

Start with the exact failed step. A successful login does not guarantee a successful profile change. Never post passwords, cookies, session JSON, or verification codes in an issue.

## Python command not found

Install Python 3.11+ and reopen your terminal. On Windows try `py --version`, then `python --version`. On macOS/Linux use `python3 --version`. Make sure the terminal is in the extracted folder containing `setup.py`.

## setup.py cannot be found

You are in the wrong folder. Open the extracted project folder. If it contains one more folder, enter that too. Open the terminal where you can see `setup.py`.

## Cannot create the virtual environment

On Linux, install your distribution's Python venv package. On Windows/macOS, repair Python with pip support. Run setup again. Do not install project packages into the system Python using sudo.

## GitHub CLI installation fails

Install [GitHub CLI](https://cli.github.com/) using its instructions for your system. Reopen the terminal and return to the project folder. Resume with `--github-only` if the Instagram session was already saved. OS administrator approval cannot be bypassed by the wizard.

## Browser cannot be opened

On a VM, open the printed GitHub device-login URL on another device. Enter the printed code, confirm the intended account, and finish authorization. Wait for the terminal to show authentication completion.

## GitHub HTTP 401 / discovery failed

Setup automatically reauthorizes and retries discovery once. If that fails:

```sh
gh auth login --hostname github.com --web
```

Complete authorization, then resume setup with `--github-only`. Environment tokens can override saved gh credentials; automatic recovery uses the browser login in its child processes without changing the shell. A discovery failure is not treated as “no copies.”

## Wrong GitHub account

Check the active account:

```sh
gh api user --jq .login
```

To use a different saved account:

```sh
gh auth switch --hostname github.com --user YOUR-USERNAME
```

If it is not saved, run `gh auth login` first. Resume setup after switching.

## Instagram HTTP 429 / Too many requests

Stop repeated attempts. Open Instagram, resolve prompts, and wait before trying again on your usual network. There is no guaranteed cooldown. A library update may fix a known bug, but it cannot remove every account/IP restriction.

## Instagram login check passes but rotation gets HTTP 403

Instagram may allow account reads while refusing profile changes. Try changing the profile picture manually in the official app and resolve restrictions there. If using browser-session login, try full setup with username/password and save the new secret. The exact cause can be account- or network-related; do not assume it is a password error or repeatedly retry.

## Session expired

Run full setup, complete Instagram login again, and replace the repository secret. `--github-only` reuses your local saved session and cannot repair an expired Instagram session.

## Workflow differs from setup

Your selected copy has older project files. Update its default branch to the current project version, keeping your photos and state, then resume setup. Changing a template does not automatically update existing copies.

## Upload failed

Use 1–100 readable PNG/JPG files under 20 MB each. Check folder paths, branch rules, and repository write permissions. If another process updated the branch during upload, retry the upload after that process finishes. Files are validated before a replacement is committed.

## Workflow failed or could not be watched

Use the specific run ID printed by setup:

```sh
gh run view RUN-ID --repo YOUR-NAME/YOUR-REPO --log-failed
```

Older gh versions may return no run URL; setup looks up the new run automatically. If multiple new runs appear together, it stops rather than guessing. A rotation may have succeeded even if saving state or watching failed; inspect the failed step before repeating it.

## Need to report a bug?

Open an issue with your OS, Python version, `gh --version`, the setup step, and sanitized error text. Remove account credentials and verification codes. Include whether the official Instagram app can perform the same action.


---
[Documentation home](Home.md) · [Project README](../README.md)
