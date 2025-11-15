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
Bot runs automatically with smart scheduling (3-4 hour intervals with random delays).  
**Impatient?** Force run: **Actions** → **Run workflow** → `force_run = true`

## Customization

Want to customize the schedule? Edit `data/config.json`:

```json
{
  "timezone": "Asia/Kolkata",       // Your timezone (see options below)
  "min_interval_hours": 3,          // Minimum time between changes
  "max_interval_hours": 4,          // Maximum time between changes
  "random_delay_minutes": 30,       // Random jitter (±30 mins)
  "weekday_windows": [              // Active hours on weekdays
    {"start": "07:00", "end": "23:30"}
  ],
  "weekend_windows": [              // Active hours on weekends
    {"start": "09:00", "end": "23:30"}
  ],
  "preferred_hours": [9, 12, 15, 18, 21],  // Peak activity hours
  "use_random_delays": true,        // Enable random delays
  "avoid_patterns": true            // Avoid predictable timing
}
```

**Timezone Options:**
You can use any of these formats:
- **Named timezones**: `"Asia/Kolkata"`, `"IST"`, `"EST"`, `"PST"`, `"JST"`, `"GMT"`, `"UTC"`
- **UTC offset**: `"UTC+5.5"`, `"UTC-8"`, `"UTC+0"`
- **Common abbreviations**:
  - `IST` - India Standard Time (UTC+5.5)
  - `EST`/`EDT` - US Eastern (UTC-5/-4)
  - `PST`/`PDT` - US Pacific (UTC-8/-7)
  - `CST`/`CDT` - US Central (UTC-6/-5)
  - `JST` - Japan (UTC+9)
  - `AEST` - Australia Eastern (UTC+10)
  - `CET`/`CEST` - Central European (UTC+1/+2)

**What you can customize:**
- 🌍 **Timezone** - Set your local timezone for accurate scheduling
- ⏰ Active time windows (different for weekdays/weekends)
- ⏱️ Interval between changes (min/max hours)
- 🎲 Randomization amount (±minutes)
- 📊 Preferred hours (when changes are more likely)
- 🎯 Pattern avoidance behavior

## How It Works

The bot uses **intelligent time management** with human-like patterns to avoid detection:

**Smart Scheduling Features:**
- 🎲 **Random Delays**: Each run is scheduled 3-4 hours apart, plus ±30 minutes of randomization
- ⏰ **Preferred Hours**: More likely to change DP during peak hours (9 AM, 12 PM, 3 PM, 6 PM, 9 PM)
- 📅 **Weekend Mode**: Different active hours for weekdays vs weekends
- 🌙 **Sleep Mode**: Automatically pauses between 11:30 PM - 7:00 AM
- 🎯 **Pattern Avoidance**: Never runs at exactly the same time twice
- ⚡ **Force Run**: Manual override to bypass all timing restrictions

**Technical Implementation:**
- Uses GitHub Actions as cron scheduler (runs every 2 hours)
- Python `TimeManager` class handles all scheduling logic
- Session persistence via encrypted cookies in `data/session.json`
- Maintains state across runs with tracking files:
  - `last_run.txt` - Timestamp of last successful change
  - `next_scheduled.txt` - When the next change should occur
  - `config.json` - Customizable time windows and behavior
  - `index.txt` - Current position in image rotation

**Default Schedule:**
- **Weekdays**: Active 7:00 AM - 11:30 PM IST
- **Weekends**: Active 9:00 AM - 11:30 PM IST  
- **Interval**: 3-4 hours between changes (with random variation)
- **Daily Limit**: Maximum 8 profile picture changes per day

## When Things Break

```bash
# Nothing happening? → Check Actions tab for red X's
# Login failed? → Double-check username/password  
# Rate limited? → Chill. Instagram will forgive you.
# Want different schedule? → Edit data/config.json
# Changes not happening? → Check data/next_scheduled.txt for next run time
```

## Advanced Usage

**Check current schedule status:**
The bot logs detailed schedule info on every run. Check the Actions logs to see:
- Current time and timezone
- Active window status
- Time since last run
- Next scheduled run time
- All configuration settings

**Understanding the files:**
- `data/config.json` - Your schedule preferences
- `data/last_run.txt` - Unix timestamp of last successful change
- `data/next_scheduled.txt` - Unix timestamp of next scheduled change
- `data/index.txt` - Current image index (0-10)
- `data/session.json` - Instagram session data (auto-managed)

<div align="center">

**That's it.** Fork → Setup → Netflix

**Built with** [instagrapi](https://github.com/adw0rd/instagrapi) - The unofficial Instagram API that actually works

*Don't blame us if Instagram gets moody* 🤷‍♂️

</div>

