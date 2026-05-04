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
    AssetMetadata,
)
from stepxmlclient.rest_client import exceptions as exc


class TestAssetModels(unittest.TestCase):
    """Tests for asset model classes."""
    
    def test_asset_metadata_creation(self):
        """Test AssetMetadata creation."""
        meta = AssetMetadata(
            filename="image.jpg",
            mime_type="image/jpeg",
            size=102400,
            creation_date=None,
            modification_date=None,
            checksum=None
        )
        self.assertEqual(meta.filename, "image.jpg")
        self.assertEqual(meta.mime_type, "image/jpeg")
        self.assertEqual(meta.size, 102400)
    
    def test_asset_metadata_with_dates(self):
        """Test AssetMetadata with timestamp fields."""
        meta = AssetMetadata(
            filename="image.jpg",
            mime_type="image/jpeg",
            size=102400,
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
            objectType="ProductImage",
            name="Product Image",
            classifications=["ProductImageRoot"],
            values=None,
            references=None,
            contentMetadata=None,
        )
        self.assertEqual(asset.id, "ASSET123")
        self.assertEqual(asset.name, "Product Image")
    
    def test_asset_response_with_content_metadata(self):
        """Test AssetResponse with contentMetadata."""
        asset = AssetResponse(
            id="ASSET123",
            objectType=None,
            name=None,
            classifications=[],
            values=None,
            references=None,
            contentMetadata={"originalFilename": "image.jpg"},
        )
        self.assertIsNotNone(asset.contentMetadata)
        self.assertEqual(asset.contentMetadata["originalFilename"], "image.jpg") #type: ignore[index]
    
    def test_asset_list_response_creation(self):
        """Test AssetListResponse creation."""
        assets = [
            AssetResponse(id="ASSET1", objectType=None, name=None, classifications=[], values=None, references=None, contentMetadata=None),
            AssetResponse(id="ASSET2", objectType=None, name=None, classifications=[], values=None, references=None, contentMetadata=None),
        ]
        response = AssetListResponse(
            items=assets,
            total=50,
            limit=20,
            offset=0,
            has_more=False
        )
        self.assertEqual(len(response.items), 2)
        self.assertEqual(response.total, 50)
    
    def test_asset_list_response_has_more(self):
        """Test AssetListResponse has_more calculation."""
        assets = [AssetResponse(id=f"ASSET{i}", objectType=None, name=None, classifications=[], values=None, references=None, contentMetadata=None) for i in range(20)]
        
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
            object_type=None,
            modified_since=None,
            limit=50,
            offset=10,
            include_metadata=True,
            include_content=False
        )
        self.assertEqual(request.query, "image")
        self.assertEqual(request.limit, 50)
    
    def test_asset_search_request_defaults(self):
        """Test AssetSearchRequest defaults."""
        request = AssetSearchRequest(
            query="*",
            object_type=None,
            modified_since=None,
            limit=20,
            offset=0,
            include_metadata=True,
            include_content=False
        )
        self.assertEqual(request.query, "*")
        self.assertTrue(request.include_metadata)
        self.assertFalse(request.include_content)
    
    def test_asset_create_request(self):
        """Test AssetCreateRequest creation."""
        request = AssetCreateRequest(
            objectType="ProductImage",
            classifications=["ProductImageRoot"],
            name="New Asset",
            values=None,
            references=None,
        )
        self.assertEqual(request.objectType, "ProductImage")
    
    def test_asset_update_request(self):
        """Test AssetUpdateRequest creation."""
        request = AssetUpdateRequest(
            name="Updated Name",
            classifications=None,
            values=None,
            references=None,
        )
        self.assertEqual(request.name, "Updated Name")
    
    def test_asset_upload_request(self):
        """Test AssetUploadRequest creation."""
        request = AssetUploadRequest(
            filename="image.jpg",
            mime_type="image/jpeg",
            description=None
        )
        self.assertEqual(request.filename, "image.jpg")
    
    def test_asset_download_response(self):
        """Test AssetDownloadResponse creation."""
        response = AssetDownloadResponse(
            asset_id="ASSET123",
            filename="image.jpg",
            mime_type="image/jpeg",
            size=102400,
            content_url=None,
            expires_at=None
        )
        self.assertEqual(response.asset_id, "ASSET123")
        self.assertEqual(response.size, 102400)




class TestAssetOperations(unittest.TestCase):
    def setUp(self):
        self.mock_client = Mock()
        self.logger = logging.getLogger(__name__)
        self.operations = AssetOperations(self.mock_client, logger=self.logger)

    def test_asset_operations_initialization(self):
        self.assertEqual(self.operations.operation_name, "AssetOperations")

    def test_get_asset_success(self):
        self.mock_client.getAsset.return_value = {"id": "ASSET123", "objectType": "ProductImage", "name": "Test Asset"}
        result = self.operations.get_asset("ASSET123")
        self.assertEqual(result.id, "ASSET123")
        call_args = self.mock_client.getAsset.call_args
        self.assertEqual(call_args[1]["id"], "ASSET123")
        self.assertNotIn("assetId", call_args[1])

    def test_get_asset_not_found(self):
        self.mock_client.getAsset.side_effect = Exception("404 not found")
        with self.assertRaises(exc.NotFoundError):
            self.operations.get_asset("NONEXISTENT")

    def test_get_asset_validation(self):
        with self.assertRaises(exc.ValidationError):
            self.operations.get_asset(None)

    def test_get_asset_with_key_id(self):
        self.mock_client.getAsset.return_value = {"id": "ASSET123"}
        self.operations.get_asset("ASSET123", key_id="MyKey")
        call_args = self.mock_client.getAsset.call_args
        self.assertEqual(call_args[1]["keyId"], "MyKey")

    def test_search_assets_success(self):
        self.mock_client.postAssetsSearch.return_value = {"items": [{"id": "ASSET1"}, {"id": "ASSET2"}], "total": 2}
        condition = {"conditionType": "objecttype", "objectType": "ProductImage"}
        result = self.operations.search_assets(condition=condition)
        self.assertEqual(len(result.items), 2)
        call_args = self.mock_client.postAssetsSearch.call_args
        self.assertEqual(call_args[1]["json"]["condition"], condition)

    def test_search_assets_requires_condition(self):
        with self.assertRaises(exc.ValidationError):
            self.operations.search_assets(condition=None)

    def test_create_asset_success(self):
        self.mock_client.postAssets.return_value = {"id": "NEWASSET", "name": "New Asset"}
        request = AssetCreateRequest(
            objectType="ProductImage",
            classifications=["ProductImageRoot"],
            name="New Asset",
            values=None,
            references=None,
        )
        result = self.operations.create_asset(request)
        self.assertEqual(result.id, "NEWASSET")
        self.mock_client.postAssets.assert_called_once()

    def test_create_asset_conflict(self):
        self.mock_client.postAssets.side_effect = Exception("409 conflict")
        request = AssetCreateRequest(
            objectType="ProductImage",
            classifications=["ProductImageRoot"],
            name=None,
            values=None,
            references=None,
        )
        with self.assertRaises(exc.ConflictError):
            self.operations.create_asset(request)

    def test_update_asset_success(self):
        self.mock_client.patchAsset.return_value = {"id": "ASSET123", "name": "Updated"}
        updates = AssetUpdateRequest(name="Updated", classifications=None, values=None, references=None)
        result = self.operations.update_asset("ASSET123", updates)
        self.assertEqual(result.name, "Updated")
        call_args = self.mock_client.patchAsset.call_args
        self.assertEqual(call_args[1]["id"], "ASSET123")
        self.assertNotIn("assetId", call_args[1])

    def test_update_asset_not_found(self):
        self.mock_client.patchAsset.side_effect = Exception("404 not found")
        updates = AssetUpdateRequest(name="Updated", classifications=None, values=None, references=None)
        with self.assertRaises(exc.NotFoundError):
            self.operations.update_asset("NONEXISTENT", updates)

    def test_update_asset_with_key_id(self):
        self.mock_client.patchAsset.return_value = {"id": "ASSET123"}
        updates = AssetUpdateRequest(name="Updated", classifications=None, values=None, references=None)
        self.operations.update_asset("ASSET123", updates, key_id="MyKey")
        call_args = self.mock_client.patchAsset.call_args
        self.assertEqual(call_args[1]["keyId"], "MyKey")

    def test_replace_asset_success(self):
        self.mock_client.putAsset.return_value = {"id": "ASSET123", "name": "Replaced"}
        data = AssetCreateRequest(
            objectType="ProductImage",
            classifications=["ProductImageRoot"],
            name="Replaced",
            values=None,
            references=None,
        )
        result = self.operations.replace_asset("ASSET123", data)
        self.assertEqual(result.id, "ASSET123")
        call_args = self.mock_client.putAsset.call_args
        self.assertEqual(call_args[1]["id"], "ASSET123")

    def test_replace_asset_with_allow_overwrite(self):
        self.mock_client.putAsset.return_value = {"id": "ASSET123"}
        data = AssetCreateRequest(
            objectType="ProductImage",
            classifications=["ProductImageRoot"],
            name=None,
            values=None,
            references=None,
        )
        self.operations.replace_asset("ASSET123", data, allow_overwrite=True)
        call_args = self.mock_client.putAsset.call_args
        self.assertEqual(call_args[1]["allow-overwrite"], True)

    def test_delete_asset_success(self):
        self.mock_client.deleteAsset.return_value = None
        result = self.operations.delete_asset("ASSET123")
        self.assertTrue(result)
        call_args = self.mock_client.deleteAsset.call_args
        self.assertEqual(call_args[1]["id"], "ASSET123")
        self.assertNotIn("assetId", call_args[1])

    def test_delete_asset_not_found(self):
        self.mock_client.deleteAsset.side_effect = Exception("404 not found")
        with self.assertRaises(exc.NotFoundError):
            self.operations.delete_asset("NONEXISTENT")

    def test_delete_asset_with_key_id(self):
        self.mock_client.deleteAsset.return_value = None
        self.operations.delete_asset("ASSET123", key_id="MyKey")
        call_args = self.mock_client.deleteAsset.call_args
        self.assertEqual(call_args[1]["keyId"], "MyKey")

    @patch("stepxmlclient.rest_client.operations.assets.open", new_callable=mock_open, read_data=b"image data")
    @patch("os.path.getsize", return_value=102400)
    @patch("os.path.exists", return_value=True)
    def test_upload_asset_content_success(self, mock_exists, mock_getsize, mock_file):
        self.mock_client.putAssetContent.return_value = {"id": "ASSET123"}
        result = self.operations.upload_asset_content("ASSET123", "/path/to/file.jpg", mime_type="image/jpeg")
        self.assertEqual(result.id, "ASSET123")
        self.mock_client.putAssetContent.assert_called_once()
        call_args = self.mock_client.putAssetContent.call_args
        self.assertEqual(call_args[1]["id"], "ASSET123")

    @patch("os.path.exists")
    def test_upload_asset_content_file_not_found(self, mock_exists):
        mock_exists.return_value = False
        with self.assertRaises(FileNotFoundError):
            self.operations.upload_asset_content("ASSET123", "/nonexistent/file.jpg")

    @patch("stepxmlclient.rest_client.operations.assets.open", new_callable=mock_open, read_data=b"image data")
    @patch("os.path.getsize", return_value=102400)
    @patch("os.path.exists", return_value=True)
    def test_upload_asset_content_asset_not_found(self, mock_exists, mock_getsize, mock_file):
        self.mock_client.putAssetContent.side_effect = Exception("404 not found")
        with self.assertRaises(exc.NotFoundError):
            self.operations.upload_asset_content("NONEXISTENT", "/path/to/file.jpg")

    def test_download_asset_content_success(self):
        mock_response = Mock()
        mock_response.filename = "image.jpg"
        mock_response.size = 102400
        mock_response.mime_type = "image/jpeg"
        mock_response.content_url = None
        mock_response.expires_at = None
        self.mock_client.getAssetContent.return_value = mock_response
        result = self.operations.download_asset_content("ASSET123")
        self.assertEqual(result.asset_id, "ASSET123")
        self.assertEqual(result.filename, "image.jpg")

    @patch("stepxmlclient.rest_client.operations.assets.open", new_callable=mock_open)
    def test_download_asset_content_save_to_file(self, mock_file):
        mock_response = MagicMock()
        mock_response.filename = "image.jpg"
        mock_response.size = 102400
        mock_response.mime_type = "image/jpeg"
        mock_response.content = b"binary content"
        mock_response.content_url = None
        mock_response.expires_at = None
        self.mock_client.getAssetContent.return_value = mock_response
        result = self.operations.download_asset_content("ASSET123", output_path="/tmp/image.jpg")
        self.assertEqual(result.asset_id, "ASSET123")
        mock_file.assert_called_once_with("/tmp/image.jpg", "wb")

    def test_download_asset_content_not_found(self):
        self.mock_client.getAssetContent.side_effect = Exception("404 not found")
        with self.assertRaises(exc.NotFoundError):
            self.operations.download_asset_content("NONEXISTENT")

    def test_search_by_type(self):
        self.mock_client.postAssetsSearch.return_value = {"items": [], "total": 0}
        self.operations.search_by_type("ImageType")
        call_args = self.mock_client.postAssetsSearch.call_args
        payload = call_args[1]["json"]
        self.assertEqual(payload["condition"]["conditionType"], "objecttype")
        self.assertEqual(payload["condition"]["objectType"], "ImageType")

    def test_list_assets(self):
        self.mock_client.postAssetsSearch.return_value = {"items": [], "total": 0}
        self.operations.list_assets()
        self.mock_client.postAssetsSearch.assert_called_once()


if __name__ == "__main__":
    import unittest
    unittest.main()
