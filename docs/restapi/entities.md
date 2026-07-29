# Entities

> **Operation group:** `client.entities` | **Source:** `stepxmlclient/rest_client/operations/entities.py`

Full CRUD, search, find-similar, match-merge, children, data containers, approval, values, and lifecycle for STEP entities.

## Operations

### CRUD

| Method | Signature | Description |
|--------|-----------|-------------|
| `get_entity` | `(entity_id, key_id=None, include_inherited_data=False) -> EntityResponse` | Retrieve by ID |
| `search_entities` | `(condition: dict) -> EntityListResponse` | Search via `queryEntities` |
| `create_entity` | `(data: EntityCreateRequest) -> EntityResponse` | Create — requires objectType + parent |
| `replace_entity` | `(entity_id, data, key_id=None, allow_overwrite=False) -> EntityResponse` | Full replace |
| `update_entity` | `(entity_id, updates, key_id=None) -> EntityResponse` | Partial update |
| `delete_entity` | `(entity_id, key_id=None) -> bool` | Delete |

### Special Entity Operations

| Method | Signature | Description |
|--------|-----------|-------------|
| `find_similar_entities` | `(entity_id, key_id=None) -> dict` | Find similar entities |
| `entity_match_and_merge` | `(data: dict) -> dict` | Match and merge entities |

### Relationships

| Method | Signature | Description |
|--------|-----------|-------------|
| `get_entity_relationships` | `(entity_id, reference_type_id, key_id=None) -> EntityRelationshipResponse` | Outgoing references by type |

### Children & Data Containers

| Method | Signature | Description |
|--------|-----------|-------------|
| `get_entity_children` | `(entity_id, key_id=None) -> list[str]` | Immediate child IDs |
| `get_entity_data_containers` | `(entity_id, key_id=None) -> dict` | Data containers |
| `get_entity_incoming_references` | `(entity_id, key_id=None) -> dict` | Incoming references |

### Values

| Method | Signature | Description |
|--------|-----------|-------------|
| `get_entity_value` | `(entity_id, attribute_id, key_id=None) -> dict` | Get value |
| `replace_entity_value` | `(entity_id, attribute_id, value, key_id=None) -> dict` | Replace value |
| `delete_entity_value` | `(entity_id, attribute_id, key_id=None) -> bool` | Delete value |

### Approval & Lifecycle

| Method | Signature | Description |
|--------|-----------|-------------|
| `get_entity_approval_status` | `(entity_id, key_id=None) -> dict` | Approval status |
| `approve_entity` | `(entity_id, key_id=None) -> dict` | Approve |
| `approve_entity_deletion` | `(entity_id, key_id=None) -> dict` | Approve deletion |
| `purge_entity` | `(entity_id, key_id=None) -> dict` | Purge from recycle bin |

### Convenience

| Method | Signature | Description |
|--------|-----------|-------------|
| `search_by_type` | `(entity_type, limit=20, offset=0) -> EntityListResponse` | Filter by object type |


## Example
```python
from stepxmlclient.rest_client.models.entity import EntityCreateRequest

created = client.entities.create_entity(EntityCreateRequest(
    objectType="Contact",
    parent="ContactsRoot",
    name="Jane Doe",
    values={"Email": {"value": "jane@example.com"}}
))

similar = client.entities.find_similar_entities(created.id)
rels = client.entities.get_entity_relationships(created.id, "ContactRelation")
```

> **Note:** `list_entities()` was removed in v1.4.0. Use `search_by_type()` or `search_entities()` instead.

