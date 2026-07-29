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
  - [Entity](#entity)
  - [Attribute & Type Definitions](#attribute--type-definitions)
  - [Relations](#relations)
  - [Contexts](#contexts)
  - [Users & User Groups](#users--user-groups)
  - [Collections](#collections)
  - [Workflows & Tasks](#workflows--tasks)
  - [Background Processes](#background-processes)
  - [Inbound Integration Endpoints](#inbound-integration-endpoints)
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
from stepxmlclient.client import StiboStepRestClient, BasicAuthorisation
from stepxmlclient.rest_client import StepRestClient
# ... import operation request models as needed
```

---

## Authentication

The REST client uses HTTP Basic Auth via an authorization object:

```python
from stepxmlclient.client import BasicAuthorisation

auth = BasicAuthorisation(user="your-username", pwd="your-password")
```

---

## Client Initialization

```python
from stepxmlclient.client import StiboStepRestClient
from stepxmlclient.rest_client import StepRestClient

# 1) Raw OpenAPI access (operation IDs on .client)
raw_client = StiboStepRestClient(
    location_base="https://your-step-server/restapiv2",
    authorisation=auth,
    context="Context1",
    workspace="Main"
)

# 2) Grouped wrapper access (recommended)
ops_client = StepRestClient(
    location_base="https://your-step-server/restapiv2",
    authorisation=auth,
    context="Context1",
    workspace="Main"
)
```

The raw client exposes the OpenAPI client as `raw_client.client`. Grouped wrappers are available on `ops_client` (for example `ops_client.products`, `ops_client.assets`, `ops_client.inbound`).

---

## Model Reference & Operations

### Product

**Model:** `ProductCreateRequest`, `ProductUpdateRequest`, `ProductResponse`

**Common Operations:**
- `get_product(product_id)`
- `search_products(condition)`
- `create_product(product_data: ProductCreateRequest)`
- `update_product(product_id, updates: ProductUpdateRequest)`
- `delete_product(product_id)`

**Example:**
```python
from stepxmlclient.rest_client.models.product import ProductCreateRequest

created = ops_client.products.create_product(
    ProductCreateRequest(
        objectType="SalesItem",
        parent="RootProduct",
        name="Sample Product"
    )
)
retrieved = ops_client.products.get_product(created.id)
```

---

### Asset

**Model:** `AssetCreateRequest`, `AssetUpdateRequest`, `AssetResponse`

**Common Operations:**
- `get_asset(asset_id)`
- `search_assets(condition)`
- `create_asset(asset_data: AssetCreateRequest)`
- `update_asset(asset_id, updates: AssetUpdateRequest)`
- `delete_asset(asset_id)`

**Example:**
```python
from stepxmlclient.rest_client.models.asset import AssetCreateRequest

created = ops_client.assets.create_asset(
    AssetCreateRequest(
        objectType="ProductImage",
        classifications=["ProductImageRoot"],
        name="Image1.jpg"
    )
)
retrieved = ops_client.assets.get_asset(created.id)
```

---

### Classification

**Model:** `ClassificationCreateRequest`, `ClassificationUpdateRequest`, `ClassificationResponse`

**Common Operations:**
- `get_classification(classification_id)`
- `search_classifications(condition)`
- `search_by_type(classification_type)`
- `create_classification(data: ClassificationCreateRequest)`
- `update_classification(classification_id, updates: ClassificationUpdateRequest)`
- `replace_classification(classification_id, data: ClassificationCreateRequest)`
- `delete_classification(classification_id)`
- `get_classification_children(classification_id)` → `List[str]`
- `get_classification_value(classification_id, attribute_id)`
- `replace_classification_value(classification_id, attribute_id, value)`
- `delete_classification_value(classification_id, attribute_id)`
- `approve_classification(classification_id)`
- `purge_classification(classification_id)`

Note: `list_classifications()` was removed. Use `search_classifications` with an objecttype condition instead.

**Example:**
```python
from stepxmlclient.rest_client.models.classification import ClassificationCreateRequest, ClassificationUpdateRequest

# Create requires objectType and parent (no id in POST body)
request = ClassificationCreateRequest(
    objectType="WebCategory",
    parent="WebRoot",
    name="Category1"
)
created = ops_client.classifications.create_classification(request)

# Partial update
ops_client.classifications.update_classification("CLASS1", ClassificationUpdateRequest(name="New Name"))

# Get direct children
children = ops_client.classifications.get_classification_children("CLASS1")  # returns List[str]
```

---

### Attribute & Type Definitions

**Model:** `AttributeResponse`, `ListOfValueResponse`

The STEP REST API v2 only provides **read-only** GET access for attribute and type-definition
resources. There is no create, update, or delete for attributes via the REST API.

**Common Operations:**
- `get_attribute(attribute_id)`
- `get_list_of_values(lov_id)`
- `get_list_of_values_entries(lov_id)`
- `get_data_container_type(type_id)`
- `get_data_type_group(group_id)`
- `get_object_type(type_id)`
- `get_object_type_children(type_id)`
- `get_reference_type(reference_type_id)`
- `get_unit(unit_id)`
- `get_unique_key(key_id)`

**Example:**
```python
attr = ops_client.attributes.get_attribute("ATTR001")
lov = ops_client.attributes.get_list_of_values("LOV_Colors")
entries = ops_client.attributes.get_list_of_values_entries("LOV_Colors")
```

---

### Entity

**Model:** `EntityCreateRequest`, `EntityUpdateRequest`, `EntityResponse`

**Common Operations:**
- `get_entity(entity_id)`
- `search_entities(condition)`
- `search_by_type(entity_type)`
- `create_entity(data: EntityCreateRequest)`
- `update_entity(entity_id, updates: EntityUpdateRequest)`
- `replace_entity(entity_id, data: EntityCreateRequest)`
- `delete_entity(entity_id)`
- `get_entity_relationships(entity_id, reference_type_id)`
- `get_entity_value(entity_id, attribute_id)`
- `replace_entity_value(entity_id, attribute_id, value)`
- `delete_entity_value(entity_id, attribute_id)`
- `find_similar_entities(entity_id)`
- `approve_entity(entity_id)`
- `purge_entity(entity_id)`

Note: `list_entities()` was removed. Use `search_entities` with an objecttype condition instead.

**Example:**
```python
from stepxmlclient.rest_client.models.entity import EntityCreateRequest, EntityUpdateRequest

# Create requires objectType and parent (no id in POST body)
request = EntityCreateRequest(
    objectType="Contact",
    parent="ContactsRoot",
    name="Macy, Charles",
    values={"Email": {"value": "charles@example.com"}}
)
created = ops_client.entities.create_entity(request)

# Partial update
ops_client.entities.update_entity("E001", EntityUpdateRequest(name="Updated Name"))
```

### Contexts

**Operations Group:** `contexts`

**Common Operations:**
- `get_contexts()` → list of contexts
- `get_context(context_id)` → single context

**Example:**
```python
all_contexts = ops_client.contexts.get_contexts()
ctx = ops_client.contexts.get_context("Context1")
```

---

### Users & User Groups

**Operations Groups:** `users`, `user_groups`

**Common Operations:**
- `get_user(user_id)`, `create_or_replace_user(user_id, data)`, `update_user(user_id, data)`, `delete_user(user_id)`
- `randomize_password(user_id)`
- `add_user_to_group(user_id, group_data)`, `remove_user_from_group(user_id, group_data)`
- `get_user_group(group_id)`, `create_or_replace_user_group(...)`, `update_user_group(...)`, `delete_user_group(...)`
- `get_user_group_users(group_id)`, `get_user_group_children(group_id)`

---

### Collections

**Operations Groups:** `collections`, `collection_groups`

**Common Operations:**
- `create_collection(data)`, `get_collection(id)`, `create_or_replace_collection(id, data)`, `delete_collection(id)`
- `get_collection_content(id)`
- `get_collection_group(id)`, `get_collection_group_children(id)`, `get_collection_group_collections(id)`

---

### Workflows & Tasks

**Operations Groups:** `workflows`, `workflow_tasks`

**Common Operations:**
- `get_workflow_ids()` → list of workflow IDs
- `get_workflow(workflow_id)`
- `create_workflow_instance(workflow_id, data)`, `delete_workflow_instance(workflow_id, instance_id)`
- `search_workflow_tasks(condition)`, `get_workflow_task(task_id)`
- `claim_workflow_task(task_id)`, `release_workflow_task(task_id)`
- `trigger_workflow_task_event(task_id, data)`

---

### Background Processes

**Operations Group:** `background_processes`

**Common Operations:**
- `get_background_process(process_id)`
- `get_execution_report(process_id)`
- `get_attachments_metadata(process_id)`, `get_attachment_metadata(process_id, attachment_id)`
- `get_attachment_content(process_id, attachment_id)`
- `get_process_types()`, `get_processes_of_type(type_id)`

---

### Relations

**Model:** `RelationshipResponse`, `RelationshipListResponse`

**Common Operations:**
- `list_references(entity_type, entity_id, reference_type_id)`
- `get_reference(entity_type, entity_id, reference_type_id, target_id)`
- `put_reference(entity_type, entity_id, reference_type_id, target_id, data)`
- `delete_reference(entity_type, entity_id, reference_type_id, target_id)`

**Example:**
```python
ops_client.relations.put_reference(
    entity_type="products",
    entity_id="P123",
    reference_type_id="Accessory",
    target_id="P456",
    data={"metadata": {"note": "linked by docs example"}}
)
```

---

### Inbound Integration Endpoints

**Operations Group:** `inbound` (available on `StiboStepRestClient` and `StepRestClient`)

Inbound Integration Endpoints (IIEP) allow you to upload STEP-XML documents directly to a configured endpoint for processing. This is the primary method for batch imports of STEP data.

**Common Operations:**
- `upload_and_invoke(endpoint_id, xml_data, file_name=None)` - Upload STEP-XML and trigger processing
- `list_endpoints()` - List all accessible inbound endpoints
- `get_status(endpoint_id)` - Get current status of an endpoint
- `enable_endpoint(endpoint_id)` - Enable an endpoint
- `disable_endpoint(endpoint_id)` - Disable an endpoint
- `get_execution_report(endpoint_id)` - Get execution details of last operations
- `get_statistics(endpoint_id)` - Get operational statistics
- `get_worker_processes(endpoint_id, status_filter=None)` - Get background processes

**Prerequisites:**
- A configured Inbound Integration Endpoint in STEP (System Setup)
- Endpoint must have a REST-enabled receiver plugin

**Basic Example:**
```python
from stepxmlclient.client import StiboStepRestClient, BasicAuthorisation
from stepxmlclient.creator import Creator

# Initialize client with context
auth = BasicAuthorisation(user="username", pwd="password")
client = StiboStepRestClient(
    location_base="https://your-step.com/restapiv2",
    authorisation=auth,
    context="Context1"
)

# Generate STEP-XML using Creator
creator = Creator(context_id="Context1")
# ... add products, assets, etc ...
creator.build()
xml_bytes = creator.to_bytes()

# Upload to inbound endpoint
result = client.inbound.upload_and_invoke(
    endpoint_id="my_inbound_endpoint",
    xml_data=xml_bytes,
    file_name="import.xml"
)

print(f"Upload successful: {result}")
```

**Check Endpoint Status:**
```python
# List available endpoints
endpoints = client.inbound.list_endpoints()
for ep in endpoints:
    print(f"Endpoint: {ep['ID']}")

# Get current status
status = client.inbound.get_status("my_inbound_endpoint")
print(f"Status: {status}")

# Get execution report (shows what was processed)
report = client.inbound.get_execution_report("my_inbound_endpoint")
for entry in report:
    print(f"Action: {entry.get('action')}, Status: {entry.get('status')}")

# Get statistics
stats = client.inbound.get_statistics("my_inbound_endpoint")
print(f"Messages: {stats.get('messageCount')}")
```

**Error Handling:**
```python
from stepxmlclient.rest_client.exceptions import NotFoundError, ValidationError

try:
    result = client.inbound.upload_and_invoke(endpoint_id, xml_data)
except NotFoundError:
    print("Endpoint not found")
except ValidationError as e:
    if "not enabled" in str(e):
        print("Endpoint is disabled, enabling it...")
        client.inbound.enable_endpoint(endpoint_id)
    else:
        print(f"Validation error: {e}")
```

**Note on Context and Workspace:**
- The `context` parameter is required for all IIEP operations
- The `workspace` parameter is optional and defaults to "Main" on the server
- Both can be set during client initialization or as operation parameters
- Works with both `StiboStepRestClient` and `StepRestClient`

---

## Asset Uploads

For binary asset uploads (images, documents), use the specialized uploader:

```python
from stepxmlclient.upload import AssetUploader

uploader = AssetUploader(client)
result = uploader.upload_file(
    file_path="image.jpg",
    asset_id="A001",
    context_id="Context1",
    workspace_id="Main"
)
print(result)
```

---

## Error Handling

All client operations raise exceptions on HTTP errors. Use try/except blocks to handle errors:

```python
try:
    product = ops_client.products.get_product("P123")
except Exception as e:
    print("Error:", e)
```

---

## Advanced: Custom Operations

You can access any operation defined in the OpenAPI spec via the `raw_client.client` object. Operation names match the OpenAPI operationId.

```python
# Example: call a custom operation
data = raw_client.client.custom_operation_name(param1="value1")
```

---

For more details, see the OpenAPI documentation or the source code in the `stepxmlclient/model/` directory.
