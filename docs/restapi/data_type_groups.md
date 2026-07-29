# Data Type Groups

> **Operation group:** `client.data_type_groups` | **Source:** `stepxmlclient/rest_client/operations/data_type_groups.py`

Read-only access to STEP Data Type Groups and their member types.

## Operations

| Method | Signature | Description |
|--------|-----------|-------------|
| `get_data_type_group` | `(group_id) -> DataTypeGroupResponse` | Get group by ID |
| `get_data_type_group_children` | `(group_id) -> list[str]` | Child group IDs |
| `get_data_type_group_attributes` | `(group_id) -> list[dict]` | Attributes in group |
| `get_data_type_group_data_container_types` | `(group_id) -> list[dict]` | DC types in group |
| `get_data_type_group_reference_types` | `(group_id) -> list[dict]` | Reference types in group |




