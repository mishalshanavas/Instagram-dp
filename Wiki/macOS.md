# Install on macOS

## 1. Install Python

Download Python 3.11 or newer from [python.org/downloads](https://www.python.org/downloads/). Open the downloaded installer and finish its steps. Open a new Terminal window afterward.

## 2. Open Terminal and check requirements

Open **Terminal** using Spotlight (**Command + Space**, type Terminal, press Enter), then run:

```sh
python3 --version
git --version
```

Python must be 3.11 or newer. If macOS prompts you to install command line developer tools when checking Git, complete that installation and retry. You can also use the ZIP fallback below if you do not want to install Git.

## 3. Clone the project

In Terminal, run:

```sh
git clone https://github.com/mishalshanavas/Instagram-dp.git
cd Instagram-dp
```

This creates a project folder in your current directory. If that folder already exists, return to your existing installation or choose another parent directory.

**ZIP fallback:** on the [repository page](https://github.com/mishalshanavas/Instagram-dp), select **Code → Download ZIP** and extract it. In Terminal, type `cd ` with a trailing space, drag the extracted folder containing `setup.py` from Finder into Terminal, and press Enter.

Cloning downloads the setup program. The wizard still creates or selects your own GitHub copy for automation.

## 4. Start setup

```sh
python3 setup.py
```

Wait for dependency installation. Setup can install GitHub CLI through Homebrew if Homebrew is already installed. Otherwise follow the [official GitHub CLI installation instructions](https://cli.github.com/), reopen Terminal, return to the project folder, and rerun setup.

**Next: [First setup](First-setup.md).**

To return later:

```sh
python3 setup.py --github-only --manage
```

The macOS path is supported in code but has not been verified on a physical Mac.


---
[Documentation home](Home.md) · [Project README](../README.md)
