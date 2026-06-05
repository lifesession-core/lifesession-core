# Architecture

LifeSession Core uses a small conceptual model.

```text
Mission -> Session -> Events -> Decisions -> State -> Review
```

## Components

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
