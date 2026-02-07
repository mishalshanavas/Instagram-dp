# Instagram Profile Picture Changer

<div align="center">

![PFP Changer](https://github.com/user-attachments/assets/83b23108-116a-4a98-9d53-658ad9dec2a6)
*Demo at 10x speed*

[![Update Instagram DP](https://github.com/mishal-scet/Instagram-dp/actions/workflows/change-dp.yml/badge.svg)](https://github.com/mishal-scet/Instagram-dp/actions/workflows/change-dp.yml)
[![Last Activity](https://img.shields.io/github/last-commit/mishal-scet/Instagram-dp/main?label=Last%20Activity&style=flat-square&color=green)](https://github.com/mishal-scet/Instagram-dp/commits/main)

</div>

> **TL;DR**: Fork this repo, add your pics, set your credentials, enable GitHub Actions — your Instagram DP changes automatically every 3-4 hours. You look active while doing nothing.

## Quick Setup

```
1. Fork → 2. Add pics → 3. Set secrets → 4. Enable Actions → 5. Done
```

### 1. Fork the Repo

Hit the **Fork** button at the top right. That's your copy now.

### 2. Add Your Images

Drop your pictures into `assets/images/`. Name them with numbers — the bot cycles through them in order.

```
assets/images/
├── 1.png
├── 2.png
├── 3.jpg     ← png, jpg, jpeg all work
├── ...
└── 11.png
```

Keep the naming simple: `1.png`, `2.png`, etc. The bot sorts by the number in the filename.

### 3. Add Your Instagram Credentials

Go to **Settings → Secrets and variables → Actions → New repository secret** and add:

| Secret Name | Value |
|---|---|
| `INSTA_USER` | Your Instagram username |
| `INSTA_PASS` | Your Instagram password |

These are encrypted by GitHub and never visible in logs.

### 4. Enable GitHub Actions

Go to the **Actions** tab → Click **"I understand my workflows, go ahead and enable them"**

### 5. That's It

The bot runs automatically every 2 hours. The built-in scheduler decides when to actually change the DP (every 3-4 hours with random variation).

**Can't wait?** Go to **Actions → Update Instagram DP → Run workflow** and set `force_run` to `true`.

## Customization

Edit `data/config.json` to tweak the schedule:

```json
{
  "timezone": "Asia/Kolkata",
  "min_interval_hours": 3,
  "max_interval_hours": 4,
  "random_delay_minutes": 30,
  "weekday_windows": [
    { "start": "07:00", "end": "23:30" }
  ],
  "weekend_windows": [
    { "start": "09:00", "end": "23:30" }
  ],
  "use_random_delays": true
}
```

| Setting | What It Does |
|---|---|
| `timezone` | Your local timezone. Supports `"IST"`, `"EST"`, `"PST"`, `"Asia/Kolkata"`, `"UTC+5.5"`, etc. |
| `min/max_interval_hours` | How long between DP changes (random value within this range) |
| `random_delay_minutes` | Extra jitter added on top (±30 mins by default) |
| `weekday_windows` | Hours when the bot is allowed to run on weekdays |
| `weekend_windows` | Same, but for weekends |
| `use_random_delays` | Set to `false` if you want exact intervals (not recommended) |

## How It Works

GitHub Actions triggers every 2 hours. The Python script then decides whether to actually change the DP based on the schedule.

**Why not just use a cron schedule directly?** Because changing your DP at exactly 00:00, 03:00, 06:00 every day looks robotic. This bot adds randomness so it feels natural.

**What happens on each run:**

1. **Schedule check** — Is it time to change? If not, skip.
2. **Session login** — Reuses your saved Instagram session (no fresh login every time). Follows [instagrapi best practices](https://subzeroid.github.io/instagrapi/usage-guide/best-practices.html) — same device UUIDs, request delays, session persistence.
3. **Change DP** — Picks the next image in rotation, uploads it. Has automatic retry if Instagram is flaky.
4. **Update state** — Saves the new index and schedules the next run.

**Session handling:** Your Instagram session is cached between runs (via GitHub Actions cache), so the bot doesn't do a fresh login every time. This is important — Instagram flags repeated fresh logins as suspicious. The session stays alive across runs, just like keeping the app open on your phone.

**Default schedule:**
- **Weekdays**: 7:00 AM – 11:30 PM
- **Weekends**: 9:00 AM – 11:30 PM
- **Interval**: 3–4 hours + up to ±30 min random variation
- Outside active hours, the bot sleeps automatically

## Troubleshooting

| Problem | Fix |
|---|---|
| Nothing happening | Check the **Actions** tab for errors (red X) |
| Login failed | Double-check `INSTA_USER` and `INSTA_PASS` in repo secrets |
| Rate limited by Instagram | Wait it out. Instagram cools down after a few hours |
| Wrong schedule | Edit `data/config.json` and push |
| Want to trigger manually | Actions → Update Instagram DP → Run workflow → `force_run = true` |

## Project Structure

```
├── .github/workflows/change-dp.yml   ← GitHub Actions workflow
├── assets/images/                     ← Your profile pictures
├── data/
│   ├── config.json                    ← Schedule settings
│   ├── index.txt                      ← Current image position
│   ├── last_run.txt                   ← When the last change happened
│   └── next_scheduled.txt             ← When the next change is due
└── src/
    ├── main.py                        ← Core logic
    ├── time_manager.py                ← Scheduling engine
    └── requirements.txt               ← Python dependencies
```

`data/session.json` (Instagram session) is cached securely via GitHub Actions and excluded from the repo via `.gitignore`.

<div align="center">

**Fork it. Set it. Forget it.**

Built with [instagrapi](https://github.com/subzeroid/instagrapi)

</div>

