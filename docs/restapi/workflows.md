# Workflows

> **Operation group:** `client.workflows` | **Source:** `stepxmlclient/rest_client/operations/workflows.py`

List, inspect, and manage STEP workflow definitions and instances.

## Operations

| Method | Signature | Description |
|--------|-----------|-------------|
| `get_workflow_ids` | `() -> list[str]` | List all workflow IDs |
| `get_workflow` | `(workflow_id) -> WorkflowResponse` | Get workflow definition |
| `create_workflow_instance` | `(workflow_id, data) -> dict` | Create a workflow instance |
| `delete_workflow_instance` | `(workflow_id, instance_id) -> bool` | Delete an instance |




