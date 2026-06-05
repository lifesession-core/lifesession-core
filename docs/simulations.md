# Simulations

LifeSession simulations are demo-only event replays.

They exist to show how a session can receive events, produce decisions, and
close with a reviewable summary. Simulations must not call real APIs or execute
real actions.

## Allowed

- Fake tickers and fake prices.
- Fake maintainer issues.
- Fake product drops.
- Fake gallery curation events.
- Deterministic local event replay.

## Not Allowed

- Exchange API calls.
- Real order placement.
- Real customer data.
- Real production logs.
- Hidden network calls.
