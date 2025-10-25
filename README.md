# Instagram Profile Picture Changer

![PFP Changer](https://github.com/user-attachments/assets/83b23108-116a-4a98-9d53-658ad9dec2a6)
*demo at 10x speed*

[![Update Instagram DP](https://github.com/mishalshanavas/Instagram-dp/actions/workflows/change-dp.yml/badge.svg)](https://github.com/mishalshanavas/Instagram-dp/actions/workflows/change-dp.yml)
[![Last DP Change](https://img.shields.io/badge/Last%20DP%20Change-never-red?style=flat-square)](https://github.com/mishalshanavas/Instagram-dp/commits/main)

Tired of manually changing your Instagram profile picture? Let GitHub do it for you. This bot rotates through your images automatically so you can pretend you're more active than you actually are.

## How to Use (The Easy Way)

### 1. Fork This Repository
Click the "Fork" button above. Yes, that green button. You now own a copy.

### 2. Add Your Pictures
Upload your images to `assets/images/` folder:
- Name them `1.png`, `2.png`, `3.png`, etc.
- Don't be creative with naming. The bot isn't that smart.

### 3. Add Your Instagram Credentials
Go to Settings → Secrets and variables → Actions, add:
- `INSTA_USER`: Your Instagram username
- `INSTA_PASS`: Your Instagram password

(Don't worry, GitHub keeps these secret. Probably safer than your browser.)

### 4. Watch the Magic
The bot runs automatically every 3 hours during decent hours (6:30 AM - 11:30 PM IST). 

Want to change your DP right now? Go to Actions tab → "Update Instagram DP" → "Run workflow" → Set force_run to "true".

## When Does It Actually Work?

**Schedule**: Every 3 hours between 6:30 AM and 11:30 PM IST  
**Why these hours**: Because changing your DP at 3 AM looks suspicious  
**Rate limiting**: Minimum 3 hours between changes (Instagram doesn't like spam)  
**Manual override**: Force run bypasses all restrictions when you're impatient  

The bot is smart enough to:
- Skip runs if it just changed your DP
- Only run during human hours
- Handle Instagram's mood swings gracefully
- Keep you logged in between runs

## Troubleshooting

**Nothing happening?** Check the Actions tab for errors  
**Login failed?** Double-check your username/password  
**Rate limited?** Wait it out, Instagram will forgive you eventually  

That's it. Fork, configure, forget. Your Instagram will look active while you binge Netflix.

---

*Disclaimer: Use responsibly. Don't blame us if Instagram gets cranky.*

