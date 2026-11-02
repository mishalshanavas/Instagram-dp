# Scheduling and timezone

## How rotation works

1. A successful rotation advances to the next image.
2. The workflow chooses a random interval from 2 to 5 hours and stores the due timestamp in `data/next_run.txt`.
3. GitHub's schedule runs hourly at minute 17 UTC.
4. Each scheduled run checks the due timestamp. It skips the change if the time has not arrived.
5. Due images rotate in sequence and wrap back to the first one.

This is not an exact-time scheduler. Hourly checks round the interval up, and GitHub can delay scheduled runs. For example, a rotation due at 16:30 IST is first eligible at the 16:47 IST check.

`check` mode validates without changing the picture or advancing the image index. A manual `rotate` runs immediately and schedules a new interval after success.

## Choose or change timezone

First setup asks for your timezone. To change it later, run setup with `--github-only --manage`, select the repository, then **Change timezone**.

Select a region or enter an IANA name such as:

- `Asia/Kolkata`
- `Europe/London`
- `America/New_York`
- `Australia/Sydney`

The choice is stored in the repository variable `TIMEZONE`. Missing/invalid display settings fall back to UTC. Daylight-saving offsets follow the date. GitHub's cron and the actual due timestamp remain UTC-based; the timezone changes display, not rotation frequency.

## Pause or resume from your terminal

Replace `YOUR-NAME/YOUR-REPO` with your selected copy's name:

```sh
# Pause
gh workflow disable change-dp.yml --repo YOUR-NAME/YOUR-REPO

# Resume
gh workflow enable change-dp.yml --repo YOUR-NAME/YOUR-REPO

# Recent runs
gh run list --repo YOUR-NAME/YOUR-REPO --workflow change-dp.yml --limit 5

# Read-only check
gh workflow run change-dp.yml --repo YOUR-NAME/YOUR-REPO -f mode=check

# Rotate immediately
gh workflow run change-dp.yml --repo YOUR-NAME/YOUR-REPO -f mode=rotate
```

Enabling a workflow activates scheduled runs too. Closing the setup terminal does not stop them. To pause, disable the workflow.


---
[Documentation home](Home.md) · [Project README](../README.md)
