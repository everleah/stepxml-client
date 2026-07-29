# Batch Operations

> **Operation group:** `client.batch` | **Source:** `stepxmlclient/rest_client/operations/batch.py`

Execute multiple STEP REST operations in a single request.

## Operations

| Method | Signature | Description |
|--------|-----------|-------------|
| `execute_batch_operation` | `(data: dict) -> BatchResponse` | Execute a batch of operations |


## Example
```python
result = client.batch.execute_batch_operation({
    "mode": "LENIENT",
    "operations": [
        {"resource": "/products/P001", "method": "GET"},
        {"resource": "/products/P002", "method": "GET", "queryParameters": {"includeInheritedData": "true"}},
    ]
})
for op_result in result.results:
    print(op_result.resource, op_result.status)
```


