"""Metadata model classes for STEP REST API v2."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class SystemMetadataResponse(BaseModel):
    """System metadata and capabilities information."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "version": "2.0.1",
            "apiVersion": "2.0",
            "capabilities": ["Products", "Assets", "Classifications"],
            "maxPageSize": 500,
            "defaultPageSize": 20
        }
    })
    
    version: str = Field(..., description="STEP system version")
    apiVersion: str = Field(..., description="REST API version")
    capabilities: List[str] = Field(..., description="Available API capabilities")
    maxPageSize: Optional[int] = Field(None, description="Maximum allowed page size")
    defaultPageSize: Optional[int] = Field(None, description="Default page size")
    supportedLanguages: Optional[List[str]] = Field(None, description="Supported languages")


class ContextResponse(BaseModel):
    """Context definition response."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "id": "Context1",
            "name": "Primary Context",
            "description": "Main data context",
            "isDefault": True,
            "type": "Basic"
        }
    })
    
    id: str = Field(..., description="Context ID")
    name: str = Field(..., description="Context name")
    description: Optional[str] = Field(None, description="Context description")
    type: Optional[str] = Field(None, description="Context type")
    isDefault: Optional[bool] = Field(False, description="Is default context")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class ContextListResponse(BaseModel):
    """Response containing list of contexts."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "items": [{"id": "Context1", "name": "Primary"}],
            "total": 5
        }
    })
    
    items: List[ContextResponse] = Field(..., description="List of contexts")
    total: Optional[int] = Field(None, description="Total number of contexts")


class QualifierResponse(BaseModel):
    """Qualifier definition response."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "id": "Qualifier1",
            "name": "Region",
            "description": "Geographic region qualifier",
            "values": ["EMEA", "APAC", "Americas"]
        }
    })
    
    id: str = Field(..., description="Qualifier ID")
    name: str = Field(..., description="Qualifier name")
    description: Optional[str] = Field(None, description="Qualifier description")
    values: Optional[List[str]] = Field(None, description="Qualifier values")
    type: Optional[str] = Field(None, description="Qualifier type")


class QualifierListResponse(BaseModel):
    """Response containing list of qualifiers."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "items": [{"id": "Qualifier1", "name": "Region"}],
            "total": 10
        }
    })
    
    items: List[QualifierResponse] = Field(..., description="List of qualifiers")
    total: Optional[int] = Field(None, description="Total number of qualifiers")


class DimensionResponse(BaseModel):
    """Dimension definition response."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "id": "Dimension1",
            "name": "Size",
            "description": "Product size dimension",
            "unit": "cm",
            "type": "Numeric"
        }
    })
    
    id: str = Field(..., description="Dimension ID")
    name: str = Field(..., description="Dimension name")
    description: Optional[str] = Field(None, description="Dimension description")
    type: Optional[str] = Field(None, description="Dimension type")
    unit: Optional[str] = Field(None, description="Measurement unit")
    minValue: Optional[float] = Field(None, description="Minimum value")
    maxValue: Optional[float] = Field(None, description="Maximum value")


class DimensionListResponse(BaseModel):
    """Response containing list of dimensions."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "items": [{"id": "Dimension1", "name": "Size"}],
            "total": 15
        }
    })
    
    items: List[DimensionResponse] = Field(..., description="List of dimensions")
    total: Optional[int] = Field(None, description="Total number of dimensions")


class UserTypeResponse(BaseModel):
    """User type definition response."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "id": "UserType1",
            "name": "StandardProduct",
            "description": "Standard product type",
            "applicableEntities": ["Product", "Asset"]
        }
    })
    
    id: str = Field(..., description="User type ID")
    name: str = Field(..., description="User type name")
    description: Optional[str] = Field(None, description="User type description")
    applicableEntities: Optional[List[str]] = Field(None, description="Applicable entity types")


class UserTypeListResponse(BaseModel):
    """Response containing list of user types."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "items": [{"id": "UserType1", "name": "StandardProduct"}],
            "total": 8
        }
    })
    
    items: List[UserTypeResponse] = Field(..., description="List of user types")
    total: Optional[int] = Field(None, description="Total number of user types")


class WorkspaceResponse(BaseModel):
    """Workspace definition response."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "id": "Main",
            "name": "Main Workspace",
            "description": "Primary workspace",
            "isDefault": True
        }
    })
    
    id: str = Field(..., description="Workspace ID")
    name: str = Field(..., description="Workspace name")
    description: Optional[str] = Field(None, description="Workspace description")
    isDefault: Optional[bool] = Field(False, description="Is default workspace")


class WorkspaceListResponse(BaseModel):
    """Response containing list of workspaces."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "items": [{"id": "Main", "name": "Main Workspace"}],
            "total": 3
        }
    })
    
    items: List[WorkspaceResponse] = Field(..., description="List of workspaces")
    total: Optional[int] = Field(None, description="Total number of workspaces")
