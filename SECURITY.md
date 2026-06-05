# Security Policy

## Reporting

Please report suspected vulnerabilities through the project's security contact
or a private maintainer channel. Do not open a public issue for secrets, data
leaks, or exploitable behavior.

## Public Package Rules

- Do not commit secrets, tokens, private keys, credentials, or `.env` files.
- Do not include real user data, real operational logs, or private organization IDs.
- Do not add live trading, exchange, payment, or production infrastructure integrations.
- Keep examples fake and simulation-only.

## Supported Scope

This repository is an OSS skeleton and demo package. Security reviews should
focus on accidental data exposure, unsafe examples, dependency changes, and
boundary violations.
