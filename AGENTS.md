# AGENTS.md — LifeSession Core

LifeSession Core may be maintained with AI coding agents, but the public package
has a strict boundary.

## Generic Roles

- Owner: sets priorities and accepts releases.
- Architect: reviews design, safety, and repository structure.
- Coding agent: prepares isolated patches, tests, examples, and documentation.
- Inspector: checks boundary compliance and release readiness.

## Rules

- Do not add private infrastructure details.
- Do not add real secrets, tokens, IDs, or production paths.
- Do not add live trading, exchange, payment, or order execution code.
- Do not import from private systems.
- Keep examples fake and clearly labeled.
- Run the boundary checker before public release.
