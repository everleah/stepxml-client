"""Phase 5: Attribute & Metadata Operations tests for STEP REST API v2."""

import unittest
from unittest.mock import Mock, MagicMock
import logging

from stepxmlclient.rest_client.operations.attributes import AttributeOperations
from stepxmlclient.rest_client import exceptions as exc
from stepxmlclient.rest_client.models.attribute import (
    AttributeResponse,
    ListOfValueResponse,
    ListOfValueItem,
)
from stepxmlclient.rest_client.exceptions import NotFoundError, ValidationError


class TestAttributeModels(unittest.TestCase):
    """Test Attribute model creation and validation."""
    
    def test_attribute_response_creation(self):
        """Test AttributeResponse model creation."""
        attr = AttributeResponse(
            id="ATTR001",
            name="Color",
            type="Text",
            lovId=None,
            multiValued=None,
            metadata=None,
            required=None,
            description=None
        )
        self.assertEqual(attr.id, "ATTR001")
        self.assertEqual(attr.name, "Color")
        self.assertEqual(attr.type, "Text")
    
    def test_attribute_list_response_creation(self):
        """Test AttributeListResponse model creation."""
        response = AttributeListResponse(
            items=[
                AttributeResponse(id="ATTR001", name="Color", type="Text", lovId=None, multiValued=None, metadata=None, required=None, description=None),
                AttributeResponse(id="ATTR002", name="Size", type="Text", lovId=None, multiValued=None, metadata=None, required=None, description=None)
            ],
            total=50,
            limit=20,
            offset=0,
            hasMore=None
        )
        self.assertEqual(len(response.items), 2)
        self.assertEqual(response.total, 50)
    
    def test_list_of_value_response_creation(self):
        """Test ListOfValueResponse model creation."""
        lov = ListOfValueResponse(
            id="LOV001",
            name="Colors",
            items=[
                ListOfValueItem(id="RED", name="Red", description=None, sequence=None),
                ListOfValueItem(id="BLUE", name="Blue", description=None, sequence=None)
            ],
            total=5
        )
        self.assertEqual(lov.id, "LOV001")
        self.assertEqual(len(lov.items), 2)
    
    def test_attribute_create_request(self):
        """Test dict creation."""
        req = dict(
            name="Size",
            type="Text",
            lovId=None,
            multiValued=None,
            required=True,
            description=None
        )
        self.assertEqual(req.name, "Size")
        self.assertEqual(req.type, "Text")
        self.assertTrue(req.required)
    
    def test_attribute_update_request(self):
        """Test dict creation."""
        req = dict(
            name=None,
            description="Product size",
            required=True,
            lovId=None
        )
        self.assertEqual(req.description, "Product size")
        self.assertTrue(req.required)


class TestAttributeOperations(unittest.TestCase):
    def setUp(self):
        self.mock_client = Mock()
        self.logger = logging.getLogger(__name__)
        self.operations = AttributeOperations(self.mock_client, logger=self.logger)

    def test_initialization(self):
        self.assertEqual(self.operations.operation_name, "AttributeOperations")

    def test_get_attribute_success(self):
        self.mock_client.getAttribute.return_value = {"id": "ATTR1", "name": "Color", "type": "Text"}
        result = self.operations.get_attribute("ATTR1")
        self.assertEqual(result.id, "ATTR1")
        call_args = self.mock_client.getAttribute.call_args
        self.assertEqual(call_args[1]["id"], "ATTR1")

    def test_get_attribute_not_found(self):
        self.mock_client.getAttribute.side_effect = Exception("404 not found")
        with self.assertRaises(exc.NotFoundError):
            self.operations.get_attribute("NONEXISTENT")

    def test_get_attribute_validation(self):
        with self.assertRaises(exc.ValidationError):
            self.operations.get_attribute(None)

    def test_search_attributes_success(self):
        self.mock_client.queryAttributes.return_value = {
            "items": [{"id": "ATTR1", "name": "Color", "type": "Text"}, {"id": "ATTR2", "name": "Size", "type": "Number"}], "total": 2}
        condition = {"conditionType": "objecttype", "objectTypeId": "AttributeType"}
        result = self.operations.search_attributes(condition=condition)
        self.assertEqual(len(result.items), 2)
        call_args = self.mock_client.queryAttributes.call_args
        self.assertEqual(call_args[1]["json"]["condition"], condition)

    def test_search_attributes_requires_condition(self):
        with self.assertRaises(exc.ValidationError):
            self.operations.search_attributes(condition=None)

    def test_create_attribute_success(self):
        self.mock_client.createAttribute.return_value = {"id": "NEWATTR", "name": "New", "type": "Text"}
        from stepxmlclient.rest_client.models.attribute import dict
        request = dict(name="New", type="Text")
        result = self.operations.create_attribute(request)
        self.assertEqual(result.id, "NEWATTR")
        self.mock_client.createAttribute.assert_called_once()

    def test_update_attribute_success(self):
        self.mock_client.patchAttribute.return_value = {"id": "ATTR1", "name": "Updated", "type": "Text"}
        from stepxmlclient.rest_client.models.attribute import dict
        updates = dict(name="Updated")
        result = self.operations.update_attribute("ATTR1", updates)
        self.assertEqual(result.name, "Updated")
        call_args = self.mock_client.patchAttribute.call_args
        self.assertEqual(call_args[1]["id"], "ATTR1")

    def test_delete_attribute_success(self):
        self.mock_client.deleteAttribute.return_value = None
        result = self.operations.delete_attribute("ATTR1")
        self.assertTrue(result)
        call_args = self.mock_client.deleteAttribute.call_args
        self.assertEqual(call_args[1]["id"], "ATTR1")

    def test_get_list_of_values_success(self):
        # Note: singular 'getListOfValue' (not 'getListOfValues')
        self.mock_client.getListOfValue.return_value = {"id": "LOV1", "name": "Colors", "items": []}
        result = self.operations.get_list_of_values("LOV1")
        self.assertIsNotNone(result)
        call_args = self.mock_client.getListOfValue.call_args
        self.assertEqual(call_args[1]["id"], "LOV1")

    def test_get_list_of_values_not_found(self):
        self.mock_client.getListOfValue.side_effect = Exception("404 not found")
        with self.assertRaises(exc.NotFoundError):
            self.operations.get_list_of_values("NONEXISTENT")

if __name__ == "__main__":
    unittest.main()
