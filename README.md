# Instagram Profile Picture Changer

<div align="center">

![PFP Changer](https://github.com/user-attachments/assets/83b23108-116a-4a98-9d53-658ad9dec2a6)
*Demo at 10x speed*

[![Update Instagram DP](https://github.com/mishal-scet/Instagram-dp/actions/workflows/change-dp.yml/badge.svg)](https://github.com/mishal-scet/Instagram-dp/actions/workflows/change-dp.yml)

</div>

> Fork this repo, drop your pics, run one command — and your Instagram DP rotates on autopilot every few hours. You'll look active while doing absolutely nothing. Peak efficiency.

## Setup

Five steps. Less effort than choosing an Instagram filter.

```
1. Fork → 2. Add pics → 3. Create session → 4. Add secrets → 5. Enable Actions
```

### 1. Fork this repo

Hit that **Fork** button ↗️ — you now own a bot. Congrats.

### 2. Add your images

Drop them into `assets/images/`:
```
assets/images/
├── 1.png
├── 2.png
├── ...
└── 11.png
```
Name them `1.png`, `2.png`, etc. The bot sorts numerically — don't get creative with filenames, it won't appreciate it.

### 3. Add secrets

**Settings → Secrets and variables → Actions** — add these two:

| Secret | Value |
|--------|-------|
| `INSTA_USER` | Your Instagram username |
| `INSTA_PASS` | Your Instagram password |

These are used for session recovery if the session ever expires. Your secrets are encrypted by GitHub — nobody can see them, not even you (after saving).

### 4. Create a session from your local machine

This is the important part. Instagram gets suspicious when a login comes from a random cloud server in Virginia. So we log in **once** from **your home network** and save the session.

```bash
cd src
pip install instagrapi
```

**Option A — Username & password (simplest)**
```bash
python create_session.py <username> <password>
```

**Option B — Browser session ID (if password login is blocked)**

1. Log in to [instagram.com](https://instagram.com) in your browser
2. Open DevTools: `F12` → **Application** → **Cookies** → `instagram.com`
3. Copy the value of the `sessionid` cookie
4. Run:
```bash
python create_session.py --sessionid <paste_session_id_here>
```

Either way, you should see **"Login successful!"**. Then push the session:
```bash
git add data/session.json
git commit -m "add session"
git push
```

GitHub Actions reuses this trusted session on every run — Instagram thinks it's still you on your couch. Because technically, it is.

> **Session expired?** Just re-run `create_session.py` from your local machine and push again. GitHub Actions will also try to re-login using your secrets as a fallback, preserving device UUIDs so Instagram doesn't freak out.

### 5. Enable GitHub Actions

**Actions tab → "I understand my workflows, go ahead and enable them"**

That's it. Go watch Netflix.

---

## How It Works

1. GitHub Actions wakes up every 4 hours
2. Waits a random 0–45 minutes (so Instagram doesn't see a perfectly timed robot — because that's exactly what it is)
3. Loads your session → validates it → falls back to credential re-login preserving device UUIDs if expired
4. Changes your DP to the next image in the rotation
5. Saves the updated session and index, commits, goes back to sleep

The bot cycles through all your images in order and loops back to the start. It's not complicated, and that's the point.

### Project structure

```
src/main.py             — The script that does the thing
src/create_session.py   — Run once locally to create a trusted session
data/index.txt          — Tracks which image is next
data/session.json       — Your Instagram session (created from your network)
```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Nothing happening | Check the Actions tab for red X's |
| `BadPassword` / IP blacklist | Run `create_session.py` from your **home/mobile** network — cloud & VPN IPs get flagged |
| `unsupported_version` | Already handled — the bot uses Instagram v410 user-agent |
| Session expired | Re-run `create_session.py` locally and push, or let the bot try credential fallback |
| `challenge_required` | Log in to Instagram on your phone/browser, approve any prompts, then re-run `create_session.py` |
| Rate limited | Relax. Instagram will forgive you. Eventually. |
| Still broken | Open an issue — or don't, I'm not your boss |

---

<div align="center">

**Built with** [instagrapi](https://github.com/adw0rd/instagrapi) — the unofficial Instagram API that actually works.

MIT License · Made by [Mishal](https://github.com/mishal-scet)

</div>

