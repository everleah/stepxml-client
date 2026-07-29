# Users

> **Operation group:** `client.users` | **Source:** `stepxmlclient/rest_client/operations/users.py`

Full CRUD, password management, and group assignment for STEP users.

## Operations

| Method | Signature | Description |
|--------|-----------|-------------|
| `get_user` | `(user_id) -> UserResponse` | Get user by ID |
| `create_or_replace_user` | `(user_id, data) -> UserResponse` | Create or full replace |
| `update_user` | `(user_id, data) -> UserResponse` | Partial update |
| `delete_user` | `(user_id) -> bool` | Delete |
| `randomize_password` | `(user_id) -> dict` | Randomize user password |
| `add_user_to_group` | `(user_id, group_data) -> dict` | Add user to group |
| `remove_user_from_group` | `(user_id, group_data) -> dict` | Remove user from group |


## Example
```python
client.users.create_or_replace_user("jdoe", {
    "name": "John Doe",
    "email": "john@example.com"
})
client.users.add_user_to_group("jdoe", {"groupId": "Admins"})
```


