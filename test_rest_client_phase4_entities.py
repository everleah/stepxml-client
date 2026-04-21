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
from stepxmlclient.rest_client import exceptions as exc


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
    def setUp(self):
        self.mock_client = Mock()
        self.logger = logging.getLogger(__name__)
        self.operations = EntityOperations(self.mock_client, logger=self.logger)

    def test_initialization(self):
        self.assertEqual(self.operations.operation_name, "EntityOperations")

    def test_get_entity_success(self):
        self.mock_client.getEntity.return_value = {"id": "ENT1", "user_type_id": "EntityType", "name": "Test Entity"}
        result = self.operations.get_entity("ENT1")
        self.assertEqual(result.id, "ENT1")
        call_args = self.mock_client.getEntity.call_args
        self.assertEqual(call_args[1]["id"], "ENT1")
        self.assertNotIn("entityId", call_args[1])

    def test_get_entity_not_found(self):
        self.mock_client.getEntity.side_effect = Exception("404 not found")
        with self.assertRaises(exc.NotFoundError):
            self.operations.get_entity("NONEXISTENT")

    def test_get_entity_validation(self):
        with self.assertRaises(exc.ValidationError):
            self.operations.get_entity(None)

    def test_get_entity_with_key_id(self):
        self.mock_client.getEntity.return_value = {"id": "ENT1", "name": "Test"}
        self.operations.get_entity("ENT1", key_id="MyKey")
        call_args = self.mock_client.getEntity.call_args
        self.assertEqual(call_args[1]["keyId"], "MyKey")

    def test_get_entity_with_include_inherited(self):
        self.mock_client.getEntity.return_value = {"id": "ENT1", "name": "Test"}
        self.operations.get_entity("ENT1", include_inherited_data=True)
        call_args = self.mock_client.getEntity.call_args
        self.assertEqual(call_args[1]["includeInheritedData"], True)

    def test_search_entities_success(self):
        self.mock_client.postEntitiesSearch.return_value = {
            "items": [{"id": "ENT1", "name": "Entity 1"}, {"id": "ENT2", "name": "Entity 2"}], "total": 2}
        condition = {"conditionType": "objecttype", "objectTypeId": "EntityType"}
        result = self.operations.search_entities(condition=condition)
        self.assertEqual(len(result.items), 2)
        call_args = self.mock_client.postEntitiesSearch.call_args
        self.assertEqual(call_args[1]["body"]["condition"], condition)

    def test_search_entities_requires_condition(self):
        with self.assertRaises(exc.ValidationError):
            self.operations.search_entities(condition=None)

    def test_create_entity_success(self):
        self.mock_client.postEntities.return_value = {"id": "NEWENT", "name": "New Entity"}
        from stepxmlclient.rest_client.models.entity import EntityCreateRequest
        request = EntityCreateRequest(name="New Entity")
        result = self.operations.create_entity(request)
        self.assertEqual(result.id, "NEWENT")
        self.mock_client.postEntities.assert_called_once()

    def test_create_entity_conflict(self):
        self.mock_client.postEntities.side_effect = Exception("409 conflict")
        from stepxmlclient.rest_client.models.entity import EntityCreateRequest
        request = EntityCreateRequest(name="Existing Entity")
        with self.assertRaises(exc.ConflictError):
            self.operations.create_entity(request)

    def test_update_entity_success(self):
        self.mock_client.patchEntity.return_value = {"id": "ENT1", "name": "Updated"}
        from stepxmlclient.rest_client.models.entity import EntityUpdateRequest
        updates = EntityUpdateRequest(name="Updated")
        result = self.operations.update_entity("ENT1", updates)
        self.assertEqual(result.name, "Updated")
        call_args = self.mock_client.patchEntity.call_args
        self.assertEqual(call_args[1]["id"], "ENT1")

    def test_update_entity_not_found(self):
        self.mock_client.patchEntity.side_effect = Exception("404 not found")
        from stepxmlclient.rest_client.models.entity import EntityUpdateRequest
        updates = EntityUpdateRequest(name="Updated")
        with self.assertRaises(exc.NotFoundError):
            self.operations.update_entity("NONEXISTENT", updates)

    def test_replace_entity_success(self):
        self.mock_client.putEntity.return_value = {"id": "ENT1", "name": "Test"}
        from stepxmlclient.rest_client.models.entity import EntityCreateRequest
        data = EntityCreateRequest(name="Test")
        result = self.operations.replace_entity("ENT1", data)
        self.assertEqual(result.id, "ENT1")
        call_args = self.mock_client.putEntity.call_args
        self.assertEqual(call_args[1]["id"], "ENT1")

    def test_replace_entity_with_allow_overwrite(self):
        self.mock_client.putEntity.return_value = {"id": "ENT1", "name": "Test"}
        from stepxmlclient.rest_client.models.entity import EntityCreateRequest
        data = EntityCreateRequest(name="Test")
        self.operations.replace_entity("ENT1", data, allow_overwrite=True)
        call_args = self.mock_client.putEntity.call_args
        self.assertEqual(call_args[1]["allow-overwrite"], True)

    def test_delete_entity_success(self):
        self.mock_client.deleteEntity.return_value = None
        result = self.operations.delete_entity("ENT1")
        self.assertTrue(result)
        call_args = self.mock_client.deleteEntity.call_args
        self.assertEqual(call_args[1]["id"], "ENT1")

    def test_delete_entity_not_found(self):
        self.mock_client.deleteEntity.side_effect = Exception("404 not found")
        with self.assertRaises(exc.NotFoundError):
            self.operations.delete_entity("NONEXISTENT")

    def test_search_by_type(self):
        self.mock_client.postEntitiesSearch.return_value = {"items": [], "total": 0}
        self.operations.search_by_type("EntityType")
        call_args = self.mock_client.postEntitiesSearch.call_args
        body = call_args[1]["body"]
        self.assertEqual(body["condition"]["conditionType"], "objecttype")
        self.assertEqual(body["condition"]["objectTypeId"], "EntityType")

    def test_list_entities(self):
        self.mock_client.postEntitiesSearch.return_value = {"items": [], "total": 0}
        self.operations.list_entities()
        self.mock_client.postEntitiesSearch.assert_called_once()


if __name__ == "__main__":
    unittest.main()
