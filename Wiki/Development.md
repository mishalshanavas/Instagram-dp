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

Documentation lives in `Wiki/` so it is versioned and included in ZIP downloads and template copies. The demo URL is backed up in `docs/demo-url.txt`.


---
[Documentation home](Home.md) · [Project README](../README.md)

## Contributing

No separate contribution policy is currently present. For a change, describe the problem, keep the patch focused, run the relevant tests, and submit a pull request with results. These are suggested review practices, not additional license terms. Tests that require Bash should be run on Linux or a suitable Bash environment.

See [Architecture](Architecture.md) for component boundaries and [Documentation maintenance](Documentation-maintenance.md) for documentation changes.

## Dependency isolation

The runtime requirements pin instagrapi, Pillow, Questionary, Rich, timezone data, and their dependencies. Development requirements additionally install the workflow YAML parser. Use the repository requirements files rather than manually reproducing their version list.

Python's [venv documentation](https://docs.python.org/3/library/venv.html) explains why project dependencies are isolated. The test workflow defines Python 3.11 and 3.14 jobs on Ubuntu; that configuration is not evidence that every platform has been tested.
