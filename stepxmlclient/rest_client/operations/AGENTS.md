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
- `__init__.py`

## Local Contracts
- Keep each operation group focused on a single API area and its associated parameter mapping.
- Preserve existing shared error handling and response normalization paths.
- Keep inbound and bulk helpers compatible with the rest client entry points that call them.

## Work Guidance
- Update the corresponding model helpers when an operation changes request or response shapes.
- Keep method names and grouping consistent with the public REST client surface.
- Prefer small wrapper adjustments over ad hoc request construction in call sites.

## Verification
- Relevant REST client phase tests.
- `test_inbound_available.py`
- `test_inbound_operations.py`
- `test_rest_client_oiep_download.py`

## Child DOX Index
- None.