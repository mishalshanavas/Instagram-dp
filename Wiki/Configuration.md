# Commands and configuration

Use this reference when you need to change setup behavior or diagnose which credentials a run uses. Start with [First setup](First-setup.md) for the guided path.

## Setup commands

Run these from the project folder. On Windows replace `python3` with `py`.

```sh
python3 setup.py
python3 setup.py --github-only
python3 setup.py --github-only --manage
```

| Option | Effect |
| --- | --- |
| No flags | Authenticate Instagram, configure GitHub, choose photos, check, then rotate |
| `--github-only` | Reuse the local session file without a new Instagram login; continue through automatic setup |
| `--manage` | Open the management menu instead of automatically checking and rotating |

`--github-only` requires a saved local session. It does not renew an expired Instagram session.

## Runner interface

For development or a deliberate local run, use the virtual environment created by setup:

```sh
.venv/bin/python src/main.py --check
```

On Windows use `.venv\Scripts\python.exe src/main.py --check`.
Without `--check`, the runner changes the profile picture. Local execution advances the image index but does **not** schedule a GitHub run: the workflow owns scheduling.

## Credentials and environment

| Name | Where used | Meaning |
| --- | --- | --- |
| `INSTA_SESSION` | Actions secret; runner environment | Required saved Instagram settings JSON in Actions. Locally takes precedence over `data/session.json` |
| `PROXY_URL` | Optional Actions secret or local environment | Passed to instagrapi's proxy configuration; no automatic proxy provisioning |
| `TIMEZONE` | Repository variable | IANA timezone for displayed due times; defaults to UTC |
| `DP_PLAIN` | Local environment | Any nonempty value selects basic terminal prompts |
| `GH_TOKEN`, `GITHUB_TOKEN` | GitHub CLI environment | May override saved CLI authentication; setup recovery ignores them in its child processes |

Do not place secrets in command examples, commits, or issue reports. The wizard saves `INSTA_SESSION` through standard input. A local proxy setting is not automatically uploaded to GitHub.

For an optional Actions proxy, create a repository secret named `PROXY_URL` through GitHub's secret settings. Check your proxy provider's supported URL format and [instagrapi proxy documentation](https://subzeroid.github.io/instagrapi/latest/usage-guide/interactions/) before use.

## Persistent files

| Path | Meaning |
| --- | --- |
| `assets/images/` | Top-level PNG/JPG/JPEG collection |
| `data/index.txt` | Zero-based position of the next photo; invalid/missing values fall back to zero |
| `data/next_run.txt` | Unix timestamp checked by the scheduled workflow |
| `data/session.json` | Ignored local credential file; never upload it as a normal repository file |

Timezone changes affect display only. See [Scheduling](Scheduling.md) and [Account safety](Account-safety.md).
