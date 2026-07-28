"""Event processor models for STEP REST API v2."""

from typing import Any, Optional
from pydantic import BaseModel, ConfigDict


class EventProcessorResponse(BaseModel):
    """STEP event processor (summary/details)."""
    model_config = ConfigDict(extra="allow")

    id: str
    name: Optional[str] = None
    user: Optional[str] = None
    values: Optional[dict[str, Any]] = None
