# STEP XML Client - REST API Usage Guide

This document provides comprehensive usage instructions for the REST API client subpackage of the STEP XML Client library. It covers general setup, authentication, and detailed usage for each model and operation, including code examples.

---

## Table of Contents
- [General Usage](#general-usage)
- [Authentication](#authentication)
- [Client Initialization](#client-initialization)
- [Model Reference & Operations](#model-reference--operations)
  - [Product](#product)
  - [Asset](#asset)
  - [Classification](#classification)
  - [Attribute](#attribute)
  - [Business Rule](#business-rule)
  - [Organization](#organization)
  - [Entity](#entity)
  - [Replacement](#replacement)
  - [Relations](#relations)
- [Asset Uploads](#asset-uploads)
- [Error Handling](#error-handling)
- [Advanced: Custom Operations](#advanced-custom-operations)

---

## General Usage

Install the package (after building):

```bash
pip install dist/stepxmlclient-x.x-py3-none-any.whl
```

Import the REST client and models:

```python
from stepxmlclient.client import StiboStepRestClient
from stepxmlclient.model.product import Product
# ... import other models as needed
```

---

## Authentication

The REST client uses HTTP Basic Auth or Bearer Token (API Key). Provide credentials on initialization:

```python
client = StiboStepRestClient(
    base_url="https://your-step-server/api/v2",
    username="your-username",
    password="your-password"
)
# Or with API key:
client = StiboStepRestClient(
    base_url="https://your-step-server/api/v2",
    api_key="your-api-key"
)
```

---

## Client Initialization

```python
from stepxmlclient.client import StiboStepRestClient
client = StiboStepRestClient(base_url="https://your-step-server/api/v2", username="user", password="pass")
```

The client exposes the OpenAPI client as `client.client`. All operations are available as methods on this object, named after the OpenAPI operation IDs.

---

## Model Reference & Operations

### Product

**Model:** `Product`

**Common Operations:**
- `get_product_by_id(product_id)`
- `list_products()`
- `create_product(product: Product)`
- `update_product(product_id, product: Product)`
- `delete_product(product_id)`

**Example:**
```python
from stepxmlclient.model.product import Product
product = Product(id="P123", name="Sample Product", description="A demo product.")
created = client.client.create_product(product=product)
retrieved = client.client.get_product_by_id(product_id="P123")
```

---

### Asset

**Model:** `Asset`

**Common Operations:**
- `get_asset_by_id(asset_id)`
- `list_assets()`
- `create_asset(asset: Asset)`
- `update_asset(asset_id, asset: Asset)`
- `delete_asset(asset_id)`

**Example:**
```python
from stepxmlclient.model.asset import Asset
asset = Asset(id="A001", name="Image1.jpg", type="image/jpeg")
created = client.client.create_asset(asset=asset)
```

---

### Classification

**Model:** `Classification`

**Common Operations:**
- `get_classification_by_id(classification_id)`
- `list_classifications()`
- `create_classification(classification: Classification)`

**Example:**
```python
from stepxmlclient.model.classification import Classification
classification = Classification(id="C001", name="Category1")
created = client.client.create_classification(classification=classification)
```

---

### Attribute

**Model:** `Attribute`

**Common Operations:**
- `get_attribute_by_id(attribute_id)`
- `list_attributes()`
- `create_attribute(attribute: Attribute)`

**Example:**
```python
from stepxmlclient.model.attribute import Attribute
attribute = Attribute(id="Attr1", name="Color", type="string")
created = client.client.create_attribute(attribute=attribute)
```

---

### Business Rule

**Model:** `BusinessRule`

**Common Operations:**
- `get_business_rule_by_id(rule_id)`
- `list_business_rules()`

**Example:**
```python
from stepxmlclient.model.business import BusinessRule
rule = client.client.get_business_rule_by_id(rule_id="BR001")
```

---

### Organization

**Model:** `Organization`

**Common Operations:**
- `get_organization_by_id(org_id)`
- `list_organizations()`

**Example:**
```python
from stepxmlclient.model.organization import Organization
org = client.client.get_organization_by_id(org_id="ORG001")
```

---

### Entity

**Model:** `Entity`

**Common Operations:**
- `get_entity_by_id(entity_id)`
- `list_entities()`
- `create_entity(entity: Entity)`

**Example:**
```python
from stepxmlclient.model.entity import Entity
entity = Entity(id="E001", name="Entity1")
created = client.client.create_entity(entity=entity)
```

---

### Replacement

**Model:** `Replacement`

**Common Operations:**
- `get_replacement_by_id(replacement_id)`
- `list_replacements()`

**Example:**
```python
from stepxmlclient.model.replacement import Replacement
replacement = client.client.get_replacement_by_id(replacement_id="R001")
```

---

### Relations

**Model:** `Relation`

**Common Operations:**
- `get_relation_by_id(relation_id)`
- `list_relations()`

**Example:**
```python
from stepxmlclient.model.relations import Relation
relation = client.client.get_relation_by_id(relation_id="REL001")
```

---

## Asset Uploads

For binary asset uploads (images, documents), use the specialized uploader:

```python
from stepxmlclient.upload import StepAssetUploader
uploader = StepAssetUploader(client)
with open("image.jpg", "rb") as f:
    uploader.upload_asset(asset_id="A001", file=f)
```

---

## Error Handling

All client operations raise exceptions on HTTP errors. Use try/except blocks to handle errors:

```python
try:
    product = client.client.get_product_by_id(product_id="P123")
except Exception as e:
    print("Error:", e)
```

---

## Advanced: Custom Operations

You can access any operation defined in the OpenAPI spec via the `client.client` object. Operation names match the OpenAPI operationId.

```python
# Example: call a custom operation
data = client.client.custom_operation_name(param1="value1")
```

---

For more details, see the OpenAPI documentation or the source code in the `stepxmlclient/model/` directory.
