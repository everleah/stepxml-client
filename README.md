# STEP XML Client

Python client library for Stibo Systems STEP MDM (Master Data Management), supporting the STEP-XML protocol and STEP REST API v2.

## Overview

This library enables seamless integration with STEP systems via:
- **OIEP (Outbound Integration Endpoint)**: Retrieve data from STEP as STEP-XML
- **IIEP (Inbound Integration Endpoint)**: Send data to STEP as STEP-XML
- **REST API v2**: Grouped, typed client for STEP REST API v2

## Current Features


**REST API v2 Client**
- 22 operation groups for STEP REST API v2
- Full CRUD, approval, values, children, data containers, purge for Products/Assets/Classifications/Entities
- Contexts, Users, User Groups, Collections, Workflows, Background Processes, Event Processors
- Inbound/Outbound/Gateway integration endpoints
- Type-safe Pydantic models, unified authentication, OpenAPI caching
- ✅ See [docs/REST_API_USAGE.md](docs/REST_API_USAGE.md) for full usage guide

STEP-XML parsing for a broad set of STEP entities, with XML generation for core entities.

### Core Capabilities
- ✅ **STEP-XML Parsing**: Parse 20+ STEP entity types including Products, Assets, Classifications, Entities, Attributes, and more
- ✅ **STEP-XML Generation**: Create and serialize XML documents for core entities (Phase 1 complete)
- ✅ **Relationship Management**: Full support for all cross-reference types (Asset, Product, Classification, Entity)
- ✅ **REST API Integration**: Client for STEP REST API v2 authentication and operations
- ✅ **Asset Binary Upload/Download**: Upload files (images, documents) and retrieve asset content via REST API
- **Schema Validation**: XML can be validated against a STEP XSD obtained from Stibo Systems
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
- **Deletion Operations** - Delete products/assets and sever links
- **Product Replacement Rules** - Create replacement configurations

## Installation


**First public release**: `1.0.0`. Package metadata and the release version are defined in `pyproject.toml`.

```bash
# Install from PyPI (or your package repository)
pip install stepxmlclient

# Or build from source
pip install -r requirements-release.txt
python -m build
pip install dist/stepxmlclient-x.x.x-py3-none-any.whl
```

**Requirements**:
- Python 3.9+
- requests-openapi
- requests
- pydantic>=2.0
- xml.etree.ElementTree (built-in)

## Quick Start


### REST API Client (Full Usage)

```python
from stepxmlclient.client import StiboStepRestClient, BasicAuthorisation
from stepxmlclient.rest_client import StepRestClient
from stepxmlclient.rest_client.models.product import ProductCreateRequest

# Shared authentication
auth = BasicAuthorisation(user="your-username", pwd="your-password")

# 1) Direct OpenAPI access (raw operation IDs)
raw_client = StiboStepRestClient(
    location_base="https://your-step-server/restapiv2",
    authorisation=auth,
    context="Context1"
)

# 2) Grouped wrapper access (recommended for most usage)
ops_client = StepRestClient(
    location_base="https://your-step-server/restapiv2",
    authorisation=auth,
    context="Context1"
)

created = ops_client.products.create_product(
    ProductCreateRequest(
        objectType="SalesItem",
        parent="RootProduct",
        name="Sample Product"
    )
)
retrieved = ops_client.products.get_product(created.id)
```

See [docs/REST_API_USAGE.md](docs/REST_API_USAGE.md) for detailed usage and all operation/model examples.

### Asset Binary Upload & Download

```python
from stepxmlclient.client import StiboStepRestClient, BasicAuthorisation
from stepxmlclient.upload import AssetUploader

# Create authenticated client
auth = BasicAuthorisation('username', 'password')
client = StiboStepRestClient(
    'https://your-step-server.com/restapiv2',
    auth
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

# Download OIEP REST delivery result by ResultURI (uses same client credentials)
result_uri = "restapi/integrationendpoints/asdf/BGP_213226/result.zip"
downloaded_file = client.download_result_uri(
    result_uri,
    target_dir="./downloads"
)
print(f"Result file downloaded to: {downloaded_file}")

# Or pass the complete OIEP response directly
oiep_response = {"ResultURI": "restapi/integrationendpoints/asdf/BGP_213226/result.zip"}
downloaded_file = client.download_oiep_result(
    oiep_response,
    target_dir="./downloads"
)
print(f"Result file downloaded to: {downloaded_file}")
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
attribute_groups = parser.attribute_groups
list_of_values = parser.list_of_values
tags = parser.tags
workflows = parser.workflows
business_rules = parser.business_rules

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
├── client.py                # StiboStepRestClient (Base client)
├── parser.py                # STEP-XML parsing engine (~2800 lines)
├── creator.py               # STEP-XML document generator  
├── upload.py                # Asset binary upload/download via REST API
├── rest_client/             # REST API v2 typed wrapper layer
│   ├── __init__.py
│   ├── client.py            # StepRestClient (grouped operation wrappers)
│   ├── base.py              # BaseOperation, handle_rest_errors
│   ├── exceptions.py
│   ├── models/              # Pydantic models (20 files)
│   └── operations/          # Operation groups (22 files)
└── model/                   # STEP-XML object models (BaseObject)

docs/
├── AGENTS.md
├── REST_API_STATE.md, REST_API_USAGE.md
├── PARSER_STATUS.md, PARSER_USAGE.md
├── CREATOR_STATUS.md, CREATOR_USAGE.md
└── INBOUND_OPERATIONS_SUMMARY.md

examples/
├── step_products_only.xml, step_assets_only.xml
├── step_products_assets_refs.xml, step_asset_pixxio.xml

tests/
├── __init__.py
├── test.py                  # Manual connectivity script
├── test_parser_phaseX_*.py  # Parser phase tests
├── test_rest_client_phaseX_*.py  # REST client tests
├── test_creator_*.py        # Creator tests
├── test_inbound_*.py        # Inbound endpoint tests
└── validate_xml_xsd.py      # XSD validation

## Development

### Build & Test

```bash
# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-release.txt

# Build wheel package
./build_wheel.bat  # Windows
# or
python -m build  # Cross-platform; creates an sdist and a wheel from that sdist

# Run the unit test suite
python -m unittest discover -s tests -p "test_*.py"

# Optional: validate if STEP.xsd has been obtained from Stibo Systems
python tests/validate_xml_xsd.py
```

The distribution does not include Stibo Systems' OpenAPI specification or XML schema. The REST client fetches the OpenAPI specification from the configured STEP server by default; alternatively, supply a licensed specification using `openapi_file`. Obtain the STEP XSD separately from Stibo Systems if you want to run schema validation.

### Publishing to PyPI

The PyPI package is `stepxmlclient`, maintained by **everleah**
(`everleah@hansch.info`). The first successful upload creates the PyPI project;
the owner is the PyPI account that issued the upload token, not the author
metadata. Sign in as `everleah`, verify the account email and enable PyPI's
required two-factor authentication before creating a token.

From the repository root, using your Python environment:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-release.txt

# Once: enter a NEW token locally at the hidden prompt, never in chat or a command.
.\upload_wheel_to_pypi.bat --configure-token

# Build and validate only; does not contact the upload endpoint.
.\upload_wheel_to_pypi.bat --check-only

# Publish the freshly built and checked wheel AND source distribution.
.\upload_wheel_to_pypi.bat
```

Cross-platform equivalents are `python publish_pypi.py --configure-token`,
`python publish_pypi.py --check-only`, and `python publish_pypi.py --publish`.
Without an action, the Python script only builds and checks.

- Tokens are saved by `keyring` in the local OS credential store (Windows
  Credential Manager on Windows), never in the repository or a `.pypirc`.
  The existing Forgejo credentials remain separate; Forgejo uses the shared
  modern build script when it needs to build a wheel.
- Revoke any token previously shared in chat. An account-wide token is needed
  for a new project. After the first upload, replace it with a token scoped to
  `stepxmlclient` by running `--configure-token` again.
- Every release uses an isolated build, builds the wheel from the sdist, checks
  metadata with `twine check --strict`, and rejects specifications and credential
  files in either archive. Only the two newly checked files are uploaded.
- Validated artifacts are retained in `dist\pypi\<version>`. Old files elsewhere
  in `dist` are not uploaded. Failures return a nonzero exit code; existing
  PyPI versions are not silently skipped.
- Before subsequent releases, update `project.version` in `pyproject.toml`,
  run the relevant tests, and run `--check-only`. PyPI releases cannot be
  overwritten; use a new version for changed content.
- To remove the locally saved token:
  `python -m keyring delete https://upload.pypi.org/legacy/ __token__`.

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

The project uses a phased testing approach with all test modules under `tests/`:
- **Primary coverage**: phase suites (`tests/test_parser_phaseX_*.py`, `tests/test_rest_client_phaseX_*.py`) plus focused `tests/test_*.py` modules
- **Utility script**: `tests/test.py` is a simple manual connectivity/example script
- **Phase tests**: `tests/test_parser_phaseX_*.py` target specific entity types
- **Validation**: `tests/validate_xml_xsd.py` checks generated XML when an authorized STEP XSD is available locally
- **Roundtrip tests**: `tests/test_creator_roundtrip.py` parses generated XML

When adding new functionality:
1. Extend existing phase test or create new `tests/test_parser_phaseX_*.py`
2. Add corresponding model class in `stepxmlclient/model/`
3. Add parser function in `stepxmlclient/parser.py`
4. Optionally add creator support in `stepxmlclient/creator.py`
5. Validate with `tests/validate_xml_xsd.py`

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
parser.parse_str(xml_string)

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


### REST API v2 Client (22 operation groups)

The typed wrappers cover the operations documented in the STEP REST API specification.
See [docs/REST_API_STATE.md](docs/REST_API_STATE.md) for the full coverage matrix.

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
- **REST API v2 Client**: 22 operation groups for STEP REST API v2
- **Parser**: Supports the documented STEP-XML entity types for data export and analysis
- **Creator**: Core functionality complete, suitable for basic import scenarios
- **Testing**: Extensive phase-based test coverage with unit and integration tests

For detailed phase status, see:
- [docs/PARSER_STATUS.md](docs/PARSER_STATUS.md)
- [docs/CREATOR_STATUS.md](docs/CREATOR_STATUS.md)
- [docs/REST_API_USAGE.md](docs/REST_API_USAGE.md)
- [docs/REST_API_STATE.md](docs/REST_API_STATE.md)

## Core References

### STEP Schema

The STEP XML schema is provided by Stibo Systems and is not included in this distribution. Obtain an authorized copy from Stibo Systems for schema reference or validation.

### Documentation
- [PARSER_STATUS.md](docs/PARSER_STATUS.md) - Detailed parser feature coverage and phase breakdown
- [CREATOR_STATUS.md](docs/CREATOR_STATUS.md) - Creator implementation status and expansion roadmap  
- [PARSER_USAGE.md](docs/PARSER_USAGE.md) - Parser implementation guide and patterns
- [CREATOR_USAGE.md](docs/CREATOR_USAGE.md) - Creator implementation guide and patterns

### Requirements

- Python 3.9+
- requests-openapi - OpenAPI client generation
- requests - HTTP library
- xml.etree.ElementTree (built-in)

## Contributing

When extending functionality:
1. **Parser**: Add `_parse_<element>()` function, create phase test in `test_parser_phaseX_*.py`
2. **Model**: Extend `BaseObject` with declarative configuration per project conventions
3. **Creator**: Implement serialization in model class `to_element()` method
4. **Schema**: Validate against a locally available, authorized STEP XSD when applicable
5. **Tests**: Ensure coverage with roundtrip parsing + XSD validation

Follow established patterns from:
- Existing parser functions in [stepxmlclient/parser.py](stepxmlclient/parser.py)
- Model classes in [stepxmlclient/model/](stepxmlclient/model/)
- Phase tests in [tests/](tests/)

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).

## Security

Please report suspected vulnerabilities privately to [everleah@hansch.info](mailto:everleah@hansch.info) rather than opening a public issue.

## Maintainer

Everleah — [everleah@hansch.info](mailto:everleah@hansch.info)