"""Phase 2 - Asset Operations tests.

Tests for asset CRUD operations, search, binary uploads/downloads, and integration.
"""

import unittest
from unittest.mock import Mock, MagicMock, patch, mock_open
import logging
import os
import tempfile

from stepxmlclient.rest_client.operations.assets import AssetOperations
from stepxmlclient.rest_client.models.asset import (
    AssetResponse,
    AssetListResponse,
    AssetSearchRequest,
    AssetCreateRequest,
    AssetUpdateRequest,
    AssetUploadRequest,
    AssetDownloadResponse,
    AssetKeyValue,
    AssetMetadata,
)
from stepxmlclient.rest_client import exceptions as exc


class TestAssetModels(unittest.TestCase):
    """Tests for asset model classes."""
    
    def test_asset_key_value_creation(self):
        """Test AssetKeyValue creation."""
        kv = AssetKeyValue(key="Usage", value="ProductImage")
        self.assertEqual(kv.key, "Usage")
        self.assertEqual(kv.value, "ProductImage")
    
    def test_asset_metadata_creation(self):
        """Test AssetMetadata creation."""
        meta = AssetMetadata(
            filename="image.jpg",
            mime_type="image/jpeg",
            size=102400
        )
        self.assertEqual(meta.filename, "image.jpg")
        self.assertEqual(meta.mime_type, "image/jpeg")
        self.assertEqual(meta.size, 102400)
    
    def test_asset_metadata_with_dates(self):
        """Test AssetMetadata with timestamp fields."""
        meta = AssetMetadata(
            filename="image.jpg",
            creation_date="2024-01-01T00:00:00Z",
            modification_date="2024-02-04T10:00:00Z",
            checksum="abc123"
        )
        self.assertEqual(meta.creation_date, "2024-01-01T00:00:00Z")
        self.assertIsNotNone(meta.checksum)
    
    def test_asset_response_creation(self):
        """Test AssetResponse creation."""
        asset = AssetResponse(
            id="ASSET123",
            user_type_id="Image",
            name="Product Image"
        )
        self.assertEqual(asset.id, "ASSET123")
        self.assertEqual(asset.name, "Product Image")
    
    def test_asset_response_with_metadata(self):
        """Test AssetResponse with metadata."""
        meta = AssetMetadata(filename="image.jpg")
        asset = AssetResponse(
            id="ASSET123",
            metadata=meta
        )
        self.assertIsNotNone(asset.metadata)
        self.assertEqual(asset.metadata.filename, "image.jpg")
    
    def test_asset_response_with_key_values(self):
        """Test AssetResponse with key-values."""
        kvs = [AssetKeyValue(key="Usage", value="ProductImage")]
        asset = AssetResponse(
            id="ASSET123",
            key_values=kvs
        )
        self.assertEqual(len(asset.key_values), 1)
        self.assertEqual(asset.key_values[0].value, "ProductImage")
    
    def test_asset_list_response_creation(self):
        """Test AssetListResponse creation."""
        assets = [
            AssetResponse(id="ASSET1"),
            AssetResponse(id="ASSET2"),
        ]
        response = AssetListResponse(
            items=assets,
            total=50,
            limit=20,
            offset=0
        )
        self.assertEqual(len(response.items), 2)
        self.assertEqual(response.total, 50)
    
    def test_asset_list_response_has_more(self):
        """Test AssetListResponse has_more calculation."""
        assets = [AssetResponse(id=f"ASSET{i}") for i in range(20)]
        
        response = AssetListResponse(
            items=assets,
            total=50,
            limit=20,
            offset=0,
            has_more=True
        )
        self.assertTrue(response.has_more)
    
    def test_asset_search_request_creation(self):
        """Test AssetSearchRequest creation."""
        request = AssetSearchRequest(
            query="image",
            limit=50,
            offset=10
        )
        self.assertEqual(request.query, "image")
        self.assertEqual(request.limit, 50)
    
    def test_asset_search_request_defaults(self):
        """Test AssetSearchRequest defaults."""
        request = AssetSearchRequest()
        self.assertEqual(request.query, "*")
        self.assertTrue(request.include_metadata)
        self.assertFalse(request.include_content)
    
    def test_asset_create_request(self):
        """Test AssetCreateRequest creation."""
        request = AssetCreateRequest(
            id="NEWASSET",
            user_type_id="Image",
            name="New Asset"
        )
        self.assertEqual(request.id, "NEWASSET")
    
    def test_asset_update_request(self):
        """Test AssetUpdateRequest creation."""
        request = AssetUpdateRequest(name="Updated Name")
        self.assertEqual(request.name, "Updated Name")
    
    def test_asset_upload_request(self):
        """Test AssetUploadRequest creation."""
        request = AssetUploadRequest(
            filename="image.jpg",
            mime_type="image/jpeg"
        )
        self.assertEqual(request.filename, "image.jpg")
    
    def test_asset_download_response(self):
        """Test AssetDownloadResponse creation."""
        response = AssetDownloadResponse(
            asset_id="ASSET123",
            filename="image.jpg",
            size=102400
        )
        self.assertEqual(response.asset_id, "ASSET123")
        self.assertEqual(response.size, 102400)


class TestAssetOperations(unittest.TestCase):
    """Tests for AssetOperations class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.logger = logging.getLogger(__name__)
        self.operations = AssetOperations(self.mock_client, logger=self.logger)
    
    def test_asset_operations_initialization(self):
        """Test AssetOperations initialization."""
        self.assertEqual(self.operations.operation_name, "AssetOperations")
        self.assertIsNotNone(self.operations.logger)
    
    def test_get_asset_success(self):
        """Test successful asset retrieval."""
        mock_response = {
            "id": "ASSET123",
            "user_type_id": "Image",
            "name": "Test Asset"
        }
        self.mock_client.getAsset.return_value = mock_response
        
        result = self.operations.get_asset("ASSET123")
        
        self.assertEqual(result.id, "ASSET123")
        self.assertEqual(result.name, "Test Asset")
    
    def test_get_asset_not_found(self):
        """Test asset retrieval when not found."""
        self.mock_client.getAsset.side_effect = Exception("404 not found")
        
        with self.assertRaises(exc.NotFoundError):
            self.operations.get_asset("NONEXISTENT")
    
    def test_get_asset_validation(self):
        """Test asset retrieval validation."""
        with self.assertRaises(exc.ValidationError):
            self.operations.get_asset(None)
    
    def test_get_asset_includes_params(self):
        """Test that get_asset passes include parameters."""
        mock_response = {"id": "ASSET123"}
        self.mock_client.getAsset.return_value = mock_response
        
        self.operations.get_asset(
            "ASSET123",
            include_metadata=False,
            include_content_reference=True
        )
        
        call_args = self.mock_client.getAsset.call_args
        self.assertEqual(call_args[1]["includeMetadata"], False)
        self.assertEqual(call_args[1]["includeContentReference"], True)
    
    def test_search_assets_success(self):
        """Test successful asset search."""
        mock_response = {
            "items": [
                {"id": "ASSET1", "name": "Asset 1"},
                {"id": "ASSET2", "name": "Asset 2"},
            ],
            "total": 50
        }
        self.mock_client.searchAssets.return_value = mock_response
        
        result = self.operations.search_assets(query="test")
        
        self.assertEqual(len(result.items), 2)
        self.assertEqual(result.total, 50)
    
    def test_search_assets_defaults(self):
        """Test search with default parameters."""
        mock_response = {"items": [], "total": 0}
        self.mock_client.searchAssets.return_value = mock_response
        
        self.operations.search_assets()
        
        call_args = self.mock_client.searchAssets.call_args
        self.assertEqual(call_args[1]["q"], "*")
        self.assertEqual(call_args[1]["limit"], 20)
    
    def test_search_assets_with_filters(self):
        """Test search with optional filters."""
        mock_response = {"items": [], "total": 0}
        self.mock_client.searchAssets.return_value = mock_response
        
        self.operations.search_assets(
            query="image",
            user_type_id="ImageType",
            modified_since="2024-01-01T00:00:00Z",
            limit=50,
            offset=10
        )
        
        call_args = self.mock_client.searchAssets.call_args
        self.assertEqual(call_args[1]["q"], "image")
        self.assertEqual(call_args[1]["userTypeId"], "ImageType")
        self.assertEqual(call_args[1]["modifiedSince"], "2024-01-01T00:00:00Z")
    
    def test_create_asset_success(self):
        """Test successful asset creation."""
        request = AssetCreateRequest(
            id="NEWASSET",
            name="New Asset"
        )
        mock_response = {
            "id": "NEWASSET",
            "name": "New Asset"
        }
        self.mock_client.createAsset.return_value = mock_response
        
        result = self.operations.create_asset(request)
        
        self.assertEqual(result.id, "NEWASSET")
    
    def test_create_asset_conflict(self):
        """Test asset creation with existing ID."""
        request = AssetCreateRequest(id="EXISTING")
        self.mock_client.createAsset.side_effect = Exception("409 conflict")
        
        with self.assertRaises(exc.ConflictError):
            self.operations.create_asset(request)
    
    def test_update_asset_success(self):
        """Test successful asset update."""
        updates = AssetUpdateRequest(name="Updated")
        mock_response = {
            "id": "ASSET123",
            "name": "Updated"
        }
        self.mock_client.updateAsset.return_value = mock_response
        
        result = self.operations.update_asset("ASSET123", updates)
        
        self.assertEqual(result.name, "Updated")
    
    def test_update_asset_not_found(self):
        """Test asset update when not found."""
        updates = AssetUpdateRequest(name="Updated")
        self.mock_client.updateAsset.side_effect = Exception("404 not found")
        
        with self.assertRaises(exc.NotFoundError):
            self.operations.update_asset("NONEXISTENT", updates)
    
    def test_delete_asset_success(self):
        """Test successful asset deletion."""
        self.mock_client.deleteAsset.return_value = None
        
        result = self.operations.delete_asset("ASSET123")
        
        self.assertTrue(result)
        self.mock_client.deleteAsset.assert_called_once_with(assetId="ASSET123")
    
    def test_delete_asset_not_found(self):
        """Test asset deletion when not found."""
        self.mock_client.deleteAsset.side_effect = Exception("404 not found")
        
        with self.assertRaises(exc.NotFoundError):
            self.operations.delete_asset("NONEXISTENT")
    
    @patch('stepxmlclient.rest_client.operations.assets.open', new_callable=mock_open, read_data=b'fake image data')
    @patch('os.path.getsize', return_value=102400)
    @patch('os.path.exists', return_value=True)
    def test_upload_asset_content_success(self, mock_exists, mock_getsize, mock_file):
        """Test successful asset content upload."""
        mock_response = {"id": "ASSET123"}
        self.mock_client.uploadAssetContent.return_value = mock_response
        
        result = self.operations.upload_asset_content(
            "ASSET123",
            "/path/to/file.jpg",
            mime_type="image/jpeg"
        )
        
        self.assertEqual(result.id, "ASSET123")
        self.mock_client.uploadAssetContent.assert_called_once()
        mock_file.assert_called_once_with("/path/to/file.jpg", 'rb')
    
    @patch('os.path.exists')
    def test_upload_asset_content_file_not_found(self, mock_exists):
        """Test upload when file doesn't exist."""
        mock_exists.return_value = False
        
        with self.assertRaises(FileNotFoundError):
            self.operations.upload_asset_content("ASSET123", "/nonexistent/file.jpg")
    
    @patch('stepxmlclient.rest_client.operations.assets.open', new_callable=mock_open, read_data=b'fake image data')
    @patch('os.path.getsize', return_value=102400)
    @patch('os.path.exists', return_value=True)
    def test_upload_asset_content_asset_not_found(self, mock_exists, mock_getsize, mock_file):
        """Test upload when asset not found."""
        self.mock_client.uploadAssetContent.side_effect = Exception("404 not found")

        with self.assertRaises(exc.NotFoundError):
            self.operations.upload_asset_content("NONEXISTENT", "/path/to/file.jpg")
    
    @patch('stepxmlclient.rest_client.operations.assets.open', new_callable=mock_open, read_data=b'fake image data')
    @patch('os.path.getsize', return_value=102400)
    @patch('os.path.exists', return_value=True)
    def test_upload_asset_mime_type_detection(self, mock_exists, mock_getsize, mock_file):
        """Test MIME type auto-detection."""
        mock_response = {"id": "ASSET123"}
        self.mock_client.uploadAssetContent.return_value = mock_response
        
        self.operations.upload_asset_content(
            "ASSET123",
            "/path/to/file.jpg"  # No mime_type provided
        )
        
        call_args = self.mock_client.uploadAssetContent.call_args
        # Should detect image/jpeg or application/octet-stream
        mime_type = call_args[1]["mimeType"]
        self.assertIsNotNone(mime_type)
    
    def test_download_asset_content_success(self):
        """Test successful asset content download."""
        mock_response = Mock()
        mock_response.filename = "image.jpg"
        mock_response.size = 102400
        mock_response.mime_type = "image/jpeg"
        self.mock_client.downloadAssetContent.return_value = mock_response
        
        result = self.operations.download_asset_content("ASSET123")
        
        self.assertEqual(result.asset_id, "ASSET123")
        self.assertEqual(result.filename, "image.jpg")
    
    @patch('stepxmlclient.rest_client.operations.assets.open', new_callable=mock_open)
    def test_download_asset_content_save_to_file(self, mock_file):
        """Test downloading and saving asset content."""
        # Create a mock response object with required attributes
        mock_response = MagicMock()
        mock_response.filename = "image.jpg"
        mock_response.size = 102400
        mock_response.mime_type = "image/jpeg"
        mock_response.content = b"binary content"
        
        self.mock_client.downloadAssetContent.return_value = mock_response
        
        result = self.operations.download_asset_content(
            "ASSET123",
            output_path="/tmp/image.jpg"
        )
        
        self.assertEqual(result.asset_id, "ASSET123")
        self.assertEqual(result.filename, "image.jpg")
        mock_file.assert_called_once_with("/tmp/image.jpg", 'wb')
    
    def test_download_asset_content_not_found(self):
        """Test download when asset not found."""
        self.mock_client.downloadAssetContent.side_effect = Exception("404 not found")
        
        with self.assertRaises(exc.NotFoundError):
            self.operations.download_asset_content("NONEXISTENT")
    
    def test_get_asset_content_url(self):
        """Test getting asset content URL."""
        mock_response = {"url": "https://example.com/assets/ASSET123"}
        self.mock_client.getAssetContentUrl.return_value = mock_response
        
        result = self.operations.get_asset_content_url("ASSET123")
        
        self.assertEqual(result, "https://example.com/assets/ASSET123")
    
    def test_get_asset_content_url_alternate_key(self):
        """Test getting asset content URL with alternate key."""
        mock_response = {"content_url": "https://example.com/content/ASSET123"}
        self.mock_client.getAssetContentUrl.return_value = mock_response
        
        result = self.operations.get_asset_content_url("ASSET123")
        
        self.assertEqual(result, "https://example.com/content/ASSET123")
    
    def test_list_assets(self):
        """Test list_assets convenience method."""
        mock_response = {"items": [], "total": 0}
        self.mock_client.searchAssets.return_value = mock_response
        
        self.operations.list_assets()
        
        call_args = self.mock_client.searchAssets.call_args
        self.assertEqual(call_args[1]["q"], "*")
    
    def test_search_by_type(self):
        """Test search_by_type convenience method."""
        mock_response = {"items": [], "total": 0}
        self.mock_client.searchAssets.return_value = mock_response
        
        self.operations.search_by_type("ImageType")
        
        call_args = self.mock_client.searchAssets.call_args
        self.assertEqual(call_args[1]["userTypeId"], "ImageType")
    
    def test_search_modified_since(self):
        """Test search_modified_since convenience method."""
        mock_response = {"items": [], "total": 0}
        self.mock_client.searchAssets.return_value = mock_response
        
        self.operations.search_modified_since("2024-01-01T00:00:00Z")
        
        call_args = self.mock_client.searchAssets.call_args
        self.assertEqual(call_args[1]["modifiedSince"], "2024-01-01T00:00:00Z")


if __name__ == '__main__':
    unittest.main()
