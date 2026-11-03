# STEP XML Client Test Suite - AGENTS.md

## Purpose
Local contract for the test suite under `tests/`.

## Ownership
All test and validation modules in this directory:
- `test_parser_phase*.py` — STEP-XML parser phase tests
- `test_rest_client_phase*.py` — REST API v2 client phase tests
- `test_rest_client_oiep_download.py` — OIEP download integration test
- `test_inbound_*.py` — inbound endpoint tests
- `test_creator_*.py`, `test_upload.py` — creator and upload tests
- `test_*fix*.py` — targeted bug-fix regression tests
- `test_*helpers*.py`, `test_*reference*.py` — entity-helper and reference tests
- `test_*debug*.py`, `test_*namespace*.py`, `test_*objects*.py` — focused behaviour tests
- `test.py` — manual connectivity / example script
- `validate_xml_xsd.py` — XML schema validation
- `test_release.py` — offline release archive, credential handling, and upload safeguards
- `test_publishing_*.py` - independent Publishing endpoints, XML, jobs and lazy v2 integration.
- `test_rest_client_phase8_background_processes.py` - status/attachment transport used by Publishing.
- `test_rest_response_handling.py` - real HTTP responses, all delete wrappers,
  typed JSON normalization, empty reference bodies and synthetic OpenAPI transport.

## Local Contracts
- Tests use `unittest` with `unittest.mock` for client mocking; no live server is required to run the suite.
- Phase test files follow a sequential numbering scheme: `test_parser_phaseN_<topic>.py` and `test_rest_client_phaseN_<topic>.py`.
- Every new REST operation group must be accompanied by a corresponding phase test.
- Publishing fixtures are synthetic and do not require vendor JSON/WADL/XSD.
  The fake HTTP adapter exercises real requests-openapi transport without a live server.
- Parser tests validate against real STEP-XML fixture data in `examples/`.

## Work Guidance
- Mock `requests_openapi.Client` methods directly when testing operation wrappers; do not mock the wrapper itself.
- Prefer `unittest.TestCase` over pytest fixtures to stay consistent with the existing suite.
- When adding a new phase, use the next available number and document the covered domain in the module docstring.

## Verification
- `python -m unittest discover -s tests -p "test_*.py"` runs test discovery; schema validation also requires an authorized local `STEP.xsd`.
- Individual phase files can be executed directly: `python tests/test_parser_phase2.py`.
- `python -m unittest tests.test_release` verifies the PyPI workflow without uploading; requires `requirements-release.txt`.

## Child DOX Index
- None.
