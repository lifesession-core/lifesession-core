import sys
import unittest
import uuid
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from lifesession.core.session import Session


class SessionTests(unittest.TestCase):
    def test_session_opens_with_defaults(self):
        session = Session(session_type="maintainer", owner="alice@example.test")

        self.assertEqual(session.status, "open")
        uuid.UUID(session.session_id)
        self.assertIsNotNone(session.opened_at)
        self.assertIsNone(session.closed_at)

    def test_close_returns_reviewable_dict(self):
        session = Session(session_type="maintainer", owner="alice@example.test")

        result = session.close(summary="Reviewed fake queue.")

        self.assertEqual(result["session_id"], session.session_id)
        self.assertIn("closed_at", result)
        self.assertEqual(result["summary"], "Reviewed fake queue.")

    def test_close_sets_status_closed(self):
        session = Session(session_type="maintainer", owner="alice@example.test")

        session.close()

        self.assertEqual(session.status, "closed")
        self.assertIsNotNone(session.closed_at)

    def test_two_sessions_have_different_ids(self):
        first = Session(session_type="maintainer", owner="alice@example.test")
        second = Session(session_type="maintainer", owner="alice@example.test")

        self.assertNotEqual(first.session_id, second.session_id)


if __name__ == "__main__":
    unittest.main()
