# Local handoff contract v1

`check-handoff` checks a session record's `handoff` extension without network
access, publication, state transitions or executing `next_action`. It is an
opt-in contract; the existing report command still accepts older records.

Required fields:

- Record: nonempty string `session_id` and object `handoff`.
- `version`: the string `1`.
- `delivery_status`: `not_sent`, `sent` or `acknowledged`.
- `review_status`: `pending`, `accepted` or `changes_requested`.
- `next_action`: nonempty text, including an explicit no-action note if complete.
- `blockers`: a list of nonempty strings; an empty list is valid.
- `evidence`: a nonempty list of objects, each with nonempty `kind`, `scope`,
  `limitations` and a `result` of `passed`, `failed`, `not_run` or `blocked`.

A completed review (`accepted` or `changes_requested`) requires
`delivery_status: acknowledged`. This convention means the reviewer received
the handoff; it does not claim the software contacted that reviewer.
Additional fields are preserved/allowed. Evidence may report failed or unrun
checks: the tool checks that their status is explicit, not that work is ready.

Exit code 0 means the contract is structurally consistent. Exit code 2 means
invalid input or inconsistent fields. Diagnostics contain fixed codes, not user
values or paths. Neither outcome establishes the truth of supplied evidence,
permission to merge, absence of sensitive data or full JSON Schema validation.
No approvals are inferred from prose. This checker does not sanitize data.
