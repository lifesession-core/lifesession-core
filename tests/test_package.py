import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from lifesession.package import check_package
from lifesession.core.session import Session
from lifesession.report import render_markdown
from lifesession.handoff import check_handoff


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / "examples/maintainer/session_package.json").read_text())

    def test_bundled_schema_subset_is_explicit(self):
        allowed = {"$schema", "$id", "title", "description", "type", "required",
                   "properties", "additionalProperties", "enum", "items", "format"}
        def walk(schema):
            self.assertFalse(set(schema) - allowed)
            types = schema.get("type", [])
            types = [types] if isinstance(types, str) else types
            self.assertFalse(set(types) - {"object", "array", "string", "null"})
            if "format" in schema:
                self.assertEqual(schema["format"], "date-time")
            for child in schema.get("properties", {}).values():
                walk(child)
            if "items" in schema:
                walk(schema["items"])
        for name in ("session_state", "event", "decision", "mission"):
            walk(json.loads((ROOT / "schemas" / (name + ".schema.json")).read_text()))

    def test_success_immutable(self):
        original = copy.deepcopy(self.data)
        self.assertEqual(check_package(self.data), [])
        self.assertEqual(self.data, original)

    def test_invalid_roots(self):
        for value in (None, [], 1, "secret"):
            self.assertEqual(check_package(value), ["package.object_required"])

    def test_version(self):
        for version in (None, 1, [], "2"):
            self.data["version"] = version
            self.assertIn("package.version_unsupported", check_package(self.data))

    def test_envelope(self):
        self.data["private-field"] = "private-value"
        self.data["note"] = []
        errors = check_package(self.data)
        self.assertIn("package.unknown_field", errors)
        self.assertIn("package.note_invalid", errors)
        self.assertNotIn("private", str(errors))

    def test_minimal_snapshot(self):
        self.assertEqual(check_package({"version": "1", "session": {"session_id": "demo", "status": "open"}}), [])

    def test_missing_required_fields(self):
        for section in ("session", "mission"):
            for key in ("session_id", "status") if section == "session" else ("id", "title", "status", "created_at"):
                data = copy.deepcopy(self.data)
                del data[section][key]
                self.assertTrue(check_package(data))
        for field in ("events", "decisions"):
            for key in self.data["session"][field][0]:
                data = copy.deepcopy(self.data)
                del data["session"][field][0][key]
                self.assertTrue(check_package(data))

    def test_record_type_and_unknown_fields(self):
        for field in ("events", "decisions"):
            for record in (None, [], {}, {"private": "value"}):
                data = copy.deepcopy(self.data)
                data["session"][field] = [record]
                self.assertTrue(check_package(data))
        self.data["session"]["unexpected"] = 1
        self.assertIn("session.structure_invalid", check_package(self.data))

    def test_duplicates_and_links(self):
        for field, name in (("events", "event"), ("decisions", "decision")):
            data = copy.deepcopy(self.data)
            item = data["session"][field][0]
            item["session_id"] = "other"
            data["session"][field].append(copy.deepcopy(item))
            errors = check_package(data)
            self.assertIn(name + ".duplicate_id", errors)
            self.assertIn(name + ".session_mismatch", errors)

    def test_mission_links(self):
        self.data["mission"]["id"] = "other"
        self.assertIn("mission.link_mismatch", check_package(self.data))
        del self.data["mission"]
        self.assertIn("mission.missing", check_package(self.data))

    def test_blank_ids(self):
        for section, field in (("session", "session_id"), ("mission", "id")):
            data = copy.deepcopy(self.data)
            data[section][field] = " "
            self.assertIn(section + ".id_required", check_package(data))
        for field, name in (("events", "event"), ("decisions", "decision")):
            data = copy.deepcopy(self.data)
            data["session"][field][0]["id"] = " "
            self.assertIn(name + ".id_required", check_package(data))

    def test_optional_types(self):
        self.data["mission"]["constraints"] = [1]
        self.assertIn("mission.structure_invalid", check_package(self.data))
        self.data["session"]["decisions"][0]["evidence"] = [False]
        self.assertIn("decision.structure_invalid", check_package(self.data))

    def test_enums(self):
        self.data["session"]["status"] = "done"
        self.assertIn("session.structure_invalid", check_package(self.data))
        self.data["session"]["status"] = "waiting"
        self.data["session"]["decisions"][0]["outcome"] = "maybe"
        self.assertIn("decision.structure_invalid", check_package(self.data))

    def test_explicit_limits(self):
        self.data["session"]["events"][0]["created_at"] = "not-a-time"
        self.data["session"]["decisions"][0]["evidence"] = ["opaque-reference"]
        self.assertEqual(check_package(self.data), [])

    def test_legacy_compatibility(self):
        closed = Session("demo", "fictional").close()
        self.assertIn("# LifeSession report", render_markdown(closed))
        handoff = json.loads((ROOT / "examples/maintainer/review_handoff.json").read_text())
        self.assertEqual(check_handoff(handoff), [])
        self.assertIn("# LifeSession report", render_markdown(handoff))
        self.assertIn("session.structure_invalid", check_package({"version": "1", "session": closed}))

    def test_cli(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input.json"
            env = dict(os.environ, PYTHONPATH=str(ROOT / "src"))
            for content, code in ((json.dumps(self.data), 0), ('{"version":"PRIVATE"}', 2), ("invalid PRIVATE", 2)):
                path.write_text(content)
                result = subprocess.run([sys.executable, "-m", "lifesession", "check-package", str(path)], env=env, text=True, capture_output=True)
                self.assertEqual(result.returncode, code)
                self.assertNotIn("PRIVATE", result.stderr)
                if code:
                    self.assertEqual(result.stdout, "")
