# REST API Client Development Plan

## Overview

Expand `stepxml-client` to provide comprehensive coverage of STEP REST API v2 through a new `rest_client` submodule, leveraging shared authentication and following the project's proven phased development approach.

## Goals

1. **Structured REST API Coverage**: Provide typed, discoverable client for STEP REST API v2
2. **Shared Authentication**: Reuse existing auth mechanisms from XML client
3. **Type Safety**: Use Pydantic for request/response models and type hints
4. **Domain Organization**: Group operations by business domain (Products, Assets, Classifications, etc.)
5. **Integration Ready**: Enable seamless data flow between XML parsing and REST operations
6. **Documentation**: Clear usage examples and operation discovery

## Architecture

### Directory Structure

```
stepxmlclient/
├── rest_client/
│   ├── __init__.py
│   ├── client.py              # Core StepRestClient (wrapper/extension)
│   ├── base.py                # Base operation class
│   ├── models/
│   │   ├── __init__.py
│   │   ├── common.py          # Shared response models (Paging, Error, etc.)
│   │   ├── product.py         # Product-related models
│   │   ├── asset.py           # Asset-related models
│   │   ├── classification.py  # Classification models
│   │   ├── entity.py          # Entity models
│   │   ├── import_export.py   # Import/Export models
│   │   └── metadata.py        # System metadata models
│   ├── operations/
│   │   ├── __init__.py
│   │   ├── products.py        # ProductOperations
│   │   ├── assets.py          # AssetOperations
│   │   ├── classifications.py # ClassificationOperations
│   │   ├── entities.py        # EntityOperations
│   │   ├── attributes.py      # AttributeOperations
│   │   ├── imports.py         # ImportOperations
│   │   ├── exports.py         # ExportOperations
│   │   └── metadata.py        # MetadataOperations
│   └── exceptions.py          # REST-specific exceptions
```

### Module Dependencies

- **Existing**: `requests-openapi` (already integrated)
- **New**: `pydantic` (for models and validation)
- **Optional**: `openapi-python-client` (future code generation)

## Development Phases

### Phase 0: Foundation & Infrastructure (Priority: CRITICAL)
**Objective**: Set up core infrastructure and patterns

#### 0.1 - Core Pydantic Models
- [x] Create `rest_client/models/common.py` with:
  - `PagedResponse[T]` - Generic paginated result wrapper
  - `ErrorResponse` - Standard error model
  - `ApiResponse[T]` - Generic API response envelope
- [x] Add validation utilities and helpers

**Files to Create**:
- `stepxmlclient/rest_client/__init__.py`
- `stepxmlclient/rest_client/models/__init__.py`
- `stepxmlclient/rest_client/models/common.py`
- `stepxmlclient/rest_client/exceptions.py`

**Tests**:
- `test_rest_client_phase0_foundation.py`

#### 0.2 - Base Operation Class
- [x] Create `rest_client/base.py` with `BaseOperation` class
  - Common patterns for all operations
  - Error handling wrapper
  - Pagination helpers
  - Logging integration
- [x] Client wrapper `rest_client/client.py`
  - Extend `StiboStepRestClient`
  - Initialize operation instances
  - Expose operation groups

**Tests**:
- `test_rest_client_phase0_foundation.py` (extended)

---

### Phase 1: Product Operations (Priority: HIGH)
**Objective**: Full CRUD and search for Products

#### 1.1 - Product Models
- [x] `rest_client/models/product.py`:
  - `ProductResponse` - Single product data
  - `ProductListResponse` - List with pagination
  - `ProductSearchRequest` - Search query model
  - `ProductCreateRequest` - Create payload
  - `ProductUpdateRequest` - Update payload

#### 1.2 - Product Operations
- [x] `rest_client/operations/products.py`:
  - `get_product(product_id)` - Retrieve single
  - `search_products(query, filters, limit, offset)` - Search/list
  - `create_product(product_data)` - Create
  - `update_product(product_id, updates)` - Update
  - `delete_product(product_id)` - Delete
  - `get_product_attributes(product_id)` - Attributes
  - `get_product_values(product_id)` - Values

**Leverage XML Client**: 
- Response data can feed into XML parser for detailed analysis
- Integrations tests should demonstrate this flow

**Tests**:
- `test_rest_client_phase1_products.py`

---

### Phase 2: Asset Operations (Priority: HIGH)
**Objective**: Asset CRUD, search, and binary operations

#### 2.1 - Asset Models
- [x] `rest_client/models/asset.py`:
  - `AssetResponse` - Asset metadata
  - `AssetListResponse` - List results
  - `AssetSearchRequest` - Search criteria
  - `AssetUploadRequest` - Binary upload metadata
  - `AssetDownloadResponse` - Download info

#### 2.2 - Asset Operations
- [x] `rest_client/operations/assets.py`:
  - `get_asset(asset_id)` - Retrieve
  - `search_assets(query, filters, limit, offset)` - Search
  - `create_asset(asset_data)` - Create
  - `update_asset(asset_id, updates)` - Update
  - `delete_asset(asset_id)` - Delete
  - `get_asset_content(asset_id)` - Get binary content
  - `upload_asset_content(asset_id, file_path)` - Upload binary

**Leverage Existing**: 
- Integrate with `upload.py` module for binary handling
- Consistency with existing asset upload patterns

**Tests**:
- `test_rest_client_phase2_assets.py`

---

### Phase 3: Classification Operations (Priority: MEDIUM)
**Objective**: Classification hierarchy and CRUD

#### 3.1 - Classification Models
- [x] `rest_client/models/classification.py`:
  - `ClassificationResponse` - Single classification
  - `ClassificationListResponse` - List
  - `ClassificationHierarchyResponse` - Hierarchical structure
  - `ClassificationCreateRequest` - Create payload

#### 3.2 - Classification Operations
- [x] `rest_client/operations/classifications.py`:
  - `get_classification(classification_id)` - Retrieve
  - `list_classifications(filters, limit, offset)` - List
  - `get_classification_hierarchy(root_id)` - Hierarchical view
  - `create_classification(data)` - Create
  - `update_classification(id, updates)` - Update
  - `delete_classification(id)` - Delete
  - `get_classification_values(id)` - Associated values

**Tests**:
- `test_rest_client_phase3_classifications.py`

---

### Phase 4: Entity Operations (Priority: MEDIUM)
**Objective**: Entity CRUD and management

#### 4.1 - Entity Models
- [x] `rest_client/models/entity.py`:
  - `EntityResponse` - Entity data
  - `EntityListResponse` - List
  - `EntityCreateRequest` - Create payload
  - `EntityUpdateRequest` - Update payload

#### 4.2 - Entity Operations
- [x] `rest_client/operations/entities.py`:
  - `get_entity(entity_id)` - Retrieve
  - `list_entities(filters, limit, offset)` - List
  - `create_entity(data)` - Create
  - `update_entity(id, updates)` - Update
  - `delete_entity(id)` - Delete
  - `get_entity_attributes(id)` - Attributes

**Tests**:
- `test_rest_client_phase4_entities.py`

---

### Phase 5: Attribute & Metadata Operations (Priority: MEDIUM)
**Objective**: Attributes, LOVs, contexts, and system metadata

#### 5.1 - Models
- [x] `rest_client/models/attribute.py`:
  - `AttributeResponse`, `AttributeListResponse`
  - `ListOfValueResponse` - LOV definitions
  - `ContextResponse` - Context definitions
  
- [x] `rest_client/models/metadata.py`:
  - `SystemMetadataResponse` - Version, capabilities
  - `QualifierResponse` - Qualifier definitions
  - `DimensionResponse` - Dimension definitions

#### 5.2 - Operations
- [x] `rest_client/operations/attributes.py`:
  - `get_attribute(attr_id)` - Retrieve
  - `list_attributes(filters)` - List
  - `get_lov_items(lov_id)` - LOV items
  
- [x] `rest_client/operations/metadata.py`:
  - `get_system_info()` - Version, capabilities
  - `list_contexts()` - Available contexts
  - `list_qualifiers()` - Available qualifiers
  - `list_dimensions()` - Available dimensions

**Tests**:
- `test_rest_client_phase5_metadata.py`

---

### Phase 6: Import/Export Operations (Priority: MEDIUM)
**Objective**: Bulk import/export and data exchange

#### 6.1 - Models
- [x] `rest_client/models/import_export.py`:
  - `ImportJobResponse` - Import job status
  - `ImportJobCreateRequest` - Create import job
  - `ExportJobResponse` - Export job status
  - `ExportJobCreateRequest` - Create export job
  - `JobProgressResponse` - Job progress tracking

#### 6.2 - Operations
- [x] `rest_client/operations/imports.py`:
  - `create_import_job(source_data, config)` - Start import
  - `get_import_job(job_id)` - Check status
  - `list_import_jobs(filters)` - List jobs
  - `cancel_import_job(job_id)` - Cancel
  - `get_import_job_errors(job_id)` - Error details

- [x] `rest_client/operations/exports.py`:
  - `create_export_job(config)` - Start export
  - `get_export_job(job_id)` - Check status
  - `list_export_jobs(filters)` - List jobs
  - `download_export_data(job_id)` - Get exported data

**Leverage XML**: 
- Export data flows naturally into XML parser
- Import operations can use XML generator output

**Tests**:
- `test_rest_client_phase6_imports_exports.py`

---

### Phase 7: Relations Operations (Priority: HIGH)
**Objective**: Relationship management, cross-references, and links

#### 7.1 - Models
- [x] `rest_client/models/relations.py`:
  - `RelationshipTypeResponse` - Relationship type definitions
  - `RelationshipResponse` - Single relationship
  - `RelationshipListResponse` - Paginated relationships
  - `RelationshipCreateRequest` - Create relationship
  - `RelationshipUpdateRequest` - Update relationship
  - `CrossReferenceResponse` - Entity cross-references
  - `CrossReferenceListResponse` - Paginated cross-references
  - `CrossReferenceCreateRequest` - Create cross-reference
  - `LinkResponse` - Product/Asset links
  - `LinkListResponse` - Paginated links
  - `LinkCreateRequest` - Create link
  - `RelationshipGraphResponse` - Graph representation

#### 7.2 - Operations
- [x] `rest_client/operations/relations.py`:
  - `get_relationship(relationship_id)` - Get relationship
  - `list_relationships(filters)` - List relationships
  - `create_relationship(data)` - Create relationship
  - `update_relationship(relationship_id, data)` - Update relationship
  - `delete_relationship(relationship_id)` - Delete relationship
  - `get_relationship_types()` - Get available types
  - `get_relationship_graph(entity_id, depth)` - Traverse graph
  - `get_cross_reference(cross_reference_id)` - Get cross-reference
  - `list_cross_references(filters)` - List cross-references
  - `create_cross_reference(data)` - Create cross-reference
  - `delete_cross_reference(cross_reference_id)` - Delete cross-reference
  - `get_link(link_id)` - Get link
  - `list_links(filters)` - List links
  - `create_link(data)` - Create link
  - `delete_link(link_id)` - Delete link

**Tests**:
- `test_rest_client_phase7_relations.py` (39 tests)

---

## Testing Strategy

### Test Organization
- **Phase-based**: `test_rest_client_phase{N}_{domain}.py`
- **Integration tests**: Validate against actual STEP instance (with mock fallbacks)
- **Unit tests**: Model validation, error handling
- **Roundtrip tests**: REST ↔ XML data flow

### Mock/Live Server
- Use mock responses for CI/CD
- Optional real STEP instance for integration
- Response fixtures from `openapi.json`

### Test Coverage Goals
- Phase 0: 100% (infrastructure must be robust)
- Phase 1-2: 80%+ (core operations)
- Phase 3+: 70%+ (nice to have comprehensive, but 70% acceptable)

---

## Integration Points

### With Existing XML Module

1. **Unified Auth**: Both clients share `BasicAuthorisation`, `OAuth2Authorisation`, etc.
   ```python
   auth = BasicAuthorisation(username, password)
   xml_client = StepXmlClient(host, auth, ...)
   rest_client = StepRestClient(host, auth, ...)
   ```

2. **Data Flow: REST → XML**
   ```python
   # Get product via REST
   product_data = rest_client.products.get_product('PROD123')
   
   # Parse detailed structure with XML
   xml_data = xml_client.get_product_xml('PROD123')
   parsed = parser.parse(xml_data)
   ```

3. **Data Flow: XML → REST**
   ```python
   # Create with XML generator
   xml_doc = creator.create_product(product_obj)
   
   # Upload via REST
   rest_client.products.create_product(xml_doc)
   ```

4. **Upload Module**: Integrate `rest_client.assets` with existing `upload.py`

---

## Dependencies to Add

### Required
```
pydantic>=2.0    # Models and validation
```

### Optional (for future phases)
```
openapi-python-client>=0.15  # Code generation (Phase 8+)
```

### Update `requirements.txt` and `setup.py`

---

## Success Criteria

- ✅ Phase 0 complete: Solid infrastructure (DONE - 37 tests)
- ✅ Phase 1 complete: Product operations (DONE - 36 tests)
- ✅ Phase 2 complete: Asset operations (DONE - 40 tests)
- ✅ Phase 3 complete: Classification operations (DONE - 33 tests)
- ✅ Phase 4 complete: Entity operations (DONE - 37 tests)
- ✅ Phase 5 complete: Attribute & metadata operations (DONE - 33 tests)
- ✅ Phase 6 complete: Import/Export operations (DONE - 29 tests)
- ✅ Phase 7 complete: Relations operations (DONE - 39 tests)
- ✅ Auth shared and working across modules (DONE)
- ✅ Type hints on all public APIs (DONE)
- ✅ Comprehensive test coverage (284/284 tests passing, 100%)
- ✅ Error handling with proper exception hierarchy (DONE)
- ⏳ Phase 8 operations (NEXT - Advanced features)

---

## Timeline & Priorities

| Phase | Priority | Estimated Effort | Status |
|-------|----------|------------------|--------|
| 0     | CRITICAL | 2-3 days         | ✅ Complete (37 tests) |
| 1     | HIGH     | 3-4 days         | ✅ Complete (36 tests) |
| 2     | HIGH     | 2-3 days         | ✅ Complete (40 tests) |
| 3     | MEDIUM   | 2-3 days         | ✅ Complete (33 tests) |
| 4     | MEDIUM   | 2-3 days         | ✅ Complete (37 tests) |
| 5     | MEDIUM   | 2-3 days         | ✅ Complete (33 tests) |
| 6     | MEDIUM   | 3-4 days         | ✅ Complete (29 tests) |
| 7     | HIGH     | 3-4 days         | ✅ Complete (39 tests) |
| 8     | LOW      | 4-5 days         | 📋 Next (Bulk Operations, Workflows) |

---

## Completion Status

### ✅ Completed Phases (284 Tests - 100% Pass Rate)

1. ✅ **Phase 0**: Foundation infrastructure (37 tests)
   - BaseOperation, exception hierarchy, pagination helpers
   - Common models: PagedResponse, ErrorResponse, ApiResponse, SearchFilter

2. ✅ **Phase 1**: Product Operations (36 tests)
   - CRUD operations, search, filtering, attributes, values
   - Cross-references and product attributes

3. ✅ **Phase 2**: Asset Operations (40 tests)
   - CRUD operations, binary upload/download
   - Asset metadata, search with filters, content retrieval

4. ✅ **Phase 3**: Classification Operations (33 tests)
   - CRUD operations, hierarchy traversal
   - Classification values and metadata

5. ✅ **Phase 4**: Entity Operations (37 tests)
   - CRUD operations, relationships with pagination
   - Bulk create/update, advanced search, entity attributes

6. ✅ **Phase 5**: Attribute & Metadata Operations (33 tests)
   - Attribute models and operations (get, search, list, create, update, delete)
   - Metadata models (System, Contexts, Qualifiers, Dimensions, UserTypes, Workspaces)
   - LOV (List of Values) retrieval and management

7. ✅ **Phase 6**: Import/Export Operations (29 tests)
   - Import job management (create, status tracking, error handling, cancellation)
   - Export job management (create, status tracking, data download)
   - Job progress tracking and error details
   - Convenience methods for filtering by status and entity type

8. ✅ **Phase 7**: Relations Operations (39 tests)
   - Relationship operations (get, list, create, update, delete)
   - Relationship type discovery and graph traversal
   - Cross-reference management (create, list, delete)
   - Link management (create, list, delete)
   - Graph operations for entity relationship analysis

### 🎯 Test Coverage Summary

```
Phase 0 (Foundation):           37/37 ✅
Phase 1 (Products):            36/36 ✅
Phase 2 (Assets):              40/40 ✅
Phase 3 (Classifications):     33/33 ✅
Phase 4 (Entities):            37/37 ✅
Phase 5 (Attributes/Metadata): 33/33 ✅
Phase 6 (Import/Export):       29/29 ✅
Phase 7 (Relations):           39/39 ✅
────────────────────────────────────────
TOTAL:                        284/284 ✅ (100%)
```

### 📋 Next Steps: Phase 8 (Advanced Features)

Phase 8 will cover remaining advanced capabilities:
1. **Bulk operations** - Batch create, update, delete operations
2. **Workflow management** - Workflow triggers and execution
3. **Advanced search** - Complex queries, aggregations
4. **Caching & performance** - Optional response caching layer
5. **Streaming** - Large result set handling

**Phase 8 Estimated Scope**:
- Bulk operations (15-20 tests)
- Workflow operations (10-15 tests)
- Advanced search (10-15 tests)
- ~40-50 total tests
- ~4-5 days estimated effort

**Milestone Achievement**: Phases 0-7 complete with 284/284 tests (100% pass rate)!
