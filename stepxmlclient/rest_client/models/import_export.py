"""Import/Export model classes for STEP REST API v2."""

from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field


class ExportJobCreateRequest(BaseModel):
    """Request to create an export job."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "entityType": "Product",
            "format": "XML",
            "filters": {"status": "ACTIVE"},
            "config": {"includeRelations": True}
        }
    })
    
    entityType: str = Field(..., description="Entity type to export (Product, Asset, Classification, Entity)")
    format: str | None = Field("XML", description="Export format (XML, JSON, CSV)")
    filters: Optional[Dict[str, Any]] = Field(None, description="Export filters")
    config: Optional[Dict[str, Any]] = Field(None, description="Export configuration")


class BackgroundProcessResponse(BaseModel):
    """Response from export/import trigger operations.

    Matches the STEP REST API v2 ``BackgroundProcessIdentification`` schema:
    ``POST /export/{id}`` and ``POST /import/{id}`` both return only the
    background-process ``id`` so the caller can poll for status.
    """

    model_config = ConfigDict(populate_by_name=True, json_schema_extra={
        "example": {"id": "bg-process-0042"}
    })

    id: str | None = Field(None, description="Background process ID")


# Backward-compatible alias so existing imports don't break immediately.
ExportJobResponse = BackgroundProcessResponse

