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
- `background_process.py` - status fields accept v2 camelCase aliases and Python snake_case names.
- `__init__.py`

## Local Contracts
- Keep payload shapes aligned with the STEP REST API specification and the repo-level REST alignment notes.
- Prefer STEP REST fields and nested structures as documented by the API, not legacy STEP XML field names.
- Keep model helpers minimal and focused on translation between API shapes and wrapper code.
- Attribute definitions expose STEP's validator/multivalued/listOfValues fields;
  legacy aliases remain optional. LOV `values` is a metadata map, not the entry array.
- Classification `attributeLinks` accepts the STEP array shape; legacy maps remain accepted.
- Export requests use optional `stepUrls` / `processDescription`; import/export
  triggers return background-process `id`, not job status/progress records.

## Work Guidance
- Update model helpers together with the operation that consumes them.
- When request shapes change, update the related tests and any example payloads.
- Avoid adding extra abstraction layers unless multiple operations share the same translation logic.

## Verification
- Relevant REST client phase tests.
- Any targeted payload or round-trip test covering the touched model.

## Child DOX Index
- None.