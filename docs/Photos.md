# Add or replace photos

## 1. Prepare a folder

Create a folder containing every photo you want in the rotation. Use **1–100 PNG, JPG, or JPEG files**, each at most **20 MB**. Subfolders are not uploaded.

Square images suit the circular profile crop. The template's eleven placeholders are 320 × 320 PNG squares in different solid colors.

Name your files in the order you want, for example `1.jpg`, `2.png`, and `3.jpg`. Numeric filenames sort first by number; other filenames sort alphabetically.

## 2. Open the photo menu

During first setup, select **Add my photos from a folder**. For later changes, run:

| Windows | macOS / Linux |
| --- | --- |
| `py setup.py --github-only --manage` | `python3 setup.py --github-only --manage` |

Select your repository, then **Replace photos from a folder**.

## 3. Paste the folder path

Examples:

```text
Windows: C:\Users\You\Pictures\Instagram
macOS:   /Users/you/Pictures/Instagram
Linux:   /home/you/Pictures/Instagram
```

Use the complete folder path. On Windows, you can copy it from File Explorer's address bar. Press Enter after pasting. A blank path cancels the upload.

## 4. Review and confirm

The wizard displays the original filenames and uploaded names. For example:

```text
holiday.jpg → 1.jpg
portrait.png → 2.png
```

Choose **Yes** only when the collection is correct. The default is No.

The uploader validates all files, replaces the old top-level PNG/JPG files in `assets/images`, and resets the rotation position to zero in one commit. Other project files and non-image files are preserved. A concurrent branch change causes the final update to fail instead of overwriting newer work.

**This replaces the complete photo set.** Include photos you want to keep. Old photos can remain in Git history. Your local originals are never renamed or deleted. Manual GitHub uploads keep their names; automatic numbering is a wizard feature.

## 5. Choose what happens next

In automatic setup, a successful upload continues to the check and first rotation. In the management menu, choose **Check login and photos** or **Change your profile picture now**.

Uploading alone does not immediately change the Instagram picture. An already enabled schedule can use the new collection on its next due run.


---
[Documentation home](Home.md) · [Project README](../README.md)
