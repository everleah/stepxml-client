"""Operation contracts verified against STEP v1.4.0, without distributing its spec."""

import ast
import json
from pathlib import Path
import re
from typing import Any
import unittest
from urllib.parse import parse_qs, urlsplit

import requests
from requests.adapters import BaseAdapter
import requests_openapi as roa

from stepxmlclient.rest_client import exceptions as exc
from stepxmlclient.rest_client.models.classification import (
    ClassificationCreateRequest, ClassificationUpdateRequest,
)
from stepxmlclient.rest_client.models.entity import EntityCreateRequest, EntityUpdateRequest
from stepxmlclient.rest_client.operations.assets import AssetOperations
from stepxmlclient.rest_client.operations.attributes import AttributeOperations
from stepxmlclient.rest_client.operations.classifications import ClassificationOperations
from stepxmlclient.rest_client.operations.entities import EntityOperations
from stepxmlclient.rest_client.operations.products import ProductOperations
from stepxmlclient.rest_client.operations.relations import RelationOperations
from tests.test_rest_response_handling import json_response, response


# Independently specified endpoint contracts, not derived from wrapper implementation.
CONTRACTS = (
    ("post", "/products/search", "queryProducts"),
    ("post", "/assets/search", "queryAssets"),
    ("post", "/classifications/search", "queryClassifications"),
    ("post", "/entities/search", "queryEntities"),
    ("get", "/list-of-values/{id}", "getListOfValues"),
    ("get", "/list-of-values/{id}/value-entries", "getListOfValuesEntries"),
    ("post", "/classifications", "createClassification"),
    ("patch", "/classifications/{id}", "updateClassification"),
    ("put", "/classifications/{id}", "createOrReplaceClassification"),
    ("delete", "/classifications/{id}", "deleteClassification"),
    ("get", "/classifications/{id}/children", "getClassificationChildren"),
    ("post", "/entities", "createEntity"),
    ("patch", "/entities/{id}", "updateEntity"),
    ("put", "/entities/{id}", "createOrReplaceEntity"),
    ("delete", "/entities/{id}", "deleteEntity"),
    ("get", "/products/{id}/references/{referenceTypeId}", "getProductReferenceByReferenceTypeId"),
    ("get", "/assets/{id}/references/{referenceTypeId}", "getAssetReferencesByReferenceTypeId"),
    ("get", "/classifications/{id}/references/{referenceTypeId}", "getClassificationReferenceByReferenceTypeId"),
    ("get", "/entities/{id}/references/{referenceTypeId}", "getEntityReferenceByReferenceTypeId"),
)


def synthetic_spec():
    paths = {}
    for method, path, operation in CONTRACTS:
        parameters = [
            {"in": "path", "name": name, "required": True, "schema": {"type": "string"}}
            for name in re.findall(r"\{(\w+)\}", path)
        ]
        parameters.extend(
            {"in": "query", "name": name, "required": name == "context",
             "schema": {"type": "boolean" if name == "allow-overwrite" else "string"}}
            for name in ("context", "workspace", "keyId", "allow-overwrite")
            if name in ("context", "workspace") or
            name == "keyId" and "{id}" in path or
            name == "allow-overwrite" and method == "put"
        )
        entry = {"operationId": operation, "parameters": parameters,
                 "responses": {"200": {"description": "Synthetic response"}}}
        if method in ("post", "put", "patch"):
            entry["requestBody"] = {"content": {
                "application/json": {"schema": {"type": "object"}}}}
        paths.setdefault(path, {})[method] = entry
    return {"openapi": "3.0.3", "info": {"title": "Synthetic contracts", "version": "1"},
            "servers": [{"url": "/restapiv2"}], "paths": paths}


class Adapter(BaseAdapter):
    def __init__(self):
        self.payload: dict[str, Any] | list[Any] | None = None
        self.status = 200
        self.calls = []

    def send(self, request, **_kwargs):
        self.calls.append(request)
        result = (response(status=self.status) if self.payload is None
                  else json_response(self.payload, status=self.status))
        result.request = request
        result.url = request.url
        return result

    def close(self):
        pass


class TestSpecTransport(unittest.TestCase):
    def specification(self):
        return synthetic_spec()

    def setUp(self):
        self.client = roa.Client()
        self.client.load_spec(self.specification())
        self.client.set_server(roa.Server(url="https://step.invalid/restapiv2"))
        session = self.client.requestor
        assert isinstance(session, requests.Session)
        self.addCleanup(session.close)
        self.adapter = Adapter()
        session.mount("https://", self.adapter)

    def assert_request(self, method, path, *, body=None, **query):
        request = self.adapter.calls[-1]
        self.assertEqual(request.method, method)
        parts = urlsplit(request.url)
        self.assertEqual(parts.path, "/restapiv2" + path)
        actual_query = parse_qs(parts.query)
        for name, value in query.items():
            if isinstance(value, bool) and name in actual_query:
                actual_query[name] = [item.lower() for item in actual_query[name]]
        self.assertEqual(actual_query, {
            "context": ["C"], "workspace": ["Main"],
            **{name: [str(value).lower() if isinstance(value, bool) else str(value)]
               for name, value in query.items()},
        })
        if body is not None:
            self.assertEqual(json.loads(request.body), body)
        else:
            self.assertIsNone(request.body)

    def test_search_arrays_are_wrapped_without_fetching_full_objects(self):
        for cls, method, group in (
            (ProductOperations, "search_products", "products"),
            (AssetOperations, "search_assets", "assets"),
            (ClassificationOperations, "search_classifications", "classifications"),
            (EntityOperations, "search_entities", "entities"),
        ):
            supertype = {"products": "product", "assets": "asset",
                         "classifications": "classification", "entities": "entity"}[group]
            for payload in ([{"id": "X", "type": supertype}], []):
                with self.subTest(group=group, payload=payload):
                    self.adapter.payload = payload
                    operations = cls(self.client, context="C", workspace="Main")
                    condition = {"conditionType": "objecttype", "objectType": "Type"}
                    calls_before = len(self.adapter.calls)
                    result = getattr(operations, method)(condition)
                    self.assertEqual([item.id for item in result.items],
                                     [item["id"] for item in payload])
                    self.assertEqual(len(self.adapter.calls), calls_before + 1)
                    self.assertIsNone(result.total)
                    self.assert_request("POST", f"/{group}/search", body={"condition": condition})

    def test_classification_and_entity_crud(self):
        for cls, group, create_model, update_model in (
            (ClassificationOperations, "classification", ClassificationCreateRequest, ClassificationUpdateRequest),
            (EntityOperations, "entity", EntityCreateRequest, EntityUpdateRequest),
        ):
            with self.subTest(group=group):
                plural = "classifications" if group == "classification" else "entities"
                operations = cls(self.client, context="C", workspace="Main")
                data = create_model.model_validate({"objectType": "Type", "parent": "Root"})
                self.adapter.payload = {"id": "X", "objectType": "Type", "parent": "Root"}
                created = getattr(operations, f"create_{group}")(data)
                self.assertEqual(created.id, "X")
                self.assert_request("POST", f"/{plural}", body={"objectType": "Type", "parent": "Root"})
                updates = update_model.model_validate({"name": "Changed"})
                self.adapter.payload = {"id": "X", "name": "Changed"}
                updated = getattr(operations, f"update_{group}")("X", updates, key_id="Key")
                self.assertEqual(updated.name, "Changed")
                self.assert_request("PATCH", f"/{plural}/X", body={"name": "Changed"}, keyId="Key")
                replaced = getattr(operations, f"replace_{group}")(
                    "X", data, key_id="Key", allow_overwrite=True)
                self.assertEqual(replaced.id, "X")
                self.assert_request("PUT", f"/{plural}/X", body={"objectType": "Type", "parent": "Root"},
                                    keyId="Key", **{"allow-overwrite": True})
                self.adapter.payload = None
                self.assertTrue(getattr(operations, f"delete_{group}")("X", key_id="Key"))
                self.assert_request("DELETE", f"/{plural}/X", keyId="Key")
                self.adapter.payload = {"message": "Referenced"}
                self.adapter.status = 400
                with self.assertRaises(exc.RestApiError):
                    getattr(operations, f"delete_{group}")("X")
                self.adapter.status = 200

    def test_classification_attribute_links_are_arrays(self):
        operations = ClassificationOperations(self.client, context="C", workspace="Main")
        payload = {"objectType": "Type", "parent": "Root", "attributeLinks": [{"attribute": "Color"}]}
        self.adapter.payload = {"id": "X", **payload}
        result = operations.create_classification(ClassificationCreateRequest.model_validate(payload))
        self.assertEqual(result.attributeLinks, [{"attribute": "Color"}])
        self.assert_request("POST", "/classifications", body=payload)

    def test_children_and_lov_shapes(self):
        self.adapter.payload = ["Child"]
        result = ClassificationOperations(
            self.client, context="C", workspace="Main").get_classification_children("Root", key_id="Key")
        self.assertEqual(result, ["Child"])
        self.assert_request("GET", "/classifications/Root/children", keyId="Key")
        operations = AttributeOperations(self.client, context="C", workspace="Main")
        metadata = {"Label": {"value": {"value": "Colors"}}}
        self.adapter.payload = {"id": "Colors", "values": metadata}
        self.assertEqual(operations.get_list_of_values("Colors").values, metadata)
        self.assert_request("GET", "/list-of-values/Colors")
        self.adapter.payload = [{"valueId": "RED", "value": "Red"}]
        self.assertEqual(operations.get_list_of_values_entries("Colors"), self.adapter.payload)
        self.assert_request("GET", "/list-of-values/Colors/value-entries")

    def test_reference_list_names_for_all_source_types(self):
        self.adapter.payload = {"relationships": []}
        operations = RelationOperations(self.client, context="C", workspace="Main")
        for group in ("products", "assets", "classifications", "entities"):
            with self.subTest(group=group):
                self.assertEqual(operations.list_references(group, "X", "R").relationships, [])
                self.assert_request("GET", f"/{group}/X/references/R")


class TestAuthorizedLocalSpecification(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parents[1]
        paths = (root / "openapi.json", root / "stepxmlclient" / "openapi.json")
        cls.specifications = [json.loads(path.read_text(encoding="utf-8-sig"))
                              for path in paths if path.is_file()]
        if not cls.specifications:
            raise unittest.SkipTest("Optional authorized STEP OpenAPI specification is not available")
        cls.root = root

    def test_independent_contracts_match_local_specification(self):
        for specification in self.specifications:
            for method, path, operation in CONTRACTS:
                with self.subTest(operation=operation):
                    self.assertEqual(specification["paths"][path][method]["operationId"], operation)

    def test_static_wrapper_calls_exist_in_local_specification(self):
        for specification in self.specifications:
            operations = {
                operation["operationId"] for item in specification["paths"].values()
                for operation in item.values()
                if isinstance(operation, dict) and "operationId" in operation
            }
            for path in (self.root / "stepxmlclient" / "rest_client" / "operations").glob("*.py"):
                for node in ast.walk(ast.parse(path.read_text(encoding="utf-8-sig"))):
                    if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                            and node.func.attr in ("_call_operation", "_get_paginated_results")
                            and node.args and isinstance(node.args[0], ast.Constant)):
                        with self.subTest(file=path.name, line=node.lineno):
                            self.assertIn(node.args[0].value, operations)


class TestAuthorizedSpecTransport(TestSpecTransport):
    def specification(self):
        path = Path(__file__).resolve().parents[1] / "openapi.json"
        if not path.is_file():
            self.skipTest("Optional authorized STEP OpenAPI specification is not available")
        return json.loads(path.read_text(encoding="utf-8-sig"))


if __name__ == "__main__":
    unittest.main()
