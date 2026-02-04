"""Import/Export model classes for STEP REST API v2."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class JobProgressResponse(BaseModel):
    """Job progress tracking information."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "totalItems": 1000,
            "processedItems": 750,
            "successfulItems": 745,
            "failedItems": 5,
            "percentComplete": 75
        }
    })
    
    totalItems: Optional[int] = Field(None, description="Total items to process")
    processedItems: Optional[int] = Field(None, description="Items processed so far")
    successfulItems: Optional[int] = Field(None, description="Successfully processed items")
    failedItems: Optional[int] = Field(None, description="Items that failed")
    percentComplete: Optional[float] = Field(None, description="Completion percentage (0-100)")


class JobErrorResponse(BaseModel):
    """Job error details."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "errorCode": "VALIDATION_ERROR",
            "errorMessage": "Invalid attribute value",
            "entityId": "ITEM_123",
            "severity": "ERROR"
        }
    })
    
    errorCode: str = Field(..., description="Error code")
    errorMessage: str = Field(..., description="Error message")
    entityId: Optional[str] = Field(None, description="Entity ID that failed")
    severity: Optional[str] = Field(None, description="Error severity (ERROR, WARNING)")
    timestamp: Optional[str] = Field(None, description="Error timestamp")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")


class JobErrorListResponse(BaseModel):
    """Response containing job errors."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "errors": [{"errorCode": "VALIDATION_ERROR", "errorMessage": "Invalid value"}],
            "totalCount": 5,
            "limit": 20,
            "offset": 0
        }
    })
    
    errors: List[JobErrorResponse] = Field(..., description="List of errors")
    totalCount: Optional[int] = Field(None, description="Total number of errors")
    limit: Optional[int] = Field(None, description="Result limit")
    offset: Optional[int] = Field(None, description="Result offset")


class ImportJobCreateRequest(BaseModel):
    """Request to create an import job."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "entityType": "Product",
            "sourceType": "S3",
            "sourceData": {"bucket": "my-bucket", "key": "products.xml"},
            "updateStrategy": "REPLACE"
        }
    })
    
    entityType: str = Field(..., description="Entity type to import (Product, Asset, Classification, Entity)")
    sourceType: str = Field(..., description="Source type (S3, FTP, LOCAL, REST)")
    sourceData: Dict[str, Any] = Field(..., description="Source data configuration")
    updateStrategy: Optional[str] = Field("REPLACE", description="Update strategy (REPLACE, MERGE, UPSERT)")
    config: Optional[Dict[str, Any]] = Field(None, description="Additional import configuration")


class ImportJobResponse(BaseModel):
    """Response from import job operations."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "jobId": "IMPORT_001",
            "status": "PROCESSING",
            "entityType": "Product",
            "createdAt": "2025-01-01T00:00:00Z",
            "startedAt": "2025-01-01T00:05:00Z",
            "completedAt": None,
            "progress": {"totalItems": 1000, "processedItems": 500}
        }
    })
    
    jobId: str = Field(..., description="Import job ID")
    status: str = Field(..., description="Job status (PENDING, PROCESSING, COMPLETED, FAILED, CANCELLED)")
    entityType: str = Field(..., description="Entity type being imported")
    createdAt: str = Field(..., description="Job creation timestamp")
    startedAt: Optional[str] = Field(None, description="Job start timestamp")
    completedAt: Optional[str] = Field(None, description="Job completion timestamp")
    updateStrategy: Optional[str] = Field(None, description="Update strategy used")
    progress: Optional[JobProgressResponse] = Field(None, description="Job progress")
    errorMessage: Optional[str] = Field(None, description="Error message if failed")
    config: Optional[Dict[str, Any]] = Field(None, description="Job configuration")


class ImportJobListResponse(BaseModel):
    """Response containing list of import jobs."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "jobs": [{"jobId": "IMPORT_001", "status": "COMPLETED", "entityType": "Product"}],
            "totalCount": 100,
            "limit": 20,
            "offset": 0
        }
    })
    
    jobs: List[ImportJobResponse] = Field(..., description="List of import jobs")
    totalCount: int = Field(..., description="Total number of jobs")
    limit: int = Field(..., description="Result limit")
    offset: int = Field(..., description="Result offset")


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
    format: Optional[str] = Field("XML", description="Export format (XML, JSON, CSV)")
    filters: Optional[Dict[str, Any]] = Field(None, description="Export filters")
    config: Optional[Dict[str, Any]] = Field(None, description="Export configuration")


class ExportJobResponse(BaseModel):
    """Response from export job operations."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "jobId": "EXPORT_001",
            "status": "COMPLETED",
            "entityType": "Product",
            "format": "XML",
            "createdAt": "2025-01-01T00:00:00Z",
            "completedAt": "2025-01-01T00:10:00Z",
            "downloadUrl": "https://api.example.com/exports/EXPORT_001/download"
        }
    })
    
    jobId: str = Field(..., description="Export job ID")
    status: str = Field(..., description="Job status (PENDING, PROCESSING, COMPLETED, FAILED)")
    entityType: str = Field(..., description="Entity type being exported")
    format: Optional[str] = Field(None, description="Export format")
    createdAt: str = Field(..., description="Job creation timestamp")
    startedAt: Optional[str] = Field(None, description="Job start timestamp")
    completedAt: Optional[str] = Field(None, description="Job completion timestamp")
    progress: Optional[JobProgressResponse] = Field(None, description="Job progress")
    downloadUrl: Optional[str] = Field(None, description="URL to download exported data")
    fileSize: Optional[int] = Field(None, description="Size of exported file in bytes")
    errorMessage: Optional[str] = Field(None, description="Error message if failed")


class ExportJobListResponse(BaseModel):
    """Response containing list of export jobs."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "jobs": [{"jobId": "EXPORT_001", "status": "COMPLETED", "entityType": "Product", "format": "XML"}],
            "totalCount": 50,
            "limit": 20,
            "offset": 0
        }
    })
    
    jobs: List[ExportJobResponse] = Field(..., description="List of export jobs")
    totalCount: int = Field(..., description="Total number of jobs")
    limit: int = Field(..., description="Result limit")
    offset: int = Field(..., description="Result offset")

