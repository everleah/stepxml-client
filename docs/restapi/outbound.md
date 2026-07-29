# Outbound Integration Endpoints

> **Operation group:** `client.outbound` | **Source:** `stepxmlclient/rest_client/operations/outbound.py`

Manage STEP Outbound Integration Endpoints (OIEP) — enable/disable, monitor, execute.

## Operations

| Method | Signature | Description |
|--------|-----------|-------------|
| `get_outbound_endpoints` | `() -> list[dict]` | List all outbound endpoints |
| `get_outbound_endpoint` | `(ep_id) -> dict` | Get details |
| `get_outbound_endpoint_status` | `(ep_id) -> dict` | Get status |
| `get_outbound_endpoint_execution_report` | `(ep_id) -> list[dict]` | Execution report |
| `enable_outbound_endpoint` | `(ep_id) -> dict` | Enable |
| `disable_outbound_endpoint` | `(ep_id) -> dict` | Disable |




