# Exports & Imports

> **Operation group:** `client.exports` | **Source:** `stepxmlclient/rest_client/operations/exports.py`

Trigger STEP exports and imports using pre-configured export/import configurations.

Both operations return a `BackgroundProcessResponse` containing `id`, not job
status/progress. Monitor that ID via `background_processes`.

Export `data` accepts an `ExportJobCreateRequest` or dictionary with optional
`stepUrls` and `processDescription` (STEP's `ExportSpecification`). Empty bodies
use roots from the server configuration; `data=None` omits the body.
No format or entity type is injected by default. Legacy
`entityType` / `format` / `filters` / `config` fields remain accepted for compatibility,
but are not part of ExportSpecification; configure formats on the server.
Import payloads are sent as binary data.

## Operations

| Method | Signature | Description |
|--------|-----------|-------------|
| `create_export_job` | `(export_configuration_id, data=None, use_request_context_workspace=None) -> BackgroundProcessResponse` | Trigger an export |
| `create_import_job` | `(import_configuration_id, data=None, process_description=None) -> BackgroundProcessResponse` | Trigger an import |


## Example
```python
from stepxmlclient.rest_client.models.import_export import ExportJobCreateRequest

process = client.exports.create_export_job(
    "MyExportConfig",
    ExportJobCreateRequest(
        stepUrls=["step://product?id=P1"],
        processDescription="Export selected product"
    )
)

# Monitor progress
status = client.background_processes.get_background_process(process.id)
print(status.status, status.progress)
```

