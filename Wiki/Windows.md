# Install on Windows

You need an internet connection, a GitHub account, and an Instagram account. Keep your verification app/email available.

## 1. Install Python

1. Open [python.org/downloads](https://www.python.org/downloads/) and download Python 3.11 or newer for Windows.
2. Run the installer. If it offers **Add Python to PATH**, select it. Include pip when offered.
3. Finish installation and close any old terminal windows.

## 2. Download the project

1. Open the [template repository](https://github.com/mishalshanavas/Instagram-dp).
2. Click the green **Code** button, then **Download ZIP**.
3. Find the ZIP in Downloads. Right-click it and choose **Extract All**.
4. Open the extracted folder. If you see another folder inside, open it too. Stop when you can see `setup.py` and `README.md`.

## 3. Open a terminal in the correct folder

1. Click File Explorer's address bar (the folder path at the top).
2. Type `powershell` and press Enter.
3. In the window that opens, type:

```powershell
py --version
```

It must show Python 3.11 or newer. If `py` is unavailable, try `python --version` and use `python` instead of `py` below.

## 4. Start setup

```powershell
py setup.py
```

Wait while dependencies install. Do not close the window. If GitHub CLI is missing, setup uses Winget when available; approve Windows administrator prompts if shown. If Winget is unavailable, install [GitHub CLI](https://cli.github.com/), reopen PowerShell, and rerun setup.

**Next: [First setup](First-setup.md).**

To return later without another Instagram login:

```powershell
py setup.py --github-only --manage
```

Do not double-click `setup.py`: a terminal window that closes immediately makes errors hard to read.


---
[Documentation home](Home.md) · [Project README](../README.md)
