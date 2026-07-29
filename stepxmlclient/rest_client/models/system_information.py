"""System information model for STEP REST API v2."""

from pydantic import BaseModel, ConfigDict


class SystemInformationResponse(BaseModel):
    """System information returned by GET /system-information."""
    model_config = ConfigDict(extra="allow")

    customer_name: str | None = None
    system_name: str | None = None
