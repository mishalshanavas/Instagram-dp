# Publish the GitHub Wiki

The full guides are already available in this repository and included in ZIP downloads. GitHub requires the Wiki's first page to be saved before its separate Git repository becomes available.

## One-time initialization (repository owner)

1. Sign in as `mishalshanavas`.
2. Open [Create the first Wiki page](https://github.com/mishalshanavas/Instagram-dp/wiki/_new).
3. Use the title **Home**. A short temporary body is enough.
4. Click **Save Page**.

## Publish the prepared guides

From the project folder, with Git installed and authenticated for this repository:

```sh
python3 scripts/publish_wiki.py
```

On Windows use `py scripts/publish_wiki.py`. The script copies the versioned guides, fixes links for Wiki URLs, creates a navigation sidebar, and pushes a normal Wiki commit. It does not force-push.

To preview without changing GitHub:

```sh
python3 scripts/publish_wiki.py --preview /tmp/instagram-dp-wiki-preview
```

The script targets the source repository's Wiki. It is a maintainer task, not part of end-user Instagram setup.

[Documentation home](Home.md)
