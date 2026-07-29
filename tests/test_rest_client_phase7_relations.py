"""Phase 7: Relations operations - Comprehensive test suite.

Tests for relationship management, cross-references, and links.
Phase 7 focuses on relationship-related operations.
"""

import unittest
import logging
from unittest.mock import Mock, MagicMock, patch, call
from stepxmlclient.rest_client.operations.relations import RelationOperations
from stepxmlclient.rest_client import exceptions as exc
from stepxmlclient.rest_client.models.relations import (
    RelationshipResponse,
    RelationshipListResponse,
    RelationshipCreateRequest,
    RelationshipUpdateRequest,
    RelationshipTypeResponse,
    RelationshipGraphResponse,
    CrossReferenceResponse,
    CrossReferenceListResponse,
    CrossReferenceCreateRequest,
    LinkResponse,
    LinkListResponse,
    LinkCreateRequest,
)
from stepxmlclient.rest_client.exceptions import (
    ValidationError,
    NotFoundError,
    RestApiError,
)




class TestRelationOperationsInit(unittest.TestCase):
    def test_initialization(self):
        mock_client = Mock()
        ops = RelationOperations(mock_client)
        self.assertEqual(ops.operation_name, "RelationOperations")


class TestRelationshipOperations(unittest.TestCase):
    def setUp(self):
        self.mock_client = Mock()
        self.operations = RelationOperations(self.mock_client)

    def test_list_references_products(self):
        mock_op = Mock(return_value={"relationships": [], "totalCount": 0, "limit": 20, "offset": 0})
        setattr(self.mock_client, "getProducts{id}References", mock_op)
        result = self.operations.list_references("products", "PROD1", "RelType")
        self.assertIsNotNone(result)
        call_args = mock_op.call_args
        self.assertEqual(call_args[1]["id"], "PROD1")

    def test_list_references_assets(self):
        mock_op = Mock(return_value={"relationships": [], "totalCount": 0, "limit": 20, "offset": 0})
        setattr(self.mock_client, "getAssets{id}References", mock_op)
        self.operations.list_references("assets", "ASSET1", "RelType")
        mock_op.assert_called_once()

    def test_list_references_classifications(self):
        mock_op = Mock(return_value={"relationships": [], "totalCount": 0, "limit": 20, "offset": 0})
        setattr(self.mock_client, "getClassifications{id}References", mock_op)
        self.operations.list_references("classifications", "CLASS1", "RelType")
        mock_op.assert_called_once()

    def test_list_references_entities(self):
        mock_op = Mock(return_value={"relationships": [], "totalCount": 0, "limit": 20, "offset": 0})
        setattr(self.mock_client, "getEntities{id}References", mock_op)
        self.operations.list_references("entities", "ENT1", "RelType")
        mock_op.assert_called_once()

    def test_get_reference_success(self):
        self.mock_client.getProductReference.return_value = {
            "relationshipId": "REL1", "relationshipType": "RelType",
            "sourceId": "PROD1", "targetId": "PROD2", "sourceType": "products", "targetType": "products"}
        result = self.operations.get_reference("products", "PROD1", "RelType", "PROD2")
        self.assertIsNotNone(result)
        call_args = self.mock_client.getProductReference.call_args
        self.assertEqual(call_args[1]["id"], "PROD1")
        self.assertEqual(call_args[1]["referenceTypeId"], "RelType")
        self.assertEqual(call_args[1]["targetId"], "PROD2")

    def test_get_reference_not_found(self):
        self.mock_client.getProductReference.side_effect = Exception("404 not found")
        with self.assertRaises(exc.NotFoundError):
            self.operations.get_reference("products", "PROD1", "RelType", "PROD2")

    def test_put_reference_success(self):
        self.mock_client.putProductReference.return_value = {
            "relationshipId": "REL1", "relationshipType": "RelType",
            "sourceId": "PROD1", "targetId": "PROD2", "sourceType": "products", "targetType": "products"}
        result = self.operations.put_reference("products", "PROD1", "RelType", "PROD2")
        self.assertTrue(result)
        call_args = self.mock_client.putProductReference.call_args
        self.assertEqual(call_args[1]["id"], "PROD1")
        self.assertEqual(call_args[1]["referenceTypeId"], "RelType")
        self.assertEqual(call_args[1]["targetId"], "PROD2")

    def test_put_reference_with_allow_overwrite(self):
        self.mock_client.putProductReference.return_value = {
            "relationshipId": "REL1", "relationshipType": "RelType",
            "sourceId": "PROD1", "targetId": "PROD2", "sourceType": "products", "targetType": "products"}
        self.operations.put_reference("products", "PROD1", "RelType", "PROD2", allow_overwrite=True)
        call_args = self.mock_client.putProductReference.call_args
        self.assertEqual(call_args[1]["allow-overwrite"], True)

    def test_delete_reference_success(self):
        self.mock_client.deleteProductReference.return_value = None
        result = self.operations.delete_reference("products", "PROD1", "RelType", "PROD2")
        self.assertTrue(result)
        call_args = self.mock_client.deleteProductReference.call_args
        self.assertEqual(call_args[1]["id"], "PROD1")

    def test_delete_reference_not_found(self):
        self.mock_client.deleteProductReference.side_effect = Exception("404 not found")
        with self.assertRaises(exc.NotFoundError):
            self.operations.delete_reference("products", "PROD1", "RelType", "PROD2")

    def test_get_incoming_references(self):
        self.mock_client.getProductIncomingReference.return_value = {
            "relationships": [], "totalCount": 0, "limit": 20, "offset": 0}
        result = self.operations.get_incoming_references("products", "PROD1", "RelType")
        self.assertIsNotNone(result)

    def test_get_reference_type(self):
        self.mock_client.getReferenceType.return_value = {"relationshipTypeId": "RelType", "name": "My Relation"}
        result = self.operations.get_reference_type("RelType")
        self.assertIsNotNone(result)
        call_args = self.mock_client.getReferenceType.call_args
        self.assertEqual(call_args[1]["id"], "RelType")

    def test_invalid_entity_type(self):
        with self.assertRaises(exc.ValidationError):
            self.operations.list_references("invalid_type", "ID1", "RelType")


if __name__ == "__main__":
    unittest.main()
