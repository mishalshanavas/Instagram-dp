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

### 3. Create a session from your local machine

This is the important part. Instagram gets suspicious when a login comes from a random cloud server in Virginia. So we log in once from **your actual network** and save the session.

```bash
cd src
pip install instagrapi
```

**Option A — Browser session ID (recommended, no password needed):**
```bash
python create_session.py --sessionid <your_sessionid>
```
Get your session ID: F12 → Application → Cookies → `instagram.com` → copy `sessionid` value.

**Option B — Username & password:**
```bash
python create_session.py <username> <password>
```

Then push the saved session:
```bash
git add data/session.json
git commit -m "add session"
git push
```

GitHub Actions reuses this trusted session on every run — Instagram thinks it's still you on your couch. Because technically, it is.

### 4. Add secrets

**Settings → Secrets and variables → Actions** — add these:

| Secret | Required | Value |
|--------|----------|-------|
| `INSTA_USER` | Yes | Your Instagram username |
| `INSTA_PASS` | Yes | Your Instagram password |
| `PROXY_URL` | No | Your Squid proxy URL (see below) |

`INSTA_USER` and `INSTA_PASS` are only used as a fallback if the session ever expires. Your secrets are encrypted by GitHub — nobody can see them, not even you (after saving).

### 5. Enable GitHub Actions

**Actions tab → "I understand my workflows, go ahead and enable them"**

That's it. Go watch Netflix.

---

## How It Works

1. GitHub Actions wakes up **every hour** to check if it's time to run
2. Compares current time against `data/next_run.txt` — skips the run if not due yet
3. Reuses the session you created locally — no suspicious cloud logins
4. Changes your DP to the next image in the rotation
5. Picks a **random 2–5 hour interval** for the next run, saves it, commits everything, goes back to sleep

The bot cycles through all your images in order and loops back to the start. It's not complicated, and that's the point.

### Project structure

```
src/main.py             — The script that does the thing
src/create_session.py   — Run once locally to create a trusted session
data/index.txt          — Tracks which image is next
data/session.json       — Your Instagram session (created from your network)
data/next_run.txt       — Unix timestamp of the next scheduled run
```

---

## Optional: Home Proxy

If you have a **Squid proxy** running at home (e.g. on a Raspberry Pi), you can route all Instagram traffic through your home IP. This makes every request look like it's coming from the same network where the session was created.

Add a `PROXY_URL` secret:

| Secret | Example value |
|--------|---------------|
| `PROXY_URL` | `https://proxy.yourdomain.com` |

The workflow checks if the proxy is reachable before each run. If your server is down or the secret is not set, the bot falls back to a direct connection automatically — no failures, no manual intervention needed.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Nothing happening | Check the Actions tab for red X's |
| Login failed | Double-check `INSTA_USER` / `INSTA_PASS` secrets |
| Session expired | Run `python create_session.py` locally again and push |
| Rate limited | Relax. Instagram will forgive you. Eventually. |
| Still broken | Open an issue — or don't, I'm not your boss |

---

<div align="center">

**Built with** [instagrapi](https://github.com/adw0rd/instagrapi) — the unofficial Instagram API that actually works.

MIT License · Made by [Mishal](https://github.com/mishal-scet)

</div>

