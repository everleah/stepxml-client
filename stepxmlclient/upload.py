import os
from typing import Optional, Dict, Any, BinaryIO, Union
from pathlib import Path

"""
Asset binary upload module for STEP XML Client.

This module provides functionality to upload binary files (images, documents, etc.)
to STEP MDM system as asset binaries using the REST API v2.

---
USAGE EXAMPLE: How to upload an asset binary

from stepxmlclient.client import StiboStepRestClient, BasicAuthorisation
from stepxmlclient.upload import AssetUploader

# 1. Create and configure the STEP REST client
client = StiboStepRestClient(
    'https://your-step-server/restapiv2',
    BasicAuthorisation('username', 'password'),
    nocert=True  # For development only
)

# 2. Create the uploader
uploader = AssetUploader(client)

# 3. Upload a file to an asset
result = uploader.upload_file(
    file_path='path/to/image.jpg',
    asset_id='A123',
    filename=None,         # Optional: use original filename
    mime_type=None,        # Optional: auto-detect
    context_id='Context1', # Optional: STEP context
    workspace_id=None      # Optional: workspace
)

print(result)
---
"""



class AssetUploader:
    """
    Handles uploading binary files to STEP as asset binaries.
    
    Uses the STEP REST API v2 to upload files that will be associated
    with Asset objects in the MDM system.
    """
    
    def __init__(self, client):
        """
        Initialize the asset uploader.
        
        Args:
            client: StiboStepRestClient instance for API communication
        """
        self.client = client
    
    def upload_file(
        self,
        file_path: Union[str, Path],
        asset_id: str,
        filename: Optional[str] = None,
        mime_type: Optional[str] = None,
        context_id: str = "Context1",
        workspace_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Upload a binary file to STEP as an asset binary.
        
        Args:
            file_path: Path to the file to upload
            asset_id: ID of the asset in STEP to associate with this binary
            filename: Optional custom filename (defaults to original filename)
            mime_type: Optional MIME type (will be detected if not provided)
            context_id: STEP context ID (default: "Context1")
            workspace_id: Optional workspace ID for multi-workspace environments
            
        Returns:
            Dictionary with upload response details
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If asset_id is empty
            Exception: If the upload fails
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if not asset_id:
            raise ValueError("asset_id cannot be empty")
        
        # Use original filename if not provided
        if filename is None:
            filename = file_path.name
        
        # Detect MIME type if not provided
        if mime_type is None:
            mime_type = self._detect_mime_type(file_path)
        
        with open(file_path, 'rb') as file_handle:
            return self.upload_stream(
                file_handle,
                asset_id,
                filename,
                mime_type,
                context_id,
                workspace_id
            )
    
    def upload_stream(
        self,
        file_stream: BinaryIO,
        asset_id: str,
        filename: str,
        mime_type: str,
        context_id: str = "Context1",
        workspace_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Upload a binary stream to STEP as an asset binary.
        
        Args:
            file_stream: Binary file stream to upload
            asset_id: ID of the asset in STEP
            filename: Filename for the uploaded binary
            mime_type: MIME type of the file
            context_id: STEP context ID (default: "Context1")
            workspace_id: Optional workspace ID
            
        Returns:
            Dictionary with upload response details
            
        Raises:
            Exception: If the upload fails
        """
        # Prepare multipart form data
        files = {
            'file': (filename, file_stream, mime_type)
        }
        
        # Prepare parameters
        params = {
            'assetId': asset_id,
            'contextId': context_id
        }
        
        if workspace_id:
            params['workspaceId'] = workspace_id
        
        # Use the underlying requests-openapi client
        # The actual endpoint path depends on the OpenAPI specification
        # Common pattern: POST /assets/{assetId}/binary or /assets/binary
        try:
            response = self.client.client.post(
                '/assets/binary',
                params=params,
                files=files
            )
            return {
                'success': True,
                'asset_id': asset_id,
                'filename': filename,
                'response': response
            }
        except Exception as e:
            raise Exception(f"Failed to upload asset binary: {str(e)}") from e
    
    def delete_binary(
        self,
        asset_id: str,
        context_id: str = "Context1",
        workspace_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Delete a binary file from a STEP asset.
        
        Args:
            asset_id: ID of the asset in STEP
            context_id: STEP context ID (default: "Context1")
            workspace_id: Optional workspace ID
            
        Returns:
            Dictionary with deletion response details
            
        Raises:
            Exception: If the deletion fails
        """
        params = {
            'assetId': asset_id,
            'contextId': context_id
        }
        
        if workspace_id:
            params['workspaceId'] = workspace_id
        
        try:
            response = self.client.client.delete(
                '/assets/binary',
                params=params
            )
            return {
                'success': True,
                'asset_id': asset_id,
                'response': response
            }
        except Exception as e:
            raise Exception(f"Failed to delete asset binary: {str(e)}") from e
    
    @staticmethod
    def _detect_mime_type(file_path: Path) -> str:
        """
        Detect MIME type based on file extension.
        
        Args:
            file_path: Path to the file
            
        Returns:
            MIME type string
        """
        extension = file_path.suffix.lower()
        
        mime_types = {
            # Images
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.bmp': 'image/bmp',
            '.tiff': 'image/tiff',
            '.webp': 'image/webp',
            '.svg': 'image/svg+xml',
            # Documents
            '.pdf': 'application/pdf',
            '.doc': 'application/msword',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.xls': 'application/vnd.ms-excel',
            '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            '.ppt': 'application/vnd.ms-powerpoint',
            '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
            # Text
            '.txt': 'text/plain',
            '.csv': 'text/csv',
            '.xml': 'application/xml',
            '.json': 'application/json',
            # Archives
            '.zip': 'application/zip',
            '.rar': 'application/x-rar-compressed',
            # Video
            '.mp4': 'video/mp4',
            '.avi': 'video/x-msvideo',
            '.mov': 'video/quicktime',
        }
        
        return mime_types.get(extension, 'application/octet-stream')