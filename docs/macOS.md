# Install on macOS

## 1. Install Python

Download Python 3.11 or newer from [python.org/downloads](https://www.python.org/downloads/). Open the downloaded installer and finish its steps. Open a new Terminal window afterward.

## 2. Download the project

Open the [template repository](https://github.com/mishalshanavas/Instagram-dp), select **Code → Download ZIP**, then double-click the downloaded ZIP to extract it. Open the folder containing `setup.py`.

## 3. Open Terminal in that folder

1. Open **Terminal** using Spotlight (Command + Space, type Terminal, press Enter).
2. Type `cd `, including the space. Do not press Enter yet.
3. Drag the extracted project folder from Finder into Terminal.
4. Press Enter. Now run:

```sh
python3 --version
```

It must show 3.11 or newer.

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
