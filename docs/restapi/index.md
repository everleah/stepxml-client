# STEP REST API v2 — Operation Group Reference

> Based on **OpenAPI v1.4.0** (200 operationIds, 22 tag groups)

All groups are accessible via `client.<group>` on a `StepRestClient` instance.
For setup instructions see [REST_API_USAGE.md](../REST_API_USAGE.md).

---

## Entity Types

| Document | Group | Description |
|----------|-------|-------------|
| [Products](products.md) | `client.products` | Full CRUD, search, children, values, approval, lifecycle |
| [Assets](assets.md) | `client.assets` | Full CRUD, search, binary upload/download, values, approval, lifecycle |
| [Classifications](classifications.md) | `client.classifications` | Full CRUD, search, children, linked assets, values, approval, lifecycle |
| [Entities](entities.md) | `client.entities` | Full CRUD, search, find-similar, match-merge, values, approval, lifecycle |

## Type Definitions & Configuration

| Document | Group | Description |
|----------|-------|-------------|
| [Attributes & Type Definitions](attributes.md) | `client.attributes` | Read-only: attributes, LOVs, object types, reference types, units, unique keys |
| [Data Type Groups](data_type_groups.md) | `client.data_type_groups` | Read-only: group hierarchy, member attributes/DC types/reference types |
| [Relations](relations.md) | `client.relations` | Cross-references between all entity types |

## Integration Endpoints

| Document | Group | Description |
|----------|-------|-------------|
| [Inbound (IIEP)](inbound.md) | `client.inbound` | Upload STEP-XML, manage endpoints, monitor execution |
| [Outbound (OIEP)](outbound.md) | `client.outbound` | Manage outbound endpoints, enable/disable, monitor |
| [Gateway](gateway.md) | `client.gateway` | Manage gateway integration endpoints |

## System & Administration

| Document | Group | Description |
|----------|-------|-------------|
| [Contexts](contexts.md) | `client.contexts` | List and query STEP contexts |
| [System Information](system_information.md) | `client.system_information` | System metadata |
| [Users](users.md) | `client.users` | CRUD, password, group assignment |
| [User Groups](user_groups.md) | `client.user_groups` | CRUD, members, hierarchy |
| [Collections](collections.md) | `client.collections` | CRUD, content |
| [Collection Groups](collection_groups.md) | `client.collection_groups` | Read-only hierarchy |
| [Background Processes](background_processes.md) | `client.background_processes` | Monitor async jobs |
| [Event Processors](event_processors.md) | `client.event_processors` | Manage event processors and queues |

## Workflows & Automation

| Document | Group | Description |
|----------|-------|-------------|
| [Workflows](workflows.md) | `client.workflows` | Definitions, instances |
| [Workflow Tasks](workflow_tasks.md) | `client.workflow_tasks` | Search, claim, release, trigger |

## Data Transfer

| Document | Group | Description |
|----------|-------|-------------|
| [Exports & Imports](exports.md) | `client.exports` | Trigger export/import configurations |
| [Reports](reports.md) | `client.reports` | Historic changes reports |
| [Batch Operations](batch.md) | `client.batch` | Multi-operation batch execution |

---

## Quick Reference

```python
from stepxmlclient.rest_client import StepRestClient
from stepxmlclient.client import BasicAuthorisation

client = StepRestClient(
    location_base="https://step.example.com/restapiv2",
    authorisation=BasicAuthorisation("user", "pass"),
    context="Context1"
)

# Entity CRUD
client.products.create_product(...)
client.assets.upload_asset_content(...)
client.classifications.get_classification_children(...)
client.entities.find_similar_entities(...)

# References
client.relations.put_reference(entity_type="products", ...)

# Inbound uploads
client.inbound.upload_and_invoke(endpoint_id="iiep", xml_data=...)

# System
ctxs = client.contexts.get_contexts()
info = client.system_information.get_system_information()

# Async monitoring
proc = client.background_processes.get_background_process("BGP_123")
```
