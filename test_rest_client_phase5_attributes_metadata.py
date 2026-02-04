"""Phase 5: Attribute & Metadata Operations tests for STEP REST API v2."""

import unittest
from unittest.mock import Mock, MagicMock
import logging

from stepxmlclient.rest_client.operations.attributes import AttributeOperations
from stepxmlclient.rest_client.operations.metadata import MetadataOperations
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
            type="Text"
        )
        self.assertEqual(attr.id, "ATTR001")
        self.assertEqual(attr.name, "Color")
        self.assertEqual(attr.type, "Text")
    
    def test_attribute_list_response_creation(self):
        """Test AttributeListResponse model creation."""
        response = AttributeListResponse(
            items=[
                AttributeResponse(id="ATTR001", name="Color", type="Text"),
                AttributeResponse(id="ATTR002", name="Size", type="Text")
            ],
            total=50,
            limit=20,
            offset=0
        )
        self.assertEqual(len(response.items), 2)
        self.assertEqual(response.total, 50)
    
    def test_list_of_value_response_creation(self):
        """Test ListOfValueResponse model creation."""
        lov = ListOfValueResponse(
            id="LOV001",
            name="Colors",
            items=[
                ListOfValueItem(id="RED", name="Red"),
                ListOfValueItem(id="BLUE", name="Blue")
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
            required=True
        )
        self.assertEqual(req.name, "Size")
        self.assertEqual(req.type, "Text")
        self.assertTrue(req.required)
    
    def test_attribute_update_request(self):
        """Test AttributeUpdateRequest creation."""
        req = AttributeUpdateRequest(
            description="Product size",
            required=True
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
            maxPageSize=500
        )
        self.assertEqual(meta.version, "2.0.1")
        self.assertEqual(meta.apiVersion, "2.0")
        self.assertEqual(len(meta.capabilities), 2)
    
    def test_context_response(self):
        """Test ContextResponse creation."""
        context = ContextResponse(
            id="Context1",
            name="Primary Context",
            isDefault=True
        )
        self.assertEqual(context.id, "Context1")
        self.assertTrue(context.isDefault)
    
    def test_context_list_response(self):
        """Test ContextListResponse creation."""
        response = ContextListResponse(
            items=[
                ContextResponse(id="Context1", name="Primary"),
                ContextResponse(id="Context2", name="Secondary")
            ],
            total=2
        )
        self.assertEqual(len(response.items), 2)
    
    def test_qualifier_response(self):
        """Test QualifierResponse creation."""
        qualifier = QualifierResponse(
            id="Qualifier1",
            name="Region",
            values=["EMEA", "APAC"]
        )
        self.assertEqual(qualifier.id, "Qualifier1")
        self.assertEqual(len(qualifier.values), 2)
    
    def test_dimension_response(self):
        """Test DimensionResponse creation."""
        dimension = DimensionResponse(
            id="Dimension1",
            name="Size",
            type="Numeric",
            unit="cm"
        )
        self.assertEqual(dimension.id, "Dimension1")
        self.assertEqual(dimension.unit, "cm")
    
    def test_user_type_response(self):
        """Test UserTypeResponse creation."""
        user_type = UserTypeResponse(
            id="UserType1",
            name="StandardProduct",
            applicableEntities=["Product"]
        )
        self.assertEqual(user_type.id, "UserType1")
        self.assertEqual(len(user_type.applicableEntities), 1)
    
    def test_workspace_response(self):
        """Test WorkspaceResponse creation."""
        workspace = WorkspaceResponse(
            id="Main",
            name="Main Workspace",
            isDefault=True
        )
        self.assertEqual(workspace.id, "Main")
        self.assertTrue(workspace.isDefault)


class TestAttributeOperations(unittest.TestCase):
    """Test Attribute operation methods."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.logger = logging.getLogger("test")
        self.operations = AttributeOperations(self.mock_client, logger=self.logger)
    
    def test_get_attribute_success(self):
        """Test successful get_attribute operation."""
        mock_response = {
            "id": "ATTR001",
            "name": "Color",
            "type": "Text"
        }
        self.mock_client.getAttribute.return_value = mock_response
        
        result = self.operations.get_attribute("ATTR001")
        
        self.assertIsInstance(result, AttributeResponse)
        self.assertEqual(result.id, "ATTR001")
        self.assertEqual(result.name, "Color")
    
    def test_get_attribute_not_found(self):
        """Test get_attribute raises NotFoundError."""
        self.mock_client.getAttribute.side_effect = Exception("404")
        
        with self.assertRaises(NotFoundError):
            self.operations.get_attribute("NONEXISTENT")
    
    def test_search_attributes_success(self):
        """Test successful search_attributes operation."""
        mock_response = {
            "items": [
                {"id": "ATTR001", "name": "Color", "type": "Text"},
                {"id": "ATTR002", "name": "Size", "type": "Text"}
            ],
            "total": 100,
            "limit": 20,
            "offset": 0
        }
        self.mock_client.searchAttributes.return_value = mock_response
        
        result = self.operations.search_attributes()
        
        self.assertIsInstance(result, AttributeListResponse)
        self.assertEqual(len(result.items), 2)
        self.assertEqual(result.total, 100)
    
    def test_search_attributes_with_filter(self):
        """Test search_attributes with type filter."""
        mock_response = {
            "items": [{"id": "ATTR001", "name": "Color", "type": "Text"}],
            "total": 10,
            "limit": 20,
            "offset": 0
        }
        self.mock_client.searchAttributes.return_value = mock_response
        
        result = self.operations.search_attributes(type_filter="Text")
        
        self.assertEqual(result.total, 10)
        call_kwargs = self.mock_client.searchAttributes.call_args[1]
        self.assertEqual(call_kwargs.get("typeFilter"), "Text")
    
    def test_list_attributes(self):
        """Test list_attributes convenience method."""
        mock_response = {
            "items": [{"id": "ATTR001", "name": "Color", "type": "Text"}],
            "total": 1,
            "limit": 20,
            "offset": 0
        }
        self.mock_client.searchAttributes.return_value = mock_response
        
        result = self.operations.list_attributes()
        
        self.assertIsInstance(result, AttributeListResponse)
    
    def test_create_attribute_success(self):
        """Test successful create_attribute operation."""
        mock_response = {
            "id": "ATTR001",
            "name": "New Attribute",
            "type": "Text"
        }
        self.mock_client.createAttribute.return_value = mock_response
        
        req = AttributeCreateRequest(name="New Attribute", type="Text")
        result = self.operations.create_attribute(req)
        
        self.assertIsInstance(result, AttributeResponse)
        self.assertEqual(result.name, "New Attribute")
    
    def test_update_attribute_success(self):
        """Test successful update_attribute operation."""
        mock_response = {
            "id": "ATTR001",
            "name": "Updated Attribute",
            "type": "Text"
        }
        self.mock_client.updateAttribute.return_value = mock_response
        
        updates = AttributeUpdateRequest(description="Updated")
        result = self.operations.update_attribute("ATTR001", updates)
        
        self.assertEqual(result.name, "Updated Attribute")
    
    def test_delete_attribute_success(self):
        """Test successful delete_attribute operation."""
        self.mock_client.deleteAttribute.return_value = True
        
        result = self.operations.delete_attribute("ATTR001")
        
        self.assertTrue(result)
    
    def test_get_list_of_values_success(self):
        """Test successful get_list_of_values operation."""
        mock_response = {
            "id": "LOV001",
            "name": "Colors",
            "items": [
                {"id": "RED", "name": "Red"},
                {"id": "BLUE", "name": "Blue"}
            ],
            "total": 2
        }
        self.mock_client.getListOfValues.return_value = mock_response
        
        result = self.operations.get_list_of_values("LOV001")
        
        self.assertIsInstance(result, ListOfValueResponse)
        self.assertEqual(result.id, "LOV001")
        self.assertEqual(len(result.items), 2)
    
    def test_search_by_type(self):
        """Test search_by_type convenience method."""
        mock_response = {
            "items": [{"id": "ATTR001", "name": "Color", "type": "Text"}],
            "total": 5,
            "limit": 20,
            "offset": 0
        }
        self.mock_client.searchAttributes.return_value = mock_response
        
        result = self.operations.search_by_type("Text")
        
        call_kwargs = self.mock_client.searchAttributes.call_args[1]
        self.assertEqual(call_kwargs.get("typeFilter"), "Text")


class TestMetadataOperations(unittest.TestCase):
    """Test Metadata operation methods."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.logger = logging.getLogger("test")
        self.operations = MetadataOperations(self.mock_client, logger=self.logger)
    
    def test_get_system_info_success(self):
        """Test successful get_system_info operation."""
        mock_response = {
            "version": "2.0.1",
            "apiVersion": "2.0",
            "capabilities": ["Products", "Assets"],
            "maxPageSize": 500
        }
        self.mock_client.getSystemInfo.return_value = mock_response
        
        result = self.operations.get_system_info()
        
        self.assertIsInstance(result, SystemMetadataResponse)
        self.assertEqual(result.version, "2.0.1")
    
    def test_list_contexts_success(self):
        """Test successful list_contexts operation."""
        mock_response = {
            "items": [
                {"id": "Context1", "name": "Primary"},
                {"id": "Context2", "name": "Secondary"}
            ],
            "total": 2
        }
        self.mock_client.listContexts.return_value = mock_response
        
        result = self.operations.list_contexts()
        
        self.assertIsInstance(result, ContextListResponse)
        self.assertEqual(len(result.items), 2)
    
    def test_get_context_success(self):
        """Test successful get_context operation."""
        mock_response = {
            "id": "Context1",
            "name": "Primary Context",
            "isDefault": True
        }
        self.mock_client.getContext.return_value = mock_response
        
        result = self.operations.get_context("Context1")
        
        self.assertIsInstance(result, ContextResponse)
        self.assertTrue(result.isDefault)
    
    def test_list_qualifiers_success(self):
        """Test successful list_qualifiers operation."""
        mock_response = {
            "items": [
                {"id": "Qualifier1", "name": "Region"}
            ],
            "total": 1
        }
        self.mock_client.listQualifiers.return_value = mock_response
        
        result = self.operations.list_qualifiers()
        
        self.assertIsInstance(result, QualifierListResponse)
    
    def test_get_qualifier_success(self):
        """Test successful get_qualifier operation."""
        mock_response = {
            "id": "Qualifier1",
            "name": "Region",
            "values": ["EMEA", "APAC"]
        }
        self.mock_client.getQualifier.return_value = mock_response
        
        result = self.operations.get_qualifier("Qualifier1")
        
        self.assertIsInstance(result, QualifierResponse)
    
    def test_list_dimensions_success(self):
        """Test successful list_dimensions operation."""
        mock_response = {
            "items": [
                {"id": "Dimension1", "name": "Size", "type": "Numeric"}
            ],
            "total": 1
        }
        self.mock_client.listDimensions.return_value = mock_response
        
        result = self.operations.list_dimensions()
        
        self.assertIsInstance(result, DimensionListResponse)
    
    def test_get_dimension_success(self):
        """Test successful get_dimension operation."""
        mock_response = {
            "id": "Dimension1",
            "name": "Size",
            "type": "Numeric",
            "unit": "cm"
        }
        self.mock_client.getDimension.return_value = mock_response
        
        result = self.operations.get_dimension("Dimension1")
        
        self.assertIsInstance(result, DimensionResponse)
        self.assertEqual(result.unit, "cm")
    
    def test_list_user_types_success(self):
        """Test successful list_user_types operation."""
        mock_response = {
            "items": [
                {"id": "UserType1", "name": "StandardProduct"}
            ],
            "total": 1
        }
        self.mock_client.listUserTypes.return_value = mock_response
        
        result = self.operations.list_user_types()
        
        self.assertIsInstance(result, UserTypeListResponse)
    
    def test_get_user_type_success(self):
        """Test successful get_user_type operation."""
        mock_response = {
            "id": "UserType1",
            "name": "StandardProduct",
            "applicableEntities": ["Product"]
        }
        self.mock_client.getUserType.return_value = mock_response
        
        result = self.operations.get_user_type("UserType1")
        
        self.assertIsInstance(result, UserTypeResponse)
    
    def test_list_workspaces_success(self):
        """Test successful list_workspaces operation."""
        mock_response = {
            "items": [
                {"id": "Main", "name": "Main Workspace"}
            ],
            "total": 1
        }
        self.mock_client.listWorkspaces.return_value = mock_response
        
        result = self.operations.list_workspaces()
        
        self.assertIsInstance(result, WorkspaceListResponse)
    
    def test_get_workspace_success(self):
        """Test successful get_workspace operation."""
        mock_response = {
            "id": "Main",
            "name": "Main Workspace",
            "isDefault": True
        }
        self.mock_client.getWorkspace.return_value = mock_response
        
        result = self.operations.get_workspace("Main")
        
        self.assertIsInstance(result, WorkspaceResponse)
        self.assertTrue(result.isDefault)


if __name__ == '__main__':
    unittest.main()
