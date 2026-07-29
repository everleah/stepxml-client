"""Context models for STEP REST API v2."""

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class ContextResponse(BaseModel):
    """STEP context representation (Context / ContextDetails)."""
    model_config = ConfigDict(extra="allow")

    id: str
    name: str | None = None
    locale: str | None = None
    dimension_points: Optional[list[str]] = None
    values: Optional[dict[str, Any]] = None
