# STEP XML Client - AI Coding Agent Instructions - AGENTS.md (project root)

## Project Overview
This is a reusable Python client library for integrating with Stibo Systems STEP MDM (Master Data Management). It supports standard STEP-XML protocol (OIEP/IIEP) and STEP REST API v2.

## Architecture
The module is structured into distinct functional areas:
- **`stepxmlclient/parser.py`**: Robust XML parser that deserializes STEP-XML into Python dictionaries. Aggregate specifically typed lists (`self.products`, `self.assets`, `self.attributes`, etc.). Supports a wide range of STEP entities (Products, Assets, Classifications, Attributes, Business Rules, etc.).
- **`stepxmlclient/creator.py`**: XML generator for creating STEP-XML documents from Python objects.
- **`stepxmlclient/model/`**: Object models inheriting from `BaseObject`. These classes define the structure of STEP entities for generation/manipulation (`Product`, `Asset`, `Attribute`, `Classification`, etc.).
- **`stepxmlclient/client.py`**: REST API configuration wrapper around `requests-openapi`.
- **`stepxmlclient/upload.py`**: Specialized client for binary asset uploads (images, documents).
- **`STEP.xsd`**: Authoritative XML schema used for validation.

## Critical Patterns & Conventions

### 1. Namespace Handling
STEP-XML uses standard namespaces. Always use `STEPXML_NS` from `__init__.py`:
```python
STEPXML_NS = {
    'step': 'http://www.stibosystems.com/step',
    'outputtemplate': 'http://www.stibosystems.com/step/outputtemplate'
}
```
In the parser, use `_get_local_tag(element)` to handle tags effectively, as they may or may not have namespace prefixes depending on the source.

### 2. Object Model & `BaseObject`
All model classes must inherit from `BaseObject` and use declarative configuration:
```python
class MyEntity(BaseObject):
    _GROUP_NAME = 'my_entities' # For creator collection
    _TAG_NAME = 'MyEntity'      # XML Element Tag
    _ATTRIBUTE_NAMES = ("ID", "UserTypeID")
    _TEXT_NAMES = ("Name",)
    _CHILDREN_NAMES = ("Values",) # Ordered list of child elements
```
- **Serialization**: `to_element()` uses these configs to auto-generate XML.
- **Children**: Use `_add_children()` which handles `BaseObject` instances, dicts, and lists automatically.

### 3. Parser Architecture
The `Parser` class maintains separate lists for each entity type (`self.products`, `self.assets`, `self.attributes`, etc.).
- **Parsing Logic**: Use `_parse_item_list(xml_tag, item_tag, parser_func)` to populate these lists.
- **Parser Functions**: Primarily follow `_parse_<element_name>(...)` naming and usually return dictionaries, with helper/utility parsing methods as needed for list/tuple/dict orchestration.
- **Boolean Handling**: Use `_str_to_bool()` for XML "true"/"false" strings.
- **Context**: The parser is stateful regarding the document it just parsed.

### 4. REST API Integration
- Wraps `requests-openapi` via `StiboStepRestClient`.
- **Two Access Styles**:
    - Direct OpenAPI access through `StiboStepRestClient.client` (`client.client.operation_id(...)`).
    - Grouped operation wrappers through `StepRestClient` in `stepxmlclient/rest_client/client.py` (e.g., `products`, `assets`, `classifications`, `entities`, `inbound`, etc.).
- **Inbound Operations**: `StiboStepRestClient` also initializes `inbound` operations (lazy import) for IIEP upload/status helpers.
- **Uploads**: Use `AssetUploader` in `upload.py` for pushing binary content.

## Workflows & Testing

### Building
- **Build**: `build_wheel.bat` (Windows) or `python setup.py bdist_wheel`.
- **Install**: `pip install dist/stepxmlclient-x.x-py3-none-any.whl`.

### Testing Strategy
The project follows a phased testing approach using `unittest`. All test modules live under `tests/`.
- **Primary Coverage**: Phase-based test modules (`tests/test_parser_phaseX_*.py`, `tests/test_rest_client_phaseX_*.py`) and focused behaviour tests in `tests/test_*.py` files.
- **Utility Script**: `tests/test.py` is a simple manual connectivity/example script, not the canonical full test runner.
- **Phase Tests**: `tests/test_parser_phaseX_....py` target specific functionalities (e.g., `tests/test_parser_phase5_attributes.py`).
- **Validation**: `tests/validate_xml_xsd.py` checks generated XML against `STEP.xsd`.
- **Development**: When adding a feature, either extend an existing phase test or create a new phase file if it enters a new domain.

## Key Files for Context
- `stepxmlclient/model/__init__.py`: Base object logic.
- `stepxmlclient/parser.py`: Implementation of all parsing logic.
- `stepxmlclient/creator.py`: Document generation logic.
- `STEP.xsd`: Reference for tag names and attribute validity.
- `openapi.json` : Reference for the STEP REST API V2

# DOX framework

- DOX is highly performant AGENTS.md hierarchy installed here
- Agent must follow DOX instructions across any edits

## Core Contract

- AGENTS.md files are binding work contracts for their subtrees
- Work products, source materials, instructions, records, assets, and durable docs must stay understandable from the nearest applicable AGENTS.md plus every parent AGENTS.md above it

## Read Before Editing

1. Read the root AGENTS.md
2. Identify every file or folder you expect to touch
3. Walk from the repository root to each target path
4. Read every AGENTS.md found along each route
5. If a parent AGENTS.md lists a child AGENTS.md whose scope contains the path, read that child and continue from there
6. Use the nearest AGENTS.md as the local contract and parent docs for repo-wide rules
7. If docs conflict, the closer doc controls local work details, but no child doc may weaken DOX

Do not rely on memory. Re-read the applicable DOX chain in the current session before editing.

## Update After Editing

Every meaningful change requires a DOX pass before the task is done.

Update the closest owning AGENTS.md when a change affects:

- purpose, scope, ownership, or responsibilities
- durable structure, contracts, workflows, or operating rules
- required inputs, outputs, permissions, constraints, side effects, or artifacts
- user preferences about behavior, communication, process, organization, or quality
- AGENTS.md creation, deletion, move, rename, or index contents

Update parent docs when parent-level structure, ownership, workflow, or child index changes. Update child docs when parent changes alter local rules. Remove stale or contradictory text immediately. Small edits that do not change behavior or contracts may leave docs unchanged, but the DOX pass still must happen.

## Hierarchy

- Root AGENTS.md is the DOX rail: project-wide instructions, global preferences, durable workflow rules, and the top-level Child DOX Index
- Child AGENTS.md files own domain-specific instructions and their own Child DOX Index
- Each parent explains what its direct children cover and what stays owned by the parent
- The closer a doc is to the work, the more specific and practical it must be

## Child Doc Shape

- Create a child AGENTS.md when a folder becomes a durable boundary with its own purpose, rules, responsibilities, workflow, materials, or quality standards
- Work Guidance must reflect the current standards of the project or user instructions; if there are no specific standards or instructions yet, leave it empty
- Verification must reflect an existing check; if no verification framework exists yet, leave it empty and update it when one exists

Default section order:
- Purpose
- Ownership
- Local Contracts
- Work Guidance
- Verification
- Child DOX Index

## Style

- Keep docs concise, current, and operational
- Document stable contracts, not diary entries
- Put broad rules in parent docs and concrete details in child docs
- Prefer direct bullets with explicit names
- Do not duplicate rules across many files unless each scope needs a local version
- Delete stale notes instead of explaining history
- Trim obvious statements, repeated rules, misplaced detail, and warnings for risks that no longer exist

## Closeout

1. Re-check changed paths against the DOX chain
2. Update nearest owning docs and any affected parents or children
3. Refresh every affected Child DOX Index
4. Remove stale or contradictory text
5. Run existing verification when relevant
6. Report any docs intentionally left unchanged and why

## User Preferences

When the user requests a durable behavior change, record it here or in the relevant child AGENTS.md

## Child DOX Index

- [stepxmlclient/AGENTS.md](stepxmlclient/AGENTS.md) - package-local contract for parser, creator, uploader, and REST entry points.
    - [stepxmlclient/model/AGENTS.md](stepxmlclient/model/AGENTS.md) - STEP XML object model and serialization rules.
    - [stepxmlclient/rest_client/AGENTS.md](stepxmlclient/rest_client/AGENTS.md) - REST API wrapper contract and operation grouping.
        - [stepxmlclient/rest_client/models/AGENTS.md](stepxmlclient/rest_client/models/AGENTS.md) - REST payload and response shape alignment.
        - [stepxmlclient/rest_client/operations/AGENTS.md](stepxmlclient/rest_client/operations/AGENTS.md) - grouped REST operations and request handling.
- [docs/AGENTS.md](docs/AGENTS.md) - project status and usage documentation.
- [tests/AGENTS.md](tests/AGENTS.md) - test suite organisation and conventions.
- Root-owned files remain under this contract, including `README.md`, `setup.py`, `requirements.txt`, `STEP.xsd`, and `openapi.json`.