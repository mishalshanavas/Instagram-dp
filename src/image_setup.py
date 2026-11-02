"""Replace a remote photo collection in one commit, using GitHub CLI."""
from terminal_ui import prompt as input, choose, step
import base64
import json
from pathlib import Path
from urllib.parse import quote


def replace_photos(repo):
    from github_setup import api_json, run_gh
    from PIL import Image

    def write_api(path, data, method='POST'):
        result = run_gh(['api', path, '--method', method, '--input', '-'],
                        input=json.dumps(data), capture_output=True, text=True)
        if result.returncode:
            raise ValueError('GitHub rejected the upload. Check permissions/branch rules or retry if the branch changed.')
        return json.loads(result.stdout)

    try:
        folder = input('Paste the folder path containing your new photos (Enter to cancel): ').strip().strip('\"\'')
        if not folder:
            return False
        directory = Path(folder).expanduser()
        if not directory.is_dir():
            raise ValueError('That folder does not exist. Paste its full path, including spaces.')
        photos = sorted([p for p in directory.iterdir() if p.is_file() and p.suffix.lower() in {'.png', '.jpg', '.jpeg'}],
                        key=lambda p: (0, int(p.stem), p.name) if p.stem.isdigit() else (1, p.name.casefold(), p.name))
        if not photos or len(photos) > 100:
            raise ValueError('Choose a folder containing 1–100 PNG/JPG photos.')
        payloads = []
        for photo in photos:
            if photo.is_symlink() or photo.stat().st_size > 20 * 1024 * 1024:
                raise ValueError(f'{photo.name}: use a regular image file smaller than 20 MB.')
            data = photo.read_bytes()
            import io
            try:
                with Image.open(io.BytesIO(data)) as image:
                    image.verify()
            except Exception:
                raise ValueError(f'{photo.name} is not a readable image.') from None
            payloads.append(data)
        print(f'\nReplace the photo set in {repo}:')
        for i, photo in enumerate(photos, 1):
            print(f'  {i}. {photo.name} → {i}{photo.suffix.lower()}')
        print('Existing PNG/JPG photos in assets/images will be replaced. Rotation restarts at the first photo.')
        print('Uploading does not change your Instagram picture immediately; scheduled runs will use the new set.')
        if input('Upload this replacement set? [y/N]: ').strip().lower() not in ('y', 'yes'):
            return False
        prefix = 'repos/' + repo
        branch = quote(api_json(prefix)['default_branch'], safe='')
        head = api_json(prefix + '/git/ref/heads/' + branch)['object']['sha']
        commit = api_json(prefix + '/git/commits/' + head)
        tree = api_json(prefix + '/git/trees/' + commit['tree']['sha'] + '?recursive=1')
        if tree.get('truncated'):
            raise ValueError('Repository listing was incomplete. Nothing was changed; use a smaller repository.')
        entries = {}
        for item in tree['tree']:
            path = Path(item['path'])
            if path.parent.as_posix() == 'assets/images' and path.suffix.lower() in {'.png', '.jpg', '.jpeg'}:
                entries[item['path']] = {'path': item['path'], 'mode': item['mode'], 'type': 'blob', 'sha': None}
        for i, (photo, data) in enumerate(zip(photos, payloads), 1):
            blob = write_api(prefix + '/git/blobs', {'content': base64.b64encode(data).decode('ascii'), 'encoding': 'base64'})
            path = f'assets/images/{i}{photo.suffix.lower()}'
            entries[path] = {'path': path, 'mode': '100644', 'type': 'blob', 'sha': blob['sha']}
        entries['data/index.txt'] = {'path': 'data/index.txt', 'mode': '100644', 'type': 'blob', 'content': '0'}
        new_tree = write_api(prefix + '/git/trees', {'base_tree': commit['tree']['sha'], 'tree': list(entries.values())})
        new_commit = write_api(prefix + '/git/commits', {'message': 'Replace profile photos and restart rotation', 'tree': new_tree['sha'], 'parents': [head]})
        # A concurrent push makes this fail rather than overwrite someone else's changes.
        write_api(prefix + '/git/refs/heads/' + branch, {'sha': new_commit['sha'], 'force': False}, 'PATCH')
        print(f'Uploaded {len(photos)} photos in one commit. Choose check or rotate from the menu next.')
        return True
    except (OSError, ValueError, KeyError) as exc:
        print(f'Photo replacement did not finish: {exc}')
        print('An upload failure before the final branch update leaves your current photo set unchanged.')
        return False
