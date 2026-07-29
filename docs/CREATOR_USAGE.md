# STEP XML Creator - Usage Guide

A practical guide to using the `stepxml-client` Creator for building STEP-XML documents with Products, Assets, and their relationships.

---

## Table of Contents

1. [Basic Setup](#basic-setup)
2. [Dynamic Class Loading](#dynamic-class-loading)
3. [Creating Products](#creating-products)
4. [Creating Assets](#creating-assets)
5. [Managing Relations](#managing-relations)
6. [Deletion Operations](#deletion-operations)
7. [Creating Classifications](#creating-classifications)
8. [Creating Entities](#creating-entities)
9. [Complex Element Helpers](#complex-element-helpers)
10. [Advanced Examples](#advanced-examples)
11. [Exporting XML](#exporting-xml)
12. [Sending to STEP API](#sending-to-step-api)

---

## Basic Setup

---
### Import the Required Classes

```python
from stepxmlclient.creator import Creator
from stepxmlclient.model import Product, Asset
from stepxmlclient.model import (
    AssetCrossReference, ProductCrossReference,
    ClassificationCrossReference, EntityCrossReference,
    DeleteAsset, DeleteProduct,
    DeleteAssetCrossReference, DeleteProductCrossReference
)
```

### Create a Creator Instance

```python
# Initialize with required context ID
creator = Creator(context_id="MyContext", workspace_id="Main")

# Build the XML structure
creator.build()

# Export as string
xml_string = creator.to_string()

# Or export as bytes
xml_bytes = creator.to_bytes()
```

---
## Dynamic Class Loading

### Get Model Class by Name

The `get_model_class()` utility function allows you to dynamically load model classes by their name as a string. This is useful when the class type is determined at runtime or comes from configuration/API calls.

```python
from stepxmlclient.model import get_model_class

# Get class by name (case-insensitive)
ProductClass = get_model_class('Product')
AssetClass = get_model_class('Asset')
DeleteClass = get_model_class('DeleteProduct')

# Returns None if class not found
UnknownClass = get_model_class('UnknownType')  # Returns None
```

### Create Instances Dynamically

```python
# Get the class
ProductClass = get_model_class('Product')

# Create instance
if ProductClass is not None:
    product = ProductClass({
        "Name": "Dynamic Product"
    })
    creator.add(product)
else:
    print("Product class not found")
```

### All Available Classes

```python
available_classes = [
    # Core entities
    'Product',
    'ProductReplacementRule',
    'Asset',
    'Classification',
    'Entity',
    # Deletion
    'DeleteAsset',
    'DeleteProduct',
    'DeleteAssetCrossReference',
    'DeleteProductCrossReference',
    # Relations
    'AssetCrossReference',
    'ProductCrossReference',
    'ClassificationReference',       # primary: Product/Asset → Classification
    'ClassificationCrossReference',  # explicit cross-ref variant
    'EntityCrossReference',
    # Complex element helpers
    'STEPWorkflowStateBind',
    'SequenceProduct',
    'OverrideSubProduct',
    'PackagingReference',
    'AssetPushLocation',
    'AssetContent',
    'AssetContentSpecification',
    'BinaryContent',
    'AssetBinaryContent',
    'Task',
    'CurrentTasks',
    'Term',
    'Terms',
    'Tables',
]

# Create all classes dynamically
instances = {}
for class_name in available_classes:
    cls = get_model_class(class_name)
        instances[class_name] = cls
```

### Dynamic Type from Configuration

```python
import json

# Configuration defining what to create
config = {
    "type": "Product",
    "data": {
        "ID": "P001",
        "Name": "Configured Product"
    }
}

# Load class dynamically
ModelClass = get_model_class(config['type'])
if ModelClass:
    obj = ModelClass(config['data'])
    creator.add(obj)
    creator.build()
else:
    raise ValueError(f"Unknown type: {config['type']}")
```

### Factory Pattern with Dynamic Classes

```python
def create_model_object(class_name: str, data: dict):
    """Factory function to create model objects dynamically"""
    ModelClass = get_model_class(class_name)
    
    if ModelClass is None:
        raise ValueError(f"Unknown model class: {class_name}")
    
    return ModelClass(data)

# Usage
product = create_model_object('Product', {"ID": "P001", "Name": "Test"})
asset = create_model_object('Asset', {"ID": "A001", "Name": "Image"})
delete = create_model_object('DeleteProduct', {"ID": "OLD-001"})

creator.add(product)
creator.add(asset)
creator.add(delete)
creator.build()
```

### Bulk Creation from List

```python
# Data from API or configuration
items = [
    {"type": "Product", "data": {"ID": "P001", "Name": "Product 1"}},
    {"type": "Product", "data": {"ID": "P002", "Name": "Product 2"}},
    {"type": "Asset", "data": {"ID": "A001", "Name": "Asset 1"}},
    {"type": "Asset", "data": {"ID": "A002", "Name": "Asset 2"}},
]

creator = Creator(context_id="BulkImport")

for item in items:
    ModelClass = get_model_class(item['type'])
    if ModelClass:
        obj = ModelClass(item['data'])
        creator.add(obj)
    else:
        print(f"Skipped unknown type: {item['type']}")

creator.build()
print(creator.to_string())
```

### Error Handling

```python
def safe_create_object(class_name: str, data: dict, default_type: str = 'Product'):
    """Create object with fallback to default type"""
    
    if ModelClass is None:
        print(f"Warning: Unknown type '{class_name}', using '{default_type}'")
        ModelClass = get_model_class(default_type)
        
        if ModelClass is None:
            raise ValueError(f"Default type '{default_type}' also not found")
    
    return ModelClass(data)

# Usage with automatic fallback
obj = safe_create_object('InvalidType', {"ID": "1"})  # Falls back to Product
```

---
## Creating Products

### Simple Product

```python
creator = Creator(context_id="ProductImport")

# Create a basic product
product = Product({
    "ID": "SKU-001",
    "Name": "Laptop Computer"
})

creator.add(product)
creator.build()
print(creator.to_string())
```

**Output:**
```xml
<?xml version='1.0' encoding='utf-8'?>
<STEP-ProductInformation ContextID="ProductImport" WorkspaceID="Main">
    <Products>
        <Product ID="SKU-001">
            <Name>Laptop Computer</Name>
        </Product>
    </Products>
</STEP-ProductInformation>
```

### Product with Hierarchy

```python
# Parent product
parent = Product({
    "ID": "LAPTOP-FAMILY",
    "Name": "Laptop Family"
})

# Child product
child = Product({
    "ID": "SKU-001",
    "ParentId": "LAPTOP-FAMILY",
    "UserTypeID": "Article",
    "Name": "Laptop Model A"
})

creator.add(parent)
creator.add(child)
creator.build()
```

### Product with Values (Attributes)

```python
product = Product({
    "ID": "SKU-001",
    "Name": "Laptop Computer",
    "Values": {
        "Manufacturer": {
            "value": "TechCorp"
        },
        "Weight": {
            "ID": "kg",
            "value": "2.5"
        },
        "Color": [  # Multi-value
            {"value": "Silver"},
            {"value": "Black"}
        ]
    }
})

creator.add(product)
creator.build()
```

### Batch Add Products

```python
products = [
    Product({"ID": "P001", "Name": "Product 1"}),
    Product({"ID": "P002", "Name": "Product 2"}),
    Product({"ID": "P003", "Name": "Product 3"})
]

not_added = creator.add_list(products)
if not_added:
    print(f"Failed to add: {not_added}")

creator.build()
```

---

## Creating Assets

### Simple Asset

```python
# Create an asset
asset = Asset({
    "ID": "IMG-001",
    "Name": "Product Front View",
    "KeyValue": "laptop-front.jpg"
})

creator.add(asset)
creator.build()
```

**Output:**
```xml
<?xml version='1.0' encoding='utf-8'?>
<STEP-ProductInformation ContextID="..." WorkspaceID="Main">
    <Assets>
        <Asset ID="IMG-001">
            <Name>Product Front View</Name>
            <KeyValue>laptop-front.jpg</KeyValue>
        </Asset>
    </Assets>
</STEP-ProductInformation>
```

### Asset with Values

```python
asset = Asset({
    "ID": "IMG-001",
    "Name": "Product Image",
    "KeyValue": "laptop.jpg",
    "Values": {
        "FileSize": {"value": "2048000"},
        "MimeType": {"value": "image/jpeg"},
        "Resolution": {"value": "1920x1080"}
    }
})

creator.add(asset)
creator.build()
```

### Multiple Assets

```python
assets = [
    Asset({"ID": "IMG-001", "Name": "Front View"}),
    Asset({"ID": "IMG-002", "Name": "Side View"}),
    Asset({"ID": "IMG-003", "Name": "Back View"})
]

creator.add_list(assets)
creator.build()
```

---

## Managing Relations

### Add Asset to Product (Quick Style)

```python
product = Product({"ID": "P001", "Name": "Laptop"})

# Link asset using parameters
product.add_asset_reference(
    asset_id="IMG-001",
    type_="MainImage",
    qualifier_id="EN"
)

creator.add(product)
creator.build()
```

### Add Asset to Product (Object Style)

```python
product = Product({"ID": "P001", "Name": "Laptop"})

# Create reference object with full control
asset_ref = AssetCrossReference({
    "AssetID": "IMG-001",
    "Type": "MainImage",
    "QualifierID": "EN"
})

# Add using object
product.add_asset_reference(ref_object=asset_ref)

creator.add(product)
creator.build()
```

**Output:**
```xml
<Product ID="P001">
    <Name>Laptop</Name>
    <AssetCrossReference AssetID="IMG-001" Type="MainImage" QualifierID="EN"/>
</Product>
```

### Multiple Asset References

```python
product = Product({"ID": "P001", "Name": "Laptop"})

# Add multiple assets
product.add_asset_reference(asset_id="IMG-001", type_="MainImage")
product.add_asset_reference(asset_id="IMG-002", type_="DetailImage")
product.add_asset_reference(asset_id="IMG-003", type_="DetailImage")

creator.add(product)
creator.build()
```

### Product-to-Product Relations

```python
# Related products
product = Product({"ID": "SKU-001", "Name": "Laptop"})

# Parent relationship
product.add_product_reference(
    product_id="LAPTOP-FAMILY",
    type_="Parent",
    mount_location="/1"
)

# Related products
product.add_product_reference(
    product_id="MOUSE-001",
    type_="Related"
)

product.add_product_reference(
    product_id="KEYBOARD-001",
    type_="Related"
)

creator.add(product)
creator.build()
```

### Classification References

```python
product = Product({"ID": "P001", "Name": "Laptop"})

# Categorize product
product.add_classification_reference(
    classification_id="Electronics",
    type_="Belongs",
    qualifier_id="Default"
)

product.add_classification_reference(
    classification_id="Computers",
    mount_location="/1"
)

creator.add(product)
creator.build()
```

### Entity References

```python
product = Product({"ID": "P001", "Name": "Laptop"})

# Link to entities
product.add_entity_reference(
    entity_id="VENDOR-001",
    type_="Supplier",
    qualifier_id="Primary"
)

product.add_entity_reference(
    entity_id="BRAND-001",
    type_="Brand"
)

creator.add(product)
creator.build()
```

### Asset with Product References

```python
# Asset can reference products too
asset = Asset({
    "ID": "IMG-001",
    "Name": "Component Image"
})

asset.add_product_reference(
    product_id="COMPONENT-001",
    type_="ShowsProduct"
)

creator.add(asset)
creator.build()
```

---

## Deletion Operations

### Delete Product (Move to Recycle Bin)

```python
creator = Creator(context_id="DeleteProducts")

# Create delete instruction
delete_product = DeleteProduct({
    "ID": "OLD-SKU-001"
})

creator.add(delete_product)
creator.build()
```

**Output:**
```xml
<STEP-ProductInformation ContextID="DeleteProducts" WorkspaceID="Main">
    <DeletedProducts>
        <DeleteProduct ID="OLD-SKU-001"/>
    </DeletedProducts>
</STEP-ProductInformation>
```

### Delete Asset

```python
delete_asset = DeleteAsset({
    "ID": "OLD-IMG-001"
})

creator.add(delete_asset)
creator.build()
```

### Sever Asset Link from Product

```python
product = Product({"ID": "P001", "Name": "Laptop"})

# Remove asset reference while keeping product
product.delete_asset_reference(
    asset_id="IMG-001",
    type_="OldImage"
)

creator.add(product)
creator.build()
```

**Output:**
```xml
<Product ID="P001">
    <Name>Laptop</Name>
    <DeleteAssetCrossReference AssetID="IMG-001" Type="OldImage"/>
</Product>
```

### Sever Product Link

```python
product = Product({"ID": "P001", "Name": "Laptop"})

# Remove relationship while keeping both products
product.delete_product_reference(
    product_id="OLD-BUNDLE-001",
    type_="BundledWith"
)

creator.add(product)
creator.build()
```

### Batch Delete Products

```python
deletes = [
    DeleteProduct({"ID": "OLD-001"}),
    DeleteProduct({"ID": "OLD-002"}),
    DeleteProduct({"ID": "OLD-003"})
]

creator.add_list(deletes)
creator.build()
```

---

## Advanced Examples

### Complete E-Commerce Product

```python
creator = Creator(context_id="ECommerceSync")

# Create main product
product = Product({
    "ID": "LAPTOP-PRO-2024",
    "ParentId": "LAPTOP-FAMILY",
    "UserTypeID": "Article",
    "Name": "Laptop Pro 2024",
    "Values": {
        "Description": {"value": "Professional laptop for developers"},
        "Price": {"value": "1299.99"},
        "Currency": {"value": "USD"},
        "Weight": {"ID": "kg", "value": "1.8"},
        "Available": {"value": "true"},
        "Colors": [
            {"value": "Space Gray"},
            {"value": "Silver"},
            {"value": "Gold"}
        ]
    }
})

# Add images
product.add_asset_reference(asset_id="LAPTOP-MAIN", type_="MainImage", qualifier_id="EN")
product.add_asset_reference(asset_id="LAPTOP-DETAIL1", type_="DetailImage")
product.add_asset_reference(asset_id="LAPTOP-DETAIL2", type_="DetailImage")

# Add related products
product.add_product_reference(
    product_id="LAPTOP-CASE",
    type_="Accessory",
    mount_location="/accessories/1"
)
product.add_product_reference(
    product_id="LAPTOP-BAG",
    type_="Accessory"
)

# Categorize
product.add_classification_reference(
    classification_id="Electronics/Computers/Laptops",
    type_="Belongs"
)

# Link to vendor
product.add_entity_reference(
    entity_id="VENDOR-TechCorp",
    type_="Supplier"
)

creator.add(product)

# Create accompanying assets
images = [
    Asset({"ID": "LAPTOP-MAIN", "Name": "Main Product Image"}),
    Asset({"ID": "LAPTOP-DETAIL1", "Name": "Detail View 1"}),
    Asset({"ID": "LAPTOP-DETAIL2", "Name": "Detail View 2"})
]

creator.add_list(images)
creator.build()

print(creator.to_string())
```

### Product Update with Changes

```python
creator = Creator(context_id="ProductUpdate")

# Update existing product
product = Product({
    "ID": "SKU-001",
    "Name": "Updated Product Name",
    "Values": {
        "Price": {"value": "99.99"},  # New price
        "Status": {"value": "Active"}
    }
})

# Remove old image
product.delete_asset_reference(asset_id="OLD-IMG", type_="MainImage")

# Add new images
product.add_asset_reference(asset_id="NEW-IMG-1", type_="MainImage")
product.add_asset_reference(asset_id="NEW-IMG-2", type_="ThumbnailImage")

# Update classification
product.delete_product_reference(product_id="OLD-BUNDLE")
product.add_product_reference(product_id="NEW-BUNDLE", type_="BundledWith")

creator.add(product)
creator.build()
```

### Multi-Language Product

```python
product = Product({
    "ID": "P001",
    "Name": "Default Name",
    "Values": {
        "Description": {
            "value": "English description"
        },
        "LocalizedName": [
            {"value": "English Name", "QualifierID": "EN"},
            {"value": "Nom Français", "QualifierID": "FR"},
            {"value": "Nombre Español", "QualifierID": "ES"}
        ]
    }
})

# Asset references for different languages
product.add_asset_reference(
    asset_id="IMG-EN",
    type_="MainImage",
    qualifier_id="EN"
)
product.add_asset_reference(
    asset_id="IMG-FR",
    type_="MainImage",
    qualifier_id="FR"
)

creator.add(product)
creator.build()
```

---

## Exporting XML

### Export to String

```python
creator = Creator(context_id="Export")
creator.add(Product({"ID": "P001", "Name": "Test"}))
creator.build()

xml_string = creator.to_string()
print(xml_string)
```

### Export to Bytes

```python
xml_bytes = creator.to_bytes()
with open("output.xml", "wb") as f:
    f.write(xml_bytes)
```

### Export with Custom Encoding

```python
# UTF-16 encoding
xml_bytes = creator.to_bytes(encoding='utf-16')

# Latin-1 encoding
xml_bytes = creator.to_bytes(encoding='iso-8859-1')
```

### Pretty Print

```python
import xml.dom.minidom as minidom

xml_string = creator.to_string()
dom = minidom.parseString(xml_string)
pretty_xml = dom.toprettyxml(indent="  ")
print(pretty_xml)
```

---

## Sending to STEP API

The library provides two ways to send generated XML directly to a STEP Inbound Integration Endpoint (IIEP):

1. **Recommended**: Use the `inbound` operations wrapper (available on both `StiboStepRestClient` and `StepRestClient`)
2. **Raw Access**: Use the underlying OpenAPI client directly

### Prerequisites

You need a configured **Inbound Integration Endpoint** in your STEP system (under System Setup).

### Method 1: Using Inbound Operations (Recommended)

Both `StiboStepRestClient` and `StepRestClient` include an `inbound` operation group for convenient Inbound Integration Endpoint management.

```python
from stepxmlclient.creator import Creator
from stepxmlclient.client import StiboStepRestClient, BasicAuthorisation

# 1. Generate your STEP-XML
creator = Creator(context_id="Context1", workspace_id="Main")
# ... add products, assets, attributes ...
creator.build()
xml_bytes = creator.to_bytes()

# 2. Setup Authentication
auth = BasicAuthorisation(user="username", pwd="password")
client = StiboStepRestClient(
    location_base="https://your-step-system.com",
    authorisation=auth,
    context="Context1",      # Set default context
    workspace="Main"         # Set default workspace (optional)
)

# 3. Send to Inbound Endpoint
try:
    result = client.inbound.upload_and_invoke(
        endpoint_id="my_inbound_endpoint_id",
        xml_data=xml_bytes,
        file_name="import_data.xml"  # Optional
    )
    print(f"Upload successful: {result}")
    
except Exception as e:
    print(f"Error: {e}")
```

### Additional Inbound Operations

The `inbound` operations group provides multiple methods:

```python
# List all accessible inbound endpoints
endpoints = client.inbound.list_endpoints()
for ep in endpoints:
    print(f"Endpoint: {ep['ID']}")

# Check endpoint status
status = client.inbound.get_status("my_inbound_endpoint_id")
print(f"Status: {status}")

# Enable an endpoint
client.inbound.enable_endpoint("my_inbound_endpoint_id")

# Disable an endpoint
client.inbound.disable_endpoint("my_inbound_endpoint_id")

# Get execution report (details of last operations)
report = client.inbound.get_execution_report("my_inbound_endpoint_id")
for entry in report:
    print(entry)

# Get endpoint statistics
stats = client.inbound.get_statistics("my_inbound_endpoint_id")
print(f"Message count: {stats.get('messageCount')}")

# Get background processes started by the endpoint
processes = client.inbound.get_worker_processes("my_inbound_endpoint_id")
```

### Method 2: Using Raw OpenAPI Client

For lower-level access or if you prefer to use the raw OpenAPI client:

```python
from stepxmlclient.creator import Creator
from stepxmlclient.client import StiboStepRestClient, BasicAuthorisation

# 1. Generate your XML
creator = Creator(context_id="Context1", workspace_id="Main")
# ... add assets and products ...
creator.build()
xml_bytes = creator.to_bytes()

# 2. Setup Authentication
auth = BasicAuthorisation(user="username", pwd="password")
client = StiboStepRestClient(
    location_base="https://your-step-system.com/restapiv2",
    authorisation=auth
)

# 3. Send to Inbound Endpoint
try:
    response = client.client.uploadFileToAndInvokeInboundRestEndpoint(
        id="my_inbound_endpoint_id",  # ID from STEP System Setup
        context="Context1",           # Required
        workspace="Main",             # Optional
        fileName="import_data.xml",   # Optional filename
        body=xml_bytes                # The XML data
    )

    if response.status_code == 200:
        print("Successfully sent to STEP")
    else:
        print(f"Error {response.status_code}: {response.text}")

except Exception as e:
    print(f"Connection error: {e}")
```

### Complete Example Function

```python
def send_xml_to_step_via_wrapper(creator: Creator, endpoint_id: str, config: dict):
    """
    Send creator content to STEP using the high-level inbound wrapper.
    config should contain: host, user, password, context
    """
    from stepxmlclient.rest_client.client import StepRestClient
    from stepxmlclient.client import BasicAuthorisation
    
    # Ensure XML is built
    if not creator.root:
        creator.build()
        
    xml_bytes = creator.to_bytes()
    
    auth = BasicAuthorisation(user=config['user'], pwd=config['password'])
    client = StepRestClient(
        location_base=config['host'],
        authorisation=auth,
        context=config.get('context', 'Context1')
    )
    
    # Simple, clean API
    return client.inbound.upload_and_invoke(
        endpoint_id=endpoint_id,
        xml_data=xml_bytes,
        file_name="data.xml"
    )
```

---

## Common Patterns

### Builder Pattern

```python
creator = Creator(context_id="MyContext")

# Add items
product = Product({"ID": "P001", "Name": "Product"})
product.add_asset_reference(asset_id="A001")
creator.add(product)

asset = Asset({"ID": "A001", "Name": "Image"})
creator.add(asset)

# Build and export
creator.build()
xml = creator.to_string()
```

### Error Handling

```python
# Check if items were added successfully
not_added = creator.add_list([product1, product2, product3])

if not_added:
    print(f"Warning: Failed to add {len(not_added)} items")
    for item in not_added:
        print(f"  - {item._TAG_NAME}")
```

### Dynamic Product Creation

```python
def create_product_from_dict(data):
    """Create product from dictionary"""
    product = Product({
        "ID": data.get("sku"),
        "Name": data.get("name"),
        "Values": data.get("attributes", {})
    })
    
    # Add images
    for img in data.get("images", []):
        product.add_asset_reference(
            asset_id=img["id"],
            type_=img.get("type", "Image")
        )
    
    return product

# Usage
product_data = {
    "sku": "P001",
    "name": "Product Name",
    "attributes": {"Color": {"value": "Red"}},
    "images": [
        {"id": "IMG-001", "type": "MainImage"},
        {"id": "IMG-002", "type": "DetailImage"}
    ]
}

product = create_product_from_dict(product_data)
creator.add(product)
creator.build()
```

---

## Tips & Best Practices

1. **Always call `creator.build()` before exporting** - This constructs the XML tree
2. **Use parameters for simple cases** - Faster than creating objects
3. **Use objects for complex relations** - More control over attributes
4. **Initialize Creator once** - Add multiple items to the same Creator
5. **Batch operations** - Use `add_list()` for multiple items
6. **Validate IDs** - Ensure Product/Asset IDs are unique
7. **Use meaningful Types** - "MainImage", "DetailImage", "Parent", "Related", etc.
8. **Document QualifierID values** - E.g., "EN", "FR", "DE" for languages
9. **Check return values** - `add_list()` returns items that weren't added
10. **Test XML output** - Validate against STEP.xsd schema

---

## Troubleshooting

### XML Not Generated
```python
# Wrong: Forgot to call build()
xml = creator.to_string()  # Empty!

# Correct:
creator.build()
xml = creator.to_string()  # Valid XML
```

### Relations Not Appearing
```python
# Make sure references exist in target system
product.add_asset_reference(asset_id="NONEXISTENT")  # Will create XML,
# but import may fail if asset doesn't exist in STEP

# Best practice: Create assets first
creator.add(asset)
creator.add(product)
```

### Encoding Issues
```python
# If you need specific encoding:
xml_bytes = creator.to_bytes(encoding='utf-8')
with open("output.xml", "wb") as f:
    f.write(xml_bytes)
```
