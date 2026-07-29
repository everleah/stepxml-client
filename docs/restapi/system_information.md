# System Information

> **Operation group:** `client.system_information` | **Source:** `stepxmlclient/rest_client/operations/system_information.py`

Retrieve STEP system metadata.

## Operations

| Method | Signature | Description |
|--------|-----------|-------------|
| `get_system_information` | `() -> SystemInformationResponse` | Get system info (customerName, systemName) |


## Example
```python
info = client.system_information.get_system_information()
print(info.customer_name, info.system_name)
```


