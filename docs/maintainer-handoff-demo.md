# Maintainer handoff demo (fictional)

## Problem

A prepared patch, a delivered handoff, an accepted review and a released change
are different outcomes. This demo keeps the difference visible in one local report.
All data is invented, not copied from a production session.

## Run

From the repository root, with Python and no additional dependencies:

```bash
PYTHONPATH=src python -m lifesession report examples/maintainer/review_handoff.json
PYTHONPATH=src python -m lifesession check-handoff examples/maintainer/review_handoff.json
python -m unittest discover -s tests -v
python src/lifesession/safety/boundary_checker.py .
```

The report begins with `# LifeSession report`. It contains Mission, Summary,
Events and Decisions sections. The Additional fields section preserves the
`handoff` object, including `delivery_status: not_sent`, `review_status: pending`,
the next action and the limited scope of the fictional test evidence. Repeating
the command with unchanged input produces identical output.

## What works and what does not

The exporter is a deterministic renderer, not an orchestrator. It does not verify
that an event occurred, enforce a workflow state machine, validate all schemas,
redact input, send messages, publish code or grant authorization. Handoff fields
are preserved extension data. The optional `check-handoff` command checks the
[version 1 handoff contract](handoff-contract.md), not the entire session schema. A human must review
the evidence and decide the next action.

Do not pass private session data to a public demo. The boundary checker is only
a heuristic; a clean result is not proof that a file is safe to publish.
