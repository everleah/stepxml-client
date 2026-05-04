"""Tests for Classification operations in STEP REST API v2."""

import unittest
import logging
from unittest.mock import MagicMock, Mock, patch
from stepxmlclient.rest_client import exceptions as exc

from stepxmlclient.rest_client.models.classification import (
    ClassificationResponse,
    ClassificationListResponse,
    ClassificationCreateRequest,
    ClassificationUpdateRequest,
)
from stepxmlclient.rest_client.operations.classifications import ClassificationOperations
from stepxmlclient.rest_client import exceptions as exc


class TestClassificationModels(unittest.TestCase):
    """Test classification model creation and validation."""

    def test_classification_response_creation(self):
        """Test creating a classification response with OpenAPI fields."""
        classification = ClassificationResponse(id="CLASS1")

        self.assertEqual(classification.id, "CLASS1")
        self.assertIsNone(classification.objectType)
        self.assertIsNone(classification.parent)

    def test_classification_response_with_all_fields(self):
        """Test classification response with all optional fields."""
        classification = ClassificationResponse(
            id="CLASS1",
            objectType="WebCategory",
            name="Color",
            parent="WebRoot",
            values={"colorCode": {"value": "RED"}},
        )

        self.assertEqual(classification.id, "CLASS1")
        self.assertEqual(classification.objectType, "WebCategory")
        self.assertEqual(classification.parent, "WebRoot")

    def test_classification_list_response(self):
        """Test classification list response."""
        list_response = ClassificationListResponse(
            items=[
                ClassificationResponse(id="CLASS1"),
                ClassificationResponse(id="CLASS2"),
            ],
            total=2
        )

        self.assertEqual(len(list_response.items), 2)
        self.assertEqual(list_response.total, 2)

    def test_classification_list_response_defaults(self):
        """Test list response default values."""
        list_response = ClassificationListResponse()

        self.assertEqual(list_response.items, [])
        self.assertIsNone(list_response.total)

    def test_classification_create_request(self):
        """Test classification create request requires objectType and parent."""
        create = ClassificationCreateRequest(
            objectType="WebCategory",
            parent="WebRoot",
            name="Material",
        )

        self.assertEqual(create.objectType, "WebCategory")
        self.assertEqual(create.parent, "WebRoot")
        self.assertEqual(create.name, "Material")
        self.assertIsNone(create.values)

    def test_classification_create_request_no_id(self):
        """Test classification create request has no id field."""
        create = ClassificationCreateRequest(objectType="WebCategory", parent="WebRoot")
        data = create.model_dump(exclude_none=True)
        self.assertNotIn("id", data)

    def test_classification_update_request(self):
        """Test classification update request allows partial updates."""
        update = ClassificationUpdateRequest(name="Updated Name")

        self.assertEqual(update.name, "Updated Name")
        self.assertIsNone(update.parent)
        self.assertIsNone(update.values)




class TestClassificationOperations(unittest.TestCase):
    def setUp(self):
        self.mock_client = Mock()
        self.logger = logging.getLogger(__name__)
        self.operations = ClassificationOperations(self.mock_client, logger=self.logger)

    def test_initialization(self):
        self.assertEqual(self.operations.operation_name, "ClassificationOperations")

    def test_get_classification_success(self):
        self.mock_client.getClassification.return_value = {
            "id": "CLASS1", "user_type_id": "ClassType", "name": "Root"}
        result = self.operations.get_classification("CLASS1")
        self.assertEqual(result.id, "CLASS1")
        call_args = self.mock_client.getClassification.call_args
        self.assertEqual(call_args[1]["id"], "CLASS1")
        self.assertNotIn("classificationId", call_args[1])

    def test_get_classification_not_found(self):
        self.mock_client.getClassification.side_effect = Exception("404 not found")
        with self.assertRaises(exc.NotFoundError):
            self.operations.get_classification("NONEXISTENT")

    def test_get_classification_validation(self):
        with self.assertRaises(exc.ValidationError):
            self.operations.get_classification(None)

    def test_get_classification_with_key_id(self):
        self.mock_client.getClassification.return_value = {"id": "CLASS1", "name": "Root"}
        self.operations.get_classification("CLASS1", key_id="MyKey")
        call_args = self.mock_client.getClassification.call_args
        self.assertEqual(call_args[1]["keyId"], "MyKey")

    def test_get_classification_with_include_inherited(self):
        self.mock_client.getClassification.return_value = {"id": "CLASS1", "name": "Root"}
        self.operations.get_classification("CLASS1", include_inherited_data=True)
        call_args = self.mock_client.getClassification.call_args
        self.assertEqual(call_args[1]["includeInheritedData"], True)

    def test_search_classifications_success(self):
        self.mock_client.postClassificationsSearch.return_value = {
            "items": [{"id": "CLASS1"}, {"id": "CLASS2"}], "total": 2}
        condition = {"conditionType": "objecttype", "objectType": "ClassType"}
        result = self.operations.search_classifications(condition=condition)
        self.assertEqual(len(result.items), 2)
        call_args = self.mock_client.postClassificationsSearch.call_args
        self.assertEqual(call_args[1]["json"]["condition"], condition)

    def test_search_classifications_requires_condition(self):
        with self.assertRaises(exc.ValidationError):
            self.operations.search_classifications(condition=None)

    def test_create_classification_success(self):
        self.mock_client.postClassifications.return_value = {"id": "NEWCLASS"}
        request = ClassificationCreateRequest(objectType="WebCategory", parent="WebRoot", name="New")
        result = self.operations.create_classification(request)
        self.assertEqual(result.id, "NEWCLASS")
        self.mock_client.postClassifications.assert_called_once()
        call_args = self.mock_client.postClassifications.call_args
        payload = call_args[1]["json"]
        self.assertNotIn("id", payload)
        self.assertEqual(payload["objectType"], "WebCategory")

    def test_create_classification_conflict(self):
        self.mock_client.postClassifications.side_effect = Exception("409 conflict")
        request = ClassificationCreateRequest(objectType="WebCategory", parent="WebRoot")
        with self.assertRaises(exc.ConflictError):
            self.operations.create_classification(request)

    def test_update_classification_success(self):
        self.mock_client.patchClassification.return_value = {"id": "CLASS1", "name": "Updated"}
        updates = ClassificationUpdateRequest(name="Updated")
        result = self.operations.update_classification("CLASS1", updates)
        self.assertEqual(result.name, "Updated")
        call_args = self.mock_client.patchClassification.call_args
        self.assertEqual(call_args[1]["id"], "CLASS1")

    def test_update_classification_not_found(self):
        self.mock_client.patchClassification.side_effect = Exception("404 not found")
        updates = ClassificationUpdateRequest(name="Updated")
        with self.assertRaises(exc.NotFoundError):
            self.operations.update_classification("NONEXISTENT", updates)

    def test_replace_classification_success(self):
        self.mock_client.putClassification.return_value = {"id": "CLASS1"}
        data = ClassificationCreateRequest(objectType="WebCategory", parent="WebRoot")
        result = self.operations.replace_classification("CLASS1", data)
        self.assertEqual(result.id, "CLASS1")
        call_args = self.mock_client.putClassification.call_args
        self.assertEqual(call_args[1]["id"], "CLASS1")

    def test_replace_classification_with_allow_overwrite(self):
        self.mock_client.putClassification.return_value = {"id": "CLASS1"}
        data = ClassificationCreateRequest(objectType="WebCategory", parent="WebRoot")
        self.operations.replace_classification("CLASS1", data, allow_overwrite=True)
        call_args = self.mock_client.putClassification.call_args
        self.assertEqual(call_args[1]["allow-overwrite"], True)

    def test_delete_classification_success(self):
        self.mock_client.deleteClassification.return_value = None
        result = self.operations.delete_classification("CLASS1")
        self.assertTrue(result)
        call_args = self.mock_client.deleteClassification.call_args
        self.assertEqual(call_args[1]["id"], "CLASS1")

    def test_delete_classification_not_found(self):
        self.mock_client.deleteClassification.side_effect = Exception("404 not found")
        with self.assertRaises(exc.NotFoundError):
            self.operations.delete_classification("NONEXISTENT")

    def test_get_classification_children(self):
        self.mock_client.getClassificationChildren.return_value = ["CHILD1", "CHILD2"]
        result = self.operations.get_classification_children("CLASS1")
        self.assertIsInstance(result, list)
        call_args = self.mock_client.getClassificationChildren.call_args
        self.assertEqual(call_args[1]["id"], "CLASS1")

    def test_search_by_type(self):
        self.mock_client.postClassificationsSearch.return_value = {"items": [], "total": 0}
        self.operations.search_by_type("ClassType")
        call_args = self.mock_client.postClassificationsSearch.call_args
        payload = call_args[1]["json"]
        self.assertEqual(payload["condition"]["conditionType"], "objecttype")
        self.assertEqual(payload["condition"]["objectType"], "ClassType")

    def test_list_classifications(self):
        self.mock_client.postClassificationsSearch.return_value = {"items": [], "total": 0}
        self.operations.list_classifications()
        self.mock_client.postClassificationsSearch.assert_called_once()


if __name__ == "__main__":
    unittest.main()

