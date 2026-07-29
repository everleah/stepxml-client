# STEP XML Client Docs - AGENTS.md

## Purpose
Local contract for durable documentation artifacts under `docs/`.

## Ownership
- `CREATOR_STATUS.md`
- `CREATOR_USAGE.md`
- `INBOUND_OPERATIONS_SUMMARY.md`
- `PARSER_STATUS.md`
- `PARSER_USAGE.md`
- `REST_API_STATE.md`
- `REST_API_USAGE.md`
- `restapi/` — per-endpoint REST API reference documentation

## Local Contracts
- Keep status documents aligned with the current implementation, not with planned work.
- Keep usage documents consistent with the public package behavior and the supported test fixtures.
- Update docs when behavior, supported fields, or workflow expectations change.

## Work Guidance
- Prefer concise, factual updates that mirror the codebase.
- When a feature changes, update the matching status and usage document together.
- Avoid duplicating package implementation details that already belong in code comments or README.

## Verification
- Manual consistency review against the touched implementation.
- Any affected parser, creator, or REST client tests when documentation reflects a behavior change.

## Child DOX Index
- [restapi/](restapi/) — detailed REST API v2 endpoint documentation with examples