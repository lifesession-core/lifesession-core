# LifeSession Core

**An early-stage, local toolkit for reviewable maintainer and AI work sessions.**

LifeSession turns work into reviewable sessions — bounded units of operational attention with missions, events, decisions, and structured close records. Think of it as a lightweight structured log for anything your team or agent does.

[![CI](https://github.com/lifesession-core/lifesession-core/actions/workflows/ci.yml/badge.svg)](https://github.com/lifesession-core/lifesession-core/actions/workflows/ci.yml)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Status](https://img.shields.io/badge/status-active-green)

---

## Why LifeSession

Modern teams and AI agents produce a constant stream of decisions, events, and state changes — but most of that work is invisible. There is no structured record of what happened, why it was decided, or how to review it later.

LifeSession solves this with a simple operational model:

```
Mission → Session → Events → Decisions → State → Review
```

Sessions make supplied records reviewable; they do not make arbitrary input safe to share. The schemas describe records, while the local exporter checks only a minimal envelope. The boundary checker flags a limited set of patterns; manual review is still required.

---

## What Is Included

| Component | Description |
|-----------|-------------|
| `schemas/` | JSON schemas — mission, event, decision, session state |
| `examples/` | Fake end-to-end workflows: maintainer, commerce, gallery, simulation |
| `src/lifesession/` | Demo session lifecycle, local Markdown exporter, heuristic boundary checker |
| `tests/` | Unit tests covering sessions, reports, boundary checks, schemas and examples |
| `docs/` | Architecture, vision, Codex workflows, public/private boundary |
| `.github/` | Issue templates, PR templates, Python CI |

---

## Quickstart

```bash
git clone https://github.com/lifesession-core/lifesession-core.git
cd lifesession-core
python -m unittest discover -s tests -v
```

Expected result: the test suite finishes with `OK`. See the CI link for checks on a specific revision.

No external dependencies required.

---

## How Codex Maintains This Project

Maintainers can use [Codex](https://openai.com/codex) to prepare changes, with human review. This repository includes documented agent-assisted workflows; it does not run an autonomous maintenance service.

The intended contribution workflow follows the same lifecycle that LifeSession models:

1. **Read context** — task card, previous session handoff, git log
2. **Execute** — schema updates, test fixes, doc improvements, issue triage
3. **Verify** — run `unittest discover`, run `boundary_checker.py`
4. **Commit** — clean commit with task reference
5. **Handoff** — write session report for next agent or human review

This creates a self-referential loop: the tool that manages sessions is itself maintained through sessions. Contributors should attach verification and handoff evidence to each change.

**Suggested agent-assisted tasks:**
- Schema evolution and validation
- Test coverage expansion
- Documentation and roadmap updates
- Issue triage and PR review assistance
- Boundary compliance checking before any public push
- Release preparation

See [docs/codex-workflows.md](docs/codex-workflows.md) for the full workflow spec.

---

## Architecture

```text
                    ┌─────────────┐
                    │   Mission   │  goal + constraints
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │   Session   │  bounded unit of attention
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
       ┌──────▼────┐ ┌─────▼────┐ ┌────▼──────┐
       │  Events   │ │Decisions │ │   State   │
       └──────┬────┘ └─────┬────┘ └────┬──────┘
              └────────────┼────────────┘
                           │
                    ┌──────▼──────┐
                    │   Review    │  close record + summary
                    └─────────────┘
```

**Components:**
- **Mission** — the goal and constraints for a work period
- **Event** — observation, signal, user action, or system update
- **Decision** — reviewable choice with rationale and outcome
- **Session state** — current snapshot; review its contents before sharing
- **Boundary checker** — scans files for private-data patterns before any push

---

## Example Session (fake data)

```json
{
  "session_id": "sess-demo-001",
  "mission": "review open pull requests",
  "status": "closed",
  "events": [
    { "type": "pr_opened", "source": "github", "ref": "pr-42" },
    { "type": "review_requested", "source": "agent", "assignee": "maintainer" }
  ],
  "decisions": [
    { "title": "Merge PR-42", "outcome": "approved", "rationale": "tests pass, boundary clean" }
  ],
  "closed_at": "2026-06-06T10:00:00Z"
}
```

All examples in `examples/` use fake data only. See [docs/public-private-boundary.md](docs/public-private-boundary.md).

---

## Safety Boundary

This repository is simulation-first and public-safe by design:

- ✅ Schemas, fake examples, docs, demo stubs
- ❌ No production code, no live APIs, no secrets, no real user data
- ❌ No exchange integrations, no private infrastructure references

The `boundary_checker.py` tool checks for some obvious patterns, but cannot certify the absence of secrets or private data:

```bash
python src/lifesession/safety/boundary_checker.py .
# OK — no private-data patterns found.
```

---

## Roadmap

| Phase | Description | Status |
|-------|-------------|--------|
| 0 | Public skeleton — schemas, examples, docs, tests | ✅ Done |
| 1 | Local session runtime — validation, replay, text dashboard | 🔜 Next |
| 2 | Maintainer workflows — issue triage, decision review, close summaries | 📋 Planned |
| 3 | Integrations — optional adapters, strict boundary checks | 📋 Planned |

See [ROADMAP.md](ROADMAP.md) and [open issues](../../issues) for details.

---

## Contributing

Contributions welcome. Before submitting:

- Run `python -m unittest discover -s tests`
- Run `python src/lifesession/safety/boundary_checker.py .`
- No secrets, internal paths, or real data in any file

See [CONTRIBUTING.md](CONTRIBUTING.md) for full guidelines.

---

## License

MIT. See [LICENSE](LICENSE).

## Export a local session report

From the repository root, render a session JSON file as Markdown:

```bash
PYTHONPATH=src python -m lifesession report examples/maintainer/session_close.json
```

The command writes to standard output. To save a report, redirect it to a file
of your choice. It uses only the Python standard library and makes no network
requests. Invalid JSON, unreadable files, and missing or empty `session_id`
values return exit code 2 without printing input contents.

The exporter supports session snapshots and `Session.close()` records. Common
fields get readable sections; additional fields are preserved as literal JSON.
Text is fenced to prevent embedded Markdown or HTML from becoming report markup.
This checks the session envelope, not full schema conformance.

**Review before sharing:** exporting is not sanitization. The report preserves
input data, including any sensitive values you supply. Use the fake examples for
public demos. Python callers can use `lifesession.report.render_markdown(record)`.

## Reproducible maintainer handoff demo

```bash
PYTHONPATH=src python -m lifesession report examples/maintainer/review_handoff.json
```

This fictional example distinguishes a prepared patch from an accepted or released
change. It includes evidence, an unresolved blocker and the next review step.
It does not contact a service, open a PR or execute the next step. See
[the walkthrough](docs/maintainer-handoff-demo.md) for expected output and limits.

## Check a handoff before review

```bash
PYTHONPATH=src python -m lifesession check-handoff examples/maintainer/review_handoff.json
```

The optional [v1 handoff contract](docs/handoff-contract.md) requires explicit
delivery/review states, the next action, blockers and scoped evidence. It rejects
a completed review without acknowledged delivery. Exit code 0 means structural
consistency only, not independent verification or permission to publish. Failed
and unrun checks can be recorded honestly. No network or external action occurs.

### Check a local session package

An opt-in [v1 package check](docs/session-package.md) validates a single snapshot,
its events and decisions, and an optional linked mission using a documented
subset of the bundled schemas. Existing reports and handoffs are unchanged.

```sh
PYTHONPATH=src python -m lifesession check-package examples/maintainer/session_package.json
```
