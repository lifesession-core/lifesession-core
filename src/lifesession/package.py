"""Opt-in local package checks. Not a general JSON Schema validator."""
import json
from pathlib import Path

SCHEMAS = Path(__file__).resolve().parents[2] / "schemas"


def _matches(value, schema):
    """The type/required/properties/items/enum subset used by bundled schemas.

    date-time format and schema metadata are deliberately not interpreted.
    Schemas are bundled project files, never input-selected or fetched.
    """
    types = schema.get("type")
    if types:
        types = types if isinstance(types, list) else [types]
        checks = {"object": isinstance(value, dict), "array": isinstance(value, list),
                  "string": isinstance(value, str), "null": value is None}
        if not any(checks.get(t, False) for t in types):
            return False
    if "enum" in schema and value not in schema["enum"]:
        return False
    if isinstance(value, dict):
        properties = schema.get("properties", {})
        if any(key not in value for key in schema.get("required", [])):
            return False
        if schema.get("additionalProperties") is False and any(k not in properties for k in value):
            return False
        return all(_matches(v, properties[k]) for k, v in value.items() if k in properties)
    if isinstance(value, list) and "items" in schema:
        return all(_matches(v, schema["items"]) for v in value)
    return True


def check_package(package):
    """Check a v1 single-session snapshot package without modifying its input.

    Fixed diagnostics never contain input values. No execution or publication.
    """
    if not isinstance(package, dict):
        return ["package.object_required"]
    errors = []
    if package.get("version") != "1":
        errors.append("package.version_unsupported")
    if set(package) - {"version", "session", "mission", "note"}:
        errors.append("package.unknown_field")
    if "note" in package and not isinstance(package["note"], str):
        errors.append("package.note_invalid")
    schemas = {}
    for name in ("session_state", "event", "decision", "mission"):
        schemas[name] = json.loads((SCHEMAS / (name + ".schema.json")).read_text(encoding="utf-8"))
    session = package.get("session")
    if not _matches(session, schemas["session_state"]):
        return errors + ["session.structure_invalid"]
    sid = session["session_id"]
    if not sid.strip():
        errors.append("session.id_required")
    for name, field in (("event", "events"), ("decision", "decisions")):
        seen = set()
        for record in session.get(field, []):
            if not _matches(record, schemas[name]):
                errors.append(name + ".structure_invalid")
                continue
            if not record["id"].strip():
                errors.append(name + ".id_required")
            if record["id"] in seen:
                errors.append(name + ".duplicate_id")
            seen.add(record["id"])
            if record["session_id"] != sid:
                errors.append(name + ".session_mismatch")
    mission = package.get("mission")
    if "mission" in package:
        if not _matches(mission, schemas["mission"]):
            errors.append("mission.structure_invalid")
        else:
            if not mission["id"].strip():
                errors.append("mission.id_required")
            if session.get("mission_id") != mission["id"]:
                errors.append("mission.link_mismatch")
    elif "mission_id" in session:
        errors.append("mission.missing")
    return list(dict.fromkeys(errors))
