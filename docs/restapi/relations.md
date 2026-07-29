# Relations (References)

> **Operation group:** `client.relations` | **Source:** `stepxmlclient/rest_client/operations/relations.py`

Manage cross-references between Products, Assets, Classifications, and Entities.

All reference operations require an `entity_type` parameter: `"products"`, `"assets"`, `"classifications"`, or `"entities"`.

## Operations

### Reference CRUD

| Method | Signature | Description |
|--------|-----------|-------------|
| `list_references` | `(entity_type, entity_id, reference_type_id, key_id=None) -> RelationshipListResponse` | List outgoing references of a type |
| `get_reference` | `(entity_type, entity_id, reference_type_id, target_id, ...) -> RelationshipResponse` | Get a single reference |
| `put_reference` | `(entity_type, entity_id, reference_type_id, target_id, data=None, ...) -> RelationshipResponse` | Create or replace a reference |
| `delete_reference` | `(entity_type, entity_id, reference_type_id, target_id, ...) -> bool` | Delete a reference |

### Incoming References

| Method | Signature | Description |
|--------|-----------|-------------|
| `get_incoming_references` | `(entity_type, entity_id, reference_type_id, key_id=None) -> RelationshipListResponse` | List incoming references |

### Type Lookup

| Method | Signature | Description |
|--------|-----------|-------------|
| `get_reference_type` | `(reference_type_id) -> RelationshipTypeResponse` | Get reference type definition |


## Examples

### Create a reference between two products
```python
client.relations.put_reference(
    entity_type="products",
    entity_id="P123",
    reference_type_id="Accessory",
    target_id="P456"
)
```

### List all accessories of a product
```python
refs = client.relations.list_references("products", "P123", "Accessory")
for ref in refs.items:
    print(ref.targetId)
```

### Check who references this product
```python
incoming = client.relations.get_incoming_references("products", "P456", "Accessory")
```


