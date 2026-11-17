# Architecture

LifeSession Core uses a small conceptual model.

```text
Mission -> Session -> Events -> Decisions -> State -> Review
```

## Conceptual components (not all implemented)

- Mission: the goal and constraints for a work period.
- Event: an observation, signal, user action, or system update.
- Decision: a reviewable choice with rationale and status.
- Session state: the current snapshot of a session.
- Router: maps incoming events to sessions or missions.
- Dashboard: renders readable session summaries.
- Simulation engine: replays fake events for examples and tests.
- Boundary checker: scans public files for obvious private-data leaks.

## Storage

The skeleton does not mandate a database. Examples are JSON files. Future
implementations may add adapters, but public adapters must remain opt-in and
safe by default.


## Implemented today

Demo Session and close summary; local Markdown report; opt-in handoff and package
structural checks; bundled schemas, fictional examples and heuristic boundary
scanning. See [the first-session walkthrough](first-session.md).

## Planned, not implemented

Router, event replay/simulation engine, interactive dashboard, durable storage,
service adapters, automatic delivery and authenticated receipts are not provided.
The simulations directory and fictional examples are not a working replay engine.
Local checks do not independently verify evidence or authorize external actions.
