"""Phase 4: Entity Operations tests for STEP REST API v2."""

import unittest
from unittest.mock import Mock, MagicMock, patch
import logging

from stepxmlclient.rest_client.operations.entities import EntityOperations
from stepxmlclient.rest_client.models.entity import (
    EntityResponse,
    EntityListResponse,
    EntityCreateRequest,
    EntityUpdateRequest,
    EntityRelationshipResponse,
)
from stepxmlclient.rest_client.exceptions import NotFoundError, ValidationError
from stepxmlclient.rest_client import exceptions as exc


class TestEntityModels(unittest.TestCase):
    """Test Entity model creation and validation."""
    
    def test_entity_response_creation(self):
        """Test EntityResponse model creation with OpenAPI fields."""
        entity = EntityResponse(
            id="ENT001",
            objectType="Contact",
            name="Macy, Charles",
            parent="ContactsRoot",
        )
        self.assertEqual(entity.id, "ENT001")
        self.assertEqual(entity.objectType, "Contact")
        self.assertEqual(entity.name, "Macy, Charles")
        self.assertEqual(entity.parent, "ContactsRoot")

    def test_entity_response_minimal(self):
        """Test EntityResponse with only required id field."""
        entity = EntityResponse(id="ENT001")
        self.assertEqual(entity.id, "ENT001")
        self.assertIsNone(entity.objectType)
        self.assertIsNone(entity.parent)

    def test_entity_response_with_values(self):
        """Test EntityResponse with values and references."""
        entity = EntityResponse(
            id="ENT001",
            objectType="Contact",
            values={"GivenNames": {"value": {"value": "Charles"}}},
            references={"Country": {"reference": {"target": "Denmark"}}},
        )
        self.assertIn("GivenNames", entity.values)  # type: ignore
        self.assertIn("Country", entity.references)  # type: ignore

    def test_entity_list_response_creation(self):
        """Test EntityListResponse model creation."""
        response = EntityListResponse(
            items=[
                EntityResponse(id="ENT001", objectType="Contact"),
                EntityResponse(id="ENT002", objectType="Contact"),
            ],
            total=100,
            limit=20,
            offset=0,
            hasMore=True,
        )
        self.assertEqual(len(response.items), 2)
        self.assertEqual(response.total, 100)
        self.assertTrue(response.hasMore)

    def test_entity_create_request_requires_object_type(self):
        """Test EntityCreateRequest requires objectType."""
        with self.assertRaises(Exception):
            EntityCreateRequest(parent="ContactsRoot")

    def test_entity_create_request_requires_parent(self):
        """Test EntityCreateRequest requires parent."""
        with self.assertRaises(Exception):
            EntityCreateRequest(objectType="Contact")

    def test_entity_create_request_creation(self):
        """Test EntityCreateRequest model creation."""
        req = EntityCreateRequest(
            objectType="Contact",
            parent="ContactsRoot",
            name="Macy, Charles",
        )
        self.assertEqual(req.objectType, "Contact")
        self.assertEqual(req.parent, "ContactsRoot")
        self.assertEqual(req.name, "Macy, Charles")

    def test_entity_update_request_creation(self):
        """Test EntityUpdateRequest model creation (all optional)."""
        req = EntityUpdateRequest(name="Updated Entity")
        self.assertEqual(req.name, "Updated Entity")
        self.assertIsNone(req.parent)

    def test_entity_relationship_response_creation(self):
        """Test EntityRelationshipResponse model creation."""
        response = EntityRelationshipResponse(
            id="ENT001",
            references={},
            total=0,
        )
        self.assertEqual(response.id, "ENT001")
        self.assertEqual(response.total, 0)


class TestEntityOperations(unittest.TestCase):
    def setUp(self):
        self.mock_client = Mock()
        self.logger = logging.getLogger(__name__)
        self.operations = EntityOperations(self.mock_client, logger=self.logger)

    def test_initialization(self):
        self.assertEqual(self.operations.operation_name, "EntityOperations")

    def test_get_entity_success(self):
        self.mock_client.getEntity.return_value = {"id": "ENT1", "objectType": "Contact", "name": "Test Entity"}
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
        self.assertEqual(call_args[1]["json"]["condition"], condition)

    def test_search_entities_requires_condition(self):
        with self.assertRaises(exc.ValidationError):
            self.operations.search_entities(condition=None)

    def test_create_entity_success(self):
        self.mock_client.postEntities.return_value = {"id": "NEWENT", "objectType": "Contact", "parent": "ContactsRoot"}
        from stepxmlclient.rest_client.models.entity import EntityCreateRequest
        request = EntityCreateRequest(objectType="Contact", parent="ContactsRoot")
        result = self.operations.create_entity(request)
        self.assertEqual(result.id, "NEWENT")
        self.mock_client.postEntities.assert_called_once()

    def test_create_entity_conflict(self):
        self.mock_client.postEntities.side_effect = Exception("409 conflict")
        from stepxmlclient.rest_client.models.entity import EntityCreateRequest
        request = EntityCreateRequest(objectType="Contact", parent="ContactsRoot")
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
        self.mock_client.putEntity.return_value = {"id": "ENT1", "objectType": "Contact"}
        from stepxmlclient.rest_client.models.entity import EntityCreateRequest
        data = EntityCreateRequest(objectType="Contact", parent="ContactsRoot")
        result = self.operations.replace_entity("ENT1", data)
        self.assertEqual(result.id, "ENT1")
        call_args = self.mock_client.putEntity.call_args
        self.assertEqual(call_args[1]["id"], "ENT1")

    def test_replace_entity_with_allow_overwrite(self):
        self.mock_client.putEntity.return_value = {"id": "ENT1", "objectType": "Contact"}
        from stepxmlclient.rest_client.models.entity import EntityCreateRequest
        data = EntityCreateRequest(objectType="Contact", parent="ContactsRoot")
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
        payload = call_args[1]["json"]
        self.assertEqual(payload["condition"]["conditionType"], "objecttype")
        self.assertEqual(payload["condition"]["objectType"], "EntityType")

    def test_list_entities(self):
        self.mock_client.postEntitiesSearch.return_value = {"items": [], "total": 0}
        self.operations.list_entities()
        self.mock_client.postEntitiesSearch.assert_called_once()


if __name__ == "__main__":
    unittest.main()
