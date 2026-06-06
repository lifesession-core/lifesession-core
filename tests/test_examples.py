import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"


class ExampleTests(unittest.TestCase):
    def test_all_examples_are_valid_json_and_marked_fake(self):
        files = sorted(EXAMPLES.rglob("*.json"))

        self.assertGreater(len(files), 0)
        for path in files:
            with self.subTest(example=str(path.relative_to(ROOT))):
                data = json.loads(path.read_text(encoding="utf-8"))
                self.assertIn("note", data)

    def test_trading_sim_examples_are_simulation_mode(self):
        files = sorted((EXAMPLES / "trading_sim").glob("*.json"))

        self.assertGreater(len(files), 0)
        for path in files:
            with self.subTest(example=path.name):
                data = json.loads(path.read_text(encoding="utf-8"))
                self.assertIs(data.get("simulation_mode"), True)


if __name__ == "__main__":
    unittest.main()
