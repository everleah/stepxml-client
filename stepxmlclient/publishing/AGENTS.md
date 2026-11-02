# STEP Publishing Client

## Purpose
- Independent client for the Publishing REST API under `/restapi`.

## Ownership
- HTTP operations, Publishing XML models, XML decoding, job backend protocol and monitoring.

## Local Contracts
- Do not import REST v2 operations, models or base classes in this package.
- Connect job monitoring through `JobBackend`; the v2 adapter belongs to `rest_client/`.
- All 16 documented operations are supported without bundling vendor specifications.
- Preserve unmodeled XML through `raw_xml` and original node attributes.
- Preserve `PagesPerSpread` as a string, as declared by Publishing XSD/OpenAPI.
- Do not enforce the vendor XSD on responses: its empty `actualPageList`
  contradicts documented page-list examples, and publication templates are omitted.
- Require explicit confirmation for document replacement and deletion, which can affect multiple pages.
- Borrowed sessions are not mutated globally or closed; owned sessions must be closed.
- Job Location is only a source of process identity, never an authenticated download URL.
- Missing, ambiguous or malformed results are errors, not successful empty fallbacks.

## Work Guidance
- Use requests and existing Pydantic; no dynamic dependency on the Publishing OpenAPI file.
- Keep Publishing independent of STEP-XML exchange parsing and generation.

## Verification
- `python -m unittest discover -s tests -p "test_publishing_*.py"`
- Authorized server checks are separate from offline contract tests.

## Child DOX Index
- None.
