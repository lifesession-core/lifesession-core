import copy
import json
import os
import subprocess
import tempfile
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from lifesession.handoff import check_handoff


class HandoffTests(unittest.TestCase):
    def setUp(self):
        self.record = json.loads((ROOT / 'examples/maintainer/review_handoff.json').read_text())

    def test_valid_and_unchanged(self):
        before = copy.deepcopy(self.record)
        self.assertEqual(check_handoff(self.record), [])
        self.assertEqual(self.record, before)

    def test_invalid_record(self):
        for item in (None, [], 'private-value'):
            self.assertEqual(check_handoff(item), ['record.object_required'])

    def test_missing_handoff(self):
        self.assertEqual(check_handoff({'session_id':'demo'}), ['handoff.object_required'])

    def test_unknown_version(self):
        self.record['handoff']['version'] = 2
        self.assertIn('handoff.version_unsupported', check_handoff(self.record))

    def test_review_requires_ack(self):
        for review in ('accepted', 'changes_requested'):
            for delivery in ('not_sent', 'sent'):
                self.record['handoff'].update(review_status=review, delivery_status=delivery)
                self.assertIn('handoff.review_requires_acknowledgment', check_handoff(self.record))
            self.record['handoff']['delivery_status'] = 'acknowledged'
            self.assertEqual(check_handoff(self.record), [])

    def test_unknown_statuses(self):
        self.record['handoff'].update(review_status='released', delivery_status='maybe')
        self.assertIn('handoff.review_status_invalid', check_handoff(self.record))
        self.assertIn('handoff.delivery_status_invalid', check_handoff(self.record))

    def test_empty_fields(self):
        self.record['session_id'] = ' '
        self.record['handoff'].update(next_action='', blockers=[''])
        errors = check_handoff(self.record)
        self.assertIn('session_id.nonempty_required', errors)
        self.assertIn('handoff.next_action_required', errors)
        self.assertIn('handoff.blockers_invalid', errors)

    def test_missing_evidence(self):
        for evidence in (None, [], 'not evidence', [None], [{}]):
            self.record['handoff']['evidence'] = evidence
            self.assertTrue(check_handoff(self.record))

    def test_failure_is_not_hidden_or_rejected(self):
        for result in ('failed', 'not_run', 'blocked'):
            self.record['handoff']['evidence'][0]['result'] = result
            self.assertEqual(check_handoff(self.record), [])

    def test_diagnostics_do_not_echo_values(self):
        self.record['handoff']['evidence'][0]['result'] = 'private-value'
        self.assertNotIn('private-value', str(check_handoff(self.record)))

    def test_extra_data_allowed(self):
        self.record['handoff']['custom'] = {'x':1}
        self.assertEqual(check_handoff(self.record), [])


class HandoffCliTests(unittest.TestCase):
    def run_cli(self, content):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'input.json'
            path.write_bytes(content)
            env = dict(os.environ, PYTHONPATH=str(ROOT / 'src'))
            return subprocess.run([sys.executable, '-m', 'lifesession',
                                   'check-handoff', str(path)],
                                  capture_output=True, text=True, env=env)

    def test_cli_valid(self):
        result = self.run_cli((ROOT / 'examples/maintainer/review_handoff.json').read_bytes())
        self.assertEqual(result.returncode, 0)
        self.assertIn('evidence not independently verified', result.stdout)
        self.assertEqual(result.stderr, '')

    def test_cli_invalid_json(self):
        for content in (b'PRIVATE-DEMO invalid', b'\xff', b'{"value":NaN}'):
            result = self.run_cli(content)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, '')
            self.assertNotIn('PRIVATE-DEMO', result.stderr)

    def test_cli_invalid_contract(self):
        result = self.run_cli(b'{"session_id":"demo","handoff":{"version":"private-value"}}')
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, '')
        self.assertIn('handoff.version_unsupported', result.stderr)
        self.assertNotIn('private-value', result.stderr)
