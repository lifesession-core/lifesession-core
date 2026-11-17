# Your first useful session report

Run from the repository root in a POSIX shell (Linux/macOS or equivalent).
CI verifies Python 3.10, 3.11 and 3.12. Start with 3.10+ recommended; other
versions are not necessarily unsupported, but have not been verified here.
No third-party dependencies: this is a source-checkout workflow, not pip install.

## Copy, edit, check, report

This creates a fresh temporary working directory, preserving the example and
existing files. Keep the printed path to inspect or copy your report later.

```sh
DEMO_DIR="$(mktemp -d)"
export DEMO_DIR
export PYTHONPATH="$PWD/src"
cp examples/maintainer/session_package.json "$DEMO_DIR/session-package.json"
python - <<'PY'
import json
import os
from pathlib import Path
path = Path(os.environ['DEMO_DIR']) / 'session-package.json'
package = json.loads(path.read_text(encoding='utf-8'))
package['session']['summary'] = 'Fictional fix prepared; maintainer review is still pending.'
path.write_text(json.dumps(package, indent=2) + '\n', encoding='utf-8')
PY
python -m lifesession check-package "$DEMO_DIR/session-package.json"
python - <<'PY'
import json
import os
from pathlib import Path
from lifesession.package import check_package
from lifesession.report import render_markdown
directory = Path(os.environ['DEMO_DIR'])
package = json.loads((directory / 'session-package.json').read_text(encoding='utf-8'))
if check_package(package):
    raise SystemExit('Package failed checks; no report written.')
report = directory / 'session-report.md'
with report.open('x', encoding='utf-8') as output:
    output.write(render_markdown(package['session']))
print(report.read_text(encoding='utf-8'))
print('Saved report:', report)
PY
```

Expected: `OK — package structure consistent; timestamps and evidence not verified.`
The report contains your edited summary, a fictional event and the decision
`needs_review`. Preparation is not acceptance. The saved report path is printed.
No service is contacted. Review before sharing: reporting is not sanitization.
Use fictional data for public contributions.

## Which format?

| Need | Input and command | Checks |
| --- | --- | --- |
| Read supplied work notes or Session.close() | Record with nonblank session_id; `report file.json` | Minimal envelope; unknown fields preserved |
| Check delivery/review consistency | review_handoff.json; `check-handoff file.json` | [Handoff v1](handoff-contract.md), not authenticity |
| Check linked snapshot records | Envelope with version/session; `check-package file.json` | [Package v1](session-package.md), documented schema subset and links |

Run commands as `python -m lifesession ...` with `PYTHONPATH=src`.
Do not feed a package envelope directly to report: render its session object as
above. Session.close() and the free-form handoff example are not strict snapshots.
No automatic migration or removal of unknown fields is performed.

Typical errors:
- `session.structure_invalid`: missing snapshot status, extra field or wrong type.
- `event.session_mismatch`: event session_id differs from the enclosing session.
- `mission.missing`: session.mission_id has no supplied mission.
- `handoff.review_requires_acknowledgment`: completed review without acknowledged delivery.

Exit 2 means failure. Exit 0 does not establish completion, authorization or full
JSON Schema conformance. Errors do not echo input values. Timestamps, ordering,
evidence authenticity and opaque evidence references are not checked.

## Next step

A human reviews the report and underlying evidence. Delivery, execution, durable
storage and independent acceptance are not automated. To verify the project:
`python -m unittest discover -s tests -v` and
`python src/lifesession/safety/boundary_checker.py .`.
