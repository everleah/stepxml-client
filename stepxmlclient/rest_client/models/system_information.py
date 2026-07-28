"""System information model for STEP REST API v2."""

from typing import Optional
from pydantic import BaseModel, ConfigDict


class SystemInformationResponse(BaseModel):
    """System information returned by GET /system-information."""
    model_config = ConfigDict(extra="allow")

    customer_name: Optional[str] = None
    system_name: Optional[str] = None
