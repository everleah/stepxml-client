# STEP XML Client - AI Coding Agent Instructions

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
- **Parser Functions**: Strictly named `_parse_<element_name>(element) -> dict`.
- **Boolean Handling**: Use `_str_to_bool()` for XML "true"/"false" strings.
- **Context**: The parser is stateful regarding the document it just parsed.

### 4. REST API Integration
- Wraps `requests-openapi` via `StiboStepRestClient`.
- **No Method Wrappers**: The client exposes the underlying `client` object (`client.client.operation_id(...)`).
- **Uploads**: Use `StepAssetUploader` in `upload.py` for pushing binary content.

## Workflows & Testing

### Building
- **Build**: `build_wheel.bat` (Windows) or `python setup.py bdist_wheel`.
- **Install**: `pip install dist/stepxmlclient-x.x-py3-none-any.whl`.

### Testing Strategy
The project follows a phased testing approach using `unittest`.
- **Main Runner**: `test.py` (runs core integration tests).
- **Phase Tests**: `test_parser_phaseX_....py` target specific functionalities (e.g., `test_parser_phase5_attributes.py`).
- **Validation**: `validate_xml_xsd.py` checks generated XML against `STEP.xsd`.
- **Development**: When adding a feature, either extend an existing phase test or create a new phase file if it enters a new domain.

## Key Files for Context
- `stepxmlclient/model/__init__.py`: Base object logic.
- `stepxmlclient/parser.py`: Implementation of all parsing logic.
- `stepxmlclient/creator.py`: Document generation logic.
- `STEP.xsd`: Reference for tag names and attribute validity.
