# Gateway Integration Endpoints

> **Operation group:** `client.gateway` | **Source:** `stepxmlclient/rest_client/operations/gateway.py`

Manage STEP Gateway Integration Endpoints.

## Operations

| Method | Signature | Description |
|--------|-----------|-------------|
| `get_gateway_endpoints` | `() -> list[dict]` | List all gateway endpoints |
| `get_gateway_endpoint` | `(ep_id) -> dict` | Get details |
| `get_gateway_endpoint_status` | `(ep_id) -> dict` | Get status |
| `enable_gateway_endpoint` | `(ep_id) -> dict` | Enable |
| `disable_gateway_endpoint` | `(ep_id) -> dict` | Disable |




