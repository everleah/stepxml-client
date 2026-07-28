"""Background process models for STEP REST API v2."""

from typing import Optional
from pydantic import BaseModel, ConfigDict


class BackgroundProcessResponse(BaseModel):
    """STEP background process status representation."""
    model_config = ConfigDict(extra="allow")

    id: Optional[str] = None
    background_process_type: Optional[str] = None
    description: Optional[str] = None
    user: Optional[str] = None
    status: Optional[str] = None
    created: Optional[str] = None
    started: Optional[str] = None
    ended: Optional[str] = None
    execution_time_millis: Optional[float] = None
    number_of_warnings: Optional[int] = None
    number_of_errors: Optional[int] = None
    progress: Optional[int] = None
