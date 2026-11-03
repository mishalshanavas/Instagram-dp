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

On Windows use `py scripts/publish_wiki.py`. The script copies the versioned guides, fixes links for Wiki URLs, exports the navigation sidebar and footer, and pushes a normal Wiki commit. It does not force-push.

To preview without changing GitHub:

```sh
python3 scripts/publish_wiki.py --preview ../instagram-dp-wiki-preview
```

The script targets the source repository's Wiki. It is a maintainer task, not part of end-user Instagram setup.

[Documentation home](Home.md)

## Source of truth and synchronization

Edit `Wiki/` in the main repository first. The publishing script exports those pages, including `_Sidebar.md` and `_Footer.md`, and converts relative `.md` page links to wiki page names. Main-repository pushes do not publish the wiki automatically.

The publisher updates matching filenames but does not delete remote-only pages. Review and remove obsolete pages deliberately when renaming a guide. Preserve any useful browser edits in `Wiki/` before publishing, because exported pages replace files with the same name.

After publishing, open Home, a platform guide, Configuration, and Architecture. Verify sidebar/footer navigation and the Mermaid rendering. Until publication succeeds, README links intentionally use the repository's `Wiki/` directory.

GitHub's [official wiki editing instructions](https://docs.github.com/en/communities/documenting-your-project-with-wikis/adding-or-editing-wiki-pages) explain first-page creation and the separate Git repository.
