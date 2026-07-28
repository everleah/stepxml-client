"""Data type group model for STEP REST API v2."""

from typing import Any, Optional
from pydantic import BaseModel, ConfigDict


class DataTypeGroupResponse(BaseModel):
    """STEP data type group representation."""
    model_config = ConfigDict(extra="allow")

    id: str
    name: Optional[str] = None
    parent: Optional[str] = None
    values: Optional[dict[str, Any]] = None
