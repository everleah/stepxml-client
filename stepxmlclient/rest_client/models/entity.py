"""Entity model classes for STEP REST API v2."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class EntityResponse(BaseModel):
    """Response from entity GET/POST operation."""

    id: str = Field(..., description="Entity ID")
    objectType: Optional[str] = Field(None, description="Entity object type ID")
    name: Optional[str] = Field(None, description="Entity name")
    parent: Optional[str] = Field(None, description="Parent entity ID")
    values: Optional[Dict[str, Any]] = Field(None, description="Attribute values")
    references: Optional[Dict[str, Any]] = Field(None, description="References")
    attributeLinks: Optional[Dict[str, Any]] = Field(None, description="Attribute links")
    dataContainers: Optional[Dict[str, Any]] = Field(None, description="Data containers")


class EntityListResponse(BaseModel):
    """Response from entity list/search operations."""

    items: List[EntityResponse] = Field(default_factory=list, description="List of entities")
    total: Optional[int] = Field(None, description="Total number of entities")
    limit: Optional[int] = Field(None, description="Result limit")
    offset: Optional[int] = Field(None, description="Result offset")
    hasMore: Optional[bool] = Field(None, description="Whether more results available")


class EntityCreateRequest(BaseModel):
    """Request model for entity creation (POST /entities).

    Object type and a parent entity must be specified. An 'id' must not be supplied.
    An auto ID pattern must be configured for the object type.
    """

    objectType: str = Field(..., description="Entity object type ID (required)")
    parent: str = Field(..., description="Parent entity ID (required)")
    name: Optional[str] = Field(None, description="Entity name")
    values: Optional[Dict[str, Any]] = Field(None, description="Attribute values")
    references: Optional[Dict[str, Any]] = Field(None, description="References")
    attributeLinks: Optional[Dict[str, Any]] = Field(None, description="Attribute links")
    dataContainers: Optional[Dict[str, Any]] = Field(None, description="Data containers")


class EntityUpdateRequest(BaseModel):
    """Request model for entity updates (PATCH /entities/{id})."""

    name: Optional[str] = Field(None, description="Updated entity name")
    parent: Optional[str] = Field(None, description="Updated parent entity ID")
    values: Optional[Dict[str, Any]] = Field(None, description="Updated attribute values")
    references: Optional[Dict[str, Any]] = Field(None, description="Updated references")
    attributeLinks: Optional[Dict[str, Any]] = Field(None, description="Updated attribute links")
    dataContainers: Optional[Dict[str, Any]] = Field(None, description="Updated data containers")


class EntityRelationshipResponse(BaseModel):
    """Response from entity references operations."""

    id: Optional[str] = Field(None, description="Entity ID")
    references: Optional[Dict[str, Any]] = Field(None, description="References data")
    total: Optional[int] = Field(None, description="Total number of references")
