# STEP XML Client - AI Coding Agent Instructions

## Project Overview
This is a reusable Python client module for integrating with Stibo Systems STEP MDM (Master Data Management) using standard STEP-XML protocol. The module provides a ready-to-use client for other software projects to communicate with STEP systems via standard Outbound Integration Endpoint (OIEP) and Inbound Integration Endpoint (IIEP).

## Architecture
The module provides a complete STEP-XML integration layer with clear separation of concerns:
- **`stepxmlclient/client.py`**: REST API client for STEP OIEP/IIEP endpoints using `requests-openapi`
- **`stepxmlclient/parser.py`**: STEP-XML parser conforming to `STEP.xsd` schema for inbound data
- **`stepxmlclient/creator.py`**: STEP-XML document generator for outbound integration
- **`stepxmlclient/model/`**: Data model classes (`Asset`, `Product`, `BaseObject`) representing STEP entities
- **`STEP.xsd`**: Official STEP-XML schema (8500+ lines) - the authoritative reference for validation

## Critical Patterns & Conventions

### Namespace Handling
All XML operations use the `STEPXML_NS` namespace dictionary defined in `__init__.py`:
```python
STEPXML_NS = {
    'step': 'http://www.stibosystems.com/step',
    'outputtemplate': 'http://www.stibosystems.com/step/outputtemplate'
}
```
Always pass this to `find()` and `findall()` calls on XML elements.

### Object Model Pattern
All model classes inherit from `BaseObject` with class-level configuration:
```python
class Product(BaseObject):
    _GROUP_NAME = 'products'  # Collection name in Creator
    _TAG_NAME = 'Product'     # XML element name
    _ATTRIBUTE_NAMES = ("ID", "ParentId", "UserTypeID")  # XML attributes
    _TEXT_NAMES = ("Name",)   # Child text elements
    _CHILDREN_NAMES = ("Values", "AssetCrossReference", "DeleteAssetCrossReference")
```

### Parser Function Naming
Parser functions follow strict naming: `_parse_<element_name>()` for element-specific parsers, using lowercase with underscores.

## Known Issues & Fix Patterns

### Critical Bug in `_parse_item_list()`
The method returns `result` instead of `results` (line 48 in parser.py), causing only the last parsed item to be returned. Always return the accumulated list.

### Authorization Pattern
The client uses composition-based authorization via `__Authorisation` base class:
```python
auth = BasicAuthorisation('username', 'password')
client = StiboStepRestClient(base_url, auth, cache_openapi=True)
```

## Development Workflows

### Building & Distribution
- **Build wheel**: Run `build_wheel.bat` (calls `python setup.py bdist_wheel`)
- **Dependencies**: Install via `pip install -r requirements.txt`
- **Testing**: Use `test.py` as the main test runner (connects to demo STEP server)

### STEP-XML Schema Compliance
- **`STEP.xsd`**: The authoritative STEP-XML schema defining all valid structures and relationships
- Use this XSD to validate generated XML output before sending to STEP IIEP
- Reference the schema when adding new parser functions to ensure correctness
- The schema covers all STEP entities: Products, Assets, Classifications, Attributes, etc.

### STEP Integration Endpoints
- **OIEP (Outbound Integration Endpoint)**: For retrieving data from STEP as STEP-XML
- **IIEP (Inbound Integration Endpoint)**: For sending data to STEP as STEP-XML
- **OpenAPI Integration**: Client caches OpenAPI specs (`openapi.json`) - use `cache_openapi=True`

## Testing & Debugging

### SSL & Certificate Handling
The client supports `nocert=True` for development environments or when a `nocert` file exists in the working directory.

### Proxy Support
Pass proxy configuration as dict to `StiboStepRestClient(proxies={...})` for corporate environments.

## File Organization
- Keep model classes focused on XML serialization/deserialization only
- Parser functions should handle XML namespace resolution
- Creator classes manage object-to-XML conversion with proper parent-child relationships
- Client classes handle REST communication and authentication exclusively

When extending functionality, follow the established patterns: parser functions for XML input, model classes for data representation, and creator methods for XML output generation.