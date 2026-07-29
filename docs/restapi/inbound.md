# Inbound Integration Endpoints (IIEP)

> **Operation group:** `client.inbound` | **Source:** `stepxmlclient/rest_client/operations/inbound.py`

Upload STEP-XML documents to configured Inbound Integration Endpoints for processing.

Available on both `StiboStepRestClient` and `StepRestClient`.

## Operations

| Method | Signature | Description |
|--------|-----------|-------------|
| `upload_and_invoke` | `(endpoint_id, xml_data, file_name=None) -> dict` | Upload XML and trigger processing |
| `list_endpoints` | `() -> list[dict]` | List all accessible endpoints |
| `get_status` | `(endpoint_id) -> dict` | Get endpoint status |
| `enable_endpoint` | `(endpoint_id) -> dict` | Enable an endpoint |
| `disable_endpoint` | `(endpoint_id) -> dict` | Disable an endpoint |
| `get_execution_report` | `(endpoint_id) -> list[dict]` | Get execution report |
| `get_statistics` | `(endpoint_id) -> dict` | Get operational statistics |
| `get_worker_processes` | `(endpoint_id, status_filter=None) -> list[str]` | Get background process IDs |


## Examples

### Upload STEP-XML
```python
from stepxmlclient.creator import Creator

creator = Creator(context_id="Context1")
# ... add entities ...
creator.build()
xml_bytes = creator.to_bytes()

result = client.inbound.upload_and_invoke(
    endpoint_id="my_iiep",
    xml_data=xml_bytes,
    file_name="import.xml"
)
```

### Manage endpoints
```python
endpoints = client.inbound.list_endpoints()
for ep in endpoints:
    print(ep["id"], ep.get("name"))

status = client.inbound.get_status("my_iiep")
if not status.get("enabled"):
    client.inbound.enable_endpoint("my_iiep")

report = client.inbound.get_execution_report("my_iiep")
stats = client.inbound.get_statistics("my_iiep")
```

> **Prerequisites:** A configured Inbound Integration Endpoint with a REST-enabled receiver plugin in STEP.

