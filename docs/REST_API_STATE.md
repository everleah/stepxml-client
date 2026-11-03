# STEP XML Client - REST API State

This document summarizes the current implementation state of the `rest_client` subpackage
based on the **OpenAPI v1.4.0** specification (200 operationIds across 22 tag groups).

---

## Overview

The `rest_client` subpackage provides grouped, typed wrappers for STEP REST API v2.
The matrix lists implemented areas, not a guarantee of complete endpoint or schema coverage.
Direct OpenAPI access remains available for operations without a grouped wrapper.

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

The reference specification contains 200 operationIds. Complete grouped coverage
of all 200 operations is not certified.

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

- **Operation mapping**: Wrappers use specification operationIds; convenience
  methods delegate to checked wrappers.
- **Pydantic models**: Response types use Pydantic; dynamic maps are retained in
  fields such as values/references. Unknown-field handling varies by model.
- **Convenience wrappers**: `search_by_type()` wraps `query{Type}()` with an `objecttype` condition.
- **Search responses**: STEP returns arrays of `{id, type}` identifiers, wrapped
  in the existing list response models without extra GETs. Results are not hydrated
  entities; totals remain unknown unless supplied by a compatible wrapped payload.
- **CRUD restoration**: Classification/entity create, update, replace and delete
  wrappers and classification children use the shared response boundary.
- **Definitions and exports**: Attributes expose validator-based STEP fields;
  LOV metadata and entries are separate. ExportSpecification supports `stepUrls`
  and `processDescription`; import/export triggers return only a process identifier.
- **Shared response boundary**: Grouped wrappers validate HTTP errors and STEP
  `httpStatus` payloads before converting models, extracting lists or returning
  delete success. JSON HTTP responses become native payloads first; binary
  downloads retain checked content.
- **Error metadata**: Exceptions retain server messages, response details and
  status codes, including authentication/authorization failures. Rate-limit
  errors also expose `retry_after`. Wrappers do not classify errors from message
  text; HTTP classification is centralized.
- **Incoming references**: Array endpoints return lists of dictionaries;
  compatible object payloads remain `RelationshipListResponse`. The return
  annotation includes both forms.
- **Required reference bodies**: Reference PUTs send `{}` when no values are supplied.
- **Offline regression coverage**: `tests/test_rest_response_handling.py` exercises
  real `requests.Response` objects and synthetic `requests-openapi` transport.
- **Specification alignment**: `tests/test_rest_client_spec_alignment.py` checks
  independent synthetic endpoint contracts. When an authorized local OpenAPI file
  exists, it also checks operation IDs and runs the same transport scenarios against
  that file. These checks do not certify every endpoint or replace live STEP validation.

---

## Integration Points
- Unified authentication via `StiboStepRestClient` / `BasicAuthorisation`
- Server OpenAPI bootstrap uses the same authenticated session and TLS/proxy
  configuration as API calls, with a timeout and no redirects. Explicit local
  specs, enabled existing caches and optionally bundled `openapi.json` avoid the
  bootstrap request. The two OpenAPI JSON files are Git-ignored, optional local
  build inputs. See [specification loading](REST_API_USAGE.md#openapi-specification-loading).
- Asset upload/download integrated via `upload.py`
- OIEP download via `StiboStepRestClient.download_oiep_result()`
- Independent Publishing subclient through lazy `.publishing`; v2 job monitoring
  is connected by an injected adapter, not additional v2 operationIds.
  See [Publishing state](PUBLISHING_STATE.md) and [usage](PUBLISHING_USAGE.md).

---

## Dependencies
- `pydantic>=2.0`
- `requests-openapi`
