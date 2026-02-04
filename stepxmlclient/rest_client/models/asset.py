"""Asset-related REST API models.

Provides Pydantic models for asset data, binary content, and CRUD operations.
"""

from typing import Optional, Any, List, Dict, BinaryIO
from pydantic import BaseModel, Field, ConfigDict


class AssetKeyValue(BaseModel):
    """Key-value pair for asset identification.
    
    Attributes:
        key: Key name (e.g., "Usage", "Reference")
        value: Key value
    """
    
    key: str = Field(..., description="Key name")
    value: str = Field(..., description="Key value")


class AssetMetadata(BaseModel):
    """Asset file metadata.
    
    Attributes:
        filename: Original filename
        mime_type: MIME type (e.g., "image/jpeg")
        size: File size in bytes
        creation_date: Upload/creation timestamp
        modification_date: Last modification timestamp
        checksum: File checksum for integrity verification
    """
    
    filename: Optional[str] = Field(None, description="Original filename")
    mime_type: Optional[str] = Field(None, description="MIME type")
    size: Optional[int] = Field(None, ge=0, description="File size in bytes")
    creation_date: Optional[str] = Field(None, description="Creation timestamp")
    modification_date: Optional[str] = Field(None, description="Modification timestamp")
    checksum: Optional[str] = Field(None, description="File checksum")


class AssetResponse(BaseModel):
    """Single asset response data.
    
    Attributes:
        id: Asset ID
        user_type_id: Asset type/classification
        name: Asset name/description
        key_values: Asset identification key-values
        attributes: Asset-specific attributes
        metadata: File metadata
        created_date: Asset creation date
        modified_date: Last modification date
        version: Asset version number
    """
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "ASSET123",
                "user_type_id": "Image",
                "name": "Product Image",
                "key_values": [{"key": "Usage", "value": "ProductImage"}],
                "metadata": {
                    "filename": "product.jpg",
                    "mime_type": "image/jpeg",
                    "size": 102400
                },
                "created_date": "2024-01-01T00:00:00Z",
                "modified_date": "2024-02-04T10:00:00Z",
                "version": 1
            }
        }
    )
    
    id: str = Field(..., description="Asset ID")
    user_type_id: Optional[str] = Field(None, description="Asset type/classification")
    name: Optional[str] = Field(None, description="Asset name/description")
    key_values: Optional[List[AssetKeyValue]] = Field(default_factory=list, description="Asset key-values")
    attributes: Optional[Dict[str, Any]] = Field(None, description="Asset attributes")
    metadata: Optional[AssetMetadata] = Field(None, description="File metadata")
    created_date: Optional[str] = Field(None, description="Creation timestamp")
    modified_date: Optional[str] = Field(None, description="Last modification timestamp")
    version: Optional[int] = Field(None, description="Asset version")


class AssetListResponse(BaseModel):
    """Paginated asset list response.
    
    Attributes:
        items: List of AssetResponse objects
        total: Total number of assets
        limit: Items per page
        offset: Current offset
        has_more: Whether more results are available
    """
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "items": [],
                "total": 50,
                "limit": 20,
                "offset": 0,
                "has_more": True
            }
        }
    )
    
    items: List[AssetResponse] = Field(default_factory=list, description="Assets in this page")
    total: Optional[int] = Field(None, ge=0, description="Total number of assets")
    limit: int = Field(20, ge=1, le=1000, description="Items per page")
    offset: int = Field(0, ge=0, description="Current offset")
    has_more: bool = Field(False, description="Whether more results are available")


class AssetSearchRequest(BaseModel):
    """Search request for assets.
    
    Attributes:
        query: Free-text search query
        user_type_id: Filter by asset type
        modified_since: Only assets modified after this date (ISO 8601)
        limit: Max results to return
        offset: Result offset for pagination
        include_metadata: Whether to include metadata
        include_content: Whether to include binary content reference
    """
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "query": "*",
                "limit": 20,
                "offset": 0,
                "include_metadata": True
            }
        }
    )
    
    query: str = Field("*", description="Free-text search query")
    user_type_id: Optional[str] = Field(None, description="Filter by asset type")
    modified_since: Optional[str] = Field(None, description="ISO 8601 timestamp filter")
    limit: int = Field(20, ge=1, le=1000, description="Max results")
    offset: int = Field(0, ge=0, description="Result offset")
    include_metadata: bool = Field(True, description="Include metadata")
    include_content: bool = Field(False, description="Include content reference")


class AssetCreateRequest(BaseModel):
    """Request to create a new asset.
    
    Attributes:
        id: Asset ID (required)
        user_type_id: Asset type/classification
        name: Asset name/description
        key_values: Asset identification key-values
        attributes: Asset attributes
    """
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "NEWASSET123",
                "user_type_id": "Image",
                "name": "New Asset",
                "key_values": [{"key": "Usage", "value": "ProductImage"}]
            }
        }
    )
    
    id: str = Field(..., description="Asset ID")
    user_type_id: Optional[str] = Field(None, description="Asset type/classification")
    name: Optional[str] = Field(None, description="Asset name/description")
    key_values: Optional[List[AssetKeyValue]] = Field(None, description="Asset key-values")
    attributes: Optional[Dict[str, Any]] = Field(None, description="Asset attributes")


class AssetUpdateRequest(BaseModel):
    """Request to update an existing asset.
    
    Attributes:
        name: Updated asset name/description
        key_values: Updated key-values
        attributes: Updated attributes
        user_type_id: Updated asset type
    """
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Updated Asset Name",
                "user_type_id": "Image"
            }
        }
    )
    
    name: Optional[str] = Field(None, description="Updated asset name")
    user_type_id: Optional[str] = Field(None, description="Updated asset type")
    key_values: Optional[List[AssetKeyValue]] = Field(None, description="Updated key-values")
    attributes: Optional[Dict[str, Any]] = Field(None, description="Updated attributes")


class AssetUploadRequest(BaseModel):
    """Request to upload asset binary content.
    
    Attributes:
        filename: Filename for the uploaded content
        mime_type: MIME type of the content (e.g., "image/jpeg")
        file_path: Local file path (used in API calls, not in model)
        description: Optional description of the upload
    """
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "filename": "product.jpg",
                "mime_type": "image/jpeg",
                "description": "Product catalog image"
            }
        }
    )
    
    filename: str = Field(..., description="Filename for uploaded content")
    mime_type: str = Field(..., description="MIME type")
    description: Optional[str] = Field(None, description="Upload description")


class AssetDownloadResponse(BaseModel):
    """Response for asset binary download.
    
    Attributes:
        asset_id: Asset ID being downloaded
        filename: Downloaded filename
        size: File size in bytes
        mime_type: MIME type of content
        content_url: URL to download content (if applicable)
        expires_at: Expiration time of download URL (if applicable)
    """
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "asset_id": "ASSET123",
                "filename": "product.jpg",
                "size": 102400,
                "mime_type": "image/jpeg"
            }
        }
    )
    
    asset_id: str = Field(..., description="Asset ID")
    filename: Optional[str] = Field(None, description="Downloaded filename")
    size: Optional[int] = Field(None, ge=0, description="File size in bytes")
    mime_type: Optional[str] = Field(None, description="MIME type")
    content_url: Optional[str] = Field(None, description="Download URL")
    expires_at: Optional[str] = Field(None, description="URL expiration time")
