# Maintaining the documentation

Edit the canonical Markdown pages in `Wiki/`. The README is the landing page; it should link to detailed guides rather than reproduce them. The old `docs/` pages retain redirects for existing links.

## Source map

| Topic | Implementation to check before editing |
| --- | --- |
| Installation and flags | `setup.py`, `src/requirements.txt` |
| Login and credentials | `src/create_session.py`, `src/session_utils.py` |
| Repository discovery and workflow runs | `src/github_setup.py` |
| Photo limits and ordering | `src/image_setup.py`, `src/main.py` |
| Scheduling and timezone | `.github/workflows/change-dp.yml`, `src/timezone_setup.py` |
| Development checks | `requirements-dev.txt`, `tests/`, `.github/workflows/tests.yml` |

Keep dependencies and feature claims tied to source files. Do not add a passing-build badge while Actions are disabled on the source repository.

## Assets

The README retains the original hosted demo, labelled 10× speed. Its URL is backed up in `docs/demo-url.txt`. The solid-color files in `assets/images/` are runtime placeholders, not screenshots. The architecture page contains a Mermaid diagram derived from the modules and workflow.

Useful future captures, requiring a real successful session:

- The photo menu, showing the choice between uploading a collection and using existing images.
- The upload review, showing original and numbered filenames without personal folder paths.
- A successful workflow result and next due time, with account identifiers removed.

Do not capture passwords, cookies, verification codes, device-login codes, or session contents. No new screenshots were fabricated for this documentation.

## Review and publishing

Check relative links, heading hierarchy, code fences, and navigation in both the repository and exported wiki. Review commands against their argument parsers without running a live rotation. See [Publishing](Wiki-publishing.md) for the export and push process.

Physical macOS validation remains outstanding. No dedicated contribution or private vulnerability-reporting policy exists in the repository; the maintainer should choose a private reporting channel before one is advertised.

## Review record: 3 November 2026

Reviewed setup arguments, image validation and replacement, credential loading, workflow dispatch/watch, timezone display, state commits, and test configuration against source. Repository and exported wiki page links and Markdown fence balance passed automated checks. Four README badges and the original demo URL were reachable; all 14 external URLs in the initial link scan returned HTTP 200. The instagrapi legacy documentation link was then updated to its verified current destination.

The publisher preview and Python compilation passed, and `setup.py --help` confirmed the documented flags. No Instagram login or picture rotation was performed during documentation verification. Mermaid syntax was reviewed, but its rendered appearance and final GitHub Wiki navigation still require inspection after publication. macOS installation remains unverified on physical hardware.
