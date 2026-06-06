import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from lifesession.safety.boundary_checker import scan_directory


class BoundaryCheckerTests(unittest.TestCase):
    def test_clean_examples_return_no_issues(self):
        issues = scan_directory(ROOT / "examples")

        self.assertEqual(issues, [])

    def test_internal_deploy_path_is_flagged(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "leak.txt"
            private_path = "/" + "home" + "/" + "deploy" + "/" + "something"
            path.write_text(f"Do not publish {private_path}", encoding="utf-8")

            issues = scan_directory(tmp)

        self.assertGreaterEqual(len(issues), 1)
        self.assertEqual(issues[0]["label"], "internal deploy path")

    def test_fake_ip_is_flagged(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ip.txt"
            fake_ip = ".".join(["192", "168", "1", "1"])
            path.write_text(f"Example private IP {fake_ip}", encoding="utf-8")

            issues = scan_directory(tmp)

        self.assertGreaterEqual(len(issues), 1)
        self.assertEqual(issues[0]["label"], "IP address")

    def test_boundary_checker_does_not_flag_its_own_source(self):
        source_dir = ROOT / "src" / "lifesession" / "safety"

        issues = scan_directory(source_dir)

        self.assertEqual(issues, [])


if __name__ == "__main__":
    unittest.main()
