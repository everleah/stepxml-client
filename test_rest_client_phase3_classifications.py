"""Tests for Classification operations in STEP REST API v2."""

import unittest
import logging
from unittest.mock import MagicMock, Mock, patch
from datetime import datetime
from stepxmlclient.rest_client import exceptions as exc

from stepxmlclient.rest_client.models.classification import (
    ClassificationResponse,
    ClassificationListResponse,
    ClassificationHierarchyResponse,
    ClassificationSearchRequest,
    ClassificationCreateRequest,
    ClassificationUpdateRequest,
    ClassificationValueResponse,
    ClassificationValue,
    ClassificationMetadata,
    ClassificationHierarchyNode,
)
from stepxmlclient.rest_client.operations.classifications import ClassificationOperations
from stepxmlclient.rest_client.models.common import PageInfo
from stepxmlclient.rest_client import exceptions as exc


class TestClassificationModels(unittest.TestCase):
    """Test classification model creation and validation."""
    
    def test_classification_response_creation(self):
        """Test creating a classification response."""
        classification = ClassificationResponse(
            id="CLASS1",
            name="Color",
            description="Product color",
            is_hierarchical=False,
            classification_type=None,
            is_system_owned=False,
            values_count=None,
            metadata=None
        )
        
        self.assertEqual(classification.id, "CLASS1")
        self.assertEqual(classification.name, "Color")
        self.assertEqual(classification.description, "Product color")
        self.assertFalse(classification.is_hierarchical)
    
    def test_classification_response_with_metadata(self):
        """Test classification response with metadata."""
        metadata = ClassificationMetadata(
            created_at=datetime.fromisoformat("2025-01-15T10:30:00+00:00"),
            created_by="admin",
            modified_at=None,
            modified_by=None,
            version=1
        )
        classification = ClassificationResponse(
            id="CLASS1",
            name="Color",
            description=None,
            classification_type=None,
            is_hierarchical=False,
            is_system_owned=False,
            values_count=None,
            metadata=metadata
        )
        
        self.assertEqual(classification.metadata.created_by, "admin") #type: ignore
        self.assertEqual(classification.metadata.version, 1) #type: ignore
    
    def test_classification_list_response(self):
        """Test classification list response."""
        list_response = ClassificationListResponse(
            items=[
                ClassificationResponse(id="CLASS1", name="Color", description=None, classification_type=None, is_hierarchical=False, is_system_owned=False, values_count=None, metadata=None),
                ClassificationResponse(id="CLASS2", name="Size", description=None, classification_type=None, is_hierarchical=False, is_system_owned=False, values_count=None, metadata=None),
            ],
            pagination=None,
            total=2
        )
        
        self.assertEqual(len(list_response.items), 2)
        self.assertEqual(list_response.total, 2)
    
    def test_classification_list_response_with_pagination(self):
        """Test list response with pagination info."""
        pagination = PageInfo(limit=20, offset=0, total=50)
        list_response = ClassificationListResponse(
            items=[],
            pagination=pagination,
            total=50
        )
        
        self.assertEqual(list_response.pagination.limit, 20) #type: ignore
        self.assertEqual(list_response.pagination.total, 50) #type: ignore
        self.assertTrue(list_response.pagination.has_more) #type: ignore
    
    def test_classification_hierarchy_node(self):
        """Test classification hierarchy node."""
        child = ClassificationHierarchyNode(
            id="CHILD1",
            name="Red",
            parent_id="ROOT",
            level=1,
            metadata=None
        )
        
        root = ClassificationHierarchyNode(
            id="ROOT",
            name="Colors",
            level=0,
            parent_id=None,
            children=[child],
            metadata=None
        )
        
        self.assertEqual(root.id, "ROOT")
        self.assertEqual(len(root.children), 1)
        self.assertEqual(root.children[0].parent_id, "ROOT")
    
    def test_classification_hierarchy_response(self):
        """Test classification hierarchy response."""
        response = ClassificationHierarchyResponse(
            classification_id="CLASS1",
            classification_name="Color",
            root_nodes=[
                ClassificationHierarchyNode(id="ROOT", name="Colors", level=0, parent_id=None, metadata=None)
            ],
            total_nodes=10,
            max_depth=3
        )
        
        self.assertEqual(response.classification_id, "CLASS1")
        self.assertEqual(response.total_nodes, 10)
        self.assertEqual(response.max_depth, 3)
    
    def test_classification_search_request(self):
        """Test classification search request."""
        search = ClassificationSearchRequest(
            query="color",
            limit=50,
            offset=0,
            type_filter="Standard",
            include_values=False
        )
        
        self.assertEqual(search.query, "color")
        self.assertEqual(search.limit, 50)
        self.assertEqual(search.type_filter, "Standard")
    
    def test_classification_create_request(self):
        """Test classification create request."""
        create = ClassificationCreateRequest(
            id="NEW_CLASS",
            name="Material",
            description="Product material",
            is_hierarchical=True,
            classification_type=None,
            attributes=None
        )
        
        self.assertEqual(create.id, "NEW_CLASS")
        self.assertEqual(create.name, "Material")
        self.assertTrue(create.is_hierarchical)
    
    def test_classification_update_request(self):
        """Test classification update request."""
        update = ClassificationUpdateRequest(
            name="Updated Name",
            description="Updated description",
            classification_type=None,
            attributes=None
        )
        
        self.assertEqual(update.name, "Updated Name")
        self.assertEqual(update.description, "Updated description")
    
    def test_classification_value(self):
        """Test classification value model."""
        value = ClassificationValue(
            id="VAL1",
            name="Red",
            description="Red color",
            parent_id=None,
            is_leaf=True
        )
        
        self.assertEqual(value.id, "VAL1")
        self.assertEqual(value.name, "Red")
        self.assertTrue(value.is_leaf)
    
    def test_classification_value_response(self):
        """Test classification value response."""
        response = ClassificationValueResponse(
            classification_id="CLASS1",
            values=[
                ClassificationValue(id="VAL1", name="Red", description=None, parent_id=None, is_leaf=False),
                ClassificationValue(id="VAL2", name="Blue", description=None, parent_id=None, is_leaf=False),
            ],
            total=2
        )
        """Test classification value response."""
        response = ClassificationValueResponse(
            classification_id="CLASS1",
            values=[
                ClassificationValue(id="VAL1", name="Red", description=None, parent_id=None, is_leaf=False),
                ClassificationValue(id="VAL2", name="Blue", description=None, parent_id=None, is_leaf=False),
            ],
            total=2
        )
        
        self.assertEqual(response.classification_id, "CLASS1")
        self.assertEqual(len(response.values), 2)
        self.assertEqual(response.total, 2)




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
            "items": [{"id": "CLASS1", "name": "Class 1"}, {"id": "CLASS2", "name": "Class 2"}], "total": 2}
        condition = {"conditionType": "objecttype", "objectTypeId": "ClassType"}
        result = self.operations.search_classifications(condition=condition)
        self.assertEqual(len(result.items), 2)
        call_args = self.mock_client.postClassificationsSearch.call_args
        self.assertEqual(call_args[1]["body"]["condition"], condition)

    def test_search_classifications_requires_condition(self):
        with self.assertRaises(exc.ValidationError):
            self.operations.search_classifications(condition=None)

    def test_create_classification_success(self):
        self.mock_client.postClassifications.return_value = {"id": "NEWCLASS", "name": "New"}
        from stepxmlclient.rest_client.models.classification import ClassificationCreateRequest
        request = ClassificationCreateRequest(id="NEWCLASS", name="New")
        result = self.operations.create_classification(request)
        self.assertEqual(result.id, "NEWCLASS")
        self.mock_client.postClassifications.assert_called_once()

    def test_create_classification_conflict(self):
        self.mock_client.postClassifications.side_effect = Exception("409 conflict")
        from stepxmlclient.rest_client.models.classification import ClassificationCreateRequest
        request = ClassificationCreateRequest(id="EXISTING", name="Existing")
        with self.assertRaises(exc.ConflictError):
            self.operations.create_classification(request)

    def test_update_classification_success(self):
        self.mock_client.patchClassification.return_value = {"id": "CLASS1", "name": "Updated"}
        from stepxmlclient.rest_client.models.classification import ClassificationUpdateRequest
        updates = ClassificationUpdateRequest(name="Updated")
        result = self.operations.update_classification("CLASS1", updates)
        self.assertEqual(result.name, "Updated")
        call_args = self.mock_client.patchClassification.call_args
        self.assertEqual(call_args[1]["id"], "CLASS1")

    def test_update_classification_not_found(self):
        self.mock_client.patchClassification.side_effect = Exception("404 not found")
        from stepxmlclient.rest_client.models.classification import ClassificationUpdateRequest
        updates = ClassificationUpdateRequest(name="Updated")
        with self.assertRaises(exc.NotFoundError):
            self.operations.update_classification("NONEXISTENT", updates)

    def test_replace_classification_success(self):
        self.mock_client.putClassification.return_value = {"id": "CLASS1", "name": "Root"}
        from stepxmlclient.rest_client.models.classification import ClassificationCreateRequest
        data = ClassificationCreateRequest(id="CLASS1", name="Root")
        result = self.operations.replace_classification("CLASS1", data)
        self.assertEqual(result.id, "CLASS1")
        call_args = self.mock_client.putClassification.call_args
        self.assertEqual(call_args[1]["id"], "CLASS1")

    def test_replace_classification_with_allow_overwrite(self):
        self.mock_client.putClassification.return_value = {"id": "CLASS1", "name": "Root"}
        from stepxmlclient.rest_client.models.classification import ClassificationCreateRequest
        data = ClassificationCreateRequest(id="CLASS1", name="Root")
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

    def test_get_classification_hierarchy(self):
        self.mock_client.getClassificationChildren.return_value = {
            "classification_id": "CLASS1", "classification_name": "Root",
            "root_nodes": [{"id": "CHILD1", "name": "Child 1"}]}
        result = self.operations.get_classification_hierarchy("CLASS1")
        self.assertIsNotNone(result)
        call_args = self.mock_client.getClassificationChildren.call_args
        self.assertEqual(call_args[1]["id"], "CLASS1")

    def test_search_by_type(self):
        self.mock_client.postClassificationsSearch.return_value = {"items": [], "total": 0}
        self.operations.search_by_type("ClassType")
        call_args = self.mock_client.postClassificationsSearch.call_args
        body = call_args[1]["body"]
        self.assertEqual(body["condition"]["conditionType"], "objecttype")
        self.assertEqual(body["condition"]["objectTypeId"], "ClassType")

    def test_list_classifications(self):
        self.mock_client.postClassificationsSearch.return_value = {"items": [], "total": 0}
        self.operations.list_classifications()
        self.mock_client.postClassificationsSearch.assert_called_once()


if __name__ == "__main__":
    unittest.main()
