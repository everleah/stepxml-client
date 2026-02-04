"""Phase 4: Entity Operations tests for STEP REST API v2."""

import unittest
from unittest.mock import Mock, MagicMock, patch
import logging

from stepxmlclient.rest_client.operations.entities import EntityOperations
from stepxmlclient.rest_client.models.entity import (
    EntityResponse,
    EntityListResponse,
    EntitySearchRequest,
    EntityCreateRequest,
    EntityUpdateRequest,
    EntityRelationshipResponse,
    EntityBulkRequest,
    EntityBulkResponse,
    EntityAttribute,
    EntityMetadata,
)
from stepxmlclient.rest_client.exceptions import NotFoundError, ValidationError


class TestEntityModels(unittest.TestCase):
    """Test Entity model creation and validation."""
    
    def test_entity_attribute_creation(self):
        """Test EntityAttribute model creation."""
        attr = EntityAttribute(name="Color", value="Blue", type="Text", unit=None)
        self.assertEqual(attr.name, "Color")
        self.assertEqual(attr.value, "Blue")
        self.assertEqual(attr.type, "Text")
    
    def test_entity_metadata_creation(self):
        """Test EntityMetadata model creation."""
        meta = EntityMetadata(
            createdAt="2025-01-01T00:00:00Z",
            modifiedAt="2025-01-02T00:00:00Z",
            createdBy="admin",
            modifiedBy="admin",
            version=1
        )
        self.assertEqual(meta.createdAt, "2025-01-01T00:00:00Z")
        self.assertEqual(meta.version, 1)
    
    def test_entity_response_creation(self):
        """Test EntityResponse model creation."""
        entity = EntityResponse(
            id="ENT001",
            name="Product A",
            type="Product",
            description="Test product",
            attributes=None,
            relationships=None,
            metadata=None
        )
        self.assertEqual(entity.id, "ENT001")
        self.assertEqual(entity.name, "Product A")
        self.assertEqual(entity.type, "Product")
    
    def test_entity_response_with_attributes(self):
        """Test EntityResponse with attributes."""
        entity = EntityResponse(
            id="ENT001",
            name="Product A",
            description=None,
            type=None,
            attributes=[
                EntityAttribute(name="Color", value="Blue", type=None, unit=None),
                EntityAttribute(name="Size", value="Large", type=None, unit=None)
            ],
            relationships=None,
            metadata=None
        )
        self.assertEqual(len(entity.attributes), 2) #type: ignore
        self.assertEqual(entity.attributes[0].name, "Color") #type: ignore
    
    def test_entity_response_with_metadata(self):
        """Test EntityResponse with metadata."""
        meta = EntityMetadata(
            createdAt="2025-01-01T00:00:00Z",
            modifiedAt="2025-01-02T00:00:00Z",
            createdBy="admin",
            modifiedBy="admin",
            version=2
        )
        entity = EntityResponse(
            id="ENT001",
            name="Product A",
            description=None,
            type=None,
            attributes=None,
            relationships=None,
            metadata=meta
        )
        self.assertEqual(entity.metadata.version, 2) #type: ignore
    
    def test_entity_list_response_creation(self):
        """Test EntityListResponse model creation."""
        response = EntityListResponse(
            items=[
                EntityResponse(id="ENT001", name="Product A", description=None, type=None, attributes=None, relationships=None, metadata=None),
                EntityResponse(id="ENT002", name="Product B", description=None, type=None, attributes=None, relationships=None, metadata=None)
            ],
            total=100,
            limit=20,
            offset=0,
            hasMore=True
        )
        self.assertEqual(len(response.items), 2)
        self.assertEqual(response.total, 100)
        self.assertTrue(response.hasMore)
    
    def test_entity_search_request_creation(self):
        """Test EntitySearchRequest model creation."""
        req = EntitySearchRequest(
            query="*",
            type="Product",
            limit=50,
            offset=0,
            attributes=None
        )
        self.assertEqual(req.query, "*")
        self.assertEqual(req.type, "Product")
        self.assertEqual(req.limit, 50)
    
    def test_entity_create_request_creation(self):
        """Test EntityCreateRequest model creation."""
        req = EntityCreateRequest(
            name="New Product",
            type="Product",
            description="Test",
            attributes=None,
            relationships=None
        )
        self.assertEqual(req.name, "New Product")
        self.assertEqual(req.type, "Product")
    
    def test_entity_update_request_creation(self):
        """Test EntityUpdateRequest model creation."""
        req = EntityUpdateRequest(
            name="Updated Product",
            description="Updated",
            attributes=None,
            relationships=None
        )
        self.assertEqual(req.name, "Updated Product")
    
    def test_entity_relationship_response_creation(self):
        """Test EntityRelationshipResponse model creation."""
        response = EntityRelationshipResponse(
            id="ENT001",
            relationships=[],
            total=0
        )
        self.assertEqual(response.id, "ENT001")
        self.assertEqual(response.total, 0)
    
    def test_entity_bulk_response_creation(self):
        """Test EntityBulkResponse model creation."""
        response = EntityBulkResponse(
            successful=8,
            failed=2,
            results=[]
        )
        self.assertEqual(response.successful, 8)
        self.assertEqual(response.failed, 2)


class TestEntityOperations(unittest.TestCase):
    """Test Entity operation methods."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.logger = logging.getLogger("test")
        self.operations = EntityOperations(self.mock_client, logger=self.logger)
    
    def test_get_entity_success(self):
        """Test successful get_entity operation."""
        mock_response = {
            "id": "ENT001",
            "name": "Product A",
            "type": "Product"
        }
        self.mock_client.getEntity.return_value = mock_response
        
        result = self.operations.get_entity("ENT001")
        
        self.assertIsInstance(result, EntityResponse)
        self.assertEqual(result.id, "ENT001")
        self.assertEqual(result.name, "Product A")
        self.mock_client.getEntity.assert_called_once()
    
    def test_get_entity_with_includes(self):
        """Test get_entity with include flags."""
        mock_response = {
            "id": "ENT001",
            "name": "Product A",
            "attributes": [{"name": "Color", "value": "Blue"}],
            "relationships": {}
        }
        self.mock_client.getEntity.return_value = mock_response
        
        result = self.operations.get_entity(
            "ENT001",
            include_attributes=True,
            include_relationships=True
        )
        
        self.assertIsInstance(result, EntityResponse)
        self.assertEqual(result.id, "ENT001")
        call_kwargs = self.mock_client.getEntity.call_args[1]
        self.assertTrue(call_kwargs.get("includeAttributes"))
        self.assertTrue(call_kwargs.get("includeRelationships"))
    
    def test_get_entity_not_found(self):
        """Test get_entity raises NotFoundError for missing entity."""
        self.mock_client.getEntity.side_effect = Exception("404")
        
        with self.assertRaises(NotFoundError):
            self.operations.get_entity("NONEXISTENT")
    
    def test_get_entity_missing_id(self):
        """Test get_entity with missing ID."""
        with self.assertRaises(ValidationError):
            self.operations.get_entity(None)
    
    def test_search_entities_success(self):
        """Test successful search_entities operation."""
        mock_response = {
            "items": [
                {"id": "ENT001", "name": "Product A"},
                {"id": "ENT002", "name": "Product B"}
            ],
            "total": 100,
            "limit": 20,
            "offset": 0,
            "hasMore": True
        }
        self.mock_client.searchEntities.return_value = mock_response
        
        result = self.operations.search_entities()
        
        self.assertIsInstance(result, EntityListResponse)
        self.assertEqual(len(result.items), 2)
        self.assertEqual(result.total, 100)
    
    def test_search_entities_with_filters(self):
        """Test search_entities with type filter."""
        mock_response = {
            "items": [{"id": "ENT001", "name": "Product A"}],
            "total": 50,
            "limit": 20,
            "offset": 0
        }
        self.mock_client.searchEntities.return_value = mock_response
        
        result = self.operations.search_entities(
            query="*",
            type_filter="Product",
            limit=50
        )
        
        self.assertEqual(result.total, 50)
        call_kwargs = self.mock_client.searchEntities.call_args[1]
        self.assertEqual(call_kwargs.get("typeFilter"), "Product")
        self.assertEqual(call_kwargs.get("limit"), 50)
    
    def test_search_entities_defaults(self):
        """Test search_entities with default parameters."""
        mock_response = {
            "items": [],
            "total": 0,
            "limit": 20,
            "offset": 0
        }
        self.mock_client.searchEntities.return_value = mock_response
        
        result = self.operations.search_entities()
        
        call_kwargs = self.mock_client.searchEntities.call_args[1]
        self.assertEqual(call_kwargs.get("q"), "*")
        self.assertEqual(call_kwargs.get("limit"), 20)
        self.assertEqual(call_kwargs.get("offset"), 0)
    
    def test_list_entities(self):
        """Test list_entities convenience method."""
        mock_response = {
            "items": [{"id": "ENT001", "name": "Product A"}],
            "total": 1,
            "limit": 20,
            "offset": 0
        }
        self.mock_client.searchEntities.return_value = mock_response
        
        result = self.operations.list_entities()
        
        self.assertIsInstance(result, EntityListResponse)
        call_kwargs = self.mock_client.searchEntities.call_args[1]
        self.assertEqual(call_kwargs.get("q"), "*")
    
    def test_create_entity_success(self):
        """Test successful create_entity operation."""
        mock_response = {
            "id": "ENT001",
            "name": "New Product",
            "type": "Product"
        }
        self.mock_client.createEntity.return_value = mock_response
        
        req = EntityCreateRequest(name="New Product", type="Product", description=None, attributes=None, relationships=None)
        result = self.operations.create_entity(req)
        
        self.assertIsInstance(result, EntityResponse)
        self.assertEqual(result.id, "ENT001")
        self.assertEqual(result.name, "New Product")
    
    def test_create_entity_validation_error(self):
        """Test create_entity with validation error."""
        self.mock_client.createEntity.side_effect = Exception("400 Bad Request")
        
        req = EntityCreateRequest(name="Product", type=None, description=None, attributes=None, relationships=None)
        with self.assertRaises(ValidationError):
            self.operations.create_entity(req)
    
    def test_update_entity_success(self):
        """Test successful update_entity operation."""
        mock_response = {
            "id": "ENT001",
            "name": "Updated Product",
            "type": "Product"
        }
        self.mock_client.updateEntity.return_value = mock_response
        
        updates = EntityUpdateRequest(name="Updated Product", description=None, attributes=None, relationships=None)
        result = self.operations.update_entity("ENT001", updates)
        
        self.assertIsInstance(result, EntityResponse)
        self.assertEqual(result.name, "Updated Product")
    
    def test_update_entity_not_found(self):
        """Test update_entity raises NotFoundError."""
        self.mock_client.updateEntity.side_effect = Exception("404")
        
        updates = EntityUpdateRequest(name="Updated", description=None, attributes=None, relationships=None)
        with self.assertRaises(NotFoundError):
            self.operations.update_entity("NONEXISTENT", updates)
    
    def test_update_entity_missing_id(self):
        """Test update_entity with missing ID."""
        updates = EntityUpdateRequest(name="Updated", description=None, attributes=None, relationships=None)
        with self.assertRaises(ValidationError):
            self.operations.update_entity(None, updates)
    
    def test_delete_entity_success(self):
        """Test successful delete_entity operation."""
        self.mock_client.deleteEntity.return_value = True
        
        result = self.operations.delete_entity("ENT001")
        
        self.assertTrue(result)
        self.mock_client.deleteEntity.assert_called_once()
    
    def test_delete_entity_not_found(self):
        """Test delete_entity raises NotFoundError."""
        self.mock_client.deleteEntity.side_effect = Exception("404")
        
        with self.assertRaises(NotFoundError):
            self.operations.delete_entity("NONEXISTENT")
    
    def test_delete_entity_missing_id(self):
        """Test delete_entity with missing ID."""
        with self.assertRaises(ValidationError):
            self.operations.delete_entity(None)
    
    def test_get_entity_relationships_success(self):
        """Test successful get_entity_relationships operation."""
        mock_response = {
            "id": "ENT001",
            "relationships": [
                {"type": "Parent", "targetId": "ENT002"}
            ],
            "total": 1
        }
        self.mock_client.getEntityRelationships.return_value = mock_response
        
        result = self.operations.get_entity_relationships("ENT001")
        
        self.assertIsInstance(result, EntityRelationshipResponse)
        self.assertEqual(result.id, "ENT001")
        self.assertEqual(len(result.relationships), 1)
    
    def test_get_entity_relationships_with_filter(self):
        """Test get_entity_relationships with type filter."""
        mock_response = {
            "id": "ENT001",
            "relationships": [
                {"type": "Parent", "targetId": "ENT002"}
            ],
            "total": 1
        }
        self.mock_client.getEntityRelationships.return_value = mock_response
        
        result = self.operations.get_entity_relationships(
            "ENT001",
            relationship_type="Parent"
        )
        
        call_kwargs = self.mock_client.getEntityRelationships.call_args[1]
        self.assertEqual(call_kwargs.get("relationshipType"), "Parent")
    
    def test_get_entity_relationships_not_found(self):
        """Test get_entity_relationships raises NotFoundError."""
        self.mock_client.getEntityRelationships.side_effect = Exception("404")
        
        with self.assertRaises(NotFoundError):
            self.operations.get_entity_relationships("NONEXISTENT")
    
    def test_bulk_create_entities_success(self):
        """Test successful bulk_create_entities operation."""
        mock_response = {
            "successful": 2,
            "failed": 0,
            "results": []
        }
        self.mock_client.bulkCreateEntities.return_value = mock_response
        
        entities = [
            EntityCreateRequest(name="Product 1", type=None, description=None, attributes=None, relationships=None),
            EntityCreateRequest(name="Product 2", type=None, description=None, attributes=None, relationships=None)
        ]
        result = self.operations.bulk_create_entities(entities)
        
        self.assertIsInstance(result, EntityBulkResponse)
        self.assertEqual(result.successful, 2)
        self.assertEqual(result.failed, 0)
    
    def test_bulk_create_entities_with_dicts(self):
        """Test bulk_create_entities with dict objects."""
        mock_response = {
            "successful": 1,
            "failed": 0,
            "results": []
        }
        self.mock_client.bulkCreateEntities.return_value = mock_response
        
        entities = [
            EntityCreateRequest(name="Product 1", type=None, description=None, attributes=None, relationships=None)
        ]
        result = self.operations.bulk_create_entities(entities)
        
        self.assertEqual(result.successful, 1)
    
    def test_bulk_create_entities_validation_error(self):
        """Test bulk_create_entities with validation error."""
        self.mock_client.bulkCreateEntities.side_effect = Exception("400")
        
        entities = [EntityCreateRequest(name="Product 1", type=None, description=None, attributes=None, relationships=None)]
        with self.assertRaises(ValidationError):
            self.operations.bulk_create_entities(entities)
    
    def test_bulk_update_entities_success(self):
        """Test successful bulk_update_entities operation."""
        mock_response = {
            "successful": 2,
            "failed": 0,
            "results": []
        }
        self.mock_client.bulkUpdateEntities.return_value = mock_response
        
        updates = {
            "ENT001": EntityUpdateRequest(name="Updated 1", description=None, attributes=None, relationships=None),
            "ENT002": EntityUpdateRequest(name="Updated 2", description=None, attributes=None, relationships=None)
        }
        result = self.operations.bulk_update_entities(updates)
        
        self.assertEqual(result.successful, 2)
    
    def test_bulk_update_entities_validation_error(self):
        """Test bulk_update_entities with validation error."""
        self.mock_client.bulkUpdateEntities.side_effect = Exception("400")
        
        updates = {"ENT001": EntityUpdateRequest(name="Updated", description=None, attributes=None, relationships=None)}
        with self.assertRaises(ValidationError):
            self.operations.bulk_update_entities(updates)
    
    def test_search_by_type(self):
        """Test search_by_type convenience method."""
        mock_response = {
            "items": [{"id": "ENT001", "name": "Product"}],
            "total": 1,
            "limit": 20,
            "offset": 0
        }
        self.mock_client.searchEntities.return_value = mock_response
        
        result = self.operations.search_by_type("Product")
        
        call_kwargs = self.mock_client.searchEntities.call_args[1]
        self.assertEqual(call_kwargs.get("typeFilter"), "Product")
    
    def test_search_modified_since(self):
        """Test search_modified_since convenience method."""
        mock_response = {
            "items": [{"id": "ENT001", "name": "Product"}],
            "total": 1,
            "limit": 20,
            "offset": 0
        }
        self.mock_client.searchEntities.return_value = mock_response
        
        result = self.operations.search_modified_since("2025-01-01T00:00:00Z")
        
        call_kwargs = self.mock_client.searchEntities.call_args[1]
        self.assertIn("modifiedAt >=", call_kwargs.get("q"))


if __name__ == '__main__':
    unittest.main()
