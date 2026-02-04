"""Entity model classes for STEP REST API v2."""

from typing import Optional, List, Dict, Any, Generic, TypeVar
from pydantic import BaseModel, Field, ConfigDict


class EntityAttribute(BaseModel):
    """Entity attribute value."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "name": "Description",
            "value": "Product description",
            "type": "Text"
        }
    })
    
    name: str = Field(..., description="Attribute name")
    value: Any = Field(..., description="Attribute value")
    type: Optional[str] = Field(None, description="Attribute type")
    unit: Optional[str] = Field(None, description="Measurement unit")


class EntityMetadata(BaseModel):
    """Entity metadata information."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "createdAt": "2025-01-01T00:00:00Z",
            "modifiedAt": "2025-01-02T00:00:00Z",
            "createdBy": "admin",
            "modifiedBy": "admin",
            "version": 1
        }
    })
    
    createdAt: Optional[str] = Field(None, description="Creation timestamp")
    modifiedAt: Optional[str] = Field(None, description="Last modification timestamp")
    createdBy: Optional[str] = Field(None, description="Creator username")
    modifiedBy: Optional[str] = Field(None, description="Last modifier username")
    version: Optional[int] = Field(None, description="Version number")


class EntityResponse(BaseModel):
    """Response from entity GET operation."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "id": "ENT001",
            "name": "Entity Name",
            "description": "Entity description",
            "type": "Product",
            "attributes": [{"name": "Attr1", "value": "Value1"}],
            "metadata": {"version": 1}
        }
    })
    
    id: str = Field(..., description="Entity ID")
    name: str = Field(..., description="Entity name")
    description: Optional[str] = Field(None, description="Entity description")
    type: Optional[str] = Field(None, description="Entity type")
    attributes: Optional[List[EntityAttribute]] = Field(None, description="Entity attributes")
    relationships: Optional[Dict[str, Any]] = Field(None, description="Entity relationships")
    metadata: Optional[EntityMetadata] = Field(None, description="Entity metadata")


class EntityListResponse(BaseModel):
    """Response from entity list/search operations."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "items": [{"id": "ENT001", "name": "Entity 1"}],
            "total": 100,
            "limit": 20,
            "offset": 0,
            "hasMore": True
        }
    })
    
    items: List[EntityResponse] = Field(..., description="List of entities")
    total: Optional[int] = Field(None, description="Total number of entities")
    limit: Optional[int] = Field(None, description="Result limit")
    offset: Optional[int] = Field(None, description="Result offset")
    hasMore: Optional[bool] = Field(None, description="Whether more results available")


class EntitySearchRequest(BaseModel):
    """Request model for entity search operations."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "query": "Product",
            "type": "Product",
            "limit": 20,
            "offset": 0
        }
    })
    
    query: Optional[str] = Field("*", description="Search query")
    type: Optional[str] = Field(None, description="Filter by entity type")
    limit: Optional[int] = Field(20, description="Result limit")
    offset: Optional[int] = Field(0, description="Result offset")
    attributes: Optional[Dict[str, Any]] = Field(None, description="Attribute filters")


class EntityCreateRequest(BaseModel):
    """Request model for entity creation."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "name": "New Entity",
            "type": "Product",
            "description": "Entity description",
            "attributes": [{"name": "Attr1", "value": "Value1"}]
        }
    })
    
    name: str = Field(..., description="Entity name")
    type: Optional[str] = Field(None, description="Entity type")
    description: Optional[str] = Field(None, description="Entity description")
    attributes: Optional[List[EntityAttribute]] = Field(None, description="Entity attributes")
    relationships: Optional[Dict[str, Any]] = Field(None, description="Entity relationships")


class EntityUpdateRequest(BaseModel):
    """Request model for entity updates."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "name": "Updated Entity",
            "description": "Updated description",
            "attributes": [{"name": "Attr1", "value": "Updated Value"}]
        }
    })
    
    name: Optional[str] = Field(None, description="Updated entity name")
    description: Optional[str] = Field(None, description="Updated description")
    attributes: Optional[List[EntityAttribute]] = Field(None, description="Updated attributes")
    relationships: Optional[Dict[str, Any]] = Field(None, description="Updated relationships")


class EntityRelationship(BaseModel):
    """Entity relationship definition."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "type": "Parent",
            "targetId": "ENT002",
            "targetName": "Parent Entity",
            "metadata": {"createdAt": "2025-01-01T00:00:00Z"}
        }
    })
    
    type: str = Field(..., description="Relationship type")
    targetId: str = Field(..., description="Target entity ID")
    targetName: Optional[str] = Field(None, description="Target entity name")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Relationship metadata")


class EntityRelationshipResponse(BaseModel):
    """Response containing entity relationships."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "id": "ENT001",
            "relationships": [{"type": "Parent", "targetId": "ENT002"}],
            "total": 5
        }
    })
    
    id: str = Field(..., description="Entity ID")
    relationships: List[EntityRelationship] = Field(..., description="List of relationships")
    total: Optional[int] = Field(None, description="Total number of relationships")


class EntityBulkRequest(BaseModel):
    """Request model for bulk entity operations."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "operations": [
                {"operation": "create", "data": {"name": "Entity 1"}},
                {"operation": "update", "id": "ENT001", "data": {"name": "Updated"}}
            ]
        }
    })
    
    operations: List[Dict[str, Any]] = Field(..., description="Bulk operations")


class EntityBulkResponse(BaseModel):
    """Response from bulk entity operations."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "successful": 8,
            "failed": 2,
            "results": [{"id": "ENT001", "status": "success"}]
        }
    })
    
    successful: int = Field(..., description="Number of successful operations")
    failed: int = Field(..., description="Number of failed operations")
    results: Optional[List[Dict[str, Any]]] = Field(None, description="Operation results")
