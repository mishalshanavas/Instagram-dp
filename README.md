# Instagram Profile Picture Changer

<div align="center">

![PFP Changer](https://github.com/user-attachments/assets/83b23108-116a-4a98-9d53-658ad9dec2a6)
*Demo at 10x speed*

[![Update Instagram DP](https://github.com/mishal-scet/Instagram-dp/actions/workflows/change-dp.yml/badge.svg)](https://github.com/mishal-scet/Instagram-dp/actions/workflows/change-dp.yml)
[![Last Activity](https://img.shields.io/github/last-commit/mishal-scet/Instagram-dp/main?label=Last%20Activity&style=flat-square&color=green)](https://github.com/mishal-scet/Instagram-dp/commits/main)

</div>

> **TL;DR**: Fork this repo, add your pics, set your credentials, enable github actions(disabled by default in forks) and let GitHub change your Instagram DP every 3 hours. You'll look active while doing absolutely nothing.

## Quick Setup
```
1. Fork → 2. Replace pics → 3. Add secrets → 4. Enable Actions → 5. Chill
```

**Step 1: Fork This Thing**  
Hit that **Fork** button up there ↗️ You now own this bot.

**Step 2: Drop Your Pics**  
Put your images in `assets/images/`:
```
assets/images/
├── 1.png
├── 2.png 
├── ...
└── 11.png
```
> Pro tip: Don't get fancy with names. The bot has trust issues.
(so follow the same nameing scheme)

**Step 3: Secret Stuff**  
**Settings** → **Secrets** → **Actions** → Add these:
- `INSTA_USER` → Your Instagram username  
- `INSTA_PASS` → Your Instagram password

**Step 4: Enable GitHub Actions**  
**Actions** → **I understand my workflows, go ahead and enable them**

**Step 5: Watch It Work**  
Bot runs every 3 hours (6:30 AM - 11:30 PM IST).  
**Impatient?** Force run: **Actions** → **Run workflow** → `force_run = true`

## How It Works

The bot leverages GitHub Actions as a cron scheduler, running Python scripts every 3 hours using the `instagrapi` library for Instagram API interactions. It maintains session persistence through encrypted cookies stored in repository data files, eliminating repeated login overhead. The system implements intelligent rate limiting by tracking execution timestamps and enforcing minimum 3-hour intervals between profile picture changes to avoid Instagram's anti-automation detection. Sleep mode functionality uses IST timezone calculations to pause operations during low-activity hours (11:30 PM - 6:30 AM), while the force run feature bypasses these restrictions via manual workflow dispatch triggers with boolean parameters.

**Smart features:**
- Remembers where it left off • Skips if it just ran • Handles Instagram's mood swings • Keeps you logged in

## When Things Break

```bash
# Nothing happening? → Check Actions tab for red X's
# Login failed? → Double-check username/password  
# Rate limited? → Chill. Instagram will forgive you.
```

<div align="center">

**That's it.** Fork → Setup → Netflix

**Built with** [instagrapi](https://github.com/adw0rd/instagrapi) - The unofficial Instagram API that actually works

*Don't blame us if Instagram gets moody* 🤷‍♂️

</div>

