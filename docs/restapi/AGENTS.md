# STEP REST API Documentation — AGENTS.md

## Purpose
Local contract for per-endpoint REST API reference documentation under `docs/restapi/`.

## Ownership
- `index.md` — master index and quick reference
- `products.md`, `assets.md`, `classifications.md`, `entities.md` — entity type reference
- `attributes.md`, `data_type_groups.md` — type definitions
- `relations.md` — cross-references
- `inbound.md`, `outbound.md`, `gateway.md` — integration endpoints
- `contexts.md`, `system_information.md` — system metadata
- `users.md`, `user_groups.md` — user management
- `collections.md`, `collection_groups.md` — collection management
- `workflows.md`, `workflow_tasks.md` — workflow automation
- `background_processes.md`, `event_processors.md` — async processing
- `exports.md`, `reports.md`, `batch.md` — data transfer

## Local Contracts
- Each document covers exactly one operation group.
- Documents follow the same template: title, group/import path, description, operations table, examples.
- Operation signatures must match the actual Python method signatures in `stepxmlclient/rest_client/operations/`.
- Examples must be self-contained and runnable (modulo authentication setup).

## Work Guidance
- When a new operation is added to an existing group, add a row to the operations table.
- When a new operation group is created, add a new document and update `index.md`.
- Keep the `index.md` categories in sync with the group listing in `client.py`.

## Verification
- Manual review against the OpenAPI v1.4.0 specification.
- Cross-reference operation signatures against the source code.

## Child DOX Index
- None.
