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

## Critical Patterns & Fix Guidelines

### XML Element Creation Pattern
When adding XML elements, always specify the tag name: `ET.SubElement(parent, tag_name)` 

### Method Call Pattern  
Ensure all method calls include parentheses: `self._get_attributes()` not `self._get_attributes`

### Loop Variable Pattern
In loops over collections, use the iteration variable: `for obj in objs: obj.method()` not `objs.method()`

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

### STEP-XML Schema Compliance
- **`STEP.xsd`**: The authoritative STEP-XML schema defining all valid structures and relationships
- Use this XSD to validate generated XML output before sending to STEP IIEP
- Reference the schema when adding new parser functions to ensure correctness
- The schema covers all STEP entities: Products, Assets, Classifications, Attributes, etc.

### STEP REST API v2 Integration
- **REST API v2**: Primary communication method using HTTP operations (GET, PUT, POST, PATCH, DELETE)
- **OIEP (Outbound Integration Endpoint)**: For retrieving data from STEP as STEP-XML via `/outbound-integration-endpoints/{id}/invoke`
- **IIEP (Inbound Integration Endpoint)**: For sending data to STEP as STEP-XML
- **Core Resources**: Assets (`/assets/{id}`), Products (`/products/{id}`), Entities (`/entities/{id}`), Classifications (`/classifications/{id}`) with full CRUD operations
- **Key Operations**: Attribute values (`/{resource}/{id}/values/{attributeId}`), References (`/{resource}/{id}/references/{referenceTypeId}`), Approval workflows (`/{resource}/{id}/approve`)
- **OpenAPI Specification**: Complete API definition in `openapi.json` - client caches specs with `cache_openapi=True`
- **Context & Workspace**: All requests require context parameter, default to "Main" workspace

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