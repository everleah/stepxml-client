# Exports & Imports

> **Operation group:** `client.exports` | **Source:** `stepxmlclient/rest_client/operations/exports.py`

Trigger STEP exports and imports using pre-configured export/import configurations.

Both operations return a `BackgroundProcessResponse` that can be monitored via `background_processes`.

## Operations

| Method | Signature | Description |
|--------|-----------|-------------|
| `create_export_job` | `(export_configuration_id, data=None, use_request_context_workspace=None) -> BackgroundProcessResponse` | Trigger an export |
| `create_import_job` | `(import_configuration_id, data=None, process_description=None) -> BackgroundProcessResponse` | Trigger an import |


## Example
```python
# Trigger an export
process = client.exports.create_export_job("MyExportConfig")

# Monitor progress
status = client.background_processes.get_background_process(process.id)
print(status.status, status.progress)
```


