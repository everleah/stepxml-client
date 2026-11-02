"""Background process models for STEP REST API v2."""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class BackgroundProcessResponse(BaseModel):
    """STEP background process status representation."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    background_process_type: str | None = Field(default=None, alias="backgroundProcessType")
    description: str | None = None
    user: str | None = None
    status: str | None = None
    created: str | None = None
    started: str | None = None
    ended: str | None = None
    execution_time_millis: Optional[float] = Field(default=None, alias="executionTimeMillis")
    number_of_warnings: Optional[int] = Field(default=None, alias="numberOfWarnings")
    number_of_errors: Optional[int] = Field(default=None, alias="numberOfErrors")
    progress: Optional[int] = None
