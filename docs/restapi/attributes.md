# Attributes & Type Definitions

> **Operation group:** `client.attributes` | **Source:** `stepxmlclient/rest_client/operations/attributes.py`

Read-only GET access for attributes, List of Values, and STEP type definitions.

> **Important:** The STEP REST API v2 only provides read access for these resources. There is no create, update, or delete for attributes via the REST API.

## Operations

### Attributes

| Method | Signature | Description |
|--------|-----------|-------------|
| `get_attribute` | `(attribute_id) -> AttributeResponse` | Get attribute definition by ID |

### Lists of Values

| Method | Signature | Description |
|--------|-----------|-------------|
| `get_list_of_values` | `(lov_id) -> ListOfValueResponse` | Get LOV definition |
| `get_list_of_values_entries` | `(lov_id) -> list[dict]` | Get LOV value entries |

### Type Definitions

| Method | Signature | Description |
|--------|-----------|-------------|
| `get_data_container_type` | `(type_id) -> dict` | Data container type |
| `get_data_type_group` | `(group_id) -> dict` | Data type group |
| `get_object_type` | `(type_id) -> dict` | Object type definition |
| `get_object_type_children` | `(type_id) -> list[str]` | Child object types |
| `get_reference_type` | `(reference_type_id) -> dict` | Reference type definition |
| `get_unit` | `(unit_id) -> dict` | Unit definition |
| `get_unique_key` | `(key_id) -> dict` | Unique key definition |


## Example
```python
attr = client.attributes.get_attribute("Description")
lov = client.attributes.get_list_of_values("ColorLOV")
entries = client.attributes.get_list_of_values_entries("ColorLOV")
obj_type = client.attributes.get_object_type("SalesItem")
children = client.attributes.get_object_type_children("SalesItem")
```


