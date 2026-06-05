# Codex Workflows

Codex can help maintain LifeSession Core as a patch and QA worker.

## Good Tasks

- Add or update JSON schemas.
- Add fake example sessions.
- Improve docs.
- Write local tests.
- Refactor demo-only package code.
- Run boundary checks.

## Unsafe Tasks

- Import private code.
- Add production credentials or private paths.
- Add live trading, payment, or infrastructure operations.
- Convert private logs or real user data into public examples.

## Recommended Handoff

Every patch should include:

- what changed;
- files changed;
- tests run;
- boundary risks;
- what a human reviewer should verify.
