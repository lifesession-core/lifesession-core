# Public / Private Boundary

LifeSession Core is public-safe only when it contains no private operations data.

## Public-Safe

A file is public-safe when all of these are true:

- no secrets, API keys, tokens, or credentials;
- no live trading, exchange, or order execution logic;
- no real user data, outcomes, or financial figures;
- no internal infrastructure details;
- useful to an OSS developer who has never used the private system.

## Private

Do not publish:

- production bots or command routers;
- private API servers;
- real signal intake or proprietary scoring logic;
- real database paths or operational logs;
- private agent memory;
- internal deployment topology;
- real Notion, Telegram, cloud, exchange, or organization IDs.

## Conditional

Some ideas can become public only after they are rewritten as standalone demos:

- indicator math without API calls;
- pattern examples without real databases;
- agent role descriptions without private routing or infrastructure;
- simulation-only trading-like examples with fake prices and fake tickers.

## Release Rule

Before public release, run boundary checks and perform human review.
