"""Tests for Classification operations in STEP REST API v2."""

import unittest
from unittest.mock import MagicMock, Mock, patch
from datetime import datetime

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
    """Test classification operations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_client = MagicMock()
        self.operations = ClassificationOperations(self.mock_client)
    
    def test_classification_operations_initialization(self):
        """Test ClassificationOperations initialization."""
        self.assertIsNotNone(self.operations)
        self.assertEqual(self.operations.client, self.mock_client)
    
    def test_get_classification_success(self):
        """Test successful classification retrieval."""
        mock_response = {
            "id": "CLASS1",
            "name": "Color",
            "description": "Product color"
        }
        self.mock_client.getClassification.return_value = mock_response
        
        result = self.operations.get_classification("CLASS1")
        
        self.assertEqual(result.id, "CLASS1")
        self.assertEqual(result.name, "Color")
        self.mock_client.getClassification.assert_called_once()
    
    def test_get_classification_validation(self):
        """Test classification retrieval validation."""
        with self.assertRaises(exc.ValidationError):
            self.operations.get_classification(None)
    
    def test_get_classification_not_found(self):
        """Test retrieval when classification not found."""
        self.mock_client.getClassification.side_effect = Exception("404 not found")
        
        with self.assertRaises(exc.NotFoundError):
            self.operations.get_classification("NONEXISTENT")
    
    def test_search_classifications_success(self):
        """Test successful classification search."""
        mock_response = {
            "items": [
                {"id": "CLASS1", "name": "Color"},
                {"id": "CLASS2", "name": "Size"},
            ],
            "total": 50
        }
        self.mock_client.searchClassifications.return_value = mock_response
        
        result = self.operations.search_classifications(query="class", limit=20, offset=0)
        
        self.assertEqual(len(result.items), 2)
        self.assertEqual(result.total, 50)
    
    def test_search_classifications_defaults(self):
        """Test search with default parameters."""
        mock_response = {"items": [], "total": 0}
        self.mock_client.searchClassifications.return_value = mock_response
        
        self.operations.search_classifications()
        
        call_args = self.mock_client.searchClassifications.call_args
        # Check the arguments passed to the client call
        self.assertEqual(call_args[1].get("q"), "*")
        self.assertIn("limit", call_args[1])
    
    def test_search_classifications_with_filters(self):
        """Test search with optional filters."""
        mock_response = {"items": [], "total": 0}
        self.mock_client.searchClassifications.return_value = mock_response
        
        self.operations.search_classifications(
            query="test",
            type_filter="Standard",
            include_values=True
        )
        
        call_args = self.mock_client.searchClassifications.call_args
        self.assertEqual(call_args[1]["q"], "test")
        self.assertEqual(call_args[1]["typeFilter"], "Standard")
        self.assertTrue(call_args[1]["includeValues"])
    
    def test_list_classifications(self):
        """Test list_classifications convenience method."""
        mock_response = {"items": [], "total": 0}
        self.mock_client.searchClassifications.return_value = mock_response
        
        self.operations.list_classifications()
        
        call_args = self.mock_client.searchClassifications.call_args
        self.assertEqual(call_args[1]["q"], "*")
    
    def test_create_classification_success(self):
        """Test successful classification creation."""
        create_req = ClassificationCreateRequest(
            id="NEW_CLASS",
            name="Material",
            description=None,
            classification_type=None,
            is_hierarchical=False,
            attributes=None
        )
        mock_response = {"id": "NEW_CLASS", "name": "Material"}
        self.mock_client.createClassification.return_value = mock_response
        
        result = self.operations.create_classification(create_req)
        
        self.assertEqual(result.id, "NEW_CLASS")
        self.mock_client.createClassification.assert_called_once()
    
    def test_create_classification_validation_error(self):
        """Test classification creation with validation error."""
        create_req = ClassificationCreateRequest(
            id="CLASS",
            name="Test",
            description=None,
            classification_type=None,
            is_hierarchical=False,
            attributes=None
        )
        self.mock_client.createClassification.side_effect = Exception("400 bad request")
        
        with self.assertRaises(exc.ValidationError):
            self.operations.create_classification(create_req)
    
    def test_update_classification_success(self):
        """Test successful classification update."""
        update_req = ClassificationUpdateRequest(
            name="Updated",
            description=None,
            classification_type=None,
            attributes=None
        )
        mock_response = {"id": "CLASS1", "name": "Updated"}
        self.mock_client.updateClassification.return_value = mock_response
        
        result = self.operations.update_classification("CLASS1", update_req)
        
        self.assertEqual(result.name, "Updated")
    
    def test_update_classification_not_found(self):
        """Test update when classification not found."""
        update_req = ClassificationUpdateRequest(
            name="Updated",
            description=None,
            classification_type=None,
            attributes=None
        )
        self.mock_client.updateClassification.side_effect = Exception("404 not found")
        
        with self.assertRaises(exc.NotFoundError):
            self.operations.update_classification("NONEXISTENT", update_req)
    
    def test_delete_classification_success(self):
        """Test successful classification deletion."""
        self.mock_client.deleteClassification.return_value = None
        
        result = self.operations.delete_classification("CLASS1")
        
        self.assertTrue(result)
        self.mock_client.deleteClassification.assert_called_once_with(classificationId="CLASS1")
    
    def test_delete_classification_not_found(self):
        """Test deletion when classification not found."""
        self.mock_client.deleteClassification.side_effect = Exception("404 not found")
        
        with self.assertRaises(exc.NotFoundError):
            self.operations.delete_classification("NONEXISTENT")
    
    def test_get_classification_hierarchy_success(self):
        """Test successful hierarchy retrieval."""
        mock_response = {
            "classification_id": "CLASS1",
            "classification_name": "Organization",
            "root_nodes": [],
            "total_nodes": 0,
            "max_depth": 0
        }
        self.mock_client.getClassificationHierarchy.return_value = mock_response
        
        result = self.operations.get_classification_hierarchy("CLASS1")
        
        self.assertEqual(result.classification_id, "CLASS1")
        self.mock_client.getClassificationHierarchy.assert_called_once()
    
    def test_get_classification_hierarchy_with_root_id(self):
        """Test hierarchy retrieval with specific root."""
        mock_response = {
            "classification_id": "CLASS1",
            "classification_name": "Organization",
            "root_nodes": [],
            "total_nodes": 0,
            "max_depth": 0
        }
        self.mock_client.getClassificationHierarchy.return_value = mock_response
        
        self.operations.get_classification_hierarchy("CLASS1", root_id="ROOT123")
        
        call_args = self.mock_client.getClassificationHierarchy.call_args
        self.assertEqual(call_args[1]["classificationId"], "CLASS1")
        self.assertEqual(call_args[1]["rootId"], "ROOT123")
    
    def test_get_classification_hierarchy_not_found(self):
        """Test hierarchy when classification not found."""
        self.mock_client.getClassificationHierarchy.side_effect = Exception("404 not found")
        
        with self.assertRaises(exc.NotFoundError):
            self.operations.get_classification_hierarchy("NONEXISTENT")
    
    def test_get_classification_values_success(self):
        """Test successful values retrieval."""
        mock_response = {
            "classification_id": "CLASS1",
            "values": [
                {"id": "VAL1", "name": "Red"},
                {"id": "VAL2", "name": "Blue"},
            ],
            "total": 2
        }
        self.mock_client.getClassificationValues.return_value = mock_response
        
        result = self.operations.get_classification_values("CLASS1")
        
        self.assertEqual(result.classification_id, "CLASS1")
        self.assertEqual(len(result.values), 2)
    
    def test_get_classification_values_not_found(self):
        """Test values retrieval when classification not found."""
        self.mock_client.getClassificationValues.side_effect = Exception("404 not found")
        
        with self.assertRaises(exc.NotFoundError):
            self.operations.get_classification_values("NONEXISTENT")
    
    def test_search_by_type(self):
        """Test search_by_type convenience method."""
        mock_response = {"items": [], "total": 0}
        self.mock_client.searchClassifications.return_value = mock_response
        
        self.operations.search_by_type("Standard")
        
        call_args = self.mock_client.searchClassifications.call_args
        self.assertEqual(call_args[1]["typeFilter"], "Standard")
    
    def test_search_modified_since(self):
        """Test search_modified_since convenience method."""
        mock_response = {"items": [], "total": 0}
        self.mock_client.searchClassifications.return_value = mock_response
        
        self.operations.search_modified_since("2025-01-01T00:00:00Z")
        
        call_args = self.mock_client.searchClassifications.call_args
        self.assertIn("modifiedAt", call_args[1]["q"])
    
    def test_get_classification_includes_params(self):
        """Test that get_classification passes include parameters."""
        mock_response = {"id": "CLASS123", "name": "Color"}
        self.mock_client.getClassification.return_value = mock_response
        
        self.operations.get_classification(
            "CLASS123",
            include_values=True
        )
        
        call_args = self.mock_client.getClassification.call_args
        self.assertTrue(call_args[1]["includeValues"])


if __name__ == '__main__':
    unittest.main()
