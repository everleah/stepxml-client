# STEP XML Client REST Models - AGENTS.md

## Purpose
Local contract for REST request and response shape helpers under `stepxmlclient/rest_client/models/`.

## Ownership
- `asset.py`
- `attribute.py`
- `bulk.py`
- `classification.py`
- `common.py`
- `entity.py`
- `import_export.py`
- `metadata.py`
- `product.py`
- `relations.py`
- `__init__.py`

## Local Contracts
- Keep payload shapes aligned with `openapi.json` and the repo-level REST alignment notes.
- Prefer STEP REST fields and nested structures as documented by the API, not legacy STEP XML field names.
- Keep model helpers minimal and focused on translation between API shapes and wrapper code.

## Work Guidance
- Update model helpers together with the operation that consumes them.
- When request shapes change, update the related tests and any example payloads.
- Avoid adding extra abstraction layers unless multiple operations share the same translation logic.

## Verification
- Relevant REST client phase tests.
- Any targeted payload or round-trip test covering the touched model.

## Child DOX Index
- None.