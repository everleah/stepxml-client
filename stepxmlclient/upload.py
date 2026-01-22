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
            file_path: Path to the file to upload or URL of the file to transfer
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
        import tempfile
        import requests

        # Check if file_path is a URL
        file_path_str = str(file_path)
        is_url = file_path_str.startswith('http://') or file_path_str.startswith('https://')

        if is_url:
            # Download file to temp location
            response = requests.get(file_path_str, stream=True)
            if response.status_code != 200:
                raise FileNotFoundError(f"Could not download file from URL: {file_path_str}")
            # Use filename from URL if not provided
            if filename is None:
                filename = Path(file_path_str).name or 'downloaded_file'
            # Detect MIME type if not provided
            if mime_type is None:
                mime_type = response.headers.get('Content-Type', 'application/octet-stream')
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                for chunk in response.iter_content(chunk_size=8192):
                    tmp_file.write(chunk)
                tmp_file_path = Path(tmp_file.name)
            with open(tmp_file_path, 'rb') as file_handle:
                result = self.upload_stream(
                    file_handle,
                    asset_id,
                    filename,
                    mime_type,
                    context_id,
                    workspace_id
                )
            os.unlink(tmp_file_path)
            return result
        else:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            if not asset_id:
                raise ValueError("asset_id cannot be empty")
            if filename is None:
                filename = file_path.name
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
        # Prepare query parameters according to STEP REST API v2 spec
        params = {
            'fileName': filename,
            'context': context_id
        }
        
        if workspace_id:
            params['workspace'] = workspace_id
        
        # Read binary data from stream
        binary_data = file_stream.read()
        
        # Use the correct REST API v2 endpoint: PUT /assets/{id}/content
        # Binary content is sent as application/octet-stream in request body
        try:
            # Access the underlying requests Session from requests-openapi client
            endpoint = f'/assets/{asset_id}/content'
            response = self.client.client.requestor.put(
                f'{self.client.client.server.url}{endpoint}',
                params=params,
                data=binary_data,
                headers={'Content-Type': mime_type}
            )
            response.raise_for_status()
            return {
                'success': True,
                'asset_id': asset_id,
                'filename': filename,
                'mime_type': mime_type,
                'status_code': response.status_code
            }
        except Exception as e:
            raise Exception(f"Failed to upload asset binary: {str(e)}") from e
    
    def get_content(
        self,
        asset_id: str,
        context_id: str = "Context1",
        workspace_id: Optional[str] = None
    ) -> bytes:
        """
        Download binary content from a STEP asset.
        
        Args:
            asset_id: ID of the asset in STEP
            context_id: STEP context ID (default: "Context1")
            workspace_id: Optional workspace ID
            
        Returns:
            Binary content as bytes
            
        Raises:
            Exception: If the download fails
        """
        params = {
            'context': context_id
        }
        
        if workspace_id:
            params['workspace'] = workspace_id
        
        try:
            endpoint = f'/assets/{asset_id}/content'
            response = self.client.client.requestor.get(
                f'{self.client.client.server.url}{endpoint}',
                params=params
            )
            response.raise_for_status()
            return response.content
        except Exception as e:
            raise Exception(f"Failed to download asset content: {str(e)}") from e
    
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