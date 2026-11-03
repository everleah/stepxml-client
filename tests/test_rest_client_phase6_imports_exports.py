"""Phase 6 - ExportSpecification, binary imports and background-process IDs."""

import unittest
from unittest.mock import Mock

from pydantic import ValidationError as ModelValidationError

from stepxmlclient.rest_client import exceptions as exc
from stepxmlclient.rest_client.models.import_export import (
    BackgroundProcessResponse, ExportJobCreateRequest, ExportJobResponse,
)
from stepxmlclient.rest_client.operations.exports import ExportOperations
from tests.test_rest_response_handling import json_response


class TestImportExportModels(unittest.TestCase):
    def test_export_specification(self):
        request = ExportJobCreateRequest(
            stepUrls=["step://product?id=P1"], processDescription="Selected roots")
        self.assertEqual(request.model_dump(exclude_none=True), {
            "stepUrls": ["step://product?id=P1"], "processDescription": "Selected roots",
        })

    def test_empty_export_specification_uses_server_configuration(self):
        self.assertEqual(ExportJobCreateRequest().model_dump(exclude_none=True), {})

    def test_export_step_urls_validation(self):
        with self.assertRaises(ModelValidationError):
            ExportJobCreateRequest.model_validate({"stepUrls": "P1"})

    def test_export_legacy_fields_are_still_accepted(self):
        request = ExportJobCreateRequest(entityType="Product", format="XML", filters={})
        self.assertEqual(request.entityType, "Product")
        self.assertEqual(request.format, "XML")

    def test_trigger_returns_identification_not_job_status(self):
        process = BackgroundProcessResponse(id="B")
        self.assertEqual(process.id, "B")
        self.assertIsNone(BackgroundProcessResponse().id)
        self.assertIs(ExportJobResponse, BackgroundProcessResponse)


class TestImportExportOperations(unittest.TestCase):
    def setUp(self):
        self.client = Mock(spec_set=["startExport", "startImport"])
        self.operations = ExportOperations(self.client, context="C", workspace="Main")

    def test_export_model_payload(self):
        self.client.startExport.return_value = json_response({"id": "B"})
        result = self.operations.create_export_job(
            "ExportConfig",
            ExportJobCreateRequest(stepUrls=["step://product?id=P1"], processDescription="Export"),
            use_request_context_workspace=False)
        self.assertIsInstance(result, BackgroundProcessResponse)
        self.assertEqual(result.id, "B")
        self.client.startExport.assert_called_once_with(
            exportConfigurationId="ExportConfig", context="C", workspace="Main",
            useRequestContextWorkspace=False,
            json={"stepUrls": ["step://product?id=P1"], "processDescription": "Export"})

    def test_export_body_absence_and_explicit_empty_body_are_distinct(self):
        for data in (None, {}, ExportJobCreateRequest()):
            with self.subTest(data=data):
                self.client.startExport.reset_mock()
                self.client.startExport.return_value = {"id": "B"}
                self.assertEqual(self.operations.create_export_job("Config", data).id, "B")
                params = self.client.startExport.call_args.kwargs
                if data is None:
                    self.assertNotIn("json", params)
                else:
                    self.assertEqual(params["json"], {})

    def test_binary_and_text_imports(self):
        for data in (b"<STEP/>", "<STEP/>"):
            with self.subTest(data=data):
                self.client.startImport.reset_mock()
                self.client.startImport.return_value = json_response({"id": "B"})
                result = self.operations.create_import_job("ImportConfig", data, process_description="Import")
                self.assertEqual(result.id, "B")
                self.client.startImport.assert_called_once_with(
                    importConfigurationId="ImportConfig", data=b"<STEP/>",
                    processDescription="Import", context="C", workspace="Main")

    def test_import_without_payload(self):
        self.client.startImport.return_value = {"id": "B"}
        self.assertEqual(self.operations.create_import_job("Config").id, "B")
        self.client.startImport.assert_called_once_with(
            importConfigurationId="Config", context="C", workspace="Main")

    def test_invalid_identification_is_not_replaced_by_success(self):
        for operation, method in (
            (self.client.startExport, self.operations.create_export_job),
            (self.client.startImport, self.operations.create_import_job),
        ):
            for payload in (None, [], "not an identification"):
                with self.subTest(method=method.__name__, payload=payload):
                    operation.return_value = payload
                    with self.assertRaises(exc.RestClientError):
                        method("Config")

    def test_http_and_embedded_errors(self):
        for operation, method in (
            (self.client.startExport, self.operations.create_export_job),
            (self.client.startImport, self.operations.create_import_job),
        ):
            for status, expected in ((400, exc.RestApiError), (404, exc.NotFoundError),
                                     (409, exc.ConflictError), (500, exc.ServerError)):
                for embedded in (False, True):
                    with self.subTest(method=method.__name__, status=status, embedded=embedded):
                        operation.return_value = json_response(
                            {"httpStatus": status, "message": "Configuration failed"},
                            status=200 if embedded else status)
                        with self.assertRaises(expected):
                            method("Config")

    def test_required_configuration_is_validated(self):
        for method in (self.operations.create_export_job, self.operations.create_import_job):
            with self.subTest(method=method.__name__), self.assertRaises(exc.ValidationError):
                method(None)
        self.assertEqual(self.client.mock_calls, [])


if __name__ == "__main__":
    unittest.main()
