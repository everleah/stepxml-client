"""Classification-related data models for STEP REST API v2."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ClassificationResponse(BaseModel):
    """Response from classification GET/POST operation."""

    id: str = Field(..., description="Classification ID")
    objectType: str | None = Field(None, description="Classification object type ID")
    name: str | None = Field(None, description="Classification name")
    parent: str | None = Field(None, description="Parent classification ID")
    values: Optional[Dict[str, Any]] = Field(None, description="Attribute values")
    references: Optional[Dict[str, Any]] = Field(None, description="References")
    attributeLinks: Optional[Dict[str, Any]] = Field(None, description="Attribute links")
    dataContainers: Optional[Dict[str, Any]] = Field(None, description="Data containers")


class ClassificationListResponse(BaseModel):
    """Response from classification list/search operations."""

    items: List[ClassificationResponse] = Field(default_factory=list, description="List of classifications")
    total: Optional[int] = Field(None, description="Total number of classifications")
    limit: Optional[int] = Field(None, description="Result limit")
    offset: Optional[int] = Field(None, description="Result offset")
    hasMore: Optional[bool] = Field(None, description="Whether more results available")


class ClassificationCreateRequest(BaseModel):
    """Request model for classification creation (POST /classifications).

    Object type and a parent classification must be specified. An 'id' must not be supplied.
    An auto ID pattern must be configured for the object type.
    """

    objectType: str = Field(..., description="Classification object type ID (required)")
    parent: str = Field(..., description="Parent classification ID (required)")
    name: str | None = Field(None, description="Classification name")
    values: Optional[Dict[str, Any]] = Field(None, description="Attribute values")
    references: Optional[Dict[str, Any]] = Field(None, description="References")
    attributeLinks: Optional[Dict[str, Any]] = Field(None, description="Attribute links")
    dataContainers: Optional[Dict[str, Any]] = Field(None, description="Data containers")


class ClassificationUpdateRequest(BaseModel):
    """Request model for classification updates (PATCH /classifications/{id})."""

    name: str | None = Field(None, description="Updated classification name")
    parent: str | None = Field(None, description="Updated parent classification ID")
    values: Optional[Dict[str, Any]] = Field(None, description="Updated attribute values")
    references: Optional[Dict[str, Any]] = Field(None, description="Updated references")
    attributeLinks: Optional[Dict[str, Any]] = Field(None, description="Updated attribute links")
    dataContainers: Optional[Dict[str, Any]] = Field(None, description="Updated data containers")


