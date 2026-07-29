"""Asset operations for STEP REST API.

Provides CRUD, search, and binary content operations for assets.
"""

import logging
import os
from typing import Any, Optional

import requests_openapi as roa

from .. import exceptions as exc
from ..base import BaseOperation, handle_rest_errors
from ..models.asset import (
    AssetCreateRequest,
    AssetDownloadResponse,
    AssetListResponse,
    AssetResponse,
    AssetUpdateRequest,
)


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
    
    def __init__(self, client: roa.Client, logger: Optional[logging.Logger] = None,
                 context: str | None = None, workspace: str | None = None):
        """Initialize AssetOperations.
        
        Args:
            client: The requests-openapi Client instance
            logger: Logger instance (optional)
            context: STEP context ID for all API calls
            workspace: STEP workspace ID (defaults to "Main" server-side)
        """
        super().__init__(client, operation_name="AssetOperations", logger=logger,
                         context=context, workspace=workspace)
    
    @handle_rest_errors
    def get_asset(self, asset_id: str,
                 key_id: str | None = None) -> AssetResponse:
        """Retrieve a single asset by ID.
        
        Args:
            asset_id: The asset ID (or alternate key value if key_id is set)
            key_id: Alternate key ID to use for lookup (optional)
            
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
        
        query_params = self._build_context_params()
        if key_id:
            query_params["keyId"] = key_id
        self._log_operation("getAsset", {"asset_id": asset_id, "keyId": key_id})
        
        try:
            response = self.client.getAsset(id=asset_id, **query_params)
        except Exception as e:
            if "404" in str(e) or "not found" in str(e).lower():
                raise exc.NotFoundError(asset_id, "Asset")
            raise
        
        if isinstance(response, dict):
            return AssetResponse(**response)
        return response
    
    @handle_rest_errors
    def search_assets(self, condition: dict) -> AssetListResponse:
        """Search for assets using a STEP condition query.
        
        Args:
            condition: A STEP condition object defining the search criteria.
                       Supported conditionTypes: 'and', 'or', 'id', 'name',
                       'textvalue', 'numericvalue', 'objecttype', 'simplebelow',
                       'lovvalue', 'hasreferenceto', 'hasdatacontainerobject'.
                       Example: {"conditionType": "objecttype", "objectTypeId": "MyType"}
            
        Returns:
            AssetListResponse with matching assets
            
        Raises:
            ValidationError: If condition is invalid
            RestApiError: For API errors
        """
        self._validate_required_params({"condition": condition}, ["condition"])
        body = {"condition": condition}
        self._log_operation("createAssetSearch", {"condition": condition})
        
        params = self._build_context_params()
        response = self.client.createAssetSearch(json=body, **params)
        
        if isinstance(response, dict):
            items = response.get("items", [])
            total = response.get("total")
        else:
            items = getattr(response, "items", [])
            total = getattr(response, "total", None)
        
        asset_items = [
            AssetResponse(**item) if isinstance(item, dict) else item
            for item in items
        ]
        
        return AssetListResponse(
            items=asset_items,
            total=total,
            limit=max(len(asset_items), 1),
            offset=0,
            has_more=False
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
        self._validate_required_params(
            {
                "objectType": asset_data.objectType,
                "classifications": asset_data.classifications,
            },
            ["objectType", "classifications"]
        )
        if not asset_data.classifications:
            raise exc.ValidationError("At least one classification is required")
        
        # Convert request to dict for API call
        asset_dict = asset_data.model_dump(exclude_none=True)
        self._log_operation("createAsset", {"objectType": asset_data.objectType})
        
        try:
            response = self.client.createAsset(json=asset_dict, **self._build_context_params())
        except Exception as e:
            if "409" in str(e) or "conflict" in str(e).lower():
                raise exc.ConflictError(409, "Asset conflict while creating asset")
            if "400" in str(e):
                raise exc.ValidationError(str(e))
            raise
        
        # Convert response to AssetResponse
        if isinstance(response, dict):
            return AssetResponse(**response)
        return response
    
    @handle_rest_errors
    def update_asset(self, asset_id: str,
                    updates: AssetUpdateRequest,
                    key_id: str | None = None) -> AssetResponse:
        """Partially update an existing asset (PATCH).
        
        Args:
            asset_id: The asset ID (or alternate key value if key_id is set)
            updates: AssetUpdateRequest with fields to update
            key_id: Alternate key ID to use for lookup (optional)
            
        Returns:
            AssetResponse with updated asset data
            
        Raises:
            NotFoundError: If asset not found
            ValidationError: If updates are invalid
            RestApiError: For other API errors
        """
        self._validate_required_params(
            {"asset_id": asset_id},
            ["asset_id"]
        )
        
        updates_dict = updates.model_dump(exclude_none=True)
        query_params = self._build_context_params()
        if key_id:
            query_params["keyId"] = key_id
        self._log_operation("updateAsset", {"asset_id": asset_id})
        
        try:
            response = self.client.updateAsset(
                id=asset_id,
                json=updates_dict,
                **query_params
            )
        except Exception as e:
            if "404" in str(e):
                raise exc.NotFoundError(asset_id, "Asset")
            if "400" in str(e):
                raise exc.ValidationError(str(e))
            raise
        
        if isinstance(response, dict):
            return AssetResponse(**response)
        return response

    @handle_rest_errors
    def replace_asset(self, asset_id: str,
                      asset_data: AssetCreateRequest,
                      key_id: str | None = None,
                      allow_overwrite: bool = False) -> AssetResponse:
        """Fully replace an asset (PUT). Creates it if it does not exist.
        
        Args:
            asset_id: The asset ID (or alternate key value if key_id is set)
            asset_data: Complete asset data to replace with
            key_id: Alternate key ID to use for lookup (optional)
            allow_overwrite: Whether to allow overwriting an existing asset
            
        Returns:
            AssetResponse with replaced asset data
            
        Raises:
            NotFoundError: If asset not found and allow_overwrite is False
            ValidationError: If data is invalid
            RestApiError: For other API errors
        """
        self._validate_required_params(
            {"asset_id": asset_id},
            ["asset_id"]
        )
        
        asset_dict = asset_data.model_dump(exclude_none=True)
        query_params: dict[str, Any] = self._build_context_params()
        if key_id:
            query_params["keyId"] = key_id
        if allow_overwrite:
            query_params["allow-overwrite"] = allow_overwrite
        self._log_operation("createOrReplaceAsset", {"asset_id": asset_id})
        
        try:
            response = self.client.createOrReplaceAsset(
                id=asset_id,
                json=asset_dict,
                **query_params
            )
        except Exception as e:
            if "404" in str(e):
                raise exc.NotFoundError(asset_id, "Asset")
            if "400" in str(e) or "409" in str(e):
                raise exc.ValidationError(str(e))
            raise
        
        if isinstance(response, dict):
            return AssetResponse(**response)
        return response
    
    @handle_rest_errors
    def delete_asset(self, asset_id: str,
                     key_id: str | None = None) -> bool:
        """Delete an asset.
        
        Args:
            asset_id: The asset ID (or alternate key value if key_id is set)
            key_id: Alternate key ID to use for lookup (optional)
            
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
        
        query_params = self._build_context_params()
        if key_id:
            query_params["keyId"] = key_id
        self._log_operation("deleteAsset", {"asset_id": asset_id})
        
        try:
            self.client.deleteAsset(id=asset_id, **query_params)
            return True
        except Exception as e:
            if "404" in str(e):
                raise exc.NotFoundError(asset_id, "Asset")
            raise
    
    @handle_rest_errors
    def upload_asset_content(self, asset_id: str,
                           file_path: str,
                           mime_type: str | None = None,
                           key_id: str | None = None) -> AssetResponse:
        """Upload binary content for an asset (PUT /assets/{id}/content).
        
        Args:
            asset_id: The asset ID (or alternate key value if key_id is set)
            file_path: Local file path to upload
            mime_type: MIME type of the content (auto-detected if not provided)
            key_id: Alternate key ID to use for lookup (optional)
            
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
        
        # Build query params (not path params)
        query_params = self._build_context_params()
        query_params["fileName"] = file_name
        if key_id:
            query_params["keyId"] = key_id
        
        self._log_operation("replaceAssetContent", {
            "asset_id": asset_id,
            "file_path": file_path,
            "size": file_size,
            "mime_type": mime_type
        })
        
        try:
            # Open file in binary mode and upload
            with open(file_path, 'rb') as f:
                response = self.client.replaceAssetContent(
                    id=asset_id,
                    data=f.read(),
                    **query_params
                )
                
            self._check_response_status(response, asset_id, "Asset")
        except FileNotFoundError as e:
            raise FileNotFoundError(f"File not found: {file_path}") from e
        except Exception as e:
            if "404" in str(e):
                raise exc.NotFoundError(asset_id, "Asset")
            if "400" in str(e) or "413" in str(e):  # 413 = Payload Too Large
                raise exc.ValidationError(f"Upload failed: {e!s}")
            raise
        
        # Convert response to AssetResponse
        if isinstance(response, dict):
            return AssetResponse(**response)
        return response
        
    @handle_rest_errors
    def download_asset_content(self, asset_id: str,
                              output_path: str | None = None,
                              key_id: str | None = None,
                              conversion_configuration_id: str | None = None) -> AssetDownloadResponse:
        """Download binary content for an asset (GET /assets/{id}/content).
        
        Args:
            asset_id: The asset ID (or alternate key value if key_id is set)
            output_path: Local path to save the file (optional)
            key_id: Alternate key ID to use for lookup (optional)
            conversion_configuration_id: Conversion configuration ID for format conversion (optional)
            
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
        
        query_params = self._build_context_params()
        if key_id:
            query_params["keyId"] = key_id
        if conversion_configuration_id:
            query_params["conversion-configuration-id"] = conversion_configuration_id
        self._log_operation("getAssetContent", {
            "asset_id": asset_id,
            "output_path": output_path
        })
        
        try:
            # Use getAssetContent (GET /assets/{id}/content)
            response = self.client.getAssetContent(id=asset_id, **query_params)
            self._check_response_status(response, asset_id, "Asset")
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
            condition={"conditionType": "objecttype", "objectType": user_type_id}
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
            condition={"conditionType": "name", "value": "*"}
        )


    # ------------------------------------------------------------------
    # Approval & lifecycle (v1.4.0)
    # ------------------------------------------------------------------

    @handle_rest_errors
    def get_asset_approval_status(self, asset_id: str,
                                  key_id: str | None = None) -> dict[str, Any]:
        self._validate_required_params({"asset_id": asset_id}, ["asset_id"])
        qp = self._build_context_params()
        if key_id: qp["keyId"] = key_id
        self._log_operation("getAssetApprovalStatus", {"id": asset_id})
        try:
            r = self.client.getAssetApprovalStatus(id=asset_id, **qp)
        except Exception as e:
            if "404" in str(e): raise exc.NotFoundError(asset_id, "Asset")
            raise
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def approve_asset(self, asset_id: str,
                      key_id: str | None = None) -> dict[str, Any]:
        self._validate_required_params({"asset_id": asset_id}, ["asset_id"])
        qp = self._build_context_params()
        if key_id: qp["keyId"] = key_id
        self._log_operation("approveAsset", {"id": asset_id})
        try:
            r = self.client.approveAsset(id=asset_id, **qp)
        except Exception as e:
            if "404" in str(e): raise exc.NotFoundError(asset_id, "Asset")
            raise
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def approve_asset_deletion(self, asset_id: str,
                               key_id: str | None = None) -> dict[str, Any]:
        self._validate_required_params({"asset_id": asset_id}, ["asset_id"])
        qp = self._build_context_params()
        if key_id: qp["keyId"] = key_id
        self._log_operation("approveAssetDeletion", {"id": asset_id})
        try:
            r = self.client.approveAssetDeletion(id=asset_id, **qp)
        except Exception as e:
            if "404" in str(e): raise exc.NotFoundError(asset_id, "Asset")
            raise
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def purge_asset(self, asset_id: str,
                    key_id: str | None = None) -> dict[str, Any]:
        self._validate_required_params({"asset_id": asset_id}, ["asset_id"])
        qp = self._build_context_params()
        if key_id: qp["keyId"] = key_id
        self._log_operation("purgeAsset", {"id": asset_id})
        try:
            r = self.client.purgeAsset(id=asset_id, **qp)
        except Exception as e:
            if "404" in str(e): raise exc.NotFoundError(asset_id, "Asset")
            raise
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def get_asset_value(self, asset_id: str, attribute_id: str,
                        key_id: str | None = None) -> dict[str, Any]:
        self._validate_required_params(
            {"asset_id": asset_id, "attribute_id": attribute_id},
            ["asset_id", "attribute_id"])
        qp = self._build_context_params()
        if key_id: qp["keyId"] = key_id
        self._log_operation("getAssetValueByAttributeId",
                           {"id": asset_id, "attributeId": attribute_id})
        try:
            r = self.client.getAssetValueByAttributeId(
                id=asset_id, attributeId=attribute_id, **qp)
        except Exception as e:
            if "404" in str(e): raise exc.NotFoundError(asset_id, "Asset")
            raise
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def replace_asset_value(self, asset_id: str, attribute_id: str,
                            value: dict[str, Any],
                            key_id: str | None = None) -> dict[str, Any]:
        self._validate_required_params(
            {"asset_id": asset_id, "attribute_id": attribute_id},
            ["asset_id", "attribute_id"])
        qp = self._build_context_params()
        if key_id: qp["keyId"] = key_id
        self._log_operation("replaceAssetValueByAttributeId",
                           {"id": asset_id, "attributeId": attribute_id})
        try:
            r = self.client.replaceAssetValueByAttributeId(
                id=asset_id, attributeId=attribute_id, json=value, **qp)
        except Exception as e:
            if "404" in str(e): raise exc.NotFoundError(asset_id, "Asset")
            if "400" in str(e): raise exc.ValidationError(str(e))
            raise
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def delete_asset_value(self, asset_id: str, attribute_id: str,
                           key_id: str | None = None) -> bool:
        self._validate_required_params(
            {"asset_id": asset_id, "attribute_id": attribute_id},
            ["asset_id", "attribute_id"])
        qp = self._build_context_params()
        if key_id: qp["keyId"] = key_id
        self._log_operation("deleteAssetValueByAttributeId",
                           {"id": asset_id, "attributeId": attribute_id})
        try:
            self.client.deleteAssetValueByAttributeId(
                id=asset_id, attributeId=attribute_id, **qp)
            return True
        except Exception as e:
            if "404" in str(e): raise exc.NotFoundError(asset_id, "Asset")
            raise

    @handle_rest_errors
    def get_asset_incoming_references(self, asset_id: str,
                                      key_id: str | None = None) -> dict[str, Any]:
        self._validate_required_params({"asset_id": asset_id}, ["asset_id"])
        qp = self._build_context_params()
        if key_id: qp["keyId"] = key_id
        self._log_operation("getAssetIncomingReferences", {"id": asset_id})
        try:
            r = self.client.getAssetIncomingReferences(id=asset_id, **qp)
        except Exception as e:
            if "404" in str(e): raise exc.NotFoundError(asset_id, "Asset")
            raise
        return r if isinstance(r, dict) else r
