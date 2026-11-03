"""Regression tests for real HTTP responses from requests-openapi."""

import ast
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock

import requests
from requests.adapters import BaseAdapter

from stepxmlclient.client import BasicAuthorisation
from stepxmlclient.rest_client import StepRestClient, exceptions as exc
from stepxmlclient.rest_client.base import BaseOperation, handle_rest_errors
from stepxmlclient.rest_client.models.asset import AssetResponse
from stepxmlclient.rest_client.models.classification import ClassificationResponse
from stepxmlclient.rest_client.models.entity import EntityResponse
from stepxmlclient.rest_client.models.product import ProductResponse
from stepxmlclient.rest_client.models.relations import RelationshipResponse
from stepxmlclient.rest_client.operations.assets import AssetOperations
from stepxmlclient.rest_client.operations.background_processes import BackgroundProcessOperations
from stepxmlclient.rest_client.operations.classifications import ClassificationOperations
from stepxmlclient.rest_client.operations.collections import CollectionOperations
from stepxmlclient.rest_client.operations.entities import EntityOperations
from stepxmlclient.rest_client.operations.inbound import InboundOperations
from stepxmlclient.rest_client.operations.products import ProductOperations
from stepxmlclient.rest_client.operations.relations import RelationOperations
from stepxmlclient.rest_client.operations.user_groups import UserGroupOperations
from stepxmlclient.rest_client.operations.users import UserOperations
from stepxmlclient.rest_client.operations.workflows import WorkflowOperations
from stepxmlclient.rest_client.publishing import V2PublishingJobBackend
from stepxmlclient.publishing import PublishingError
from tests.test_publishing_client import response


def json_response(payload, status=200, **headers):
    return response(json.dumps(payload).encode(), status=status,
                    **{"Content-Type": "application/json", **headers})


def assert_closed(result: requests.Response) -> None:
    close = result.close
    assert isinstance(close, Mock)
    close.assert_called_once()


DELETE_CASES = (
    (AssetOperations, "delete_asset", ("A",), "deleteAsset"),
    (AssetOperations, "delete_asset_value", ("A", "V"), "deleteAssetValueByAttributeId"),
    (ProductOperations, "delete_product", ("P",), "deleteProduct"),
    (ProductOperations, "delete_product_value", ("P", "V"), "deleteProductValueByAttributeId"),
    (ClassificationOperations, "delete_classification_value", ("C", "V"),
     "deleteClassificationValueByAttributeId"),
    (ClassificationOperations, "delete_classification", ("C",), "deleteClassification"),
    (EntityOperations, "delete_entity", ("E",), "deleteEntity"),
    (EntityOperations, "delete_entity_value", ("E", "V"), "deleteEntityValueByAttributeId"),
    (CollectionOperations, "delete_collection", ("C",), "deleteCollection"),
    (RelationOperations, "delete_reference", ("assets", "A", "R", "T"),
     "deleteAssetReferenceEntryByReferenceTypeIdAndTargetId"),
    (UserOperations, "delete_user", ("U",), "deleteUser"),
    (UserGroupOperations, "delete_user_group", ("G",), "deleteUserGroup"),
    (WorkflowOperations, "delete_workflow_instance", ("W", "I"), "deleteWorkflowInstance"),
)


class TestDeleteResponses(unittest.TestCase):
    def test_all_deletes_reject_http_and_embedded_errors(self):
        for cls, method, args, operation in DELETE_CASES:
            for status in (400, 404, 409, 500):
                for embedded in (False, True):
                    with self.subTest(method=method, status=status, embedded=embedded):
                        payload = {"httpStatus": status, "message": "Referenced object cannot be deleted"}
                        result = json_response(payload, status=200 if embedded else status)
                        client = Mock()
                        getattr(client, operation).return_value = result
                        with self.assertRaises(exc.RestApiError) as caught:
                            getattr(cls(client), method)(*args)
                        self.assertEqual(caught.exception.status_code, status)
                        self.assertEqual(caught.exception.details, payload)
                        self.assertIn(payload["message"], str(caught.exception))
                        assert_closed(result)

    def test_all_deletes_accept_empty_success_responses(self):
        for cls, method, args, operation in DELETE_CASES:
            for status in (200, 202, 204):
                with self.subTest(method=method, status=status):
                    client = Mock()
                    result = response(status=status)
                    getattr(client, operation).return_value = result
                    operations = cls(client, context="C", workspace="Main")
                    self.assertIs(getattr(operations, method)(*args), True)
                    self.assertEqual(getattr(client, operation).call_args.kwargs["context"], "C")
                    assert_closed(result)

    def test_native_error_dict_cannot_be_discarded_by_delete(self):
        client = Mock()
        client.deleteAsset.return_value = {"httpStatus": 400, "message": "Still referenced"}
        with self.assertRaises(exc.RestApiError):
            AssetOperations(client).delete_asset("A")


class TestResponseNormalization(unittest.TestCase):
    def setUp(self):
        self.client = Mock()
        self.operations = BaseOperation(self.client)

    def test_getters_return_models_instead_of_responses(self):
        cases = (
            (AssetOperations, "get_asset", "getAsset", AssetResponse,
             {"id": "A", "classifications": ["C"]}),
            (ProductOperations, "get_product", "getProduct", ProductResponse, {"id": "P"}),
            (ClassificationOperations, "get_classification", "getClassification",
             ClassificationResponse, {"id": "C"}),
            (EntityOperations, "get_entity", "getEntity", EntityResponse, {"id": "E"}),
        )
        for cls, method, operation, model, payload in cases:
            with self.subTest(method=method):
                result = json_response(payload)
                getattr(self.client, operation).return_value = result
                entity = getattr(cls(self.client), method)(payload["id"])
                self.assertIsInstance(entity, model)
                self.assertEqual(entity.id, payload["id"])
                if isinstance(entity, AssetResponse):
                    self.assertEqual(entity.classifications, ["C"])
                assert_closed(result)

    def test_search_convenience_methods_normalize_and_propagate_errors(self):
        cases = (
            (AssetOperations, "search_by_type", ("Type",), "queryAssets"),
            (AssetOperations, "search_modified_since", ("2026-01-01",), "queryAssets"),
            (ProductOperations, "search_by_type", ("Type",), "queryProducts"),
            (ProductOperations, "search_by_id", ("P",), "queryProducts"),
            (ClassificationOperations, "search_by_type", ("Type",), "queryClassifications"),
            (EntityOperations, "search_by_type", ("Type",), "queryEntities"),
        )
        for cls, method, args, operation in cases:
            with self.subTest(method=method, cls=cls):
                getattr(self.client, operation).return_value = json_response(
                    {"items": [{"id": "X"}], "total": 1})
                result = getattr(cls(self.client), method)(*args)
                self.assertEqual(result.items[0].id, "X")
                getattr(self.client, operation).return_value = json_response(
                    {"message": "Search forbidden"}, status=403)
                with self.assertRaises(exc.AuthorizationError):
                    getattr(cls(self.client), method)(*args)

    def test_native_payloads_and_models_are_preserved(self):
        for payload in ({"id": "A"}, [{"id": "A"}], None, AssetResponse.model_validate({"id": "A"})):
            with self.subTest(payload=payload):
                self.assertIs(self.operations._process_response(payload), payload)

    def test_list_payload_and_pagination_are_decoded(self):
        self.client.getItems.return_value = json_response([{"id": "A"}])
        self.assertEqual(self.operations._call_operation("getItems"), [{"id": "A"}])
        self.client.getItems.return_value = json_response({"items": [{"id": "A"}], "total": 3})
        self.assertEqual(self.operations._get_paginated_results("getItems"), ([{"id": "A"}], 3))

    def test_malformed_json_is_explicit_failure_not_empty_success(self):
        self.client.getAsset.return_value = response(b"not json")
        with self.assertRaises(exc.RestClientError):
            AssetOperations(self.client).get_asset("A")
        assert_closed(self.client.getAsset.return_value)

    def test_empty_json_object_is_not_dropped(self):
        self.client.getItems.return_value = json_response({})
        self.assertEqual(self.operations._call_operation("getItems"), {})

    def test_reference_put_always_sends_body_and_returns_model(self):
        for entity_type, prefix in (("assets", "Asset"), ("products", "Product"),
                                    ("classifications", "Classification"), ("entities", "Entity")):
            for data in (None, {}, {"values": {}}):
                with self.subTest(entity_type=entity_type, data=data):
                    operation = getattr(self.client, f"replace{prefix}ReferenceEntryByReferenceTypeIdAndTargetId")
                    operation.reset_mock()
                    operation.return_value = json_response({"target": "T", "targetType": "Asset"})
                    result = RelationOperations(
                        self.client, context="C", workspace="Main"
                    ).put_reference(entity_type, "A", "R", "T", data=data)
                    self.assertIsInstance(result, RelationshipResponse)
                    self.assertEqual(result.target, "T")
                    operation.assert_called_once_with(
                        id="A", referenceTypeId="R", targetId="T",
                        json=data if data is not None else {}, context="C", workspace="Main")


class TestHttpErrors(unittest.TestCase):
    def test_status_mapping_body_and_metadata_for_all_transports(self):
        cases = (
            (400, exc.RestApiError), (401, exc.AuthenticationError),
            (403, exc.AuthorizationError), (404, exc.NotFoundError),
            (409, exc.ConflictError), (413, exc.RestApiError),
            (429, exc.RateLimitError), (500, exc.ServerError), (503, exc.ServerError),
        )
        for status, error_type in cases:
            for transport in ("response", "exception", "dict", "embedded"):
                with self.subTest(status=status, transport=transport):
                    payload = {"httpStatus": status, "message": "Detailed failure",
                               "httpReason": "Rejected", "detail": "Dependency exists"}
                    client = Mock()
                    result = json_response(payload, status=status, **{"Retry-After": "17"})
                    if transport == "exception":
                        client.getAsset.side_effect = requests.HTTPError("HTTP failure", response=result)
                    elif transport == "dict":
                        client.getAsset.return_value = payload
                    else:
                        if transport == "embedded":
                            result.status_code = 200
                        client.getAsset.return_value = result
                    with self.assertRaises(error_type) as caught:
                        AssetOperations(client).get_asset("A")
                    self.assertEqual(caught.exception.status_code, status)
                    self.assertEqual(caught.exception.details, payload)
                    self.assertIn("Detailed failure", str(caught.exception))
                    if isinstance(caught.exception, exc.RateLimitError) and transport in ("response", "exception"):
                        self.assertEqual(caught.exception.retry_after, "17")

    def test_text_and_non_object_json_errors_include_reason(self):
        for result in (response(b"Proxy unavailable", status=502),
                       json_response("Proxy unavailable", status=502),
                       json_response(["Proxy unavailable"], status=502)):
            with self.subTest(result=result):
                client = Mock()
                client.getAsset.return_value = result
                with self.assertRaises(exc.ServerError) as caught:
                    AssetOperations(client).get_asset("A")
                self.assertIn("Proxy unavailable", str(caught.exception))
                assert_closed(result)

    def test_decorator_also_checks_raw_http_responses(self):
        @handle_rest_errors
        def operation():
            return json_response({"message": "Not allowed"}, status=400)

        with self.assertRaises(exc.RestApiError):
            operation()

    def test_falsey_nested_response_is_checked_without_truthiness(self):
        result = Mock()
        result._response = json_response({"message": "Missing"}, status=404)
        operation = BaseOperation(Mock())
        with self.assertRaises(exc.NotFoundError):
            operation._check_response_status(result, "A", "Asset")

    def test_status_only_response_like_objects_are_checked(self):
        operation = BaseOperation(Mock())
        result = SimpleNamespace(status_code=400, text="Rejected by STEP")
        with self.assertRaises(exc.RestApiError) as caught:
            operation._check_response_status(result)
        self.assertIn("Rejected by STEP", str(caught.exception))

    def test_message_digits_do_not_override_structured_status(self):
        client = Mock()
        client.getAsset.return_value = json_response(
            {"message": "Object 404 has a conflict"}, status=409)
        with self.assertRaises(exc.ConflictError) as caught:
            AssetOperations(client).get_asset("404")
        self.assertEqual(caught.exception.status_code, 409)

    def test_network_and_timeout_errors_are_not_successful(self):
        client = Mock()
        for error, expected in ((requests.ConnectionError("Offline"), exc.RestClientError),
                                (requests.Timeout("Too slow"), exc.TimeoutError)):
            with self.subTest(error=error):
                client.deleteAsset.side_effect = error
                with self.assertRaises(expected):
                    AssetOperations(client).delete_asset("A")

    def test_inbound_direct_request_checks_error_body(self):
        client = Mock()
        client.server.url = "https://step.invalid/restapiv2"
        client.requestor.post.return_value = json_response(
            {"message": "Endpoint disabled"}, status=400)
        with self.assertRaises(exc.RestApiError) as caught:
            InboundOperations(client).upload_and_invoke("I", b"<STEP-ProductInformation/>")
        self.assertIn("Endpoint disabled", str(caught.exception))
        assert_closed(client.requestor.post.return_value)

    def test_publishing_adapter_preserves_structured_status(self):
        client = Mock()
        backend = V2PublishingJobBackend(BackgroundProcessOperations(client))
        cases = (
            ("getBackgroundProcess", backend.get_status, ("B",)),
            ("getBackgroundProcessAttachmentsMetadata", backend.list_files, ("B",)),
            ("getBackgroundProcessAttachmentContent", backend.get_file, ("B", "A")),
        )
        for operation, method, args in cases:
            with self.subTest(operation=operation):
                getattr(client, operation).return_value = json_response({"message": "Forbidden"}, status=403)
                with self.assertRaises(PublishingError) as caught:
                    method(*args, timeout=1)
                self.assertEqual(caught.exception.status_code, 403)
                self.assertIsInstance(caught.exception.__cause__, exc.AuthorizationError)


class TestBinaryResponses(unittest.TestCase):
    def test_asset_download_keeps_binary_content(self):
        client = Mock()
        result = response(b"%PDF\x00\xff")
        result.headers["Content-Type"] = "application/pdf"
        client.getAssetContent.return_value = result
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "asset.pdf"
            AssetOperations(client).download_asset_content("A", output_path=str(target))
            self.assertEqual(target.read_bytes(), b"%PDF\x00\xff")
        assert_closed(client.getAssetContent.return_value)

    def test_error_download_does_not_overwrite_existing_file(self):
        client = Mock()
        client.getAssetContent.return_value = json_response({"message": "Missing"}, status=404)
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "asset.pdf"
            target.write_bytes(b"existing")
            with self.assertRaises(exc.NotFoundError):
                AssetOperations(client).download_asset_content("A", output_path=str(target))
            self.assertEqual(target.read_bytes(), b"existing")

    def test_embedded_json_error_is_not_saved_as_binary(self):
        client = Mock()
        client.getAssetContent.return_value = json_response({"httpStatus": 400, "message": "No content"})
        with self.assertRaises(exc.RestApiError):
            AssetOperations(client).download_asset_content("A")


class TestGroupedTransportContract(unittest.TestCase):
    def test_generated_calls_use_shared_helper(self):
        directory = Path(__file__).resolve().parents[1] / "stepxmlclient" / "rest_client" / "operations"
        for path in directory.glob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8-sig"))
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
                    continue
                with self.subTest(path=path.name, line=node.lineno):
                    self.assertNotEqual(ast.unparse(node.func.value), "self.client")


class TestRealOpenApiTransport(unittest.TestCase):
    def test_get_delete_and_empty_put_through_requests_openapi(self):
        paths = {}
        for path, methods in (
            ("/assets/{id}", {"get": "getAsset", "delete": "deleteAsset"}),
            ("/assets/{id}/references/{referenceTypeId}/{targetId}",
             {"put": "replaceAssetReferenceEntryByReferenceTypeIdAndTargetId"}),
        ):
            paths[path] = {}
            for method, operation in methods.items():
                parameters = [
                    {"name": name, "in": "path", "required": True, "schema": {"type": "string"}}
                    for name in ("id", "referenceTypeId", "targetId") if "{" + name + "}" in path
                ]
                entry = {"operationId": operation, "parameters": parameters,
                         "responses": {"200": {"description": "Synthetic response"}}}
                if method == "put":
                    entry["requestBody"] = {"required": True, "content": {
                        "application/json": {"schema": {"type": "object"}}}}
                paths[path][method] = entry
        spec = {"openapi": "3.0.3", "info": {"title": "Synthetic", "version": "1"},
                "servers": [{"url": "/restapiv2"}], "paths": paths}

        class Adapter(BaseAdapter):
            def send(self, request, **_kwargs):
                if request.method == "DELETE":
                    result = json_response({"message": "Asset is referenced"}, status=400)
                elif request.method == "PUT":
                    self.put_body = request.body
                    result = json_response({"target": "T", "targetType": "Asset"})
                else:
                    result = json_response({"id": "A", "classifications": ["C"]})
                result.request = request
                result.url = request.url
                return result

            def close(self):
                pass

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "synthetic.json"
            path.write_text(json.dumps(spec), encoding="utf-8")
            client = StepRestClient(
                "https://step.invalid/restapiv2", BasicAuthorisation("user", "pwd"),
                openapi_file=str(path))
            session = client.client.requestor
            assert isinstance(session, requests.Session)
            self.addCleanup(session.close)
            adapter = Adapter()
            session.mount("https://", adapter)
            self.assertEqual(client.assets.get_asset("A").classifications, ["C"])
            with self.assertRaises(exc.RestApiError) as caught:
                client.assets.delete_asset("A")
            self.assertIn("Asset is referenced", str(caught.exception))
            self.assertEqual(client.relations.put_reference("assets", "A", "R", "T", {}).target, "T")
            self.assertEqual(json.loads(adapter.put_body), {})


if __name__ == "__main__":
    unittest.main()
