"""Integration endpoint models for STEP REST API v2."""

from typing import Any, Optional
from pydantic import BaseModel, ConfigDict


class IntegrationEndpointResponse(BaseModel):
    """STEP integration endpoint (summary/details) — Inbound, Outbound, Gateway."""
    model_config = ConfigDict(extra="allow")

    id: str
    name: Optional[str] = None
    description: Optional[str] = None
    user: Optional[str] = None
    values: Optional[dict[str, Any]] = None
