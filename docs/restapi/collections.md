# Collections

> **Operation group:** `client.collections` | **Source:** `stepxmlclient/rest_client/operations/collections.py`

Full CRUD and content access for STEP Collections.

## Operations

| Method | Signature | Description |
|--------|-----------|-------------|
| `create_collection` | `(data) -> CollectionResponse` | Create collection |
| `get_collection` | `(collection_id) -> CollectionResponse` | Get by ID |
| `create_or_replace_collection` | `(collection_id, data) -> CollectionResponse` | Full replace |
| `delete_collection` | `(collection_id) -> bool` | Delete |
| `get_collection_content` | `(collection_id) -> dict` | Get collection content |




