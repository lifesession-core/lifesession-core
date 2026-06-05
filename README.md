# LifeSession Core

LifeSession is an open-source operational terminal for maintainers and small teams.

It helps teams turn work into reviewable sessions: missions, events, decisions,
state updates, and simulation logs. The public package is intentionally small and
safe: it contains schemas, fake examples, documentation, and demo-only Python
stubs. It does not include production infrastructure, private data, live trading,
exchange integrations, or internal automation code.

## What Is Included

- JSON schemas for missions, events, decisions, and session state.
- Fake example workflows for maintainers, commerce, gallery curation, and trading-like simulation.
- A tiny Python package for session lifecycle demos.
- A boundary checker that scans files for obvious private-data leaks.
- GitHub issue, pull request, and CI stubs.

## Quickstart

```bash
cd lifesession-core
python -m unittest discover -s tests
```

This skeleton currently has no external runtime dependencies.

## Safety Boundary

The public package is simulation-first. It must not import private systems, call
real exchange APIs, contain secrets, expose internal paths, or include real user
data. See [docs/public-private-boundary.md](docs/public-private-boundary.md).

## License

MIT. See [LICENSE](LICENSE).
