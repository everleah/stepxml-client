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

## Local Contracts
- Preserve `STEPXML_NS` and namespace-aware parsing behavior across package entry points.
- Keep parser, creator, and uploader changes aligned with the STEP XML schema and the test fixtures.
- Keep public imports stable unless a deliberate API change is being made and documented.
- When REST-facing code changes, align request and response shapes with `openapi.json` and the repo-level REST model notes.

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