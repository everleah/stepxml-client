# Contexts

> **Operation group:** `client.contexts` | **Source:** `stepxmlclient/rest_client/operations/contexts.py`

Query STEP contexts — the dimension-dependent workspaces within a STEP system.

## Operations

| Method | Signature | Description |
|--------|-----------|-------------|
| `get_contexts` | `() -> list[ContextResponse]` | List all contexts |
| `get_context` | `(context_id) -> ContextResponse` | Get a single context by ID |


## Example
```python
ctxs = client.contexts.get_contexts()
for ctx in ctxs:
    print(ctx.id, ctx.name or "(unnamed)")

details = client.contexts.get_context("Context1")
print(details.locale, details.dimension_points)
```


