# STEP XML Client REST Client - AGENTS.md

## Purpose
Local contract for the STEP REST API v2 wrapper layer under `stepxmlclient/rest_client/`.

## Ownership
- `base.py`
- `client.py`
- `exceptions.py`
- `publishing.py` - optional v2 adapter implementing the independent Publishing job protocol.
- `models/`
- `operations/`

## Local Contracts
- Keep grouped operation wrappers aligned with the dynamic `requests-openapi` client and the STEP REST API specification supplied by the server or caller.
- Verify operation IDs and response shapes against an authorized local specification,
  not unrestricted mocks. Search endpoints are `queryProducts`, `queryAssets`,
  `queryClassifications` and `queryEntities`; their arrays contain IDs, not hydrated objects.
- Preserve shared error handling through the base operation layer.
- Route generated calls through `BaseOperation._call_operation`: check HTTP/STEP
  errors before discarding bodies or constructing models, and decode HTTP JSON.
  Keep the raw `.client` transport unchanged. Binary operations explicitly retain
  checked raw responses and close them after consuming content.
- Preserve status codes, STEP error details and `Retry-After` in exceptions;
  never reinterpret structured errors by matching digits in their messages.
- Keep request payloads compatible with the STEP REST API shapes documented in the repo notes.
- Avoid introducing duplicate REST client surfaces when an existing grouped wrapper can absorb the change.
- Publishing endpoints are not v2 operations. Only the main-client composition
  and job adapter may couple the two APIs; reuse BackgroundProcessOperations.
- Pass context/workspace to the base client and background-process group so
  the lazy Publishing integration inherits the same configuration.

## Work Guidance
- Update the matching operation group and any request/response model files together.
- Prefer `json=` for structured payloads and `data=` for raw payloads when wiring request calls.
- Keep wrapper names and group boundaries consistent with the current REST API organization.

## Verification
- `tests/test_rest_client_phase0_foundation.py`
- `tests/test_rest_client_phase1_products.py`
- `tests/test_rest_client_phase2_assets.py`
- `tests/test_rest_client_phase3_classifications.py`
- `tests/test_rest_client_phase4_entities.py`
- `tests/test_rest_client_phase5_attributes_metadata.py`
- `tests/test_rest_client_phase6_imports_exports.py`
- `tests/test_rest_client_phase7_relations.py`
- `tests/test_rest_client_oiep_download.py`
- `tests/test_rest_client_phase8_background_processes.py`
- `tests/test_publishing_integration.py`
- `tests/test_rest_client_spec_alignment.py` - independent synthetic contracts and
  optional authorized local-specification checks, never live requests.

## Child DOX Index
- [models/AGENTS.md](models/AGENTS.md) - REST payload and response shape models.
- [operations/AGENTS.md](operations/AGENTS.md) - grouped REST operation wrappers.