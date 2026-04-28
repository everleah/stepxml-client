"""Asset-related REST API models.

Provides Pydantic models aligned with STEP REST API v2 asset schemas.
"""

from typing import Optional, Any, List, Dict
from pydantic import BaseModel, Field, ConfigDict


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

    Mirrors the REST API Asset schema:
    - objectType/classifications describe placement and type
    - values/references are dynamic maps keyed by ID
    - contentMetadata is read-only metadata returned by STEP
    """
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "ASSET123",
                "objectType": "ProductImage",
                "name": "Product Image",
                "classifications": ["ProductImageRoot"],
                "values": {
                    "AssetKeywords": {
                        "values": [
                            {"value": "TV"},
                            {"value": "Television"}
                        ]
                    }
                },
                "references": {},
                "contentMetadata": {
                    "originalFilename": "product.jpg",
                    "mimeType": "image/jpeg"
                }
            }
        }
    )

    id: str = Field(..., description="Asset ID")
    objectType: Optional[str] = Field(None, description="Object type ID")
    name: Optional[str] = Field(None, description="Asset name/description")
    classifications: Optional[List[str]] = Field(default_factory=list, description="Linked classification IDs")
    values: Optional[Dict[str, Any]] = Field(None, description="Asset values keyed by attribute ID")
    references: Optional[Dict[str, Any]] = Field(None, description="Asset references keyed by reference type ID")
    contentMetadata: Optional[Dict[str, str]] = Field(None, description="Read-only asset content metadata")


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
        object_type: Filter by object type
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
                "object_type": "ProductImage",
                "limit": 20,
                "offset": 0,
                "include_metadata": True
            }
        }
    )
    
    query: str = Field("*", description="Free-text search query")
    object_type: Optional[str] = Field(None, description="Filter by object type")
    modified_since: Optional[str] = Field(None, description="ISO 8601 timestamp filter")
    limit: int = Field(20, ge=1, le=1000, description="Max results")
    offset: int = Field(0, ge=0, description="Result offset")
    include_metadata: bool = Field(True, description="Include metadata")
    include_content: bool = Field(False, description="Include content reference")


class AssetCreateRequest(BaseModel):
    """Request to create a new asset.

    Attributes:
        objectType: Asset object type (required)
        classifications: Classification IDs to link asset into (required, min 1)
        name: Asset name/description
        values: Asset values map keyed by attribute ID
        references: Asset references map keyed by reference/link type ID
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "objectType": "ProductImage",
                "classifications": ["ProductImageRoot"],
                "name": "New Asset",
                "values": {
                    "AssetKeywords": {
                        "values": [{"value": "TV"}]
                    }
                }
            }
        }
    )

    objectType: str = Field(..., description="Object type ID")
    classifications: List[str] = Field(..., min_length=1, description="Parent classification IDs")
    name: Optional[str] = Field(None, description="Asset name/description")
    values: Optional[Dict[str, Any]] = Field(None, description="Asset values")
    references: Optional[Dict[str, Any]] = Field(None, description="Asset references")


class AssetUpdateRequest(BaseModel):
    """Request to update an existing asset.
    
    Attributes:
        name: Updated asset name/description
        classifications: Classifications to add
        values: Updated asset values
        references: Updated references
    """
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Updated Asset Name",
                "classifications": ["ProductImageRoot"],
                "values": {
                    "AssetKeywords": {
                        "values": [{"value": "TV"}]
                    }
                }
            }
        }
    )

    name: Optional[str] = Field(None, description="Updated asset name")
    classifications: Optional[List[str]] = Field(None, description="Classifications to add")
    values: Optional[Dict[str, Any]] = Field(None, description="Values to update")
    references: Optional[Dict[str, Any]] = Field(None, description="References to update")


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
