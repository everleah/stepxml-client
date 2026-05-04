"""Phase 1 - Product Operations tests.

Tests for product CRUD operations, search, and integration with the REST client.
"""

import unittest
from unittest.mock import Mock, MagicMock, patch
import logging

from stepxmlclient.rest_client.operations.products import ProductOperations
from stepxmlclient.rest_client.models.product import (
    ProductResponse,
    ProductListResponse,
    ProductSearchRequest,
    ProductCreateRequest,
    ProductUpdateRequest,
)
from stepxmlclient.rest_client import exceptions as exc


class TestProductModels(unittest.TestCase):
    """Tests for product model classes."""
    
    def test_product_response_creation(self):
        """Test ProductResponse creation."""
        product = ProductResponse(
            id="PROD123",
            name="Test Product",
            objectType="SalesItem",
            parent="I-Level3-122",
            values=None,
            references=None,
            attributeLinks=None,
            dataContainers=None,
        )
        self.assertEqual(product.id, "PROD123")
        self.assertEqual(product.name, "Test Product")
    
    def test_product_response_with_values_and_references(self):
        """Test ProductResponse with values and references."""
        product = ProductResponse(
            id="PROD123",
            objectType=None,
            parent=None,
            name=None,
            values={"UPC": {"value": {"value": "123"}}},
            references={"Accessory": {"references": [{"target": "I-SalesItem-1111"}]}},
            attributeLinks=None,
            dataContainers=None,
        )
        self.assertIn("UPC", product.values) #type: ignore[operator]
        self.assertIn("Accessory", product.references) #type: ignore[operator]
    
    def test_product_list_response_creation(self):
        """Test ProductListResponse creation."""
        products = [
            ProductResponse(id="PROD1", objectType=None, parent=None, name=None, values=None, references=None, attributeLinks=None, dataContainers=None),
            ProductResponse(id="PROD2", objectType=None, parent=None, name=None, values=None, references=None, attributeLinks=None, dataContainers=None),
        ]
        response = ProductListResponse(
            items=products,
            total=100,
            limit=20,
            offset=0,
            has_more=True
        )
        self.assertEqual(len(response.items), 2)
        self.assertEqual(response.total, 100)
    
    def test_product_list_response_has_more(self):
        """Test ProductListResponse has_more calculation."""
        products = [ProductResponse(id=f"PROD{i}", objectType=None, parent=None, name=None, values=None, references=None, attributeLinks=None, dataContainers=None) for i in range(20)]
        
        # Has more results
        response = ProductListResponse(
            items=products,
            total=100,
            limit=20,
            offset=0,
            has_more=True
        )
        self.assertTrue(response.has_more)
        
        # No more results
        response = ProductListResponse(
            items=products,
            total=100,
            limit=20,
            offset=80,
            has_more=False
        )
        self.assertFalse(response.has_more)
    
    def test_product_search_request_creation(self):
        """Test ProductSearchRequest creation."""
        request = ProductSearchRequest(
            query="widget",
            object_type=None,
            modified_since=None,
            limit=50,
            offset=10,
            include_values=True,
            include_attributes=True
        )
        self.assertEqual(request.query, "widget")
        self.assertEqual(request.limit, 50)
        self.assertEqual(request.offset, 10)
    
    def test_product_search_request_defaults(self):
        """Test ProductSearchRequest defaults."""
        request = ProductSearchRequest(
            query="*",
            object_type=None,
            modified_since=None,
            limit=20,
            offset=0,
            include_values=True,
            include_attributes=True
        )
        self.assertEqual(request.query, "*")
        self.assertEqual(request.limit, 20)
        self.assertEqual(request.offset, 0)
        self.assertTrue(request.include_values)
        self.assertTrue(request.include_attributes)
    
    def test_product_create_request(self):
        """Test ProductCreateRequest creation."""
        request = ProductCreateRequest(
            objectType="SalesItem",
            parent="I-Level3-122",
            name="New Product",
            values=None,
            references=None,
            attributeLinks=None,
            dataContainers=None,
        )
        self.assertEqual(request.objectType, "SalesItem")
        self.assertEqual(request.name, "New Product")
    
    def test_product_update_request(self):
        """Test ProductUpdateRequest creation."""
        request = ProductUpdateRequest(
            name="Updated Name",
            parent=None,
            values=None,
            references=None,
            attributeLinks=None,
            dataContainers=None,
        )
        self.assertEqual(request.name, "Updated Name")
        self.assertIsNone(request.parent)


class TestProductOperations(unittest.TestCase):
    """Tests for ProductOperations class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.logger = logging.getLogger(__name__)
        self.operations = ProductOperations(self.mock_client, logger=self.logger)
    
    def test_product_operations_initialization(self):
        """Test ProductOperations initialization."""
        self.assertEqual(self.operations.operation_name, "ProductOperations")
        self.assertIsNotNone(self.operations.logger)
    
    def test_get_product_success(self):
        """Test successful product retrieval."""
        mock_response = {
            "id": "PROD123",
            "objectType": "SalesItem",
            "name": "Test Product"
        }
        self.mock_client.getProduct.return_value = mock_response
        
        result = self.operations.get_product("PROD123")
        
        self.assertEqual(result.id, "PROD123")
        self.assertEqual(result.name, "Test Product")
        self.mock_client.getProduct.assert_called_once()
    
    def test_get_product_not_found(self):
        """Test product retrieval when not found."""
        self.mock_client.getProduct.side_effect = Exception("404 not found")
        
        with self.assertRaises(exc.NotFoundError):
            self.operations.get_product("NONEXISTENT")
    
    def test_get_product_validation(self):
        """Test product retrieval validation."""
        with self.assertRaises(exc.ValidationError):
            self.operations.get_product(None)
    
    def test_get_product_with_key_id(self):
        """Test that get_product passes keyId when provided."""
        mock_response = {"id": "PROD123"}
        self.mock_client.getProduct.return_value = mock_response
        
        self.operations.get_product("PROD123", key_id="MyKey")
        
        call_args = self.mock_client.getProduct.call_args
        self.assertEqual(call_args[1]["id"], "PROD123")
        self.assertEqual(call_args[1]["keyId"], "MyKey")
    
    def test_get_product_with_include_inherited_data(self):
        """Test that get_product passes includeInheritedData when True."""
        mock_response = {"id": "PROD123"}
        self.mock_client.getProduct.return_value = mock_response
        
        self.operations.get_product("PROD123", include_inherited_data=True)
        
        call_args = self.mock_client.getProduct.call_args
        self.assertEqual(call_args[1]["includeInheritedData"], True)
    
    def test_get_product_uses_id_param(self):
        """Test that get_product uses 'id' (not 'productId') as path parameter."""
        mock_response = {"id": "PROD123"}
        self.mock_client.getProduct.return_value = mock_response
        
        self.operations.get_product("PROD123")
        
        call_args = self.mock_client.getProduct.call_args
        self.assertIn("id", call_args[1])
        self.assertNotIn("productId", call_args[1])
        self.assertEqual(call_args[1]["id"], "PROD123")
    
    def test_search_products_success(self):
        """Test successful product search with condition."""
        mock_response = {
            "items": [
                {"id": "PROD1", "name": "Product 1"},
                {"id": "PROD2", "name": "Product 2"},
            ],
            "total": 2
        }
        self.mock_client.postProductsSearch.return_value = mock_response
        condition = {"conditionType": "objecttype", "objectType": "MyType"}
        
        result = self.operations.search_products(condition=condition)
        
        self.mock_client.postProductsSearch.assert_called_once()
        call_args = self.mock_client.postProductsSearch.call_args
        self.assertEqual(call_args[1]["json"]["condition"], condition)
    
    def test_search_products_uses_json(self):
        """Test that search_products passes condition in JSON payload."""
        mock_response = {"items": [], "total": 0}
        self.mock_client.postProductsSearch.return_value = mock_response
        condition = {"conditionType": "name", "value": "Widget*"}
        
        self.operations.search_products(condition=condition)
        
        call_args = self.mock_client.postProductsSearch.call_args
        self.assertIn("json", call_args[1])
        self.assertEqual(call_args[1]["json"]["condition"], condition)
    
    def test_search_products_requires_condition(self):
        """Test that search_products requires a condition."""
        with self.assertRaises(exc.ValidationError):
            self.operations.search_products(condition=None)
    
    def test_create_product_success(self):
        """Test successful product creation."""
        request = ProductCreateRequest(
            objectType="SalesItem",
            parent="I-Level3-122",
            name="New Product",
            values=None,
            references=None,
            attributeLinks=None,
            dataContainers=None,
        )
        mock_response = {
            "id": "NEWPROD",
            "name": "New Product"
        }
        self.mock_client.postProducts.return_value = mock_response
        
        result = self.operations.create_product(request)
        
        self.assertEqual(result.id, "NEWPROD")
        self.mock_client.postProducts.assert_called_once()
    
    def test_create_product_conflict(self):
        """Test product creation with existing ID."""
        request = ProductCreateRequest(
            objectType="SalesItem",
            parent="I-Level3-122",
            name=None,
            values=None,
            references=None,
            attributeLinks=None,
            dataContainers=None,
        )
        self.mock_client.postProducts.side_effect = Exception("409 conflict")
        
        with self.assertRaises(exc.ConflictError):
            self.operations.create_product(request)
    
    def test_create_product_validation_error(self):
        """Test product creation with invalid data."""
        request = ProductCreateRequest(
            objectType="SalesItem",
            parent="I-Level3-122",
            name=None,
            values=None,
            references=None,
            attributeLinks=None,
            dataContainers=None,
        )
        self.mock_client.postProducts.side_effect = Exception("400 invalid")
        
        with self.assertRaises(exc.ValidationError):
            self.operations.create_product(request)
    
    def test_create_product_requires_object_type(self):
        """Test that product creation requires objectType."""
        from pydantic import ValidationError as PydanticValidationError
        
        with self.assertRaises(PydanticValidationError):
            ProductCreateRequest(
                objectType=None, #type: ignore
                parent="I-Level3-122",
                name=None,
                values=None,
                references=None,
                attributeLinks=None,
                dataContainers=None,
            )

    def test_create_product_requires_parent(self):
        """Test that product creation requires parent."""
        from pydantic import ValidationError as PydanticValidationError

        with self.assertRaises(PydanticValidationError):
            ProductCreateRequest(
                objectType="SalesItem",
                parent=None, #type: ignore
                name=None,
                values=None,
                references=None,
                attributeLinks=None,
                dataContainers=None,
            )
    
    def test_update_product_success(self):
        """Test successful product update (PATCH)."""
        updates = ProductUpdateRequest(
            name="Updated Name",
            parent=None,
            values=None,
            references=None,
            attributeLinks=None,
            dataContainers=None,
        )
        mock_response = {
            "id": "PROD123",
            "name": "Updated Name"
        }
        self.mock_client.patchProduct.return_value = mock_response
        
        result = self.operations.update_product("PROD123", updates)
        
        self.assertEqual(result.name, "Updated Name")
        self.mock_client.patchProduct.assert_called_once()
        call_args = self.mock_client.patchProduct.call_args
        self.assertEqual(call_args[1]["id"], "PROD123")
        self.assertNotIn("productId", call_args[1])
    
    def test_update_product_not_found(self):
        """Test product update when not found."""
        updates = ProductUpdateRequest(name="Updated", parent=None, values=None, references=None, attributeLinks=None, dataContainers=None)
        self.mock_client.patchProduct.side_effect = Exception("404 not found")
        
        with self.assertRaises(exc.NotFoundError):
            self.operations.update_product("NONEXISTENT", updates)
    
    def test_update_product_with_key_id(self):
        """Test update_product passes keyId when provided."""
        updates = ProductUpdateRequest(name="Updated", parent=None, values=None, references=None, attributeLinks=None, dataContainers=None)
        mock_response = {"id": "PROD123"}
        self.mock_client.patchProduct.return_value = mock_response
        
        self.operations.update_product("PROD123", updates, key_id="MyKey")
        
        call_args = self.mock_client.patchProduct.call_args
        self.assertEqual(call_args[1]["keyId"], "MyKey")
    
    def test_replace_product_success(self):
        """Test full product replacement (PUT)."""
        data = ProductCreateRequest(
            objectType="SalesItem",
            parent="ElectricGuitars",
            name="Replaced Product",
            values=None,
            references=None,
            attributeLinks=None,
            dataContainers=None,
        )
        mock_response = {"id": "PROD123", "name": "Replaced Product"}
        self.mock_client.putProduct.return_value = mock_response
        
        result = self.operations.replace_product("PROD123", data)
        
        self.assertEqual(result.id, "PROD123")
        self.mock_client.putProduct.assert_called_once()
        call_args = self.mock_client.putProduct.call_args
        self.assertEqual(call_args[1]["id"], "PROD123")
    
    def test_replace_product_with_allow_overwrite(self):
        """Test replace_product passes allow-overwrite."""
        data = ProductCreateRequest(
            objectType="SalesItem",
            parent="ElectricGuitars",
            name=None,
            values=None,
            references=None,
            attributeLinks=None,
            dataContainers=None,
        )
        mock_response = {"id": "PROD123"}
        self.mock_client.putProduct.return_value = mock_response
        
        self.operations.replace_product("PROD123", data, allow_overwrite=True)
        
        call_args = self.mock_client.putProduct.call_args
        self.assertEqual(call_args[1]["allow-overwrite"], True)
    
    def test_delete_product_success(self):
        """Test successful product deletion."""
        self.mock_client.deleteProduct.return_value = None
        
        result = self.operations.delete_product("PROD123")
        
        self.assertTrue(result)
        call_args = self.mock_client.deleteProduct.call_args
        self.assertEqual(call_args[1]["id"], "PROD123")
        self.assertNotIn("productId", call_args[1])
    
    def test_delete_product_not_found(self):
        """Test product deletion when not found."""
        self.mock_client.deleteProduct.side_effect = Exception("404 not found")
        
        with self.assertRaises(exc.NotFoundError):
            self.operations.delete_product("NONEXISTENT")
    
    def test_delete_product_with_key_id(self):
        """Test delete_product passes keyId when provided."""
        self.mock_client.deleteProduct.return_value = None
        
        self.operations.delete_product("PROD123", key_id="MyKey")
        
        call_args = self.mock_client.deleteProduct.call_args
        self.assertEqual(call_args[1]["keyId"], "MyKey")
    
    def test_get_product_attributes(self):
        """Test getting product attributes (calls getProductValue)."""
        mock_response = {
            "items": [
                {"name": "Color", "value": "Red"},
                {"name": "Size", "value": "Large"},
            ]
        }
        self.mock_client.getProductValue.return_value = mock_response
        
        result = self.operations.get_product_attributes("PROD123")
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["name"], "Color")
    
    def test_get_product_attributes_list_response(self):
        """Test getting product attributes with list response."""
        mock_response = [
            {"name": "Color", "value": "Red"},
        ]
        self.mock_client.getProductValue.return_value = mock_response
        
        result = self.operations.get_product_attributes("PROD123")
        
        self.assertEqual(len(result), 1)
    
    def test_get_product_values(self):
        """Test getting product values (calls getProductValue)."""
        mock_response = {
            "items": [
                {"id": "SKU001"},
                {"id": "SKU002"},
            ]
        }
        self.mock_client.getProductValue.return_value = mock_response
        
        result = self.operations.get_product_values("PROD123")
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id"], "SKU001")
    
    def test_search_by_type(self):
        """Test search_by_type convenience method uses condition."""
        mock_response = {"items": [], "total": 0}
        self.mock_client.postProductsSearch.return_value = mock_response
        
        self.operations.search_by_type("ProductType1")
        
        call_args = self.mock_client.postProductsSearch.call_args
        payload = call_args[1]["json"]
        self.assertEqual(payload["condition"]["conditionType"], "objecttype")
        self.assertEqual(payload["condition"]["objectType"], "ProductType1")
    
    def test_search_by_id(self):
        """Test search_by_id convenience method uses condition."""
        mock_response = {"items": [], "total": 0}
        self.mock_client.postProductsSearch.return_value = mock_response
        
        self.operations.search_by_id("PROD123")
        
        call_args = self.mock_client.postProductsSearch.call_args
        payload = call_args[1]["json"]
        self.assertEqual(payload["condition"]["conditionType"], "id")
        self.assertEqual(payload["condition"]["id"], "PROD123")
    

if __name__ == '__main__':
    unittest.main()
