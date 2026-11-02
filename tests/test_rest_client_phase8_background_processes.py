"""Phase 8 - Background process transport normalization used by Publishing."""

import unittest
from unittest.mock import Mock

from stepxmlclient.rest_client import exceptions as exc
from stepxmlclient.rest_client.models.background_process import BackgroundProcessResponse
from stepxmlclient.rest_client.operations.background_processes import BackgroundProcessOperations
from stepxmlclient.rest_client.publishing import V2PublishingJobBackend
from stepxmlclient.publishing import PublishingError
from tests.test_publishing_client import response


class TestBackgroundProcessTransport(unittest.TestCase):
    def setUp(self):
        self.transport = Mock()
        self.operations = BackgroundProcessOperations(self.transport, context="C", workspace="Main")

    def test_json_response_normalization_and_aliases(self):
        r = response(b'{"id":"B","status":"succeeded","numberOfErrors":1,"numberOfWarnings":2,'
                     b'"backgroundProcessType":"P","executionTimeMillis":12}')
        self.transport.getBackgroundProcess.return_value = r
        result = self.operations.get_background_process("B", timeout=4)
        self.assertIsInstance(result, BackgroundProcessResponse)
        self.assertEqual(result.number_of_errors, 1)
        self.assertEqual(result.number_of_warnings, 2)
        self.assertEqual(result.background_process_type, "P")
        self.assertEqual(result.execution_time_millis, 12)
        self.transport.getBackgroundProcess.assert_called_once_with(
            id="B", context="C", workspace="Main", _timeout=4)
        r.close.assert_called_once()
        self.assertEqual(BackgroundProcessResponse(number_of_errors=3).number_of_errors, 3)

    def test_plain_dict_list_and_bytes_still_work(self):
        self.transport.getBackgroundProcess.return_value = {"id": "B", "status": "succeeded"}
        self.assertEqual(self.operations.get_background_process("B").id, "B")
        self.transport.getBackgroundProcess.assert_called_once_with(
            id="B", context="C", workspace="Main")
        self.transport.getBackgroundProcessAttachmentsMetadata.return_value = [{"id": "A"}]
        self.assertEqual(self.operations.get_attachments_metadata("B"), [{"id": "A"}])
        self.transport.getBackgroundProcessAttachmentContent.return_value = b"file"
        self.assertEqual(self.operations.get_attachment_content("B", "A"), b"file")

    def test_http_failures_and_bad_shapes(self):
        for status in (401, 403, 404, 409, 429, 500):
            self.transport.getBackgroundProcessAttachmentsMetadata.return_value = response(
                b'{"message":"failure"}', status=status)
            with self.assertRaises(exc.RestClientError):
                self.operations.get_attachments_metadata("B")
        for value in (None, {}, "not a list", [1]):
            self.transport.getBackgroundProcessAttachmentsMetadata.return_value = value
            with self.assertRaises(exc.RestClientError):
                self.operations.get_attachments_metadata("B")
        for value in ({}, "not bytes", None):
            self.transport.getBackgroundProcessAttachmentContent.return_value = value
            with self.assertRaises(exc.RestClientError):
                self.operations.get_attachment_content("B", "A")
        self.transport.getBackgroundProcess.return_value = response(b"not json")
        with self.assertRaises(exc.RestClientError):
            self.operations.get_background_process("B")

    def test_embedded_errors_and_invalid_adapter_metadata(self):
        self.transport.getBackgroundProcess.return_value = {"httpStatus": 404}
        with self.assertRaises(exc.NotFoundError):
            self.operations.get_background_process("B")
        backend = V2PublishingJobBackend(self.operations)
        self.transport.getBackgroundProcess.return_value = {"id": "OTHER", "status": "succeeded"}
        with self.assertRaises(PublishingError):
            backend.get_status("B", timeout=2)
        for items in ([{"name": "missing id"}], [{"id": ""}]):
            self.transport.getBackgroundProcessAttachmentsMetadata.return_value = items
            with self.assertRaises(PublishingError):
                backend.list_files("B", timeout=2)

    def test_path_parameters_are_encoded_before_openapi_substitution(self):
        self.transport.getBackgroundProcessAttachmentContent.return_value = b"file"
        self.operations.get_attachment_content("B /1", "A/#2")
        self.transport.getBackgroundProcessAttachmentContent.assert_called_once_with(
            id="B%20%2F1", attachmentId="A%2F%232", context="C", workspace="Main")


if __name__ == "__main__":
    unittest.main()
