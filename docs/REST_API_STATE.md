# STEP XML Client - REST API State

This document summarizes the current implementation state of the `rest_client` subpackage
based on the **OpenAPI v1.4.0** specification (200 operationIds across 22 tag groups).

---

## Overview

The `rest_client` subpackage provides typed, spec-compliant coverage of the STEP REST API v2.
All operation wrappers map 1:1 to OpenAPI operationIds; no phantom or invented endpoints exist.

---

## Coverage Matrix (OpenAPI v1.4.0)

| Group | Tag(s) | File | Key Operations |
|-------|--------|------|----------------|
| Assets | Assets | `operations/assets.py` | Full CRUD, search, content, approval, values, purge |
| Products | Products | `operations/products.py` | Full CRUD, search, children, data containers, approval, values, purge |
| Classifications | Classifications | `operations/classifications.py` | Full CRUD, search, children, assets, approval, values, purge |
| Entities | Entities | `operations/entities.py` | Full CRUD, search, find-similar, match-merge, children, data containers, approval, values, purge |
| Attributes | Attributes, Lists Of Values, Data Container Types, Object Types, Reference Types, Units, Unique Keys | `operations/attributes.py` | GET-only: attribute, LOV, LOV entries, DC type, object type (with children), reference type, unit, unique key |
| Data Type Groups | Data Type Groups | `operations/data_type_groups.py` | GET: group, children, attributes, DC types, reference types |
| Background Processes | Background Processes, Background Process Types | `operations/background_processes.py` | GET: process, execution report, attachments, types, type processes |
| Event Processors | Event Processors | `operations/event_processors.py` | GET, enable/disable, invoke, status, statistics, queue |
| Export / Import | Export, Import | `operations/exports.py` | startExport, startImport |
| Inbound | Inbound Integration Endpoints | `operations/inbound.py` | Upload, invoke, status, enable/disable, statistics, execution report |
| Outbound | Outbound Integration Endpoints | `operations/outbound.py` | GET, enable/disable, status, statistics, execution report |
| Gateway | Gateway Integration Endpoints | `operations/gateway.py` | GET, enable/disable, status |
| Relations | Products/Assets/Classifications/Entities references | `operations/relations.py` | List, get, put, delete references + incoming references + reference types |
| Workflows | Workflows, Workflow Tasks | `operations/workflows.py`, `operations/workflow_tasks.py` | GET workflow IDs/definition, create/delete instance, search/claim/release tasks |
| Reporting | Reporting | `operations/reports.py` | Historic changes report |
| Contexts | Contexts | `operations/contexts.py` | GET /contexts, GET /contexts/{id} |
| System | System Information | `operations/system_information.py` | GET /system-information |
| Users | Users | `operations/users.py` | CRUD, randomize password, add/remove from group |
| User Groups | User groups | `operations/user_groups.py` | CRUD, users, children |
| Collections | Collections | `operations/collections.py` | CRUD, content |
| Collection Groups | Collection Groups | `operations/collection_groups.py` | GET, children, collections |
| Batch | Batch Operations | `operations/batch.py` | executeBatchOperation |

**Total: 22 operation files covering all 200 operationIds from OpenAPI v1.4.0.**

---

## Directory Structure

```
stepxmlclient/rest_client/
    __init__.py
    client.py          # StepRestClient (grouped wrappers)
    base.py            # BaseOperation, handle_rest_errors
    exceptions.py
    models/
        __init__.py
        common.py, product.py, asset.py, classification.py, entity.py
        attribute.py, relations.py, import_export.py
        batch.py, collection.py, context.py, data_type_group.py
        background_process.py, event_processor.py, integration_endpoint.py
        system_information.py, user.py, workflow.py
    operations/
        __init__.py
        products.py, assets.py, classifications.py, entities.py
        attributes.py, relations.py, exports.py, inbound.py
        contexts.py, system_information.py, users.py, user_groups.py
        collections.py, collection_groups.py, batch.py
        data_type_groups.py, background_processes.py, event_processors.py
        outbound.py, gateway.py, workflows.py, workflow_tasks.py, reports.py
```

---

## Key Design Principles

- **1:1 mapping**: Every method maps directly to an OpenAPI operationId from v1.4.0.
- **No phantom operations**: Methods that don't exist in the spec were removed.
- **Pydantic models**: Response types use Pydantic with `ConfigDict(extra="allow")` for STEP's dynamic schemas.
- **Convenience wrappers**: `search_by_type()` wraps `query{Type}()` with an `objecttype` condition.

---

## Integration Points
- Unified authentication via `StiboStepRestClient` / `BasicAuthorisation`
- Asset upload/download integrated via `upload.py`
- OIEP download via `StiboStepRestClient.download_oiep_result()`

---

## Dependencies
- `pydantic>=2.0`
- `requests-openapi`
