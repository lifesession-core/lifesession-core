"""Regression checks for the fictional, local-only handoff walkthrough."""
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]


class HandoffDemoTests(unittest.TestCase):
    def test_demo_preserves_evidence_and_pending_review(self):
        source = ROOT / 'examples/maintainer/review_handoff.json'
        before = source.read_bytes()
        data = json.loads(before)
        env = dict(os.environ, PYTHONPATH=str(ROOT / 'src'))
        command = [sys.executable, '-m', 'lifesession', 'report', str(source)]
        first = subprocess.run(command, capture_output=True, text=True, env=env)
        second = subprocess.run(command, capture_output=True, text=True, env=env)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(source.read_bytes(), before)
        self.assertIn('## Additional fields', first.stdout)
        self.assertIn('"delivery_status": "not_sent"', first.stdout)
        self.assertIn('"review_status": "pending"', first.stdout)
        self.assertIn(data['handoff']['evidence'][0]['limitations'], first.stdout)
        self.assertIn(data['note'], first.stdout)
