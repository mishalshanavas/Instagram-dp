"""Publish versioned documentation after the first GitHub Wiki page is created."""
import argparse
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://github.com/mishalshanavas/Instagram-dp'


def export_pages(destination):
    for page in (ROOT / 'Wiki').glob('*.md'):
        text = page.read_text()
        text = text.replace('(../README.md)', '(' + BASE + '#readme)')
        text = re.sub(r'\]\(([A-Za-z_-]+)\.md(#[^)]*)?\)',
                      lambda match: '](' + match.group(1) + (match.group(2) or '') + ')', text)
        (destination / page.name).write_text(text)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preview', type=Path, help='Export pages locally without GitHub changes')
    args = parser.parse_args()
    if args.preview:
        args.preview.mkdir(parents=True, exist_ok=True)
        export_pages(args.preview)
        return
    with tempfile.TemporaryDirectory(prefix='instagram-dp-wiki-') as folder:
        directory = Path(folder) / 'wiki'
        clone = subprocess.run(['git', 'clone', BASE + '.wiki.git', str(directory)], capture_output=True)
        if clone.returncode:
            raise SystemExit('Wiki is not initialized or accessible. Create and save its first page at ' + BASE + '/wiki/_new, then retry.')
        export_pages(directory)
        subprocess.run(['git', '-C', str(directory), 'add', '.'], check=True)
        if subprocess.run(['git', '-C', str(directory), 'diff', '--cached', '--quiet']).returncode == 0:
            print('Wiki is already current.')
            return
        subprocess.run(['git', '-C', str(directory), 'commit', '-m', 'Publish beginner setup documentation'], check=True)
        subprocess.run(['git', '-C', str(directory), 'push'], check=True)


if __name__ == '__main__':
    main()
