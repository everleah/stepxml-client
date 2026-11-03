# STEP XML Client Package - AGENTS.md

## Purpose
Package-local contract for the public Python package surface under `stepxmlclient/`.

## Ownership
- `__init__.py`
- `parser.py`
- `creator.py`
- `upload.py`
- `model/`
- `rest_client/`
- `publishing/`

## Local Contracts
- Preserve `STEPXML_NS` and namespace-aware parsing behavior across package entry points.
- Keep parser, creator, and uploader changes aligned with the STEP XML schema and the test fixtures.
- Keep public imports stable unless a deliberate API change is being made and documented.
- REST request and response shapes follow the STEP REST API specification, fetched from the server, supplied by the caller, or optionally bundled from local build inputs under the root contract.
- Publishing is a separate API implementation, composed lazily into both main
  clients. It must not import REST v2 operations/models; job integration is injected.
- Borrowed sessions retain their authentication/TLS/proxy settings and remain
  owned by the caller. Publishing does not change global session headers.
- REST server specification bootstrap must use the configured authenticated
  request session, TLS and proxies before any remote spec request. Local specs
  retain their loading priority, including optionally bundled `openapi.json`.
- Authentication hooks run once; during remote bootstrap they configure the
  session before generated operations exist. Local specs are loaded before hooks.

## Work Guidance
- Prefer focused parser, creator, or REST client tests over broad repo-wide changes.
- Update package-facing documentation when exported behavior changes.
- Preserve existing naming and grouping conventions for models and REST wrappers.

## Verification
- Relevant parser and creator phase tests.
- Relevant REST client phase tests.
- Targeted behavior tests for the touched module.

## Child DOX Index
- [model/AGENTS.md](model/AGENTS.md) - STEP XML object model hierarchy.
- [rest_client/AGENTS.md](rest_client/AGENTS.md) - REST API client wrappers and grouped operations.
- [publishing/AGENTS.md](publishing/AGENTS.md) - independent Publishing API and job backend.