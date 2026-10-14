import io
import tempfile
from pathlib import Path
from unittest import TestCase
from unittest.mock import MagicMock, patch

from stepxmlclient.upload import AssetUploader


class TestAssetUploader(TestCase):
    def setUp(self):
        self.client = MagicMock()
        self.client.client.server.url = "https://step.example/restapiv2"
        self.uploader = AssetUploader(self.client)

    def test_upload_file_uses_upload_stream(self):
        content = b"test image content"

        with tempfile.TemporaryDirectory() as directory:
            file_path = Path(directory) / "image.png"
            file_path.write_bytes(content)

            def read_stream(file_stream, *args):
                return file_stream.read()

            with patch.object(
                self.uploader, "upload_stream", side_effect=read_stream
            ) as upload_stream:
                result = self.uploader.upload_file(
                    file_path,
                    asset_id="ASSET-1",
                    context_id="Context1",
                )

        self.assertEqual(result, content)
        self.assertEqual(upload_stream.call_args.args[1:], (
            "ASSET-1",
            "image.png",
            "image/png",
            "Context1",
            None,
        ))

    def test_upload_stream_sends_binary_content(self):
        response = MagicMock()
        response.status_code = 200
        self.client.client.requestor.put.return_value = response

        result = self.uploader.upload_stream(
            io.BytesIO(b"image bytes"),
            asset_id="ASSET-1",
            filename="image.png",
            mime_type="image/png",
            context_id="Context1",
            workspace_id="Main",
        )

        self.client.client.requestor.put.assert_called_once_with(
            "https://step.example/restapiv2/assets/ASSET-1/content",
            params={"fileName": "image.png", "context": "Context1", "workspace": "Main"},
            data=b"image bytes",
            headers={"Content-Type": "application/octet-stream"},
        )
        response.raise_for_status.assert_called_once_with()
        self.assertTrue(result["success"])
        self.assertEqual(result["asset_id"], "ASSET-1")

    def test_get_content_returns_response_bytes(self):
        response = MagicMock()
        response.content = b"downloaded content"
        self.client.client.requestor.get.return_value = response

        result = self.uploader.get_content("ASSET-1", context_id="Context1")

        self.client.client.requestor.get.assert_called_once_with(
            "https://step.example/restapiv2/assets/ASSET-1/content",
            params={"context": "Context1"},
        )
        response.raise_for_status.assert_called_once_with()
        self.assertEqual(result, b"downloaded content")
