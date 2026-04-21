"""Phase 5: Attribute & Metadata Operations tests for STEP REST API v2."""

import unittest
from unittest.mock import Mock, MagicMock
import logging

from stepxmlclient.rest_client.operations.attributes import AttributeOperations
from stepxmlclient.rest_client.operations.metadata import MetadataOperations
from stepxmlclient.rest_client import exceptions as exc
from stepxmlclient.rest_client.models.attribute import (
    AttributeResponse,
    AttributeListResponse,
    ListOfValueResponse,
    AttributeSearchRequest,
    AttributeCreateRequest,
    AttributeUpdateRequest,
    ListOfValueItem,
)
from stepxmlclient.rest_client.models.metadata import (
    SystemMetadataResponse,
    ContextResponse,
    ContextListResponse,
    QualifierResponse,
    QualifierListResponse,
    DimensionResponse,
    DimensionListResponse,
    UserTypeResponse,
    UserTypeListResponse,
    WorkspaceResponse,
    WorkspaceListResponse,
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
        """Test AttributeCreateRequest creation."""
        req = AttributeCreateRequest(
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
        """Test AttributeUpdateRequest creation."""
        req = AttributeUpdateRequest(
            name=None,
            description="Product size",
            required=True,
            lovId=None
        )
        self.assertEqual(req.description, "Product size")
        self.assertTrue(req.required)


class TestMetadataModels(unittest.TestCase):
    """Test Metadata model creation and validation."""
    
    def test_system_metadata_response(self):
        """Test SystemMetadataResponse creation."""
        meta = SystemMetadataResponse(
            version="2.0.1",
            apiVersion="2.0",
            capabilities=["Products", "Assets"],
            maxPageSize=500,
            defaultPageSize=None,
            supportedLanguages=None
        )
        self.assertEqual(meta.version, "2.0.1")
        self.assertEqual(meta.apiVersion, "2.0")
        self.assertEqual(len(meta.capabilities), 2)
    
    def test_context_response(self):
        """Test ContextResponse creation."""
        context = ContextResponse(
            id="Context1",
            name="Primary Context",
            isDefault=True, 
            description=None, 
            metadata=None, 
            type=None
        )
        self.assertEqual(context.id, "Context1")
        self.assertTrue(context.isDefault)
    
    def test_context_list_response(self):
        """Test ContextListResponse creation."""
        response = ContextListResponse(
            items=[
                ContextResponse(id="Context1", name="Primary", isDefault=None, description=None, metadata=None, type=None),
                ContextResponse(id="Context2", name="Secondary", isDefault=None, description=None, metadata=None, type=None)
            ],
            total=2
        )
        self.assertEqual(len(response.items), 2)
    
    def test_qualifier_response(self):
        """Test QualifierResponse creation."""
        qualifier = QualifierResponse(
            id="Qualifier1",
            name="Region",
            values=["EMEA", "APAC"],
            description=None,
            type=None
        )
        self.assertEqual(qualifier.id, "Qualifier1")
        self.assertEqual(len(qualifier.values), 2) #type: ignore
    
    def test_dimension_response(self):
        """Test DimensionResponse creation."""
        dimension = DimensionResponse(
            id="Dimension1",
            name="Size",
            type="Numeric",
            unit="cm",
            description=None,
            minValue=None,
            maxValue=None
        )
        self.assertEqual(dimension.id, "Dimension1")
        self.assertEqual(dimension.unit, "cm")
    
    def test_user_type_response(self):
        """Test UserTypeResponse creation."""
        user_type = UserTypeResponse(
            id="UserType1",
            name="StandardProduct",
            applicableEntities=["Product"],
            description=None
        )
        self.assertEqual(user_type.id, "UserType1")
        self.assertEqual(len(user_type.applicableEntities), 1) #type: ignore
    
    def test_workspace_response(self):
        """Test WorkspaceResponse creation."""
        workspace = WorkspaceResponse(
            id="Main",
            name="Main Workspace",
            isDefault=True,
            description=None
        )
        self.assertEqual(workspace.id, "Main")
        self.assertTrue(workspace.isDefault)




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
        self.mock_client.postAttributesSearch.return_value = {
            "items": [{"id": "ATTR1", "name": "Color", "type": "Text"}, {"id": "ATTR2", "name": "Size", "type": "Number"}], "total": 2}
        condition = {"conditionType": "objecttype", "objectTypeId": "AttributeType"}
        result = self.operations.search_attributes(condition=condition)
        self.assertEqual(len(result.items), 2)
        call_args = self.mock_client.postAttributesSearch.call_args
        self.assertEqual(call_args[1]["body"]["condition"], condition)

    def test_search_attributes_requires_condition(self):
        with self.assertRaises(exc.ValidationError):
            self.operations.search_attributes(condition=None)

    def test_create_attribute_success(self):
        self.mock_client.postAttributes.return_value = {"id": "NEWATTR", "name": "New", "type": "Text"}
        from stepxmlclient.rest_client.models.attribute import AttributeCreateRequest
        request = AttributeCreateRequest(name="New", type="Text")
        result = self.operations.create_attribute(request)
        self.assertEqual(result.id, "NEWATTR")
        self.mock_client.postAttributes.assert_called_once()

    def test_create_attribute_conflict(self):
        self.mock_client.postAttributes.side_effect = Exception("409 conflict")
        from stepxmlclient.rest_client.models.attribute import AttributeCreateRequest
        request = AttributeCreateRequest(name="Existing", type="Text")
        with self.assertRaises(exc.ConflictError):
            self.operations.create_attribute(request)

    def test_update_attribute_success(self):
        self.mock_client.patchAttribute.return_value = {"id": "ATTR1", "name": "Updated", "type": "Text"}
        from stepxmlclient.rest_client.models.attribute import AttributeUpdateRequest
        updates = AttributeUpdateRequest(name="Updated")
        result = self.operations.update_attribute("ATTR1", updates)
        self.assertEqual(result.name, "Updated")
        call_args = self.mock_client.patchAttribute.call_args
        self.assertEqual(call_args[1]["id"], "ATTR1")

    def test_update_attribute_not_found(self):
        self.mock_client.patchAttribute.side_effect = Exception("404 not found")
        from stepxmlclient.rest_client.models.attribute import AttributeUpdateRequest
        updates = AttributeUpdateRequest(name="Updated")
        with self.assertRaises(exc.NotFoundError):
            self.operations.update_attribute("NONEXISTENT", updates)

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

    def test_search_list_of_values(self):
        self.mock_client.postListOfValuesSearch.return_value = {
            "items": [{"id": "LOV1"}], "total": 1}
        condition = {"conditionType": "name", "value": "Colors"}
        result = self.operations.search_list_of_values(condition=condition)
        call_args = self.mock_client.postListOfValuesSearch.call_args
        self.assertEqual(call_args[1]["body"]["condition"], condition)

    def test_list_attributes(self):
        self.mock_client.postAttributesSearch.return_value = {"items": [], "total": 0}
        self.operations.list_attributes()
        self.mock_client.postAttributesSearch.assert_called_once()

    def test_search_by_type(self):
        self.mock_client.postAttributesSearch.return_value = {"items": [], "total": 0}
        self.operations.search_by_type("AttributeType")
        call_args = self.mock_client.postAttributesSearch.call_args
        body = call_args[1]["body"]
        self.assertEqual(body["condition"]["conditionType"], "objecttype")
        self.assertEqual(body["condition"]["objectTypeId"], "AttributeType")



class TestMetadataOperations(unittest.TestCase):
    def setUp(self):
        self.mock_client = Mock()
        self.logger = logging.getLogger(__name__)
        self.operations = MetadataOperations(self.mock_client, logger=self.logger)
        self.has_meta = True

    def test_initialization_skipped_if_no_meta_ops(self):
        # If MetadataOperations doesn't exist, skip gracefully
        if not self.has_meta:
            self.skipTest("MetadataOperations not found in attributes module")


if __name__ == "__main__":
    unittest.main()
