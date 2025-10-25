# Instagram Profile Picture Changer

![PFP Changer](https://github.com/user-attachments/assets/83b23108-116a-4a98-9d53-658ad9dec2a6)

[![Update Instagram DP](https://github.com/mishalshanavas/Instagram-dp/actions/workflows/change-dp.yml/badge.svg)](https://github.com/mishalshanavas/Instagram-dp/actions/workflows/change-dp.yml)
[![Last DP Change](https://img.shields.io/badge/Last%20DP%20Change-never-red?style=flat-square)](https://github.com/mishalshanavas/Instagram-dp/commits/main)

A Python application that automatically rotates your Instagram profile picture using GitHub Actions. No servers needed - just set it up once and let GitHub handle the rest.

## Current Status

> **🔄 Active Rotation**: Check the [Actions tab](../../actions) to see the latest runs  
> **📊 Stats**: Monitor profile picture changes and system health  
> **⏰ Next Run**: Scheduled every 3 hours during active hours (6:30 AM - 11:30 PM IST)

## Features

- **GitHub Actions Automation**: Runs completely on GitHub's infrastructure
- **Smart Scheduling**: Automatic profile picture changes every 3 hours
- **Manual Triggers**: Force immediate changes when you want
- **Time-aware**: Only runs during reasonable hours (6:30 AM - 11:30 PM IST)
- **Rate Limited**: Built-in cooldown to prevent Instagram restrictions
- **Session Persistence**: Maintains login sessions between runs
- **Error Recovery**: Robust error handling and logging

## Project Structure

```
Instagram-dp/
├── src/                    # Source code and dependencies
│   ├── main.py            # Main application logic
│   └── requirements.txt   # Python dependencies
├── assets/images/         # Your profile pictures (1.png, 2.png, etc.)
├── data/                  # Runtime data (auto-managed by GitHub Actions)
├── .github/workflows/     # GitHub Actions configuration
└── README.md             # This file
```

## Getting Started

The easiest way to use this is through GitHub Actions - no local setup required!

### 1. Fork This Repository

Click the "Fork" button at the top of this page to create your own copy.

### 2. Add Your Profile Pictures

Upload your images to the `assets/images/` folder:
- Name them sequentially: `1.png`, `2.png`, `3.png`, etc.
- Supported formats: PNG, JPG, JPEG
- Instagram recommends 320x320 pixels for best quality

### 3. Configure GitHub Secrets

This is the most important step. Go to your repository's Settings → Secrets and variables → Actions, and add:

- **INSTA_USER**: Your Instagram username
- **INSTA_PASS**: Your Instagram password

### 4. Enable GitHub Actions

That's it! The workflow will start running automatically. Check the Actions tab to see it in action.

## How It Works

### Automatic Schedule
- Runs every 3 hours during active hours (6:30 AM - 11:30 PM IST)
- Uses UTC cron schedule: `"0 1,4,7,10,13,16 * * *"`
- Automatically skips runs that are too close together (3-hour minimum gap)

### Manual Control
Want to change your profile picture right now? Go to Actions → "Update Instagram DP" → "Run workflow":
- **Normal run**: Respects time windows and rate limits
- **Force run**: Bypasses all restrictions for immediate change

### Smart Rate Limiting
The system prevents Instagram from flagging your account by:
- Enforcing minimum 3-hour gaps between changes
- Only running during reasonable hours
- Maintaining persistent login sessions
- Graceful error handling and retries

## GitHub Actions Configuration

The workflow is in `.github/workflows/change-dp.yml`. You can customize:

```yaml
# Change the schedule (currently every 3 hours)
- cron: "0 1,4,7,10,13,16 * * *"

# Modify time windows (currently 6:30 AM - 11:30 PM IST)
if [ "$current_hour" -ge 6 ] && [ "$current_hour" -lt 23 ]

# Adjust rate limiting (currently 3 hours = 10800 seconds)
min_interval=10800
```

## Local Development (Optional)

If you want to test locally before deploying:

```bash
git clone https://github.com/yourusername/Instagram-dp.git
cd Instagram-dp
pip install -r src/requirements.txt

export USERNAME="your_username"
export PASSWORD="your_password"
python src/main.py
```

## Monitoring

### GitHub Actions Dashboard
- Check the **Actions tab** for run history and logs
- Each run shows detailed output including success/failure reasons
- Failed runs include error messages for easy debugging

### Current State
- Monitor `data/index.txt` to see which image is current
- Check `data/last_run.txt` for the last successful execution time

## Security

Your Instagram credentials are stored as GitHub Secrets, which are:
- Encrypted and only accessible to your repository
- Never exposed in logs or workflow outputs
- Automatically injected as environment variables during runs

## Troubleshooting

**Workflow not running?**
- Check that GitHub Actions is enabled in your repository settings
- Verify your secrets are correctly named: `INSTA_USER` and `INSTA_PASS`

**Login failures?**
- Double-check your username and password
- If you have 2FA enabled, you might need an app-specific password

**Rate limited by Instagram?**
- The system is designed to prevent this, but if it happens, just wait
- Instagram restrictions are usually temporary (a few hours)

**Images not found?**
- Ensure images are in `assets/images/` folder
- Check that they're named correctly: `1.png`, `2.png`, etc.

## Contributing

Found a bug or want to add a feature? Pull requests are welcome! This project aims to be simple and reliable.

## License

MIT License - feel free to use this for your own projects.

---

**Disclaimer**: This tool is for personal use. Please use responsibly and in accordance with Instagram's Terms of Service. Automated interactions should always respect platform guidelines.

