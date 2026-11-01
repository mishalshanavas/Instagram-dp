"""Execute workflow shell logic in temporary repositories, without Instagram or GitHub."""
import os
from pathlib import Path
import subprocess
import tempfile
import time
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = yaml.safe_load((ROOT / '.github/workflows/change-dp.yml').read_text())
STEPS = {step.get('name'): step for step in WORKFLOW['jobs']['update-dp']['steps'] if step.get('name')}


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'data').mkdir()
        self.output = self.root / 'output'

    def run_step(self, name, **env):
        return subprocess.run(['bash', '-e', '-o', 'pipefail', '-c', STEPS[name]['run']], cwd=self.root,
                              env={**os.environ, 'GITHUB_OUTPUT': str(self.output), **env},
                              capture_output=True, text=True)

    def test_schedule_missing_due_future_corrupt_and_leading_zero(self):
        for value, expected in [(None, 'true'), ('0', 'true'), (str(int(time.time()) + 3600), 'false'), ('broken', 'true'), ('000000000008', 'true')]:
            with self.subTest(value=value):
                path = self.root / 'data/next_run.txt'
                if value is not None:
                    path.write_text(value)
                self.output.write_text('')
                result = self.run_step('Check schedule', EVENT_NAME='schedule')
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(self.output.read_text().strip(), 'should_run=' + expected)

    def test_manual_run_ignores_future_schedule(self):
        (self.root / 'data/next_run.txt').write_text(str(int(time.time()) + 10000))
        result = self.run_step('Check schedule', EVENT_NAME='workflow_dispatch')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('should_run=true', self.output.read_text())

    def test_missing_secret_fails_clearly(self):
        result = self.run_step('Check setup secret', INSTA_SESSION='')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Setup needed', result.stdout)
        self.assertEqual(self.run_step('Check setup secret', INSTA_SESSION='fake-test-secret').returncode, 0)

    def test_workflow_never_stages_session(self):
        script = STEPS['Save next run and image position']['run']
        self.assertIn('git add data/index.txt data/next_run.txt', script)
        self.assertNotIn('session.json', script)
        self.assertNotIn('INSTA_PASS', str(WORKFLOW))
        self.assertFalse(WORKFLOW['concurrency']['cancel-in-progress'])

    def test_all_shell_scripts_parse(self):
        for name, step in STEPS.items():
            if 'run' in step:
                result = subprocess.run(['bash', '-n'], input=step['run'], text=True, capture_output=True)
                self.assertEqual(result.returncode, 0, name + result.stderr)


if __name__ == '__main__':
    unittest.main()
