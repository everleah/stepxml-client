"""Collection and collection group models for STEP REST API v2."""

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class CollectionResponse(BaseModel):
    """STEP collection representation."""
    model_config = ConfigDict(extra="allow")

    id: str
    name: str | None = None
    parent: str | None = None
    values: Optional[dict[str, Any]] = None
    content: Optional[list[dict[str, Any]]] = None


class CollectionGroupResponse(BaseModel):
    """STEP collection group representation."""
    model_config = ConfigDict(extra="allow")

    id: str
    name: str | None = None
    parent: str | None = None
    values: Optional[dict[str, Any]] = None
