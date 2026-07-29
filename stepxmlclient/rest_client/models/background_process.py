"""Background process models for STEP REST API v2."""

from typing import Optional

from pydantic import BaseModel, ConfigDict


class BackgroundProcessResponse(BaseModel):
    """STEP background process status representation."""
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    background_process_type: str | None = None
    description: str | None = None
    user: str | None = None
    status: str | None = None
    created: str | None = None
    started: str | None = None
    ended: str | None = None
    execution_time_millis: Optional[float] = None
    number_of_warnings: Optional[int] = None
    number_of_errors: Optional[int] = None
    progress: Optional[int] = None
