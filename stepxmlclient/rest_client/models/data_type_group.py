"""Data type group model for STEP REST API v2."""

from typing import Any

from pydantic import BaseModel, ConfigDict


class DataTypeGroupResponse(BaseModel):
    """STEP data type group representation."""
    model_config = ConfigDict(extra="allow")

    id: str
    name: str | None = None
    parent: str | None = None
    values: dict[str, Any] | None = None
