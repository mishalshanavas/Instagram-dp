"""GitHub CLI onboarding; never put session contents in command arguments."""
from terminal_ui import prompt as input, choose, step
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys


USE_SAVED_GITHUB_LOGIN = False


class GitHubAuthenticationExpired(ValueError):
    pass


def run_gh(args, **kwargs):
    environment = {**os.environ, 'GH_HOST': 'github.com'}
    if USE_SAVED_GITHUB_LOGIN:
        for key in ('GH_TOKEN', 'GITHUB_TOKEN'):
            environment.pop(key, None)
    return subprocess.run(['gh', *args], env=environment, **kwargs)


def recover_github_login():
    global USE_SAVED_GITHUB_LOGIN
    print('GitHub login expired. Opening browser sign-in; your Instagram session is already saved.')
    if os.getenv('GH_TOKEN') or os.getenv('GITHUB_TOKEN'):
        print('An environment token may override gh login. This setup will use the saved browser login instead.')
    # Child processes only: leave the user's shell and token values untouched.
    USE_SAVED_GITHUB_LOGIN = True
    result = run_gh(['auth', 'login', '--hostname', 'github.com', '--git-protocol', 'https', '--web'])
    return result.returncode == 0



def ensure_gh():
    if shutil.which('gh'):
        return True
    command = None
    if sys.platform == 'win32' and shutil.which('winget'):
        command = ['winget', 'install', '--id', 'GitHub.cli', '--exact', '--source', 'winget', '--accept-package-agreements', '--accept-source-agreements']
    elif sys.platform == 'darwin' and shutil.which('brew'):
        command = ['brew', 'install', 'gh']
    elif sys.platform.startswith('linux'):
        for manager, args in [('apt-get', ['install', '-y', 'gh']), ('dnf', ['install', '-y', 'gh']), ('pacman', ['-S', '--needed', 'github-cli'])]:
            if shutil.which(manager):
                command = [manager, *args]
                if os.geteuid() != 0:
                    if not shutil.which('sudo'):
                        command = None
                    else:
                        command.insert(0, 'sudo')
                break
    if command:
        print('GitHub CLI is missing. Installer: ' + ' '.join(command))
        result = subprocess.run(command)
        if result.returncode == 0 and shutil.which('gh'):
            return True
        # Windows installers may update the registry PATH, not this process.
        if sys.platform == 'win32':
            folder = Path(os.environ.get('ProgramFiles', r'C:\Program Files')) / 'GitHub CLI'
            if (folder / 'gh.exe').exists():
                os.environ['PATH'] = str(folder) + os.pathsep + os.environ.get('PATH', '')
                return True
        print('Installation did not make gh available in this terminal.')
    print('Install GitHub CLI from https://cli.github.com/, reopen your terminal, and run python setup.py --github-only.')
    return False


def manual_instructions(session_file, repo=''):
    url = f'https://github.com/{repo}/settings/secrets/actions' if repo else 'your repository → Settings → Secrets and variables → Actions'
    print(f'\nManual setup: open {url}')
    print('Choose New repository secret. Name: INSTA_SESSION')
    print(f'Copy the ENTIRE contents of {session_file} into the secret value. Never upload this file.')
    print('Then open Actions → Update Instagram DP → Run workflow → check.')


SOURCE_REPO = 'mishalshanavas/Instagram-dp'


def api_json(endpoint):
    result = run_gh(['api', endpoint], capture_output=True, text=True)
    if result.returncode:
        # Never print raw stderr, which may contain credentials or proxy URLs.
        error = result.stderr if isinstance(result.stderr, str) else ''
        status = re.search(r'HTTP (\d{3})', error)
        if status and status.group(1) == '401':
            raise GitHubAuthenticationExpired('GitHub authentication expired (HTTP 401).')
        if status:
            reason = {'401': 'GitHub authentication expired; run gh auth login.',
                      '403': 'GitHub denied access; check token scopes, organization access, or API limits.',
                      '404': 'GitHub could not find or grant access to the requested repository.'}.get(status.group(1), 'GitHub API request failed.')
            raise ValueError(f'{reason} (HTTP {status.group(1)})')
        raise ValueError('GitHub API request failed. Check network access and run gh auth status.')
    return json.loads(result.stdout)


def discover_repositories():
    """Read every owned repository page and inspect provenance, not names."""
    user = api_json('user')['login']
    matches = []
    page = 1
    while True:
        repositories = api_json(f'user/repos?affiliation=owner&per_page=100&page={page}')
        for item in repositories:
            if item['owner']['login'].casefold() != user.casefold():
                continue
            repo = api_json('repos/' + item['full_name'])
            relations = {key: (repo.get(key) or {}).get('full_name', '').casefold()
                         for key in ('parent', 'source', 'template_repository')}
            source = SOURCE_REPO.casefold()
            kind = None
            if repo['full_name'].casefold() == source:
                kind = 'source repository'
            elif relations['template_repository'] == source:
                kind = 'template copy'
            elif source in (relations['parent'], relations['source']):
                kind = 'fork'
            if kind:
                matches.append((repo['full_name'], kind, repo.get('archived', False)))
        if len(repositories) < 100:
            break
        page += 1
    return user, sorted(matches, key=lambda item: item[0].casefold())


def create_repository(user, automatic=False):
    source = api_json('repos/' + SOURCE_REPO)
    if not source.get('is_template'):
        print('The source is not enabled as a template. Its owner must enable Settings → Template repository.')
        if automatic:
            print('A private template copy is unavailable. Use Create new to choose a fork explicitly.')
            return None
        if input('Create a fork instead? [y/N]: ').strip().lower() not in ('y', 'yes'):
            return None
        result = run_gh(['repo', 'fork', 'github.com/' + SOURCE_REPO, '--clone=false'], capture_output=True, text=True)
        if result.returncode:
            print('Fork creation failed. Check your permissions or existing forks, then retry.')
            return None
        return user + '/' + SOURCE_REPO.split('/')[1]
    if automatic:
        name = 'Instagram-dp'
        # Check names without mistaking authentication/network failures for availability.
        for suffix in range(1, 101):
            candidate = name if suffix == 1 else f'{name}-{suffix}'
            check = run_gh(['api', f'repos/{user}/{candidate}'], capture_output=True, text=True)
            if check.returncode == 0:
                continue
            if 'HTTP 404' not in (check.stderr or ''):
                print('Could not verify repository-name availability. Check gh auth status and network access.')
                return None
            name = candidate
            break
        else:
            print('No free default repository name found. Choose Create new to enter a name manually.')
            return None
        repo = user + '/' + name
        flag = '--private'
        print(f'Creating private template copy: {repo}')
    else:
        while True:
            name = input('New repository name [Instagram-dp]: ').strip() or 'Instagram-dp'
            if re.fullmatch(r'[A-Za-z0-9_.-]+', name) and name not in ('.', '..'):
                break
            print('Use letters, numbers, dots, underscores, or hyphens.')
        visibility = choose('Repository visibility', [('1', 'Private — only you can see your photos'),
                             ('2', 'Public — anyone can see your photos')], '1', 'Visibility [1]: ')
        if visibility not in ('1', '2'):
            print('Invalid visibility; nothing was created.')
            return None
        repo = user + '/' + name
        flag = '--private' if visibility == '1' else '--public'
        print(f'Create {repo} from {SOURCE_REPO} ({flag[2:]})')
        if input('Continue? [Y/n]: ').strip().lower() in ('n', 'no'):
            return None
    result = run_gh(['repo', 'create', repo, '--template', 'github.com/' + SOURCE_REPO, flag], capture_output=True, text=True)
    if result.returncode:
        print('Creation failed. The name may already exist, or your account may lack permission. Nothing was overwritten.')
        return None
    return repo


def select_repository():
    try:
        print('Finding your forks and template copies...')
        try:
            user, matches = discover_repositories()
        except GitHubAuthenticationExpired:
            if not recover_github_login():
                print('GitHub sign-in did not finish. Resume with --github-only; no Instagram login is needed.')
                return None
            print('Signed in. Retrying repository discovery...')
            try:
                user, matches = discover_repositories()
            except GitHubAuthenticationExpired:
                print('GitHub still rejected authentication after sign-in. No repository was created. '
                      'Check account access, then resume with --github-only.')
                return None
        if not matches:
            print('No existing copies found. Creating a private copy automatically...')
            return create_repository(user, automatic=True)
    except (OSError, ValueError, KeyError) as exc:
        reason = str(exc) if isinstance(exc, ValueError) else 'Network or GitHub response error.'
        print(f'Could not finish repository discovery: {reason}')
        print('Discovery failed; no repository was created. Sign in again with gh auth login if needed.')
        user, matches = None, []
    while True:
        if user:
            print(f'\nGitHub account: {user}')
            if not matches:
                print('No matching forks or template copies found in this account.')
        default = next((str(i) for i, item in enumerate(matches, 1) if not item[2]),
                       'N' if user else '0')
        from terminal_ui import interactive
        if not interactive():
            for number, (name, kind, archived) in enumerate(matches, 1):
                suffix = ' — archived, cannot configure' if archived else ''
                selected = ' [default]' if str(number) == default else ''
                print(f'  {number}. {name} ({kind}){suffix}{selected}')
            if user:
                print('  N. Create a new copy from the source' + (' [default]' if default == 'N' else ''))
            print('  M. Enter a repository manually\n  0. Manual secret instructions / exit')
        from terminal_ui import interactive
        if interactive():
            options = [(str(i), f'{name} · {kind}' + (' · archived' if archived else ''))
                       for i, (name, kind, archived) in enumerate(matches, 1)]
            if user:
                options.append(('N', 'Create a new repository'))
            options.extend([('M', 'Enter a repository manually'), ('0', 'Finish / manual setup')])
            choice = choose('Choose a repository', options, default, '').strip()
        else:
            choice = input(f'Choose an option [{default}]: ').strip() or default
        if choice == '0':
            return None
        if choice.lower() == 'n' and user:
            repo = create_repository(user)
            if repo:
                return repo
            continue
        if choice.isdigit() and 1 <= int(choice) <= len(matches):
            name, _, archived = matches[int(choice) - 1]
            if archived:
                print('Unarchive that repository in GitHub first, or choose another copy.')
                continue
            return name
        if choice.lower() == 'm':
            choice = input('Repository owner/name or GitHub URL: ').strip()
        # Also accept pasted repository URLs directly at the picker.
        repo = re.sub(r'^https://github\.com/', '', choice).rstrip('/')
        if repo.endswith('.git'):
            repo = repo[:-4]
        if re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repo):
            return repo
        print('Choose a listed number, N, M, or 0.')


def prepare_workflow(repo):
    """Only offer activation after the remote workflow matches this setup version."""
    if repo.casefold() == SOURCE_REPO.casefold():
        print('This is the template repository. Create or select your own copy to run automation.')
        return False
    remote = run_gh(['workflow', 'view', 'change-dp.yml', '--repo', 'github.com/' + repo, '--yaml'], capture_output=True, text=True)
    local = (Path(__file__).resolve().parent.parent / '.github/workflows/change-dp.yml').read_text()
    if remote.returncode or remote.stdout.strip() != local.strip():
        print('The GitHub workflow is missing or differs from this setup version. Publish the updated project files to the default branch first.')
        print('Your secret is saved. Then rerun setup with --github-only; no Instagram login is needed.')
        return False
    info = api_json(f'repos/{repo}/actions/workflows/change-dp.yml')
    if info.get('state') != 'active':
        print('This workflow is disabled. Enabling it also enables scheduled picture changes.')
        enabled = run_gh(['workflow', 'enable', 'change-dp.yml', '--repo', 'github.com/' + repo], capture_output=True)
        if enabled.returncode:
            print('Could not enable the workflow. Check repository Actions permissions.')
            return False
    return True


def show_run_failure(repo, run_id):
    logs = run_gh(['run', 'view', run_id, '--repo', 'github.com/' + repo, '--log-failed'],
                  capture_output=True, text=True)
    if logs.returncode or not isinstance(logs.stdout, str):
        return
    # Show our own safe error messages, never arbitrary API response bodies.
    messages = [line.split('DP_ERROR: ', 1)[1] for line in logs.stdout.splitlines() if 'DP_ERROR: ' in line]
    if messages:
        print('\nWhat happened: ' + messages[-1])
    elif re.search(r'\[403\] POST .*accounts/change_profile_picture/', logs.stdout):
        from failure_help import instagram_failure
        error = type('ClientForbiddenError', (Exception,), {})()
        print('\nWhat happened: ' + instagram_failure(error))
    else:
        print('No safe Instagram error summary was available. Use the command above for the failed step.')


def workflow_run_ids(repo):
    result = run_gh(['run', 'list', '--repo', 'github.com/' + repo, '--workflow', 'change-dp.yml',
                     '--event', 'workflow_dispatch', '--limit', '100', '--json', 'databaseId'],
                    capture_output=True, text=True)
    if result.returncode:
        return None
    try:
        return {str(item['databaseId']) for item in json.loads(result.stdout)}
    except (ValueError, KeyError, TypeError):
        return None


def find_dispatched_run(repo, previous):
    import time
    for attempt in range(10):
        current = workflow_run_ids(repo)
        if current is None:
            return None
        candidates = current - previous
        if len(candidates) == 1:
            return candidates.pop()
        if len(candidates) > 1:
            print('Multiple new runs appeared. Refusing to guess which one belongs to this setup.')
            return None
        if attempt < 9:
            time.sleep(2)
    return None


def run_workflow(repo, mode):
    previous = workflow_run_ids(repo)
    if previous is None:
        print('Could not read workflow runs. No new run was requested; check GitHub access and retry.')
        return False
    result = run_gh(['workflow', 'run', 'change-dp.yml', '--repo', 'github.com/' + repo,
                     '-f', 'mode=' + mode], capture_output=True, text=True)
    if result.returncode:
        print('Could not start the workflow. Your secret is saved; rerun setup with --github-only to retry.')
        return False
    match = re.search(r'https://github.com/[^/]+/[^/]+/actions/runs/(\d+)', result.stdout or '')
    run_id = match.group(1) if match else find_dispatched_run(repo, previous)
    if not run_id:
        print('Workflow requested; this does not mean the check passed yet.')
        print(f'Check progress with: gh run list --repo {repo} --workflow change-dp.yml')
        return False
    print('Waiting for GitHub Actions. Press Ctrl+C to stop watching; the remote run will continue.')
    watched = run_gh(['run', 'watch', run_id, '--repo', 'github.com/' + repo, '--exit-status', '--interval', '10'])
    if watched.returncode:
        print('Workflow did not pass or could not be watched. Inspect it from this terminal:')
        print(f'gh run view {run_id} --repo {repo} --log-failed')
        show_run_failure(repo, run_id)
        return False
    print('Setup check passed. Your picture was not changed. This read-only check does not test profile-update permission.' if mode == 'check'
          else 'Your profile picture was updated and the next rotation was scheduled.')
    return True


def finish_setup(repo):
    step('3 / 3', 'Photos & automation')
    while True:
        choice = choose('What would you like to do?', [
            ('1', 'Check login and photos (recommended)'),
            ('2', 'Change your profile picture now'),
            ('3', 'Replace photos from a folder'), ('0', 'Finish')],
            '1', 'Choose an option [1]: ').lower()
        if choice in ('0', 'n', 'no'):
            print('Saved. Run setup with --github-only whenever you want to start a workflow.')
            return
        if choice == '3':
            from image_setup import replace_photos
            replace_photos(repo)
            print('\nNext: 1. Check setup   2. Rotate now   3. Replace photos   0. Finish')
            continue
        if choice in ('1', '2'):
            break
        print('Choose 1, 2, 3, or 0.')
    if not prepare_workflow(repo):
        return
    mode = 'check' if choice == '1' else 'rotate'
    if not run_workflow(repo, mode):
        return
    if mode == 'check' and input('Change your profile picture now? [y/N]: ').strip().lower() in ('y', 'yes'):
        run_workflow(repo, 'rotate')


def automatic_setup(repo):
    step('3 / 3', 'Automatic check & first rotation')
    print('Using the photos currently in this repository, including placeholders if not replaced.')
    if not prepare_workflow(repo):
        return False
    if not run_workflow(repo, 'check'):
        print('Stopped after the check. No rotation was requested.')
        return False
    return run_workflow(repo, 'rotate')


def configure_github(session_file, manage=False):
    try:
        if not ensure_gh():
            manual_instructions(session_file)
            return
        step('2 / 3', 'GitHub')
        status = run_gh(['auth', 'status', '--hostname', 'github.com'], capture_output=True)
        if status.returncode:
            print('Sign in to GitHub in your browser. Follow the device-code instructions below.')
            if not recover_github_login():
                print('GitHub sign-in did not finish. Your local session is safe.')
                manual_instructions(session_file)
                return
        repo = select_repository()
        if not repo:
            manual_instructions(session_file)
            return
        info = run_gh(['repo', 'view', 'github.com/' + repo, '--json', 'nameWithOwner,viewerPermission'], capture_output=True, text=True)
        if info.returncode:
            print('Cannot access that repository. Check its name and your GitHub account.')
            manual_instructions(session_file, repo)
            return
        metadata = json.loads(info.stdout)
        if metadata.get('viewerPermission') != 'ADMIN':
            print('Repository admin access is required to configure Actions secrets. Use your own copy or ask its admin.')
            manual_instructions(session_file, repo)
            return
        repo = metadata['nameWithOwner']
        print(f'Target repository: https://github.com/{repo}')
        print('Saving INSTA_SESSION automatically in the selected repository...')
        with session_file.open('rb') as session:
            result = run_gh(['secret', 'set', 'INSTA_SESSION', '--repo', 'github.com/' + repo], stdin=session, capture_output=True)
        if result.returncode:
            print('Secret upload failed. Check repository permissions and try python setup.py --github-only.')
            manual_instructions(session_file, repo)
            return
        print('INSTA_SESSION saved. Your Instagram password was not uploaded.')
        if manage:
            finish_setup(repo)
        else:
            automatic_setup(repo)

    except (OSError, ValueError, KeyError):
        print('GitHub setup could not finish. Your local session is saved. Retry with python setup.py --github-only.')
        manual_instructions(session_file)
