# STEP XML Client

A robust Python client library for integrating with Stibo Systems STEP MDM (Master Data Management) using standard STEP-XML protocol and REST API v2.

## Overview

This library provides a production-ready client for software projects to communicate with STEP systems via:
- **OIEP (Outbound Integration Endpoint)**: Retrieve data from STEP as STEP-XML
- **IIEP (Inbound Integration Endpoint)**: Send data to STEP as STEP-XML  
- **REST API v2**: Full access to STEP's HTTP API operations

## Current Features

**Comprehensive STEP-XML support** with extensive parsing (~80% schema coverage) and growing generation capabilities (~10% schema coverage).

### Core Capabilities
- ✅ **STEP-XML Parsing**: Parse 20+ STEP entity types including Products, Assets, Classifications, Entities, Attributes, and more
- ✅ **STEP-XML Generation**: Create and serialize XML documents for core entities (Phase 1 complete)
- ✅ **Relationship Management**: Full support for all cross-reference types (Asset, Product, Classification, Entity)
- ✅ **REST API Integration**: Configured client for STEP REST API v2 authentication and operations
- ✅ **Asset Binary Upload/Download**: Upload files (images, documents) and retrieve asset content via REST API
- ✅ **Schema Validation**: Reference implementation against official `STEP.xsd` (8500+ line authoritative schema)
- ✅ **Deletion Operations**: Support for product and asset deletions, link severance
- ✅ **Product Replacement Rules**: Create and manage product replacement configurations

### Parsed Entity Types (Phase 2-14)
- **Products** - Full support with all attributes and relationships ✅
- **Assets** - Full support with key values and cross-references ✅
- **Classifications** - Full hierarchical parsing ✅
- **Entities** - Complete entity structure parsing ✅
- **Attributes** - Full attribute definition parsing ✅
- **AttributeGroups** - Hierarchical group definitions ✅
- **ListOfValues** - LOV items and associations ✅
- **Contexts, Qualifiers, Dimensions** - Configuration elements ✅
- **UserTypes, LinkTypes** - Type definitions ✅
- **Tags, TagGroups, Units** - Metadata and classification ✅
- **BusinessRules, Workflows** - Advanced configuration ✅
- **Collections, CollectionGroups** - Collection management ✅
- **Delete Operations** - Products, Assets, and link severance ✅
- **Replacement Rules** - Product replacement configurations ✅

### Generation Capabilities (Phase 1 Complete)
- **Products** - Create with attributes, values, and cross-references
- **Assets** - Create with key values and cross-references
- **Cross-References** - All relationship types (Asset, Product, Classification, Entity)
- **Deletion Operations** - Delete products/assets and severe links
- **Product Replacement Rules** - Create replacement configurations

## Installation

**Latest Version**: 0.4

```bash
# Install from PyPI (or your package repository)
pip install stepxmlclient

# Or build from source
pip install -r requirements.txt
python setup.py bdist_wheel
pip install dist/stepxmlclient-0.4-py3-none-any.whl
```

**Requirements**:
- Python 3.7+
- requests-openapi
- requests
- xml.etree.ElementTree (built-in)

## Quick Start

### REST API Client

```python
from stepxmlclient.client import StiboStepRestClient, BasicAuthorisation

# Configure authentication
auth = BasicAuthorisation('username', 'password')

# Create client with OpenAPI caching
client = StiboStepRestClient(
    'https://your-step-server.com/restapiv2',
    auth,
    cache_openapi=True,    # Cache API specification locally
    nocert=True            # Skip SSL verification (dev only)
)

# Access underlying requests-openapi client for operations
response = client.client.operation_id_here(param1='value', param2='value')
```

### Asset Binary Upload & Download

```python
from stepxmlclient.client import StiboStepRestClient, BasicAuthorisation
from stepxmlclient.upload import AssetUploader

# Create authenticated client
auth = BasicAuthorisation('username', 'password')
client = StiboStepRestClient(
    'https://your-step-server.com/restapiv2',
    auth,
    nocert=True
)

# Initialize uploader
uploader = AssetUploader(client)

# Upload local file to asset
result = uploader.upload_file(
    file_path='product_image.jpg',
    asset_id='ASSET_001',
    context_id='Context1',
    workspace_id='Main'
)
print(f"Upload successful: {result['asset_id']}")

# Upload from URL
result = uploader.upload_file(
    file_path='https://example.com/image.jpg',
    asset_id='ASSET_002',
    context_id='Context1'
)

# Download asset content
content = uploader.get_content(
    asset_id='ASSET_001',
    context_id='Context1'
)
with open('downloaded.jpg', 'wb') as f:
    f.write(content)
```

### XML Parsing (Comprehensive)

```python
from stepxmlclient.parser import Parser

# Parse STEP-XML from file
parser = Parser()
parser.parse_file('step_export.xml')

# Access parsed entities (20+ types supported)
products = parser.products
assets = parser.assets
classifications = parser.classifications
entities = parser.entities
attributes = parser.attributes
attribute_groups = parser.attributegroups
list_of_values = parser.listofvalues
tags = parser.tags
workflows = parser.workflows
business_rules = parser.businessrules

# Handle deletion operations
deleted_products = parser.delete_products
deleted_assets = parser.delete_assets

# Example: Navigate product relationships
for product in products:
    print(f"Product: {product['ID']}")
    print(f"  Name: {product.get('Name')}")
    
    # Check for asset relationships
    if 'AssetCrossReference' in product:
        asset_ref = product['AssetCrossReference']
        print(f"  Asset: {asset_ref['AssetID']}")
    
    # Check for product relationships
    if 'ProductCrossReference' in product:
        prod_ref = product['ProductCrossReference']
        print(f"  Related Product: {prod_ref['ProductID']}")
    
    # Check for classification relationships
    if 'ClassificationCrossReference' in product:
        class_ref = product['ClassificationCrossReference']
        print(f"  Classification: {class_ref['ClassificationID']}")
    
    # Access attribute values
    if 'Values' in product:
        for value in product['Values']:
            print(f"    {value['AttributeID']}: {value.get('Value')}")
```

### XML Creation

```python
from stepxmlclient.creator import Creator
from stepxmlclient.model import Product, Asset

# Create XML document for specific context and workspace
creator = Creator(
    context_id="Context1", 
    workspace_id="Main"
)

# Create a product with asset relationship
product = Product({
    "ID": "PROD_001",
    "Name": "Sample Product",
    "UserTypeID": "StandardProduct",
    "AssetCrossReference": {
        "AssetID": "ASSET_001", 
        "Changed": True,
        "Type": "Primary Image"
    }
})

# Create an asset
asset = Asset({
    "ID": "ASSET_001",
    "Name": "Product Image",
    "KeyValue": "IMG_001"
})

# Add entities to creator
creator.add(product)
creator.add(asset)

# Generate XML document
creator.build()

# Export as string or tree
xml_string = creator.to_string()
print(xml_string)

# Or save to file
creator.tree.write('output.xml', encoding='utf-8')
```

### Product Replacement Rules

```python
from stepxmlclient.creator import Creator
from stepxmlclient.model import ProductReplacementRule

creator = Creator(context_id="Context1", workspace_id="Main")

# Create replacement rule
replacement = ProductReplacementRule({
    "ID": "RULE_001",
    "SourceProductID": "OLD_PROD",
    "ReplacementProductID": "NEW_PROD"
})

creator.add(replacement)
creator.build()
xml_string = creator.to_string()
```

## Project Structure

```
stepxmlclient/
├── __init__.py              # Namespace definitions (STEPXML_NS)
├── client.py                # REST API client wrapper (requests-openapi)
├── parser.py                # STEP-XML parsing engine (~2800 lines, ~80% coverage)
├── creator.py               # STEP-XML document generator  
├── upload.py                # Asset binary upload/download via REST API
└── model/                   # BaseObject model classes
    ├── __init__.py          # BaseObject base class
    ├── product.py           # Product and ProductReplacementRule
    ├── asset.py             # Asset model
    ├── attribute.py         # Attribute and AttributeGroup
    ├── classification.py     # Classification model
    ├── entity.py            # Entity model
    ├── business.py          # BusinessRule model
    ├── deletion.py          # Deletion specification models
    ├── metadata.py          # MetaData model
    ├── organization.py      # Organization and Context models
    ├── relations.py         # Cross-reference models
    └── replacement.py       # Product replacement models

docs/
├── PARSER_STATUS.md         # Parser feature status (Phase 14 complete)
├── CREATOR_STATUS.md        # Creator feature status (Phase 1 complete)
├── PARSER_USAGE.md          # Parser implementation guide
└── CREATOR_USAGE.md         # Creator implementation guide

examples/
├── step_products_only.xml   # Product export sample
├── step_assets_only.xml     # Asset export sample
├── step_products_assets_refs.xml
└── step_asset_pixxio.xml    # Asset with metadata sample

tests/
├── test.py                  # Core integration tests
├── test_parser_phaseX_*.py  # Phase-specific parser tests (2-14)
├── test_creator_*.py        # Creator functionality tests
└── validate_xml_xsd.py      # XSD schema validation utility
```

## Development

### Build & Test

```bash
# Install development dependencies
pip install -r requirements.txt

# Build wheel package
./build_wheel.bat  # Windows
# or
python setup.py bdist_wheel  # Cross-platform

# Run all core tests
python test.py

# Run phase-specific parser tests
python test_parser_phase2.py       # Products
python test_parser_phase3_classification.py
python test_parser_phase5_attributes.py
# ... and so on up to phase14

# Validate generated XML against schema
python validate_xml_xsd.py
```

### Architecture Highlights

**Parser Architecture**:
- Stateful parser maintains separate typed lists (products, assets, classifications, etc.)
- Namespace-aware tag handling with `_get_local_tag()` for robust XML processing
- Parser functions strictly named `_parse_<element_name>()` for consistency
- Boolean conversion with `_str_to_bool()` for XML "true"/"false" strings
- ~80% STEP-XML schema coverage across 14 phases

**Creator Architecture**:
- BaseObject declarative model with `_TAG_NAME`, `_GROUP_NAME`, `_ATTRIBUTE_NAMES`, `_TEXT_NAMES`, `_CHILDREN_NAMES`
- Auto-serialization via `to_element()` based on model configuration
- Automatic routing of objects to correct collection lists via `_GROUP_NAME`
- Support for 20+ entity types with full relationship mapping

**REST Client**:
- Wraps `requests-openapi` for type-safe API calls
- Basic authentication with configurable SSL/proxy support
- OpenAPI specification caching for improved performance
- No method wrappers—access underlying client directly

### Key Patterns

**XML Namespace Handling**:
```python
from stepxmlclient import STEPXML_NS

# Use namespace dictionary for find operations
element.find('Products', STEPXML_NS)
element.findall('Product', STEPXML_NS)
```

**Model Class Configuration**:
```python
from stepxmlclient.model import BaseObject

class MyEntity(BaseObject):
    _GROUP_NAME = 'my_entities'              # Collection name in Creator
    _TAG_NAME = 'MyEntity'                   # XML element tag name
    _ATTRIBUTE_NAMES = ("ID", "UserTypeID")  # XML attributes
    _TEXT_NAMES = ("Name",)                  # Child text elements
    _CHILDREN_NAMES = ("Values",)            # Ordered child elements
```

**Parser Function Pattern**:
```python
def _parse_my_entity(element: ET.Element) -> dict:
    """Parse MyEntity element into dictionary."""
    data = {}
    # Extract attributes
    data['ID'] = element.get('ID')
    # Extract text content
    name_elem = element.find('Name', STEPXML_NS)
    if name_elem is not None:
        data['Name'] = name_elem.text
    # Process children
    data['Values'] = self._parse_item_list(element, 'Value', self._parse_value)
    return data
```

### Testing Strategy

The project uses a phased testing approach:
- **Main runner**: `test.py` for integration tests
- **Phase tests**: `test_parser_phaseX_*.py` target specific entity types
- **Validation**: `validate_xml_xsd.py` ensures generated XML matches STEP.xsd
- **Roundtrip tests**: `test_creator_roundtrip.py` parses generated XML

When adding new functionality:
1. Extend existing phase test or create new `test_parser_phaseX_*.py`
2. Add corresponding model class in `stepxmlclient/model/`
3. Add parser function in `stepxmlclient/parser.py`
4. Optionally add creator support in `stepxmlclient/creator.py`
5. Validate with `validate_xml_xsd.py`

## Configuration

### REST API Client

```python
from stepxmlclient.client import StiboStepRestClient, BasicAuthorisation

# Standard configuration
auth = BasicAuthorisation('username', 'password')
client = StiboStepRestClient(
    'https://your-step-server.com/restapiv2',
    auth
)

# Development - disable SSL verification
client = StiboStepRestClient(..., nocert=True)

# Or create 'nocert' file in working directory to disable SSL globally
# Production - proper certificates handled by OS certificate store

# Proxy support
client = StiboStepRestClient(
    ...,
    proxies={'http': 'proxy.company.com:8080', 
             'https': 'proxy.company.com:8080'}
)

# OpenAPI caching for better performance
client = StiboStepRestClient(
    ...,
    cache_openapi=True
    # Creates/uses 'openapi.json' in working directory
)
```

### XML Parsing Configuration

```python
from stepxmlclient.parser import Parser

parser = Parser()

# Parse from file
parser.parse_file('data.xml')

# Parse from string
parser.parse_string(xml_string)

# Access results
products = parser.products
classifications = parser.classifications
# ... all 20+ entity types
```

### XML Creation Configuration

```python
from stepxmlclient.creator import Creator

# Specify context and workspace
creator = Creator(
    context_id='YourContext',
    workspace_id='Main'  # Default: 'Main'
)

# Generate XML with specific encoding
creator.build()
xml_bytes = creator.to_bytes(encoding='utf-8')
```

## Roadmap

### ✅ Parser - Complete (Phase 14, ~80% coverage)

**Implemented**:
- Core entities: Products, Assets, Classifications, Entities
- Attributes system: Attributes, AttributeGroups, ListOfValues  
- Configuration: Contexts, Qualifiers, Dimensions, LinkTypes, UserTypes
- Metadata: Tags, TagGroups, Units
- Advanced: BusinessRules, Workflows, Collections
- Operations: Deletion, Replacement Rules
- Relations: All cross-reference types (Asset, Product, Classification, Entity)

**Next**: Remaining 20% of STEP-XML schema (minor/specialized elements)

### 🔄 Creator - Phase 1 Complete, Expanding (~10% coverage)

**Phase 1 Complete (Core Entities)**:
- ✅ Products with all attributes and cross-references
- ✅ Assets with key values and cross-references
- ✅ All cross-reference types
- ✅ Deletion operations
- ✅ Product replacement rules

**Phase 2 Planning (Attributes & Classification)**:
- Classifications and hierarchies
- Attributes and AttributeGroups
- ListOfValues with proper associations

**Future Phases**:
- Entities and EntityTypes
- Tags, Units, and Metadata
- Workflows and BusinessRules
- Collections and CollectionGroups
- Full parity with Parser coverage

### Current Status Summary
- **Parser**: Comprehensive, production-ready for data export/analysis
- **Creator**: Core functionality complete, suitable for basic import scenarios
- **REST API**: Fully functional with authentication and asset management
- **Testing**: Extensive phase-based test coverage with XSD validation

For detailed phase status, see:
- [docs/PARSER_STATUS.md](docs/PARSER_STATUS.md)
- [docs/CREATOR_STATUS.md](docs/CREATOR_STATUS.md)

## Core References

### STEP Schema
- **STEP.xsd** - 8500+ line authoritative XML schema for all supported entities, attributes, and structures
  - Reference for understanding valid XML structures
  - Used for validation and adding new entity support
  - Covers ~80% currently implemented

### Documentation
- [PARSER_STATUS.md](docs/PARSER_STATUS.md) - Detailed parser feature coverage and phase breakdown
- [CREATOR_STATUS.md](docs/CREATOR_STATUS.md) - Creator implementation status and expansion roadmap  
- [PARSER_USAGE.md](docs/PARSER_USAGE.md) - Parser implementation guide and patterns
- [CREATOR_USAGE.md](docs/CREATOR_USAGE.md) - Creator implementation guide and patterns

### Requirements

- Python 3.7+
- requests-openapi - OpenAPI client generation
- requests - HTTP library
- xml.etree.ElementTree (built-in)

## Contributing

When extending functionality:
1. **Parser**: Add `_parse_<element>()` function, create phase test in `test_parser_phaseX_*.py`
2. **Model**: Extend `BaseObject` with declarative configuration per project conventions
3. **Creator**: Implement serialization in model class `to_element()` method
4. **Schema**: Validate new entities against `STEP.xsd`
5. **Tests**: Ensure coverage with roundtrip parsing + XSD validation

Follow established patterns from:
- Existing parser functions in [stepxmlclient/parser.py](stepxmlclient/parser.py)
- Model classes in [stepxmlclient/model/](stepxmlclient/model/)
- Phase tests in workspace root