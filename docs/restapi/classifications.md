# Classifications

> **Operation group:** `client.classifications` | **Source:** `stepxmlclient/rest_client/operations/classifications.py`

Full CRUD, search, children, linked assets, approval, values, and lifecycle for STEP classifications.

## Operations

### CRUD

| Method | Signature | Description |
|--------|-----------|-------------|
| `get_classification` | `(classification_id, key_id=None, include_inherited_data=False) -> ClassificationResponse` | Retrieve by ID |
| `search_classifications` | `(condition: dict) -> ClassificationListResponse` | Search via `queryClassifications` |
| `create_classification` | `(data: ClassificationCreateRequest) -> ClassificationResponse` | Create — requires objectType + parent |
| `replace_classification` | `(classification_id, data, key_id=None, allow_overwrite=False) -> ClassificationResponse` | Full replace |
| `update_classification` | `(classification_id, updates, key_id=None) -> ClassificationResponse` | Partial update |
| `delete_classification` | `(classification_id, key_id=None) -> bool` | Delete |

### Children & Assets

| Method | Signature | Description |
|--------|-----------|-------------|
| `get_classification_children` | `(classification_id, key_id=None) -> list[str]` | Direct child IDs |
| `get_classification_assets` | `(classification_id, key_id=None) -> list[dict]` | Linked assets |

### Values

| Method | Signature | Description |
|--------|-----------|-------------|
| `get_classification_value` | `(classification_id, attribute_id, key_id=None) -> dict` | Get value |
| `replace_classification_value` | `(classification_id, attribute_id, value, key_id=None) -> dict` | Replace value |
| `delete_classification_value` | `(classification_id, attribute_id, key_id=None) -> bool` | Delete value |

### Approval & Lifecycle

| Method | Signature | Description |
|--------|-----------|-------------|
| `get_classification_approval_status` | `(classification_id, key_id=None) -> dict` | Approval status |
| `approve_classification` | `(classification_id, key_id=None) -> dict` | Approve |
| `approve_classification_deletion` | `(classification_id, key_id=None) -> dict` | Approve deletion |
| `purge_classification` | `(classification_id, key_id=None) -> dict` | Purge from recycle bin |
| `get_classification_incoming_references` | `(classification_id, key_id=None) -> dict` | Incoming references |

### Convenience

| Method | Signature | Description |
|--------|-----------|-------------|
| `search_by_type` | `(classification_type) -> ClassificationListResponse` | Filter by object type |


## Example
```python
from stepxmlclient.rest_client.models.classification import ClassificationCreateRequest

created = client.classifications.create_classification(ClassificationCreateRequest(
    objectType="WebCategory",
    parent="WebRoot",
    name="Electronics"
))

children = client.classifications.get_classification_children(created.id)
```

> **Note:** `list_classifications()` was removed in v1.4.0. Use `search_by_type()` or `search_classifications()` instead.

