import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"


class SchemaTests(unittest.TestCase):
    def _load_schema(self, name):
        with (SCHEMAS / name).open(encoding="utf-8") as fh:
            return json.load(fh)

    def test_all_schemas_have_base_fields(self):
        for path in sorted(SCHEMAS.glob("*.json")):
            with self.subTest(schema=path.name):
                data = json.loads(path.read_text(encoding="utf-8"))
                self.assertIn("$schema", data)
                self.assertIn("title", data)
                self.assertIn("type", data)
                self.assertIn("properties", data)

    def test_mission_required_fields(self):
        schema = self._load_schema("mission.schema.json")

        self.assertTrue({"id", "title", "status", "created_at"}.issubset(schema["required"]))

    def test_event_required_fields(self):
        schema = self._load_schema("event.schema.json")

        self.assertTrue({"id", "type", "source"}.issubset(schema["required"]))

    def test_decision_required_fields(self):
        schema = self._load_schema("decision.schema.json")

        self.assertTrue({"id", "title", "outcome"}.issubset(schema["required"]))

    def test_session_state_required_fields(self):
        schema = self._load_schema("session_state.schema.json")

        self.assertTrue({"session_id", "status"}.issubset(schema["required"]))


if __name__ == "__main__":
    unittest.main()
