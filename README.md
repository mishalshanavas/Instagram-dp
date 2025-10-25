# Instagram Profile Picture Changer

<div align="center">

![PFP Changer](https://github.com/user-attachments/assets/83b23108-116a-4a98-9d53-658ad9dec2a6)

*Demo at 10x speed*

[![Update Instagram DP](https://github.com/mishalshanavas/Instagram-dp/actions/workflows/change-dp.yml/badge.svg)](https://github.com/mishalshanavas/Instagram-dp/actions/workflows/change-dp.yml)
[![Last Activity](https://img.shields.io/github/last-commit/mishalshanavas/Instagram-dp?label=Last%20Activity&style=flat-square&color=green)](https://github.com/mishalshanavas/Instagram-dp/commits/main)

</div>

---

> **TL;DR**: Fork this repo, add your pics, set your credentials, and let GitHub change your Instagram DP every 3 hours. You'll look active while doing absolutely nothing.

##  Quick Setup

```
1. Fork → 2. Upload pics → 3. Add secrets → 4. Chill
```

### Step 1: Fork This Thing
Hit that **Fork** button up there ↗️ You now own this bot.

### Step 2: Drop Your Pics
Put your images in `assets/images/`:
```
assets/images/
├── 1.png
├── 2.png 
└── ...
```
> Pro tip: Don't get fancy with names. The bot has trust issues.

### Step 3: Secret Stuff
**Settings** → **Secrets** → **Actions** → Add these:
- `INSTA_USER` → Your Instagram username  
- `INSTA_PASS` → Your Instagram password

### Step 4: Watch It Work
Bot runs every 3 hours (6:30 AM - 11:30 PM IST). 

**Impatient?** Force run: **Actions** → **Run workflow** → `force_run = true`

---

## ⚡ How It Works

| What | When | Why |
|------|------|-----|
| **Auto mode** | Every 3 hours | Set it and forget it |
| **Sleep mode** | 11:30 PM - 6:30 AM | Nobody changes DP at 3 AM |
| **Rate limit** | 3+ hour gaps | Instagram gets cranky otherwise |
| **Force mode** | Anytime you want | Because patience is overrated |

**Smart features:**
- Remembers where it left off
- Skips if it just ran
- Handles Instagram's mood swings
- Keeps you logged in

---

## 🔧 When Things Break

```bash
# Nothing happening?
→ Check Actions tab for red X's

# Login failed?  
→ Double-check username/password

# Rate limited?
→ Chill. Instagram will forgive you.
```

---

<div align="center">

**That's it.** Fork → Setup → Netflix

---

**Built with** [instagrapi](https://github.com/adw0rd/instagrapi) - The unofficial Instagram API that actually works

*Don't blame us if Instagram gets moody* 🤷‍♂️

</div>

