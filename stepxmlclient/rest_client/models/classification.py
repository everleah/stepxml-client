"""Classification-related data models for STEP REST API v2."""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

from .common import PageInfo


class ClassificationValue(BaseModel):
    """Represents a value/item in a classification."""
    
    id: str = Field(..., description="Value ID")
    name: Optional[str] = Field(None, description="Display name")
    description: Optional[str] = Field(None, description="Value description")
    parent_id: Optional[str] = Field(None, description="Parent value ID for hierarchies")
    is_leaf: bool = Field(False, description="Whether this is a leaf node")


class ClassificationMetadata(BaseModel):
    """Metadata about a classification."""
    
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    created_by: Optional[str] = Field(None, description="Creator user")
    modified_at: Optional[datetime] = Field(None, description="Last modification timestamp")
    modified_by: Optional[str] = Field(None, description="Last modifier user")
    version: Optional[int] = Field(None, description="Version number")


class ClassificationResponse(BaseModel):
    """Response model for a single classification."""
    
    id: str = Field(..., description="Classification ID")
    name: str = Field(..., description="Classification name")
    description: Optional[str] = Field(None, description="Classification description")
    classification_type: Optional[str] = Field(None, description="Type of classification")
    is_hierarchical: bool = Field(False, description="Whether classification has hierarchy")
    is_system_owned: bool = Field(False, description="Whether this is a system classification")
    values_count: Optional[int] = Field(None, description="Number of values in classification")
    metadata: Optional[ClassificationMetadata] = Field(None, description="Metadata")
    attributes: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Custom attributes")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "CLASS123",
                "name": "Color",
                "description": "Product color classification",
                "classification_type": "Standard",
                "is_hierarchical": False,
                "is_system_owned": False,
                "values_count": 12,
                "metadata": {
                    "created_at": "2025-01-15T10:30:00Z",
                    "created_by": "admin",
                    "modified_at": "2025-01-20T14:45:00Z",
                    "modified_by": "editor",
                    "version": 3
                }
            }
        }
    )


class ClassificationListResponse(BaseModel):
    """Response model for classification list with pagination."""
    
    items: List[ClassificationResponse] = Field(default_factory=list, description="Classifications")
    pagination: Optional[PageInfo] = Field(None, description="Pagination info")
    total: int = Field(0, description="Total count")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "items": [
                    {
                        "id": "CLASS1",
                        "name": "Color",
                        "description": "Product colors"
                    }
                ],
                "pagination": {
                    "limit": 20,
                    "offset": 0,
                    "total": 42
                },
                "total": 42
            }
        }
    )


class ClassificationHierarchyNode(BaseModel):
    """Single node in a classification hierarchy."""

    id: Optional[str] = Field(None, description="Node ID")
    name: Optional[str] = Field(None, description="Node name")
    parent_id: Optional[str] = Field(None, description="Parent node ID")
    level: Optional[int] = Field(None, description="Depth level in hierarchy")
    children: Optional[List['ClassificationHierarchyNode']] = Field(
        None,
        description="Child nodes"
    )
    metadata: Optional[ClassificationMetadata] = Field(None, description="Node metadata")


class ClassificationHierarchyResponse(BaseModel):
    """Response model for classification hierarchy / children list.

    The STEP REST API spec defines ``getClassificationChildren`` as returning an
    ``array``.  This model is a convenience wrapper used when the raw list is
    wrapped in a dict, or when the caller wants a typed container.
    All fields are optional to match the spec's ``required: []`` philosophy.
    """

    classification_id: Optional[str] = Field(None, description="Classification ID")
    classification_name: Optional[str] = Field(None, description="Classification name")
    root_nodes: Optional[List[ClassificationHierarchyNode]] = Field(
        None,
        description="Root nodes of hierarchy"
    )
    total_nodes: Optional[int] = Field(None, description="Total nodes in hierarchy")
    max_depth: Optional[int] = Field(None, description="Maximum depth of hierarchy")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "classification_id": "CLASS123",
                "classification_name": "Organization",
                "root_nodes": [],
                "total_nodes": 0,
                "max_depth": 0
            }
        }
    )


class ClassificationSearchRequest(BaseModel):
    """Request model for classification search."""
    
    query: str = Field("*", description="Search query string")
    limit: int = Field(20, ge=1, le=500, description="Result limit")
    offset: int = Field(0, ge=0, description="Result offset")
    type_filter: Optional[str] = Field(None, description="Filter by classification type")
    include_values: bool = Field(False, description="Include classification values")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "query": "color",
                "limit": 20,
                "offset": 0,
                "type_filter": "Standard",
                "include_values": False
            }
        }
    )


class ClassificationCreateRequest(BaseModel):
    """Request model for creating a classification."""
    
    id: str = Field(..., description="Classification ID")
    name: str = Field(..., description="Classification name")
    description: Optional[str] = Field(None, description="Classification description")
    classification_type: Optional[str] = Field(None, description="Type of classification")
    is_hierarchical: bool = Field(False, description="Whether classification has hierarchy")
    attributes: Optional[Dict[str, Any]] = Field(None, description="Custom attributes")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "NEW_CLASS",
                "name": "Brand",
                "description": "Product brand classification",
                "classification_type": "Standard",
                "is_hierarchical": False,
                "attributes": {}
            }
        }
    )


class ClassificationUpdateRequest(BaseModel):
    """Request model for updating a classification."""
    
    name: Optional[str] = Field(None, description="Updated name")
    description: Optional[str] = Field(None, description="Updated description")
    classification_type: Optional[str] = Field(None, description="Updated type")
    attributes: Optional[Dict[str, Any]] = Field(None, description="Updated attributes")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Updated Brand Name",
                "description": "Updated description",
                "attributes": {"key": "value"}
            }
        }
    )


class ClassificationValueResponse(BaseModel):
    """Response model for classification values."""
    
    classification_id: str = Field(..., description="Parent classification ID")
    values: List[ClassificationValue] = Field(default_factory=list, description="Classification values")
    total: int = Field(0, description="Total value count")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "classification_id": "CLASS123",
                "values": [
                    {
                        "id": "VAL1",
                        "name": "Red",
                        "description": "Red color"
                    }
                ],
                "total": 12
            }
        }
    )
