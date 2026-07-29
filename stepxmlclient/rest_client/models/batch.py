"""Batch operation models for STEP REST API v2."""

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class OperationRequest(BaseModel):
    """Single operation within a batch."""
    model_config = ConfigDict(extra="allow")

    resource: str
    method: str
    query_parameters: Optional[dict[str, Any]] = None
    body: Optional[dict[str, Any]] = None


class BatchRequest(BaseModel):
    """Batch execution request."""
    model_config = ConfigDict(extra="allow")

    mode: str | None = "LENIENT"
    operations: list[OperationRequest]


class OperationResponse(BaseModel):
    """Single operation result within a batch response."""
    model_config = ConfigDict(extra="allow")

    resource: str | None = None
    method: str | None = None
    status: Optional[int] = None
    body: Optional[dict[str, Any]] = None
    duration: Optional[int] = None


class BatchResponse(BaseModel):
    """Batch execution response."""
    model_config = ConfigDict(extra="allow")

    results: Optional[list[OperationResponse]] = None
