
new_content = """

class TestAssetOperations(unittest.TestCase):
    def setUp(self):
        self.mock_client = Mock()
        self.logger = logging.getLogger(__name__)
        self.operations = AssetOperations(self.mock_client, logger=self.logger)

    def test_asset_operations_initialization(self):
        self.assertEqual(self.operations.operation_name, "AssetOperations")

    def test_get_asset_success(self):
        self.mock_client.getAsset.return_value = {"id": "ASSET123", "user_type_id": "Image", "name": "Test Asset"}
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
        condition = {"conditionType": "objecttype", "objectTypeId": "Image"}
        result = self.operations.search_assets(condition=condition)
        self.assertEqual(len(result.items), 2)
        call_args = self.mock_client.postAssetsSearch.call_args
        self.assertEqual(call_args[1]["body"]["condition"], condition)

    def test_search_assets_requires_condition(self):
        with self.assertRaises(exc.ValidationError):
            self.operations.search_assets(condition=None)

    def test_create_asset_success(self):
        self.mock_client.postAssets.return_value = {"id": "NEWASSET", "name": "New Asset"}
        request = AssetCreateRequest(id="NEWASSET", user_type_id=None, name="New Asset", key_values=None, attributes=None)
        result = self.operations.create_asset(request)
        self.assertEqual(result.id, "NEWASSET")
        self.mock_client.postAssets.assert_called_once()

    def test_create_asset_conflict(self):
        self.mock_client.postAssets.side_effect = Exception("409 conflict")
        request = AssetCreateRequest(id="EXISTING", user_type_id=None, name=None, key_values=None, attributes=None)
        with self.assertRaises(exc.ConflictError):
            self.operations.create_asset(request)

    def test_update_asset_success(self):
        self.mock_client.patchAsset.return_value = {"id": "ASSET123", "name": "Updated"}
        updates = AssetUpdateRequest(name="Updated", user_type_id=None, key_values=None, attributes=None)
        result = self.operations.update_asset("ASSET123", updates)
        self.assertEqual(result.name, "Updated")
        call_args = self.mock_client.patchAsset.call_args
        self.assertEqual(call_args[1]["id"], "ASSET123")
        self.assertNotIn("assetId", call_args[1])

    def test_update_asset_not_found(self):
        self.mock_client.patchAsset.side_effect = Exception("404 not found")
        updates = AssetUpdateRequest(name="Updated", user_type_id=None, key_values=None, attributes=None)
        with self.assertRaises(exc.NotFoundError):
            self.operations.update_asset("NONEXISTENT", updates)

    def test_update_asset_with_key_id(self):
        self.mock_client.patchAsset.return_value = {"id": "ASSET123"}
        updates = AssetUpdateRequest(name="Updated", user_type_id=None, key_values=None, attributes=None)
        self.operations.update_asset("ASSET123", updates, key_id="MyKey")
        call_args = self.mock_client.patchAsset.call_args
        self.assertEqual(call_args[1]["keyId"], "MyKey")

    def test_replace_asset_success(self):
        self.mock_client.putAsset.return_value = {"id": "ASSET123", "name": "Replaced"}
        data = AssetCreateRequest(id="ASSET123", user_type_id=None, name="Replaced", key_values=None, attributes=None)
        result = self.operations.replace_asset("ASSET123", data)
        self.assertEqual(result.id, "ASSET123")
        call_args = self.mock_client.putAsset.call_args
        self.assertEqual(call_args[1]["id"], "ASSET123")

    def test_replace_asset_with_allow_overwrite(self):
        self.mock_client.putAsset.return_value = {"id": "ASSET123"}
        data = AssetCreateRequest(id="ASSET123", user_type_id=None, name=None, key_values=None, attributes=None)
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
        body = call_args[1]["body"]
        self.assertEqual(body["condition"]["conditionType"], "objecttype")
        self.assertEqual(body["condition"]["objectTypeId"], "ImageType")

    def test_list_assets(self):
        self.mock_client.postAssetsSearch.return_value = {"items": [], "total": 0}
        self.operations.list_assets()
        self.mock_client.postAssetsSearch.assert_called_once()


if __name__ == "__main__":
    import unittest
    unittest.main()
"""

with open("test_rest_client_phase2_assets.py", "a") as f:
    f.write(new_content)
print("Done")
