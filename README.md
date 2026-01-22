# STEP XML Client

A Python client library for integrating with Stibo Systems STEP MDM (Master Data Management) using standard STEP-XML protocol and REST API v2.

## Overview

This module provides a ready-to-use client for software projects to communicate with STEP systems via:
- **OIEP (Outbound Integration Endpoint)**: Retrieve data from STEP as STEP-XML
- **IIEP (Inbound Integration Endpoint)**: Send data to STEP as STEP-XML  
- **REST API v2**: Full access to STEP's HTTP API operations

## Current Features

**Early Development Focus**: Products and Assets with their relationships - covers primary MDM use cases.

### Core Functionality
- ✅ **STEP-XML Parsing**: Parse Products, Assets, and Delete operations
- ✅ **STEP-XML Generation**: Create XML documents for Products, Assets, and Product Replacement Rules
- ✅ **Product-Asset Relations**: Handle `AssetCrossReference` and `DeleteAssetCrossReference`  
- ✅ **REST API Integration**: Configure and authenticate with STEP REST API v2
- ✅ **Asset Binary Upload**: Upload files (images, documents) to STEP assets via REST API
- ✅ **Schema Validation**: Reference implementation against official `STEP.xsd`

### Supported Entities
- **Product**: Full CRUD with asset relationships
- **Asset**: Full CRUD with key values and attributes  
- **ProductReplacementRule**: Creation and management
- **Delete Operations**: Products and Assets

## Installation

```bash
pip install -r requirements.txt
python setup.py bdist_wheel
pip install dist/stepxmlclient-0.1-py3-none-any.whl
```

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
    nocert=True           # Skip SSL verification (dev only)
)

# Access underlying requests-openapi client
response = client.client.some_operation(...)
```

### Asset Binary Upload

```python
from stepxmlclient.client import StiboStepRestClient, BasicAuthorisation
from stepxmlclient.upload import AssetUploader

# Create client
auth = BasicAuthorisation('username', 'password')
client = StiboStepRestClient(
    'https://your-step-server.com/restapiv2',
    auth,
    nocert=True
)

# Create uploader
uploader = AssetUploader(client)

# Upload local file to asset
result = uploader.upload_file(
    file_path='product_image.jpg',
    asset_id='ASSET_001',
    filename='product_image.jpg',  # Optional
    context_id='Context1',
    workspace_id='Main'            # Optional
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

### XML Parsing

```python
from stepxmlclient.parser import Parser

# Parse STEP-XML from file
parser = Parser()
parser.parse_file('step_export.xml')

# Access parsed data
products = parser.products        # List of product dictionaries
assets = parser.assets           # List of asset dictionaries  
deleted_products = parser.delete_products
deleted_assets = parser.delete_assets

# Example product with asset relationship
for product in products:
    print(f"Product ID: {product['ID']}")
    if 'AssetCrossReference' in product:
        asset_ref = product['AssetCrossReference']
        print(f"  -> Asset: {asset_ref['AssetID']}")
```

### XML Creation

```python
from stepxmlclient.creator import Creator
from stepxmlclient.model import Product, Asset

# Create XML document
creator = Creator(
    context_id="Main", 
    workspace_id="Main"
)

# Add products and assets
product_data = {
    "ID": "PROD_001",
    "Name": "Sample Product",
    "AssetCrossReference": {
        "AssetID": "ASSET_001", 
        "Changed": True,
        "Type": "Primary Image"
    }
}

asset_data = {
    "ID": "ASSET_001",
    "Name": "Product Image",
    "KeyValue": "IMG_001"
}

creator.add(Product(product_data))
creator.add(Asset(asset_data))

# Generate XML
creator.build()
xml_tree = creator.tree
```

## Project Structure

```
stepxmlclient/
├── __init__.py              # Namespace definitions
├── client.py               # REST API client wrapper  
├── parser.py               # STEP-XML parsing engine
├── creator.py              # STEP-XML document generator
├── upload.py               # Asset binary upload/download
└── model/
    ├── __init__.py         # BaseObject class
    ├── product.py          # Product and ProductReplacementRule
    └── asset.py            # Asset model class
```

## Development

### Build & Test

```bash
# Build wheel package
./build_wheel.bat

# Run tests (connects to demo server)  
python test.py

# Install dependencies
pip install -r requirements.txt
```

### Key Patterns

**XML Namespace Handling**:
```python
from stepxmlclient import STEPXML_NS
# Always use STEPXML_NS with find() and findall()
element.find('Products', STEPXML_NS)
```

**Model Class Configuration**:
```python
class Product(BaseObject):
    _GROUP_NAME = 'products'           # Collection name in Creator
    _TAG_NAME = 'Product'              # XML element name
    _ATTRIBUTE_NAMES = ("ID", "ParentId", "UserTypeID")  
    _TEXT_NAMES = ("Name",)            # Child text elements
    _CHILDREN_NAMES = ("Values", "AssetCrossReference")
```

### Schema Reference

Use `STEP.xsd` (8500+ lines) as the authoritative reference for:
- Understanding valid XML structures  
- Adding support for new STEP entities
- Validating generated XML output

## Configuration

### SSL & Certificates
```python
# Development - skip SSL verification
client = StiboStepRestClient(..., nocert=True)

# OR create 'nocert' file in working directory
# Production - use proper certificates
```

### Proxy Support  
```python
client = StiboStepRestClient(
    ...,
    proxies={'http': 'proxy.company.com:8080'}
)
```

### OpenAPI Caching
```python  
# Cache API specification locally for better performance
client = StiboStepRestClient(..., cache_openapi=True)
# Creates/uses 'openapi.json' in working directory
```

## Roadmap

### Current Scope (Early Development)
- ✅ Products and Assets with relationships
- ✅ Essential CRUD operations  
- ✅ Product-Asset linking via CrossReference

### Future Expansion  
- Classifications and Entity support
- Advanced attribute handling
- Workflow integration  
- Additional STEP object types per `STEP.xsd`

## Requirements

- Python 3.7+
- requests-openapi  
- requests
- xml.etree.ElementTree (built-in)

## Contributing

When extending functionality:
1. Follow established patterns (parser functions, model classes, creator methods)
2. Reference `STEP.xsd` for XML structure validation  
3. Maintain namespace consistency using `STEPXML_NS`
4. Add corresponding tests in `test.py`

## License

[Add your license information here]

## Support

For STEP MDM integration questions, consult:
- Official STEP documentation
- `STEP.xsd` schema reference  
- Stibo Systems support channels