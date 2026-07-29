"""Workflow and workflow task models for STEP REST API v2."""

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class WorkflowResponse(BaseModel):
    """STEP workflow definition."""
    model_config = ConfigDict(extra="allow")

    id: str
    name: str | None = None
    valid_object_types: Optional[list[str]] = None


class WorkflowTaskResponse(BaseModel):
    """STEP workflow task."""
    model_config = ConfigDict(extra="allow")

    id: str
    node: Optional[dict[str, Any]] = None
    workflow: str | None = None
    state: str | None = None
    user_assignee: str | None = None
    group_assignee: str | None = None
    deadline: str | None = None
    status_flag: Optional[dict[str, Any]] = None
    task_creation_time: str | None = None
    instance: str | None = None
