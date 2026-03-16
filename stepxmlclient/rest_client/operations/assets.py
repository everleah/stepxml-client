"""Asset operations for STEP REST API.

Provides CRUD, search, and binary content operations for assets.
"""

from typing import Optional, List, Dict, Any, BinaryIO
import logging
import os

import requests_openapi as roa

from ..base import BaseOperation, handle_rest_errors
from ..models.common import PagedResponse, PageInfo
from ..models.asset import (
    AssetResponse,
    AssetListResponse,
    AssetSearchRequest,
    AssetCreateRequest,
    AssetUpdateRequest,
    AssetUploadRequest,
    AssetDownloadResponse,
    AssetKeyValue,
)
from .. import exceptions as exc


class AssetOperations(BaseOperation):
    """Asset CRUD, search, and binary operations.
    
    Provides methods for:
    - Retrieving single assets
    - Searching and listing assets
    - Creating new assets
    - Updating existing assets
    - Deleting assets
    - Uploading binary content
    - Downloading binary content
    """
    
    def __init__(self, client: roa.Client, logger: Optional[logging.Logger] = None):
        """Initialize AssetOperations.
        
        Args:
            client: The requests-openapi Client instance
            logger: Logger instance (optional)
        """
        super().__init__(client, operation_name="AssetOperations", logger=logger)
    
    @handle_rest_errors
    def get_asset(self, asset_id: str,
                 include_metadata: bool = True,
                 include_content_reference: bool = False) -> AssetResponse:
        """Retrieve a single asset by ID.
        
        Args:
            asset_id: The asset ID to retrieve
            include_metadata: Whether to include metadata
            include_content_reference: Whether to include content reference/URL
            
        Returns:
            AssetResponse with asset data
            
        Raises:
            NotFoundError: If asset not found
            RestApiError: For other API errors
        """
        self._validate_required_params(
            {"asset_id": asset_id},
            ["asset_id"]
        )
        
        params = {
            "assetId": asset_id,
            "includeMetadata": include_metadata,
            "includeContentReference": include_content_reference,
        }
        self._log_operation("getAsset", params)
        
        try:
            response = self.client.getAsset(**params)
        except Exception as e:
            if "404" in str(e) or "not found" in str(e).lower():
                raise exc.NotFoundError(asset_id, "Asset")
            raise
        
        # Convert response to AssetResponse if needed
        if isinstance(response, dict):
            return AssetResponse(**response)
        return response
    
    @handle_rest_errors
    def search_assets(self, query: str = "*",
                     user_type_id: Optional[str] = None,
                     modified_since: Optional[str] = None,
                     limit: int = 20,
                     offset: int = 0,
                     include_metadata: bool = True) -> AssetListResponse:
        """Search for assets with optional filters.
        
        Args:
            query: Free-text search query (default: "*" for all)
            user_type_id: Filter by asset type ID
            modified_since: ISO 8601 timestamp - only assets modified after this date
            limit: Maximum results to return (1-1000, default: 20)
            offset: Result offset for pagination (default: 0)
            include_metadata: Whether to include metadata (default: True)
            
        Returns:
            AssetListResponse with paginated results
            
        Raises:
            ValidationError: If parameters are invalid
            RestApiError: For API errors
        """
        # Validate pagination parameters
        pagination_params = self._build_pagination_params(limit, offset)
        
        params = {
            "q": query,
            "limit": pagination_params["limit"],
            "offset": pagination_params["offset"],
            "includeMetadata": include_metadata,
        }
        
        # Add optional filters
        if user_type_id:
            params["userTypeId"] = user_type_id
        if modified_since:
            params["modifiedSince"] = modified_since
        
        # Clean parameters
        params = self._clean_params(params)
        self._log_operation("searchAssets", params)
        
        # Call API
        response = self.client.searchAssets(**params)
        
        # Handle response and build list response
        if isinstance(response, dict):
            items = response.get("items", [])
            total = response.get("total")
        else:
            items = getattr(response, "items", [])
            total = getattr(response, "total", None)
        
        # Convert items to AssetResponse objects
        asset_items = [
            AssetResponse(**item) if isinstance(item, dict) else item
            for item in items
        ]
        
        page_info = self._build_page_info(
            limit=pagination_params["limit"],
            offset=pagination_params["offset"],
            total=total
        )
        
        return AssetListResponse(
            items=asset_items,
            total=total,
            limit=pagination_params["limit"],
            offset=pagination_params["offset"],
            has_more=page_info.has_more
        )
    
    @handle_rest_errors
    def create_asset(self, asset_data: AssetCreateRequest) -> AssetResponse:
        """Create a new asset.
        
        Args:
            asset_data: AssetCreateRequest with asset data
            
        Returns:
            AssetResponse with created asset data
            
        Raises:
            ValidationError: If asset data is invalid
            ConflictError: If asset ID already exists
            RestApiError: For other API errors
        """
        # Validate that ID is present
        self._validate_required_params(
            {"id": asset_data.id},
            ["id"]
        )
        
        # Convert request to dict for API call
        asset_dict = asset_data.model_dump(exclude_none=True)
        self._log_operation("createAsset", {"assetId": asset_data.id})
        
        try:
            response = self.client.createAsset(body=asset_dict)
        except Exception as e:
            if "409" in str(e) or "conflict" in str(e).lower():
                raise exc.ConflictError(409, f"Asset {asset_data.id} already exists")
            if "400" in str(e):
                raise exc.ValidationError(str(e))
            raise
        
        # Convert response to AssetResponse
        if isinstance(response, dict):
            return AssetResponse(**response)
        return response
    
    @handle_rest_errors
    def update_asset(self, asset_id: str,
                    updates: AssetUpdateRequest) -> AssetResponse:
        """Update an existing asset.
        
        Args:
            asset_id: The asset ID to update
            updates: AssetUpdateRequest with updates
            
        Returns:
            AssetResponse with updated asset data
            
        Raises:
            NotFoundError: If asset not found
            ValidationError: If updates are invalid
            RestApiError: For other API errors
        """
        # Validate asset ID
        self._validate_required_params(
            {"asset_id": asset_id},
            ["asset_id"]
        )
        
        # Convert updates to dict
        updates_dict = updates.model_dump(exclude_none=True)
        self._log_operation("updateAsset", {"assetId": asset_id})
        
        try:
            response = self.client.updateAsset(
                assetId=asset_id,
                body=updates_dict
            )
        except Exception as e:
            if "404" in str(e):
                raise exc.NotFoundError(asset_id, "Asset")
            if "400" in str(e):
                raise exc.ValidationError(str(e))
            raise
        
        # Convert response to AssetResponse
        if isinstance(response, dict):
            return AssetResponse(**response)
        return response
    
    @handle_rest_errors
    def delete_asset(self, asset_id: str) -> bool:
        """Delete an asset.
        
        Args:
            asset_id: The asset ID to delete
            
        Returns:
            True if deletion was successful
            
        Raises:
            NotFoundError: If asset not found
            RestApiError: For other API errors
        """
        self._validate_required_params(
            {"asset_id": asset_id},
            ["asset_id"]
        )
        
        self._log_operation("deleteAsset", {"assetId": asset_id})
        
        try:
            self.client.deleteAsset(assetId=asset_id)
            return True
        except Exception as e:
            if "404" in str(e):
                raise exc.NotFoundError(asset_id, "Asset")
            raise
    
    @handle_rest_errors
    def upload_asset_content(self, asset_id: str,
                           file_path: str,
                           mime_type: Optional[str] = None) -> AssetResponse:
        """Upload binary content for an asset.
        
        Args:
            asset_id: The asset ID to upload content for
            file_path: Local file path to upload
            mime_type: MIME type of the content (auto-detected if not provided)
            
        Returns:
            AssetResponse with updated asset data
            
        Raises:
            FileNotFoundError: If file doesn't exist
            NotFoundError: If asset not found
            ValidationError: If content is invalid
            RestApiError: For other API errors
        """
        self._validate_required_params(
            {"asset_id": asset_id, "file_path": file_path},
            ["asset_id", "file_path"]
        )
        
        # Verify file exists - this should NOT be wrapped in handle_rest_errors
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Get file size
        file_size = os.path.getsize(file_path)
        
        # Auto-detect MIME type if not provided
        if mime_type is None:
            import mimetypes
            mime_type, _ = mimetypes.guess_type(file_path)
            mime_type = mime_type or "application/octet-stream"
        
        # Extract filename for fileName query parameter
        file_name = os.path.basename(file_path)
        
        self._log_operation("putAssetContent", {
            "id": asset_id,
            "file_path": file_path,
            "size": file_size,
            "mime_type": mime_type
        })
        
        try:
            # Open file in binary mode and upload
            # Use putAssetContent (PUT /assets/{id}/content)
            # Path parameter is 'id', not 'assetId'
            with open(file_path, 'rb') as f:
                response = self.client.putAssetContent(
                    id=asset_id,
                    fileName=file_name,
                    body=f
                )
        except FileNotFoundError as e:
            raise FileNotFoundError(f"File not found: {file_path}") from e
        except Exception as e:
            if "404" in str(e):
                raise exc.NotFoundError(asset_id, "Asset")
            if "400" in str(e) or "413" in str(e):  # 413 = Payload Too Large
                raise exc.ValidationError(f"Upload failed: {str(e)}")
            raise
        
        # Convert response to AssetResponse
        if isinstance(response, dict):
            return AssetResponse(**response)
        return response
    
    @handle_rest_errors
    def download_asset_content(self, asset_id: str,
                              output_path: Optional[str] = None) -> AssetDownloadResponse:
        """Download binary content for an asset.
        
        Args:
            asset_id: The asset ID to download content for
            output_path: Local path to save the file (optional)
            
        Returns:
            AssetDownloadResponse with download information
            
        Raises:
            NotFoundError: If asset not found
            RestApiError: For other API errors
        """
        self._validate_required_params(
            {"asset_id": asset_id},
            ["asset_id"]
        )
        
        self._log_operation("getAssetContent", {
            "id": asset_id,
            "save_to": output_path
        })
        
        try:
            # Use getAssetContent (GET /assets/{id}/content)
            # Path parameter is 'id', not 'assetId'
            response = self.client.getAssetContent(id=asset_id)
        except Exception as e:
            if "404" in str(e):
                raise exc.NotFoundError(asset_id, "Asset")
            raise
        
        # If output_path provided, save the content
        if output_path and hasattr(response, 'content'):
            with open(output_path, 'wb') as f:
                f.write(response.content)
            self.logger.info(f"Asset content saved to: {output_path}")
        
        # Build download response
        filename = getattr(response, 'filename', None) or asset_id
        size = getattr(response, 'size', None)
        mime_type = getattr(response, 'mime_type', None)
        content_url = getattr(response, 'content_url', None)
        expires_at = getattr(response, 'expires_at', None)
        
        return AssetDownloadResponse(
            asset_id=asset_id,
            filename=filename,
            size=size,
            mime_type=mime_type,
            content_url=content_url,
            expires_at=expires_at
        )
    
    def get_asset_content_url(self, asset_id: str) -> str:
        """Get download URL for asset binary content.
        
        Constructs the API endpoint URL for downloading asset content.
        Note: This returns the direct API endpoint URL, not a temporary/signed URL.
        Use this URL with appropriate authentication credentials.
        
        Args:
            asset_id: The asset ID
            
        Returns:
            Download URL for the asset content (API endpoint)
            
        Raises:
            ValidationError: If asset_id is invalid
        """
        self._validate_required_params(
            {"asset_id": asset_id},
            ["asset_id"]
        )
        
        # Get the base URL from the client's server URL
        if hasattr(self.client, 'server') and self.client.server:
            base_url = self.client.server.url
        elif hasattr(self.client, '_server') and self.client._server:
            base_url = self.client._server.url
        else:
            # Fallback: try to extract from a requestor URL
            raise exc.ValidationError(
                "Cannot determine API server URL. Ensure client is properly initialized."
            )
        
        # Construct and return the content URL
        content_url = f"{base_url}/assets/{asset_id}/content"
        self._log_operation("getAssetContentUrl", {"url": content_url})
        return content_url
    
    def list_assets(self, limit: int = 20, offset: int = 0,
                   include_metadata: bool = True) -> AssetListResponse:
        """List all assets (convenience method).
        
        Args:
            limit: Max results per page
            offset: Result offset
            include_metadata: Whether to include metadata
            
        Returns:
            AssetListResponse with paginated results
        """
        return self.search_assets(
            query="*",
            limit=limit,
            offset=offset,
            include_metadata=include_metadata
        )
    
    def search_by_type(self, user_type_id: str,
                      limit: int = 20,
                      offset: int = 0) -> AssetListResponse:
        """Search assets by type (convenience method).
        
        Args:
            user_type_id: Asset type to filter by
            limit: Max results per page
            offset: Result offset
            
        Returns:
            AssetListResponse with paginated results
        """
        return self.search_assets(
            query="*",
            user_type_id=user_type_id,
            limit=limit,
            offset=offset
        )
    
    def search_modified_since(self, modified_since: str,
                             limit: int = 20,
                             offset: int = 0) -> AssetListResponse:
        """Search assets modified after a specific timestamp (convenience method).
        
        Args:
            modified_since: ISO 8601 timestamp
            limit: Max results per page
            offset: Result offset
            
        Returns:
            AssetListResponse with paginated results
        """
        return self.search_assets(
            query="*",
            modified_since=modified_since,
            limit=limit,
            offset=offset
        )
