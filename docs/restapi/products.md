# Products

> **Operation group:** `client.products` | **Source:** `stepxmlclient/rest_client/operations/products.py`

Full CRUD, search, children, data containers, approval, values, and lifecycle management for STEP products.

## Operations

### CRUD

| Method | Signature | Description |
|--------|-----------|-------------|
| `get_product` | `(product_id, key_id=None, include_inherited_data=False) -> ProductResponse` | Retrieve a product by ID or key |
| `search_products` | `(condition: dict) -> ProductListResponse` | Search via `queryProducts` with STEP condition object |
| `create_product` | `(product_data: ProductCreateRequest) -> ProductResponse` | Create with auto-generated ID |
| `replace_product` | `(product_id, product_data, key_id=None, allow_overwrite=False) -> ProductResponse` | Full replace (PUT) — creates if absent |
| `update_product` | `(product_id, updates: ProductUpdateRequest, key_id=None) -> ProductResponse` | Partial update (PATCH) |
| `delete_product` | `(product_id, key_id=None) -> bool` | Delete (moves to recycle bin) |

### Children & Data Containers

| Method | Signature | Description |
|--------|-----------|-------------|
| `get_product_children` | `(product_id, key_id=None) -> list[str]` | Immediate child IDs |
| `get_product_data_containers` | `(product_id, key_id=None) -> dict` | Data containers |

### Values

| Method | Signature | Description |
|--------|-----------|-------------|
| `get_product_value` | `(product_id, attribute_id, key_id=None) -> dict` | Get a single attribute value |
| `replace_product_value` | `(product_id, attribute_id, value, key_id=None) -> dict` | Replace an attribute value |
| `delete_product_value` | `(product_id, attribute_id, key_id=None) -> bool` | Delete an attribute value |

### Approval & Lifecycle

| Method | Signature | Description |
|--------|-----------|-------------|
| `get_product_approval_status` | `(product_id, key_id=None) -> dict` | Get approval status |
| `approve_product` | `(product_id, key_id=None) -> dict` | Approve |
| `approve_product_deletion` | `(product_id, key_id=None) -> dict` | Approve deletion |
| `purge_product` | `(product_id, key_id=None) -> dict` | Purge from recycle bin |

### Convenience

| Method | Signature | Description |
|--------|-----------|-------------|
| `search_by_type` | `(user_type_id) -> ProductListResponse` | Filter by object type |
| `search_by_id` | `(product_id) -> ProductListResponse` | Filter by ID condition |


## Examples

### Create and retrieve a product
```python
from stepxmlclient.rest_client import StepRestClient
from stepxmlclient.rest_client.models.product import ProductCreateRequest

client = StepRestClient("https://step.example.com/restapiv2", auth, context="Context1")

# Create
created = client.products.create_product(ProductCreateRequest(
    objectType="SalesItem",
    parent="SalesItemRoot",
    name="Widget Pro"
))

# Read
product = client.products.get_product(created.id)

# Update
from stepxmlclient.rest_client.models.product import ProductUpdateRequest
client.products.update_product(created.id, ProductUpdateRequest(name="Widget Ultra"))

# Delete
client.products.delete_product(created.id)
```

### Set attribute value
```python
client.products.replace_product_value("P123", "Description", {
    "value": "A premium widget"
})
```

### Search by type
```python
results = client.products.search_by_type("SalesItem")
for p in results.items:
    print(p.id, p.name)
```


