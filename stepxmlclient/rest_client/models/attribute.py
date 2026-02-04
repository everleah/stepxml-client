"""Attribute model classes for STEP REST API v2."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class AttributeValue(BaseModel):
    """Individual attribute value."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "value": "Blue",
            "context": "Context1",
            "language": "en"
        }
    })
    
    value: Any = Field(..., description="The attribute value")
    context: Optional[str] = Field(None, description="Context for this value")
    language: Optional[str] = Field(None, description="Language code")


class ListOfValueItem(BaseModel):
    """Individual item in a List of Values."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "id": "LOV_ITEM_001",
            "name": "Option 1",
            "description": "First option",
            "sequence": 1
        }
    })
    
    id: str = Field(..., description="LOV item ID")
    name: str = Field(..., description="LOV item name")
    description: Optional[str] = Field(None, description="LOV item description")
    sequence: Optional[int] = Field(None, description="Display sequence")


class ListOfValueResponse(BaseModel):
    """Response containing List of Values items."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "id": "LOV_001",
            "name": "Color LOV",
            "items": [{"id": "LOV_ITEM_001", "name": "Red"}],
            "total": 5
        }
    })
    
    id: str = Field(..., description="LOV ID")
    name: str = Field(..., description="LOV name")
    items: List[ListOfValueItem] = Field(..., description="List of items")
    total: Optional[int] = Field(None, description="Total number of items")


class AttributeMetadata(BaseModel):
    """Metadata about an attribute."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "type": "Text",
            "required": True,
            "multiValued": False,
            "createdAt": "2025-01-01T00:00:00Z",
            "modifiedAt": "2025-01-02T00:00:00Z"
        }
    })
    
    type: str = Field(..., description="Attribute data type (Text, Number, Boolean, etc.)")
    required: Optional[bool] = Field(None, description="Whether attribute is required")
    multiValued: Optional[bool] = Field(None, description="Whether attribute supports multiple values")
    createdAt: Optional[str] = Field(None, description="Creation timestamp")
    modifiedAt: Optional[str] = Field(None, description="Last modification timestamp")


class AttributeResponse(BaseModel):
    """Response from attribute GET operation."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "id": "ATTR_001",
            "name": "Color",
            "type": "Text",
            "required": True,
            "lovId": "LOV_001",
            "metadata": {"type": "Text"}
        }
    })
    
    id: str = Field(..., description="Attribute ID")
    name: str = Field(..., description="Attribute name")
    description: Optional[str] = Field(None, description="Attribute description")
    type: str = Field(..., description="Attribute data type")
    lovId: Optional[str] = Field(None, description="Associated List of Values ID")
    required: Optional[bool] = Field(None, description="Is required")
    multiValued: Optional[bool] = Field(None, description="Supports multiple values")
    metadata: Optional[AttributeMetadata] = Field(None, description="Attribute metadata")


class AttributeListResponse(BaseModel):
    """Response from attribute list/search operations."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "items": [{"id": "ATTR_001", "name": "Color"}],
            "total": 100,
            "limit": 20,
            "offset": 0,
            "hasMore": True
        }
    })
    
    items: List[AttributeResponse] = Field(..., description="List of attributes")
    total: Optional[int] = Field(None, description="Total number of attributes")
    limit: Optional[int] = Field(None, description="Result limit")
    offset: Optional[int] = Field(None, description="Result offset")
    hasMore: Optional[bool] = Field(None, description="Whether more results available")


class AttributeSearchRequest(BaseModel):
    """Request model for attribute search operations."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "query": "Color",
            "type": "Text",
            "limit": 20,
            "offset": 0
        }
    })
    
    query: Optional[str] = Field("*", description="Search query")
    type: Optional[str] = Field(None, description="Filter by attribute type")
    limit: Optional[int] = Field(20, description="Result limit")
    offset: Optional[int] = Field(0, description="Result offset")


class AttributeCreateRequest(BaseModel):
    """Request model for attribute creation."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "name": "Size",
            "type": "Text",
            "required": True,
            "lovId": "LOV_SIZE"
        }
    })
    
    name: str = Field(..., description="Attribute name")
    type: str = Field(..., description="Attribute data type")
    description: Optional[str] = Field(None, description="Attribute description")
    required: Optional[bool] = Field(False, description="Is required")
    multiValued: Optional[bool] = Field(False, description="Supports multiple values")
    lovId: Optional[str] = Field(None, description="Associated List of Values ID")


class AttributeUpdateRequest(BaseModel):
    """Request model for attribute updates."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "description": "Product size attribute",
            "required": True
        }
    })
    
    name: Optional[str] = Field(None, description="Updated attribute name")
    description: Optional[str] = Field(None, description="Updated description")
    required: Optional[bool] = Field(None, description="Updated required flag")
    lovId: Optional[str] = Field(None, description="Updated List of Values ID")
