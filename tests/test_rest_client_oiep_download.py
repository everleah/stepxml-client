"""Tests for OIEP ResultURI download helper on base REST client."""

import os
import tempfile
import unittest
from unittest.mock import MagicMock

from stepxmlclient.client import StiboStepRestClient


class TestOiepResultUriDownload(unittest.TestCase):
    def setUp(self):
        self.client = object.__new__(StiboStepRestClient)
        self.client.logger = MagicMock()
        self.client.client = MagicMock()
        self.client.client.server = MagicMock()
        self.client.client.server.url = "https://example.mdm.stibosystems.com/restapiv2"
        self.client.client.requestor = MagicMock()

    def test_resolve_download_url_with_absolute_url(self):
        absolute = "https://host/restapi/integrationendpoints/demo/job/result.zip"
        resolved = self.client.resolve_download_url(absolute)
        self.assertEqual(resolved, absolute)

    def test_resolve_download_url_with_relative_result_uri(self):
        relative = "restapi/integrationendpoints/demo/BGP_1/result.zip"
        resolved = self.client.resolve_download_url(relative)
        self.assertEqual(
            resolved,
            "https://example.mdm.stibosystems.com/restapi/integrationendpoints/demo/BGP_1/result.zip",
        )

    def test_download_result_uri_writes_file(self):
        mock_response = MagicMock()
        mock_response.iter_content.return_value = [b"abc", b"", b"def"]
        self.client.client.requestor.get.return_value = mock_response

        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = self.client.download_result_uri(
                "restapi/integrationendpoints/demo/BGP_2/result.zip",
                tmp_dir,
            )
            self.assertTrue(os.path.isfile(output_path))
            with open(output_path, "rb") as f:
                self.assertEqual(f.read(), b"abcdef")

        self.client.client.requestor.get.assert_called_once_with(
            "https://example.mdm.stibosystems.com/restapi/integrationendpoints/demo/BGP_2/result.zip",
            stream=True,
            allow_redirects=True,
            timeout=120,
        )
        mock_response.raise_for_status.assert_called_once()
        mock_response.close.assert_called_once()

    def test_download_result_uri_existing_file_without_overwrite(self):
        mock_response = MagicMock()
        mock_response.iter_content.return_value = [b"content"]
        self.client.client.requestor.get.return_value = mock_response

        with tempfile.TemporaryDirectory() as tmp_dir:
            existing = os.path.join(tmp_dir, "result.zip")
            with open(existing, "wb") as f:
                f.write(b"old")

            with self.assertRaises(FileExistsError):
                self.client.download_result_uri(
                    "restapi/integrationendpoints/demo/BGP_3/result.zip",
                    tmp_dir,
                )

        self.client.client.requestor.get.assert_not_called()

    def test_download_oiep_result_from_payload(self):
        mock_response = MagicMock()
        mock_response.iter_content.return_value = [b"payload"]
        self.client.client.requestor.get.return_value = mock_response

        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = self.client.download_oiep_result(
                {"ResultURI": "restapi/integrationendpoints/demo/BGP_9/result.zip"},
                tmp_dir,
            )
            self.assertTrue(os.path.isfile(output_path))
            with open(output_path, "rb") as f:
                self.assertEqual(f.read(), b"payload")

    def test_download_oiep_result_missing_result_uri(self):
        with self.assertRaises(ValueError):
            self.client.download_oiep_result({}, "C:/tmp")


if __name__ == "__main__":
    unittest.main()
