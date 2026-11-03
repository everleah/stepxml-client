# STEP XML Client REST Operations - AGENTS.md

## Purpose
Local contract for grouped STEP REST API operations under `stepxmlclient/rest_client/operations/`.

## Ownership
- `assets.py`
- `attributes.py`
- `bulk.py`
- `classifications.py`
- `entities.py`
- `exports.py`
- `imports.py`
- `inbound.py`
- `metadata.py`
- `products.py`
- `relations.py`
- `background_processes.py` - v2 process status and attachment transport used by the Publishing adapter.
- `__init__.py`

## Local Contracts
- Keep each operation group focused on a single API area and its associated parameter mapping.
- Classification/entity CRUD and classification children use the existing typed
  models and `_call_operation`, with context/workspace and optional alternate keys.
- LOV operations are `getListOfValues` / `getListOfValuesEntries` on
  `/list-of-values`; definitions contain metadata, entries are a separate resource.
- Preserve existing shared error handling and response normalization paths.
- Use `_call_operation` for every generated OpenAPI request, including deletes
  and dynamically selected reference operations. Deletes return `True` only after
  response validation; reference PUTs always send JSON, including `{}`.
- Re-raise `RestClientError` unchanged before legacy exception-message fallbacks,
  so HTTP status, server messages and details survive operation-level handlers.
- Keep inbound and bulk helpers compatible with the rest client entry points that call them.
- Background-process status, attachment lists and binary content normalize HTTP
  responses and native payloads, preserve errors, and accept optional request timeouts.

## Work Guidance
- Update the corresponding model helpers when an operation changes request or response shapes.
- Keep method names and grouping consistent with the public REST client surface.
- Prefer small wrapper adjustments over ad hoc request construction in call sites.

## Verification
- Relevant REST client phase tests under `tests/`.
- `tests/test_inbound_available.py`
- `tests/test_inbound_operations.py`
- `tests/test_rest_client_oiep_download.py`

## Child DOX Index
- None.