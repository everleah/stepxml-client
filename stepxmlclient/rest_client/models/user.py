"""User and user group models for STEP REST API v2."""

from typing import Any, Optional
from pydantic import BaseModel, ConfigDict


class UserResponse(BaseModel):
    """STEP user representation."""
    model_config = ConfigDict(extra="allow")

    id: str
    name: Optional[str] = None
    email: Optional[str] = None
    deactivated: Optional[bool] = None
    values: Optional[dict[str, Any]] = None
    user_groups: Optional[list[str]] = None


class UserGroupResponse(BaseModel):
    """STEP user group representation."""
    model_config = ConfigDict(extra="allow")

    id: str
    parent_id: Optional[str] = None
    name: Optional[str] = None
    vendor_root: Optional[str] = None
    values: Optional[dict[str, Any]] = None
