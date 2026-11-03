# Account safety and sessions

The wizard uses instagrapi, an unofficial Instagram API client. Instagram can expire sessions, request verification, or block automated operations. Continuous operation is not guaranteed.

## What is stored?

- `data/session.json`: private Instagram session saved on your computer. It is ignored by Git.
- `INSTA_SESSION`: the same session stored as a GitHub Actions secret in your selected repository.
- `TIMEZONE`: a repository variable for displaying schedule times.
- `data/index.txt` and `data/next_run.txt`: non-secret rotation state committed by the workflow.

Your Instagram password is not uploaded as a repository secret. A session token is still a credential: never share the session file or paste it in issues. Login diagnostics show allowlisted request metadata and suppress the library's verification-code echo.

## Session renewal

Workflow runs reuse the stored session secret. They do not automatically update GitHub secrets. If Instagram rejects it, run full setup and save a fresh session.

If an old installation committed session credentials, revoke that session in Instagram. Deleting the file does not remove it from Git history or forks. The old `INSTA_USER` and `INSTA_PASS` secrets are no longer used.

## Photo privacy

Private copies keep photos restricted to repository access. Public copies expose uploaded photos publicly. Replacing photos does not erase earlier versions from history.

## Optional proxy

Set `PROXY_URL` as an Actions secret if you use a stable proxy. Set the same environment variable locally before login. A configured proxy failure stops the request rather than silently switching networks. A proxy does not guarantee that Instagram will accept a login or profile change.


---
[Documentation home](Home.md) · [Project README](../README.md)
