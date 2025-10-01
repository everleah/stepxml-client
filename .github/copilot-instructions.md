# STEP XML Client - AI Coding Agent Instructions

## Project Overview
This is a reusable Python client module for integrating with Stibo Systems STEP MDM (Master Data Management) using standard STEP-XML protocol. The module provides a ready-to-use client for other software projects to communicate with STEP systems via standard Outbound Integration Endpoint (OIEP) and Inbound Integration Endpoint (IIEP).

## Architecture
The module provides focused STEP-XML processing for core MDM entities in early development:
- **`stepxmlclient/client.py`**: REST API client wrapper using `requests-openapi` - handles configuration only
- **`stepxmlclient/parser.py`**: STEP-XML parser for Products, Assets, and their relationships
- **`stepxmlclient/creator.py`**: STEP-XML document generator for Products, Assets, and Product Replacement Rules
- **`stepxmlclient/model/`**: Core model classes - `Asset`, `Product`, `ProductReplacementRule`
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
Note: `AssetCrossReference` and `DeleteAssetCrossReference` handle the critical product-to-asset relationships.

### Parser Function Naming
Parser functions follow strict naming: `_parse_<element_name>()` for element-specific parsers, using lowercase with underscores.

## Critical Patterns & Fix Guidelines

### XML Element Creation Pattern
When adding XML elements, always specify the tag name: `ET.SubElement(parent, tag_name)` 

### Attribute Conversion Pattern
The parser supports conversions for both attributes and child elements. Use `conversions` parameter to transform data types during parsing.

### Child Data Handling Pattern
`BaseObject._add_children()` handles multiple data types:
- Objects with `to_element()` method (other BaseObject instances)
- Dictionaries (converted to XML elements with attributes)
- Lists (processes each item individually)

### Creator Naming Pattern
Use explicit mapping between XML element names and object attributes to avoid naming conflicts.

### REST Client Configuration
The client integrates with STEP REST API v2 via `requests-openapi`:
```python
auth = BasicAuthorisation('username', 'password')  
client = StiboStepRestClient(
    'https://server.com/restapiv2',  # REST API v2 endpoint
    auth, 
    cache_openapi=True,              # Cache openapi.json locally
    nocert=True                      # For development environments
)
```

## Development Workflows

### Building & Distribution
- **Build wheel**: Run `build_wheel.bat` (calls `python setup.py bdist_wheel`)
- **Dependencies**: Install via `pip install -r requirements.txt`
- **Testing**: Use `test.py` as the main test runner (connects to demo STEP server)

### Current Development Focus
- **Core Entity Support**: Products and Assets with their relationships - covers primary MDM use cases
- **Product-Asset Relations**: Handles `AssetCrossReference` and `DeleteAssetCrossReference` for linking products to assets
- **Essential Operations**: Create, parse, and delete operations for Products and Assets
- **Strategic Scope**: Early development stage focused on most important STEP entities
- **Future Expansion**: Use `STEP.xsd` as reference when adding Classifications, Entities, or other STEP objects

### STEP REST API v2 Integration
- **Client Wrapper**: `StiboStepRestClient` is a configuration wrapper around `requests-openapi` client
- **No Direct API Methods**: Client does not expose specific REST operations - users must call `client.client` to access underlying API
- **OpenAPI Integration**: Loads STEP REST API v2 specification from `/specification/openapi.json` endpoint
- **Configuration Only**: Handles authentication, SSL settings, proxy configuration, and OpenAPI spec caching
- **Usage Pattern**: `client = StiboStepRestClient(...); api_response = client.client.some_operation(...)`

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