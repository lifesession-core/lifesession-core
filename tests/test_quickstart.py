"""Run the documented user path against a fresh source copy."""
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(shutil.which('sh') and shutil.which('mktemp'),
                     'POSIX walkthrough requires sh and mktemp')
class QuickstartTests(unittest.TestCase):
    def test_documented_first_session(self):
        text = (ROOT / 'docs/first-session.md').read_text(encoding='utf-8')
        blocks = re.findall(r'```sh\n(.*?)```', text, re.S)
        self.assertEqual(len(blocks), 1)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for name in ('src', 'schemas', 'examples'):
                shutil.copytree(ROOT / name, root / name,
                                ignore=shutil.ignore_patterns('__pycache__'))
            fixture = root / 'examples/maintainer/session_package.json'
            original = fixture.read_bytes()
            bin_dir = root / 'bin'
            bin_dir.mkdir()
            (bin_dir / 'python').symlink_to(sys.executable)
            env = dict(os.environ, PATH=str(bin_dir) + os.pathsep + os.environ['PATH'],
                       TMPDIR=str(root), PYTHONDONTWRITEBYTECODE='1')
            result = subprocess.run(['sh', '-c', blocks[0]], cwd=root,
                                    env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('OK — package structure consistent', result.stdout)
            self.assertIn('maintainer review is still pending', result.stdout)
            self.assertIn('needs_review', result.stdout)
            reports = list(root.glob('*/session-report.md'))
            self.assertEqual(len(reports), 1)
            self.assertIn('# LifeSession report', reports[0].read_text())
            self.assertEqual(original, fixture.read_bytes())
