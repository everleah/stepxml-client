"""Workflow and workflow task models for STEP REST API v2."""

from typing import Any, Optional
from pydantic import BaseModel, ConfigDict


class WorkflowResponse(BaseModel):
    """STEP workflow definition."""
    model_config = ConfigDict(extra="allow")

    id: str
    name: Optional[str] = None
    valid_object_types: Optional[list[str]] = None


class WorkflowTaskResponse(BaseModel):
    """STEP workflow task."""
    model_config = ConfigDict(extra="allow")

    id: str
    node: Optional[dict[str, Any]] = None
    workflow: Optional[str] = None
    state: Optional[str] = None
    user_assignee: Optional[str] = None
    group_assignee: Optional[str] = None
    deadline: Optional[str] = None
    status_flag: Optional[dict[str, Any]] = None
    task_creation_time: Optional[str] = None
    instance: Optional[str] = None
