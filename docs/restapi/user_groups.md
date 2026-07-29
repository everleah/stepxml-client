# User Groups

> **Operation group:** `client.user_groups` | **Source:** `stepxmlclient/rest_client/operations/user_groups.py`

Full CRUD, member listing, and hierarchy access for STEP user groups.

## Operations

| Method | Signature | Description |
|--------|-----------|-------------|
| `get_user_group` | `(group_id) -> UserGroupResponse` | Get group by ID |
| `create_or_replace_user_group` | `(group_id, data) -> UserGroupResponse` | Create or full replace |
| `update_user_group` | `(group_id, data) -> UserGroupResponse` | Partial update |
| `delete_user_group` | `(group_id) -> bool` | Delete |
| `get_user_group_users` | `(group_id) -> list[dict]` | List members |
| `get_user_group_children` | `(group_id) -> list[str]` | Child group IDs |




