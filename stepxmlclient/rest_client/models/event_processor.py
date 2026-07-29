"""Event processor models for STEP REST API v2."""

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class EventProcessorResponse(BaseModel):
    """STEP event processor (summary/details)."""
    model_config = ConfigDict(extra="allow")

    id: str
    name: str | None = None
    user: str | None = None
    values: Optional[dict[str, Any]] = None
