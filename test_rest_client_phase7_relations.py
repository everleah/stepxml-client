"""Phase 7: Relations operations - Comprehensive test suite.

Tests for relationship management, cross-references, and links.
Phase 7 focuses on relationship-related operations.
"""

import unittest
from unittest.mock import Mock, MagicMock, patch, call
from stepxmlclient.rest_client.operations.relations import RelationOperations
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
    """Test RelationOperations initialization."""
    
    def test_init_without_logger(self):
        """Test initialization without logger."""
        mock_client = Mock()
        ops = RelationOperations(mock_client)
        
        self.assertEqual(ops.client, mock_client)
        self.assertEqual(ops.operation_name, "RelationOperations")
        self.assertIsNotNone(ops.logger)
    
    def test_init_with_logger(self):
        """Test initialization with logger."""
        mock_client = Mock()
        mock_logger = Mock()
        ops = RelationOperations(mock_client, logger=mock_logger)
        
        self.assertEqual(ops.client, mock_client)
        self.assertEqual(ops.logger, mock_logger)


class TestRelationshipOperations(unittest.TestCase):
    """Test relationship-specific operations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.ops = RelationOperations(self.mock_client)
    
    def test_get_relationship_success(self):
        """Test getting a relationship successfully."""
        relationship_id = "rel_123"
        mock_response = {
            "relationshipId": relationship_id,
            "relationshipType": "contains",
            "sourceId": "prod_1",
            "targetId": "prod_2",
            "sourceType": "Product",
            "targetType": "Product",
            "status": "active"
        }
        
        self.mock_client.getRelationship.return_value = mock_response
        
        result = self.ops.get_relationship(relationship_id)
        
        self.assertIsInstance(result, RelationshipResponse)
        self.assertEqual(result.relationshipId, relationship_id)
        self.mock_client.getRelationship.assert_called_once_with(relationshipId=relationship_id)
    
    def test_get_relationship_not_found(self):
        """Test getting non-existent relationship."""
        self.mock_client.getRelationship.side_effect = Exception("404 Not Found")
        
        with self.assertRaises(NotFoundError):
            self.ops.get_relationship("nonexistent")
    
    def test_get_relationship_missing_id(self):
        """Test getting relationship without ID."""
        with self.assertRaises(ValidationError):
            self.ops.get_relationship(None)
    
    def test_list_relationships_success(self):
        """Test listing relationships successfully."""
        mock_response = {
            "relationships": [
                {
                    "relationshipId": "rel_1",
                    "relationshipType": "contains",
                    "sourceId": "prod_1",
                    "targetId": "prod_2",
                    "sourceType": "Product",
                    "targetType": "Product"
                }
            ],
            "totalCount": 1,
            "limit": 20,
            "offset": 0
        }
        
        self.mock_client.listRelationships.return_value = mock_response
        
        result = self.ops.list_relationships(source_id="prod_1")
        
        self.assertIsInstance(result, RelationshipListResponse)
        self.assertEqual(len(result.relationships), 1)
        self.assertEqual(result.totalCount, 1)
    
    def test_list_relationships_with_filters(self):
        """Test listing relationships with multiple filters."""
        self.mock_client.listRelationships.return_value = {
            "relationships": [],
            "totalCount": 0,
            "limit": 20,
            "offset": 0
        }
        
        self.ops.list_relationships(
            source_id="prod_1",
            target_id="prod_2",
            relationship_type="contains",
            limit=50,
            offset=10
        )
        
        self.mock_client.listRelationships.assert_called_once()
        call_args = self.mock_client.listRelationships.call_args[1]
        self.assertEqual(call_args["sourceId"], "prod_1")
        self.assertEqual(call_args["targetId"], "prod_2")
        self.assertEqual(call_args["relationshipType"], "contains")
        self.assertEqual(call_args["limit"], 50)
        self.assertEqual(call_args["offset"], 10)
    
    def test_create_relationship_success(self):
        """Test creating a relationship."""
        create_data = RelationshipCreateRequest(
            relationshipType="contains",
            sourceId="prod_1",
            targetId="prod_2",
            metadata=None,
            status=None
        )
        
        mock_response = {
            "relationshipId": "rel_123",
            "relationshipType": "contains",
            "sourceId": "prod_1",
            "targetId": "prod_2",
            "sourceType": "Product",
            "targetType": "Product"
        }
        
        self.mock_client.createRelationship.return_value = mock_response
        
        result = self.ops.create_relationship(create_data)
        
        self.assertIsInstance(result, RelationshipResponse)
        self.assertEqual(result.relationshipId, "rel_123")
    
    def test_create_relationship_invalid_data(self):
        """Test creating relationship with invalid data."""
        self.mock_client.createRelationship.side_effect = Exception("400 Bad Request")
        
        create_data = RelationshipCreateRequest(
            relationshipType="contains",
            sourceId="prod_1",
            targetId="prod_2",
            metadata=None,
            status=None
        )
        
        with self.assertRaises(ValidationError):
            self.ops.create_relationship(create_data)
    
    def test_update_relationship_success(self):
        """Test updating a relationship."""
        relationship_id = "rel_123"
        update_data = RelationshipUpdateRequest(status="inactive", metadata={"note": "Updated"})
        
        mock_response = {
            "relationshipId": relationship_id,
            "relationshipType": "contains",
            "sourceId": "prod_1",
            "targetId": "prod_2",
            "sourceType": "Product",
            "targetType": "Product",
            "status": "inactive"
        }
        
        self.mock_client.updateRelationship.return_value = mock_response
        
        result = self.ops.update_relationship(relationship_id, update_data)
        
        self.assertIsInstance(result, RelationshipResponse)
        self.assertEqual(result.status, "inactive")
    
    def test_update_relationship_not_found(self):
        """Test updating non-existent relationship."""
        self.mock_client.updateRelationship.side_effect = Exception("404 Not Found")
        
        with self.assertRaises(NotFoundError):
            self.ops.update_relationship(
                "nonexistent",
                RelationshipUpdateRequest(status="inactive", metadata=None)
            )
    
    def test_delete_relationship_success(self):
        """Test deleting a relationship."""
        relationship_id = "rel_123"
        self.mock_client.deleteRelationship.return_value = None
        
        result = self.ops.delete_relationship(relationship_id)
        
        self.assertTrue(result)
        self.mock_client.deleteRelationship.assert_called_once_with(relationshipId=relationship_id)
    
    def test_delete_relationship_not_found(self):
        """Test deleting non-existent relationship."""
        self.mock_client.deleteRelationship.side_effect = Exception("404 Not Found")
        
        with self.assertRaises(NotFoundError):
            self.ops.delete_relationship("nonexistent")
    
    def test_get_relationship_types_success(self):
        """Test getting relationship types."""
        mock_response = {
            "contains": {
                "relationshipTypeId": "contains",
                "name": "Contains",
                "description": "Parent-child relationship",
                "bidirectional": False
            },
            "related": {
                "relationshipTypeId": "related",
                "name": "Related",
                "description": "Generic relation",
                "bidirectional": True
            }
        }
        
        self.mock_client.getRelationshipTypes.return_value = mock_response
        
        result = self.ops.get_relationship_types()
        
        self.assertIsInstance(result, dict)
        self.assertIn("contains", result)
        self.assertIn("related", result)
    
    def test_get_relationship_graph_success(self):
        """Test getting relationship graph."""
        entity_id = "prod_1"
        mock_response = {
            "rootEntityId": entity_id,
            "rootEntityType": "Product",
            "nodes": [
                {"entityId": entity_id, "entityType": "Product"},
                {"entityId": "prod_2", "entityType": "Product"}
            ],
            "edges": [
                {"source": entity_id, "target": "prod_2", "relationshipType": "contains"}
            ],
            "depth": 2
        }
        
        self.mock_client.getRelationshipGraph.return_value = mock_response
        
        result = self.ops.get_relationship_graph(entity_id, depth=2)
        
        self.assertIsInstance(result, RelationshipGraphResponse)
        self.assertEqual(result.rootEntityId, entity_id)
    
    def test_get_relationship_graph_not_found(self):
        """Test getting graph for non-existent entity."""
        self.mock_client.getRelationshipGraph.side_effect = Exception("404 Not Found")
        
        with self.assertRaises(NotFoundError):
            self.ops.get_relationship_graph("nonexistent")


class TestCrossReferenceOperations(unittest.TestCase):
    """Test cross-reference operations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.ops = RelationOperations(self.mock_client)
    
    def test_get_cross_reference_success(self):
        """Test getting a cross-reference."""
        xref_id = "xref_123"
        mock_response = {
            "crossReferenceId": xref_id,
            "sourceEntityId": "prod_1",
            "targetEntityId": "prod_2",
            "referenceType": "competitor",
            "metadata": {"source": "market_data"}
        }
        
        self.mock_client.getCrossReference.return_value = mock_response
        
        result = self.ops.get_cross_reference(xref_id)
        
        self.assertIsInstance(result, CrossReferenceResponse)
        self.assertEqual(result.crossReferenceId, xref_id)
    
    def test_get_cross_reference_not_found(self):
        """Test getting non-existent cross-reference."""
        self.mock_client.getCrossReference.side_effect = Exception("404 Not Found")
        
        with self.assertRaises(NotFoundError):
            self.ops.get_cross_reference("nonexistent")
    
    def test_list_cross_references_success(self):
        """Test listing cross-references."""
        mock_response = {
            "crossReferences": [
                {
                    "crossReferenceId": "xref_1",
                    "sourceEntityId": "prod_1",
                    "targetEntityId": "prod_2",
                    "referenceType": "competitor"
                }
            ],
            "totalCount": 1,
            "limit": 20,
            "offset": 0
        }
        
        self.mock_client.listCrossReferences.return_value = mock_response
        
        result = self.ops.list_cross_references(source_id="prod_1")
        
        self.assertIsInstance(result, CrossReferenceListResponse)
        self.assertEqual(len(result.crossReferences), 1)
    
    def test_list_cross_references_with_filters(self):
        """Test listing cross-references with filters."""
        self.mock_client.listCrossReferences.return_value = {
            "crossReferences": [],
            "totalCount": 0,
            "limit": 20,
            "offset": 0
        }
        
        self.ops.list_cross_references(
            source_id="prod_1",
            reference_type="competitor",
            limit=50
        )
        
        self.mock_client.listCrossReferences.assert_called_once()
        call_args = self.mock_client.listCrossReferences.call_args[1]
        self.assertEqual(call_args["sourceId"], "prod_1")
        self.assertEqual(call_args["referenceType"], "competitor")
    
    def test_create_cross_reference_success(self):
        """Test creating a cross-reference."""
        create_data = CrossReferenceCreateRequest(
            sourceEntityId="prod_1",
            targetEntityId="prod_2",
            referenceType="competitor",
            description=None,
            sequence=None
        )
        
        mock_response = {
            "crossReferenceId": "xref_123",
            "sourceEntityId": "prod_1",
            "targetEntityId": "prod_2",
            "referenceType": "competitor"
        }
        
        self.mock_client.createCrossReference.return_value = mock_response
        
        result = self.ops.create_cross_reference(create_data)
        
        self.assertIsInstance(result, CrossReferenceResponse)
        self.assertEqual(result.crossReferenceId, "xref_123")
    
    def test_create_cross_reference_invalid_data(self):
        """Test creating cross-reference with invalid data."""
        self.mock_client.createCrossReference.side_effect = Exception("400 Bad Request")
        
        create_data = CrossReferenceCreateRequest(
            sourceEntityId="prod_1",
            targetEntityId="prod_2",
            referenceType="competitor",
            description=None,
            sequence=None
        )
        
        with self.assertRaises(ValidationError):
            self.ops.create_cross_reference(create_data)
    
    def test_delete_cross_reference_success(self):
        """Test deleting a cross-reference."""
        xref_id = "xref_123"
        self.mock_client.deleteCrossReference.return_value = None
        
        result = self.ops.delete_cross_reference(xref_id)
        
        self.assertTrue(result)
        self.mock_client.deleteCrossReference.assert_called_once_with(crossReferenceId=xref_id)
    
    def test_delete_cross_reference_not_found(self):
        """Test deleting non-existent cross-reference."""
        self.mock_client.deleteCrossReference.side_effect = Exception("404 Not Found")
        
        with self.assertRaises(NotFoundError):
            self.ops.delete_cross_reference("nonexistent")


class TestLinkOperations(unittest.TestCase):
    """Test link operations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.ops = RelationOperations(self.mock_client)
    
    def test_get_link_success(self):
        """Test getting a link."""
        link_id = "link_123"
        mock_response = {
            "linkId": link_id,
            "sourceId": "prod_1",
            "targetId": "asset_1",
            "linkType": "has_asset",
            "sequence": 1
        }
        
        self.mock_client.getLink.return_value = mock_response
        
        result = self.ops.get_link(link_id)
        
        self.assertIsInstance(result, LinkResponse)
        self.assertEqual(result.linkId, link_id)
    
    def test_get_link_not_found(self):
        """Test getting non-existent link."""
        self.mock_client.getLink.side_effect = Exception("404 Not Found")
        
        with self.assertRaises(NotFoundError):
            self.ops.get_link("nonexistent")
    
    def test_list_links_success(self):
        """Test listing links."""
        mock_response = {
            "links": [
                {
                    "linkId": "link_1",
                    "sourceId": "prod_1",
                    "targetId": "asset_1",
                    "linkType": "has_asset",
                    "sequence": 1
                }
            ],
            "totalCount": 1,
            "limit": 20,
            "offset": 0
        }
        
        self.mock_client.listLinks.return_value = mock_response
        
        result = self.ops.list_links(source_id="prod_1")
        
        self.assertIsInstance(result, LinkListResponse)
        self.assertEqual(len(result.links), 1)
    
    def test_list_links_with_filters(self):
        """Test listing links with filters."""
        self.mock_client.listLinks.return_value = {
            "links": [],
            "totalCount": 0,
            "limit": 20,
            "offset": 0
        }
        
        self.ops.list_links(
            source_id="prod_1",
            link_type="has_asset",
            limit=50
        )
        
        self.mock_client.listLinks.assert_called_once()
        call_args = self.mock_client.listLinks.call_args[1]
        self.assertEqual(call_args["sourceId"], "prod_1")
        self.assertEqual(call_args["linkType"], "has_asset")
    
    def test_create_link_success(self):
        """Test creating a link."""
        create_data = LinkCreateRequest(
            sourceId="prod_1",
            targetId="asset_1",
            linkType="has_asset",
            sequence=None,
            metadata=None
        )
        
        mock_response = {
            "linkId": "link_123",
            "sourceId": "prod_1",
            "targetId": "asset_1",
            "linkType": "has_asset"
        }
        
        self.mock_client.createLink.return_value = mock_response
        
        result = self.ops.create_link(create_data)
        
        self.assertIsInstance(result, LinkResponse)
        self.assertEqual(result.linkId, "link_123")
    
    def test_create_link_invalid_data(self):
        """Test creating link with invalid data."""
        self.mock_client.createLink.side_effect = Exception("400 Bad Request")
        
        create_data = LinkCreateRequest(
            sourceId="prod_1",
            targetId="asset_1",
            linkType="has_asset",
            sequence=None,
            metadata=None
        )
        
        with self.assertRaises(ValidationError):
            self.ops.create_link(create_data)
    
    def test_delete_link_success(self):
        """Test deleting a link."""
        link_id = "link_123"
        self.mock_client.deleteLink.return_value = None
        
        result = self.ops.delete_link(link_id)
        
        self.assertTrue(result)
        self.mock_client.deleteLink.assert_called_once_with(linkId=link_id)
    
    def test_delete_link_not_found(self):
        """Test deleting non-existent link."""
        self.mock_client.deleteLink.side_effect = Exception("404 Not Found")
        
        with self.assertRaises(NotFoundError):
            self.ops.delete_link("nonexistent")


class TestErrorHandling(unittest.TestCase):
    """Test error handling in relation operations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.ops = RelationOperations(self.mock_client)
    
    def test_missing_relationship_id_validation(self):
        """Test validation for missing relationship ID."""
        with self.assertRaises(ValidationError):
            self.ops.get_relationship(None)
    
    def test_missing_cross_reference_id_validation(self):
        """Test validation for missing cross-reference ID."""
        with self.assertRaises(ValidationError):
            self.ops.get_cross_reference(None)
    
    def test_missing_link_id_validation(self):
        """Test validation for missing link ID."""
        with self.assertRaises(ValidationError):
            self.ops.get_link(None)
    
    def test_generic_api_error_handling(self):
        """Test generic API error handling."""
        self.mock_client.getRelationship.side_effect = Exception("500 Internal Server Error")
        
        with self.assertRaises(Exception):
            self.ops.get_relationship("rel_123")


class TestPaginationHandling(unittest.TestCase):
    """Test pagination parameter handling."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.ops = RelationOperations(self.mock_client)
    
    def test_list_relationships_default_pagination(self):
        """Test list relationships with default pagination."""
        self.mock_client.listRelationships.return_value = {
            "relationships": [],
            "totalCount": 0,
            "limit": 20,
            "offset": 0
        }
        
        self.ops.list_relationships()
        
        call_args = self.mock_client.listRelationships.call_args[1]
        self.assertEqual(call_args["limit"], 20)
        self.assertEqual(call_args["offset"], 0)
    
    def test_list_relationships_custom_pagination(self):
        """Test list relationships with custom pagination."""
        self.mock_client.listRelationships.return_value = {
            "relationships": [],
            "totalCount": 0,
            "limit": 100,
            "offset": 50
        }
        
        self.ops.list_relationships(limit=100, offset=50)
        
        call_args = self.mock_client.listRelationships.call_args[1]
        self.assertEqual(call_args["limit"], 100)
        self.assertEqual(call_args["offset"], 50)
    
    def test_list_links_pagination(self):
        """Test list links with pagination."""
        self.mock_client.listLinks.return_value = {
            "links": [],
            "totalCount": 0,
            "limit": 30,
            "offset": 20
        }
        
        self.ops.list_links(limit=30, offset=20)
        
        call_args = self.mock_client.listLinks.call_args[1]
        self.assertEqual(call_args["limit"], 30)
        self.assertEqual(call_args["offset"], 20)


if __name__ == '__main__':
    unittest.main()
