# Background Processes

> **Operation group:** `client.background_processes` | **Source:** `stepxmlclient/rest_client/operations/background_processes.py`

Monitor STEP background processes (exports, imports, and other async jobs).

## Operations

### Process Monitoring

| Method | Signature | Description |
|--------|-----------|-------------|
| `get_background_process` | `(process_id) -> BackgroundProcessResponse` | Get process status |
| `get_execution_report` | `(process_id) -> list[dict]` | Get execution report |
| `get_attachments_metadata` | `(process_id) -> list[dict]` | List attachments |
| `get_attachment_metadata` | `(process_id, attachment_id) -> dict` | Get attachment details |
| `get_attachment_content` | `(process_id, attachment_id) -> bytes` | Download attachment content |

### Process Types

| Method | Signature | Description |
|--------|-----------|-------------|
| `get_process_types` | `() -> list[dict]` | List available process types |
| `get_processes_of_type` | `(type_id) -> list[dict]` | List processes of a type |


## Example
```python
# Check export progress
proc = client.background_processes.get_background_process("BGP_123")
if proc.status == "succeeded":
    report = client.background_processes.get_execution_report("BGP_123")
    for entry in report:
        print(entry.get("summary"))

# Download result attachment
content = client.background_processes.get_attachment_content("BGP_123", "ATT_1")
with open("result.zip", "wb") as f:
    f.write(content)
```


