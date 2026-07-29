# Event Processors

> **Operation group:** `client.event_processors` | **Source:** `stepxmlclient/rest_client/operations/event_processors.py`

Manage STEP event processors — enable/disable, invoke, monitor queues and statistics.

## Operations

| Method | Signature | Description |
|--------|-----------|-------------|
| `get_event_processors` | `() -> list[dict]` | List all event processors |
| `get_event_processor` | `(ep_id) -> EventProcessorResponse` | Get details |
| `get_event_processor_status` | `(ep_id) -> dict` | Get status |
| `get_event_processor_execution_report` | `(ep_id) -> list[dict]` | Execution report |
| `get_event_processor_statistics` | `(ep_id) -> dict` | Statistics |
| `enable_event_processor` | `(ep_id) -> dict` | Enable |
| `disable_event_processor` | `(ep_id) -> dict` | Disable |
| `invoke_event_processor` | `(ep_id, data=None) -> dict` | Invoke |
| `get_event_queue_status` | `(ep_id) -> dict` | Queue status |
| `get_event_queue_unread_count` | `(ep_id) -> dict` | Unread event count |
| `enable_event_queue` | `(ep_id) -> dict` | Enable queue |
| `disable_event_queue` | `(ep_id) -> dict` | Disable queue |




