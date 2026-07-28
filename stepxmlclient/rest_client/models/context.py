"""Context models for STEP REST API v2."""

from typing import Any, Optional
from pydantic import BaseModel, ConfigDict


class ContextResponse(BaseModel):
    """STEP context representation (Context / ContextDetails)."""
    model_config = ConfigDict(extra="allow")

    id: str
    name: Optional[str] = None
    locale: Optional[str] = None
    dimension_points: Optional[list[str]] = None
    values: Optional[dict[str, Any]] = None
