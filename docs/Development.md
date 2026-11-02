# Development

Install dependencies in a virtual environment before testing.

## Windows

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -p test_app.py -v
```

## macOS / Linux

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m unittest discover -s tests -v
```

Tests use fake clients. Workflow shell tests require Bash. CI workflows are included for user copies; Actions are disabled in the template. Setup has been exercised on Windows and Linux; macOS has not been verified on a physical Mac.

## Project map

| File | Purpose |
| --- | --- |
| `setup.py` | Environment creation, dependency install, wizard launcher |
| `src/create_session.py` | Instagram authentication and session creation |
| `src/github_setup.py` | GitHub installation/authentication, repository selection, workflow control |
| `src/image_setup.py` | Photo validation and atomic replacement |
| `src/timezone_setup.py` | Timezone selection and schedule display |
| `src/terminal_ui.py` | Interactive menus, masked input, sanitized login logs |
| `src/main.py` | Read-only check or picture rotation |
| `.github/workflows/change-dp.yml` | Scheduled/manual automation |

Documentation lives in `docs/` so it is versioned and included in ZIP downloads and template copies. The demo URL is backed up in `docs/demo-url.txt`.


---
[Documentation home](Home.md) · [Project README](../README.md)
