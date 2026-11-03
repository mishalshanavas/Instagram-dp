# Install on Linux or a VM

## 1. Check Python

Open Terminal and run:

```sh
python3 --version
```

You need Python 3.11 or newer, pip, and the venv module. Install those through your distribution's package manager if missing. Package names depend on your distribution. On a distribution whose default Python meets the version requirement, a typical Debian/Ubuntu command is:

```sh
sudo apt-get update
sudo apt-get install git python3 python3-venv python3-pip
```

Check the version again afterward; older distributions may need a newer Python installation.

## 2. Clone the project

Git downloads the project into a new `Instagram-dp` folder. Run these commands from the directory where you want to keep it:

```sh
git --version
git clone https://github.com/mishalshanavas/Instagram-dp.git
cd Instagram-dp
```

If Git is missing, install it through your distribution's package manager. The Debian/Ubuntu command above includes it. If `Instagram-dp` already exists, use that folder or choose another parent directory; do not delete an existing installation to repeat this step.

Prefer a download? Choose **Code → Download ZIP** on the [repository page](https://github.com/mishalshanavas/Instagram-dp), extract it, and open a terminal in the folder containing `setup.py`.

Cloning downloads the setup program. The wizard still creates or selects your own GitHub copy for automation.

## 3. Start setup

```sh
python3 setup.py
```

The wizard creates its own virtual environment; you don't need to activate it or run pip manually. It installs GitHub CLI through apt, dnf, or pacman when available. `sudo` may ask for your Linux password. Do not run the whole wizard with sudo.

## 4. Browser sign-in on a headless VM

If setup cannot open a browser, that is not a failed login:

1. Copy the displayed GitHub device-login URL.
2. Open it on a computer or phone with a browser.
3. Sign in to the GitHub account you want the bot to use.
4. Enter the displayed one-time code and complete **Authorize**.
5. Return to the VM terminal and wait for **Authentication complete**.

**Next: [First setup](First-setup.md).**

To return later:

```sh
python3 setup.py --github-only --manage
```


---
[Documentation home](Home.md) · [Project README](../README.md)
