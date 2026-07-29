# Workflow Tasks

> **Operation group:** `client.workflow_tasks` | **Source:** `stepxmlclient/rest_client/operations/workflow_tasks.py`

Search, claim, release, and trigger events on STEP workflow tasks.

## Operations

| Method | Signature | Description |
|--------|-----------|-------------|
| `search_workflow_tasks` | `(condition) -> dict` | Search tasks |
| `get_workflow_task` | `(task_id) -> WorkflowTaskResponse` | Get task details |
| `claim_workflow_task` | `(task_id) -> dict` | Claim a task |
| `release_workflow_task` | `(task_id) -> dict` | Release a claimed task |
| `get_workflow_task_events` | `(task_id) -> list[dict]` | Get task events |
| `trigger_workflow_task_event` | `(task_id, data) -> dict` | Trigger an event |


## Example
```python
tasks = client.workflow_tasks.search_workflow_tasks({
    "conditionType": "and",
    "conditions": [
        {"conditionType": "status", "status": "In Review"}
    ]
})

for task in tasks.get("items", []):
    client.workflow_tasks.claim_workflow_task(task["id"])
```


