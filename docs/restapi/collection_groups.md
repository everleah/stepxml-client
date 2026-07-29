# Collection Groups

> **Operation group:** `client.collection_groups` | **Source:** `stepxmlclient/rest_client/operations/collection_groups.py`

Read-only access to STEP Collection Groups.

## Operations

| Method | Signature | Description |
|--------|-----------|-------------|
| `get_collection_group` | `(group_id) -> dict` | Get group by ID |
| `get_collection_group_children` | `(group_id) -> list[str]` | Child group IDs |
| `get_collection_group_collections` | `(group_id) -> list[dict]` | Collections in group |




