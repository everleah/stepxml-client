"""Integration endpoint models for STEP REST API v2."""

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class IntegrationEndpointResponse(BaseModel):
    """STEP integration endpoint (summary/details) — Inbound, Outbound, Gateway."""
    model_config = ConfigDict(extra="allow")

    id: str
    name: str | None = None
    description: str | None = None
    user: str | None = None
    values: dict[str, Any] | None = None
