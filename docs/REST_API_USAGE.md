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

### OpenAPI specification loading

`openapi.json` and `openapi_pub.json` are local, Git-ignored build inputs.
If present at the repository root or directly in `stepxmlclient/`, they are
included in the source distribution and copied into the wheel's `stepxmlclient/`
package (root copies take precedence). Builds without them remain supported.
Publishing does not load or require its JSON specification at runtime.

Loading order:

1. Existing `openapi_file`.
2. Existing `openapi.json` in the application's working directory, only when
   `cache_openapi=True`.
3. Package-local `openapi.json` if supplied at build time or present in a source installation.
4. GET `{location_base}/specification/openapi.json` using the configured,
   authenticated request session, including its TLS and proxy settings.

For applications that already have a local specification, pass its absolute path:

```python
ops_client = StepRestClient(
    location_base="https://your-step-server/restapiv2",
    authorisation=auth,
    openapi_file=r"C:\app\config\step-openapi.json",
)
```

This avoids a specification download (API calls still require authentication).
Without caching, a missing explicit file raises `FileNotFoundError`; with
`cache_openapi=True`, the existing cache/package/server fallback remains enabled.
Successful remote specifications are parsed and loaded before caching. Invalid
responses, HTTP authentication failures and other HTTP errors propagate instead
of being cached or silently ignored. The bootstrap request has a 30-second
timeout and does not follow redirects.

Earlier releases fetched the server specification through an unauthenticated
standalone request before configuring authentication. That could raise HTTP 401
during construction despite correct API credentials, especially in installations
without a local specification. Supplying `openapi_file` also avoids this problem
in those releases; merely having a file in a different repository does not.

Custom authentication handlers run `adapt_client` followed by `do_authorisation`
once, with the server and session configured. When fetching the spec from the
server, these hooks run **before operations exist** and must set up authentication
on the request session rather than call generated API operations. With a local
specification, the existing behavior (hooks see loaded operations) is preserved.

Search wrappers call `queryProducts`, `queryAssets`, `queryClassifications` or
`queryEntities` and wrap STEP's identifier arrays in the existing list models.
Search items contain IDs, not full objects; call `get_product`, `get_asset`,
`get_classification` or `get_entity` when full fields are needed. Compatible
`{"items": [...], "total": ...}` responses are also accepted.

Both clients also expose lazy `client.publishing` for the separate Publishing API.
It borrows authentication/session settings and uses a separate v2 adapter for job
monitoring, without mixing Publishing operations into the v2 OpenAPI client.
See [Publishing usage](PUBLISHING_USAGE.md) for all 16 operations and safeguards.

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

Attribute definitions expose STEP fields such as `validator`, `multivalued`,
`listOfValues` and `validForObjectTypes`. A legacy `type` field is not required.
LOV `values` contains metadata keyed by attribute ID; actual entries come from
`get_list_of_values_entries()` as `value` / `valueId` / optional `unit` dictionaries.
Legacy attribute fields and LOV entry-list inputs remain accepted.

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
- Outgoing references: `ops_client.relations.list_references("entities", entity_id, reference_type_id)`
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
from stepxmlclient.rest_client.exceptions import NotFoundError, RestApiError, ValidationError

try:
    result = client.inbound.upload_and_invoke(endpoint_id, xml_data)
except NotFoundError:
    print("Endpoint not found")
except ValidationError as error:
    print(f"Invalid local parameters: {error}")
except RestApiError as error:
    print(error.status_code, str(error), error.details)
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

Grouped operations check HTTP status codes before processing the response.
HTTP errors and STEP error bodies with `httpStatus >= 400` raise library exceptions,
including on deletes. A rejected delete never returns `True`; `True` means the
server accepted the request, not that an asynchronous deletion has completed.

JSON responses are decoded before model construction: for example,
`ops_client.assets.get_asset("A")` returns `AssetResponse`, so its
`classifications` field can be read directly. Binary downloads are not JSON-decoded.
Reference PUTs send the required empty JSON object when `data` is `None` or `{}`.

HTTP errors expose `status_code` and `details`, with STEP's `message`, `httpReason`
and `detail` included in the exception text. Status 401/403/404/409/429/5xx maps to
`AuthenticationError` / `AuthorizationError` / `NotFoundError` / `ConflictError` /
`RateLimitError` / `ServerError`; other HTTP errors, including 400, raise
`RestApiError`. Local parameter validation still raises `ValidationError`.
`RateLimitError.retry_after` preserves the `Retry-After` header when present.
Network errors raise `RestClientError`, and timeouts raise the library's `TimeoutError`.
HTTP classification uses structured status codes only, never digits in exception
messages. Other unexpected operation errors become `RestClientError`; filesystem
errors and existing library exceptions pass through unchanged.

```python
from stepxmlclient.rest_client.exceptions import NotFoundError, RestApiError

try:
    ops_client.assets.delete_asset("A")
except NotFoundError:
    print("Asset not found")
except RestApiError as error:
    print(error.status_code, str(error), error.details)
```

These guarantees apply to grouped wrappers, not direct calls through
`raw_client.client`: raw OpenAPI access retains the transport's original response
and error behavior. Convenience search methods reuse the checked wrappers.
The Publishing job adapter uses the same checked v2 background-process operations.

---

## Advanced: Custom Operations

You can access any operation defined in the OpenAPI spec via the `raw_client.client` object. Operation names match the OpenAPI operationId.

```python
# Example: call a custom operation
data = raw_client.client.custom_operation_name(param1="value1")
```

---

For more details, see the OpenAPI documentation or the source code in the `stepxmlclient/model/` directory.
