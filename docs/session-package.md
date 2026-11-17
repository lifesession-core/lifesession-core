# Local session package v1

Run from the repository checkout (Python 3.10+; no extra dependencies):

```sh
PYTHONPATH=src python -m lifesession check-package examples/maintainer/session_package.json
```

A package is an object with string `version: "1"`, required `session`,
optional `mission` and optional string `note`. Other envelope fields fail.
The session uses the bundled session_state schema; its events and decisions
are additionally checked against their respective bundled schemas.
The optional mission uses the mission schema. A session mission_id requires
a supplied matching mission; a supplied mission requires a matching mission_id.

The checker implements only the bundled schemas' type, required, properties,
additionalProperties, enum and items checks. It is **not a full JSON Schema
validator**. In particular date-time formats, timestamp chronology, event
ordering, evidence references and authenticity are not checked. Decision
evidence strings are opaque, not assumed to be event IDs. No external schema
references are fetched. The schemas directory must accompany this checkout.

Session, event, decision and mission identifiers must be nonblank. Event IDs
must be unique among events and decision IDs among decisions. Event and decision
session_id values must match the enclosing session. Cross-kind IDs may coincide.
No action follows an approved outcome: all records are inert input data.
The checker returns fixed error codes, not offending values. Exit 0 means
these structural checks passed; exit 2 means failure.

## Compatibility

This is a new **opt-in package format**, not a replacement for report or
check-handoff. Session.close() summaries and the existing handoff example are
not strict session snapshots and must not be wrapped blindly as packages.
They remain supported by their existing commands unchanged. No implicit
migration, field removal or change to the bundled schemas is performed.

To render a checked package's session without modifying the fixture:

```sh
PYTHONPATH=src python - <<'PY'
import json
from pathlib import Path
from lifesession.package import check_package
from lifesession.report import render_markdown
data = json.loads(Path("examples/maintainer/session_package.json").read_text())
assert not check_package(data)
print(render_markdown(data["session"]), end="")
PY
```

Input is not sanitized. Reports preserve data: review before sharing. Passing
checks proves neither completion, independent acceptance nor production safety.
