# Instagram Profile Picture Changer

[![Update Instagram DP](https://github.com/mishalshanavas/Instagram-dp/actions/workflows/change-dp.yml/badge.svg)](https://github.com/mishalshanavas/Instagram-dp/actions/workflows/change-dp.yml)

A professional Python application that automatically rotates your Instagram profile picture using a collection of images. Optimized for serverless execution via GitHub Actions.

## ✨ Features

- **Automated Rotation**: Cycles through multiple profile images automatically
- **Serverless Ready**: Optimized for GitHub Actions (no server required)
- **Smart Scheduling**: Runs at configurable intervals with rate limiting
- **Session Management**: Persistent login sessions to minimize Instagram API calls
- **Error Handling**: Robust error handling and logging
- **Time Zone Aware**: Respects IST timezone for scheduling
- **State Persistence**: Maintains rotation state between runs

## 🏗️ Project Structure

```
Instagram-dp/
├── src/                    # Source code
│   └── main.py            # Main application logic
├── assets/                # Static assets
│   └── images/           # Profile pictures (1.png, 2.png, etc.)
├── data/                  # Runtime data (auto-generated)
│   ├── index.txt         # Current image index
│   └── session.json      # Instagram session data
├── .github/
│   └── workflows/
│       └── change-dp.yml # GitHub Actions workflow
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🚀 Quick Start

### 1. Fork & Clone

```bash
git clone https://github.com/yourusername/Instagram-dp.git
cd Instagram-dp
```

### 2. Add Your Images

Add your profile pictures to `assets/images/`:
- Name them sequentially: `1.png`, `2.png`, `3.png`, etc.
- Supported formats: PNG, JPG, JPEG
- Recommended size: 320x320 pixels

### 3. Configure Secrets

In your GitHub repository, go to Settings → Secrets and variables → Actions, and add:

- `INSTA_USER`: Your Instagram username
- `INSTA_PASS`: Your Instagram password

### 4. Enable GitHub Actions

The workflow is pre-configured to run automatically. Check `.github/workflows/change-dp.yml` for scheduling details.

## ⚙️ Configuration

### Scheduling

The default schedule runs every 3 hours between 6:30 AM and 11:30 PM IST:
- Cron: `"0 1,4,7,10,13,16 * * *"` (UTC times)
- Rate limiting: Minimum 3 hours between runs
- Time window: 6:30 AM - 11:30 PM IST

### Customization

Edit `.github/workflows/change-dp.yml` to modify:
- Run frequency
- Time windows
- Rate limiting
- Timezone settings

## 🔧 Local Development

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export USERNAME="your_instagram_username"
export PASSWORD="your_instagram_password"

# Run locally
python src/main.py
```

### Testing

```bash
# Test with a single run
python src/main.py
```

## 📊 Monitoring

- **GitHub Actions**: Check the Actions tab for run history
- **Logs**: Detailed logging in each workflow run
- **State**: Monitor `data/index.txt` for current rotation state

## 🔒 Security & Privacy

- **Credentials**: Stored securely as GitHub Secrets
- **Sessions**: Encrypted session data in `data/session.json`
- **Rate Limiting**: Built-in protection against excessive API calls
- **No Data Collection**: No personal data is stored or transmitted

## ⚠️ Important Notes

- **Instagram Terms**: This tool is for personal use only. Ensure compliance with Instagram's Terms of Service
- **Rate Limits**: Instagram may temporarily restrict accounts for excessive automation
- **Backup**: Keep backups of your profile images
- **2FA**: Two-factor authentication may require app-specific passwords

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🐛 Troubleshooting

### Common Issues

1. **Login Failed**: Check credentials and 2FA settings
2. **No Images Found**: Ensure images are in `assets/images/` with correct naming
3. **Rate Limited**: Wait for the cooling period (3 hours)
4. **Workflow Not Running**: Check GitHub Actions permissions

### Getting Help

- Check the [Actions tab](../../actions) for run logs
- Review the [Issues section](../../issues) for common problems
- Create a new issue for specific problems

---

**Note**: This tool is for educational and personal use. Please use responsibly and in accordance with Instagram's Terms of Service.

