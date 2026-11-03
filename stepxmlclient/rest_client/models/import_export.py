"""Import/Export model classes for STEP REST API v2."""

from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field


class ExportJobCreateRequest(BaseModel):
    """Optional ExportSpecification payload; select format in the server configuration.

    Legacy entityType/format/filters/config fields remain accepted for compatibility.
    """
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "stepUrls": ["step://product?id=P1"],
            "processDescription": "Export selected roots"
        }
    })
    
    stepUrls: Optional[list[str]] = Field(default=None, description="STEP URLs of export roots")
    processDescription: str | None = Field(default=None, description="Export process description")
    entityType: str | None = Field(default=None, description="Legacy entity type")
    format: str | None = Field(default=None, description="Legacy export format")
    filters: Optional[Dict[str, Any]] = Field(default=None, description="Export filters")
    config: Optional[Dict[str, Any]] = Field(default=None, description="Export configuration")


class BackgroundProcessResponse(BaseModel):
    """Response from export/import trigger operations.

    Matches the STEP REST API v2 ``BackgroundProcessIdentification`` schema:
    ``POST /export/{id}`` and ``POST /import/{id}`` both return only the
    background-process ``id`` so the caller can poll for status.
    """

    model_config = ConfigDict(populate_by_name=True, json_schema_extra={
        "example": {"id": "bg-process-0042"}
    })

    id: str | None = Field(default=None, description="Background process ID")


# Backward-compatible alias so existing imports don't break immediately.
ExportJobResponse = BackgroundProcessResponse
