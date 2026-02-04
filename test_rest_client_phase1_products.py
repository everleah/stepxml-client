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
    ProductAttribute,
    ProductValue,
    CrossReference,
)
from stepxmlclient.rest_client import exceptions as exc


class TestProductModels(unittest.TestCase):
    """Tests for product model classes."""
    
    def test_product_attribute_creation(self):
        """Test ProductAttribute creation."""
        attr = ProductAttribute(name="Color", value="Red", context=None, language=None)
        self.assertEqual(attr.name, "Color")
        self.assertEqual(attr.value, "Red")
    
    def test_product_attribute_with_context(self):
        """Test ProductAttribute with context."""
        attr = ProductAttribute(
            name="Description",
            value="A red widget",
            context="Web",
            language="en"
        )
        self.assertEqual(attr.context, "Web")
        self.assertEqual(attr.language, "en")
    
    def test_product_value_creation(self):
        """Test ProductValue creation."""
        value = ProductValue(id="SKU123", attributes=None, key_values=None)
        self.assertEqual(value.id, "SKU123")
    
    def test_product_value_with_attributes(self):
        """Test ProductValue with attributes."""
        attrs = [ProductAttribute(name="Size", value="Large", context=None, language=None)]
        value = ProductValue(id="SKU123", attributes=attrs, key_values=None)
        self.assertEqual(len(value.attributes), 1) #type: ignore
        self.assertEqual(value.attributes[0].value, "Large") #type: ignore
    
    def test_cross_reference_creation(self):
        """Test CrossReference creation."""
        xref = CrossReference(type="Product", target_id="RELATED123", attributes=None)
        self.assertEqual(xref.type, "Product")
        self.assertEqual(xref.target_id, "RELATED123")
    
    def test_product_response_creation(self):
        """Test ProductResponse creation."""
        product = ProductResponse(
            id="PROD123",
            user_type_id="Product",
            name="Test Product",
            created_date=None,
            modified_date=None,
            version=None,
            metadata=None
        )
        self.assertEqual(product.id, "PROD123")
        self.assertEqual(product.name, "Test Product")
    
    def test_product_response_with_attributes_and_values(self):
        """Test ProductResponse with attributes and values."""
        attrs = [ProductAttribute(name="Color", value="Blue", context=None, language=None)]
        values = [ProductValue(id="SKU001", attributes=None, key_values=None)]
        
        product = ProductResponse(
            id="PROD123",
            user_type_id=None,
            name=None,
            attributes=attrs,
            values=values,
            created_date=None,
            modified_date=None,
            version=None,
            metadata=None
        )
        self.assertEqual(len(product.attributes), 1) #type: ignore
        self.assertEqual(len(product.values), 1) #type: ignore  
    
    def test_product_list_response_creation(self):
        """Test ProductListResponse creation."""
        products = [
            ProductResponse(id="PROD1", user_type_id=None, name=None, created_date=None, modified_date=None, version=None, metadata=None),
            ProductResponse(id="PROD2", user_type_id=None, name=None, created_date=None, modified_date=None, version=None, metadata=None),
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
        products = [ProductResponse(id=f"PROD{i}", user_type_id=None, name=None, created_date=None, modified_date=None, version=None, metadata=None) for i in range(20)]
        
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
            user_type_id=None,
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
            user_type_id=None,
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
            id="NEWPROD123",
            user_type_id="Product",
            name="New Product",
            attributes=None,
            values=None,
            cross_references=None
        )
        self.assertEqual(request.id, "NEWPROD123")
        self.assertEqual(request.name, "New Product")
    
    def test_product_update_request(self):
        """Test ProductUpdateRequest creation."""
        request = ProductUpdateRequest(
            name="Updated Name",
            user_type_id=None,
            attributes=None,
            values=None,
            cross_references=None
        )
        self.assertEqual(request.name, "Updated Name")
        self.assertIsNone(request.user_type_id)


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
            "user_type_id": "Product",
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
    
    def test_get_product_includes_params(self):
        """Test that get_product passes include parameters."""
        mock_response = {"id": "PROD123"}
        self.mock_client.getProduct.return_value = mock_response
        
        self.operations.get_product(
            "PROD123",
            include_attributes=False,
            include_values=False
        )
        
        call_args = self.mock_client.getProduct.call_args
        self.assertEqual(call_args[1]["includeAttributes"], False)
        self.assertEqual(call_args[1]["includeValues"], False)
    
    def test_search_products_success(self):
        """Test successful product search."""
        mock_response = {
            "items": [
                {"id": "PROD1", "name": "Product 1"},
                {"id": "PROD2", "name": "Product 2"},
            ],
            "total": 100
        }
        self.mock_client.searchProducts.return_value = mock_response
        
        result = self.operations.search_products(query="test")
        
        self.assertEqual(len(result.items), 2)
        self.assertEqual(result.total, 100)
        self.assertTrue(result.has_more)
    
    def test_search_products_defaults(self):
        """Test search with default parameters."""
        mock_response = {"items": [], "total": 0}
        self.mock_client.searchProducts.return_value = mock_response
        
        self.operations.search_products()
        
        call_args = self.mock_client.searchProducts.call_args
        self.assertEqual(call_args[1]["q"], "*")
        self.assertEqual(call_args[1]["limit"], 20)
        self.assertEqual(call_args[1]["offset"], 0)
    
    def test_search_products_with_filters(self):
        """Test search with optional filters."""
        mock_response = {"items": [], "total": 0}
        self.mock_client.searchProducts.return_value = mock_response
        
        self.operations.search_products(
            query="widget",
            user_type_id="ProductType1",
            modified_since="2024-01-01T00:00:00Z",
            limit=50,
            offset=10
        )
        
        call_args = self.mock_client.searchProducts.call_args
        self.assertEqual(call_args[1]["q"], "widget")
        self.assertEqual(call_args[1]["userTypeId"], "ProductType1")
        self.assertEqual(call_args[1]["modifiedSince"], "2024-01-01T00:00:00Z")
        self.assertEqual(call_args[1]["limit"], 50)
        self.assertEqual(call_args[1]["offset"], 10)
    
    def test_search_products_pagination(self):
        """Test search pagination handling."""
        mock_response = {
            "items": [{"id": f"PROD{i}"} for i in range(20)],
            "total": 100
        }
        self.mock_client.searchProducts.return_value = mock_response
        
        result = self.operations.search_products(limit=20, offset=0)
        
        self.assertTrue(result.has_more)  # 0 + 20 < 100
        
        result = self.operations.search_products(limit=20, offset=80)
        # No total in mock for second call, so has_more should be False
    
    def test_create_product_success(self):
        """Test successful product creation."""
        request = ProductCreateRequest(
            id="NEWPROD",
            user_type_id=None,
            name="New Product",
            attributes=None,
            values=None,
            cross_references=None
        )
        mock_response = {
            "id": "NEWPROD",
            "name": "New Product"
        }
        self.mock_client.createProduct.return_value = mock_response
        
        result = self.operations.create_product(request)
        
        self.assertEqual(result.id, "NEWPROD")
        self.mock_client.createProduct.assert_called_once()
    
    def test_create_product_conflict(self):
        """Test product creation with existing ID."""
        request = ProductCreateRequest(
            id="EXISTING",
            user_type_id=None,
            name=None,
            attributes=None,
            values=None,
            cross_references=None
        )
        self.mock_client.createProduct.side_effect = Exception("409 conflict")
        
        with self.assertRaises(exc.ConflictError):
            self.operations.create_product(request)
    
    def test_create_product_validation_error(self):
        """Test product creation with invalid data."""
        request = ProductCreateRequest(
            id="NEWPROD",
            user_type_id=None,
            name=None,
            attributes=None,
            values=None,
            cross_references=None
        )
        self.mock_client.createProduct.side_effect = Exception("400 invalid")
        
        with self.assertRaises(exc.ValidationError):
            self.operations.create_product(request)
    
    def test_create_product_requires_id(self):
        """Test that product creation requires an ID."""
        # Pydantic validates at model creation, so we test the exception type
        from pydantic import ValidationError as PydanticValidationError
        
        with self.assertRaises(PydanticValidationError):
            ProductCreateRequest(
                id=None, #type: ignore
                user_type_id=None,
                name=None,
                attributes=None,
                values=None,
                cross_references=None
            )
    
    def test_update_product_success(self):
        """Test successful product update."""
        updates = ProductUpdateRequest(
            name="Updated Name",
            user_type_id=None,
            attributes=None,
            values=None,
            cross_references=None
        )
        mock_response = {
            "id": "PROD123",
            "name": "Updated Name"
        }
        self.mock_client.updateProduct.return_value = mock_response
        
        result = self.operations.update_product("PROD123", updates)
        
        self.assertEqual(result.name, "Updated Name")
        self.mock_client.updateProduct.assert_called_once()
    
    def test_update_product_not_found(self):
        """Test product update when not found."""
        updates = ProductUpdateRequest(name="Updated", user_type_id=None, attributes=None, values=None, cross_references=None)
        self.mock_client.updateProduct.side_effect = Exception("404 not found")
        
        with self.assertRaises(exc.NotFoundError):
            self.operations.update_product("NONEXISTENT", updates)
    
    def test_delete_product_success(self):
        """Test successful product deletion."""
        self.mock_client.deleteProduct.return_value = None
        
        result = self.operations.delete_product("PROD123")
        
        self.assertTrue(result)
        self.mock_client.deleteProduct.assert_called_once_with(productId="PROD123")
    
    def test_delete_product_not_found(self):
        """Test product deletion when not found."""
        self.mock_client.deleteProduct.side_effect = Exception("404 not found")
        
        with self.assertRaises(exc.NotFoundError):
            self.operations.delete_product("NONEXISTENT")
    
    def test_get_product_attributes(self):
        """Test getting product attributes."""
        mock_response = {
            "items": [
                {"name": "Color", "value": "Red"},
                {"name": "Size", "value": "Large"},
            ]
        }
        self.mock_client.getProductAttributes.return_value = mock_response
        
        result = self.operations.get_product_attributes("PROD123")
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["name"], "Color")
    
    def test_get_product_attributes_list_response(self):
        """Test getting product attributes with list response."""
        mock_response = [
            {"name": "Color", "value": "Red"},
        ]
        self.mock_client.getProductAttributes.return_value = mock_response
        
        result = self.operations.get_product_attributes("PROD123")
        
        self.assertEqual(len(result), 1)
    
    def test_get_product_values(self):
        """Test getting product values."""
        mock_response = {
            "items": [
                {"id": "SKU001"},
                {"id": "SKU002"},
            ]
        }
        self.mock_client.getProductValues.return_value = mock_response
        
        result = self.operations.get_product_values("PROD123")
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id"], "SKU001")
    
    def test_list_products(self):
        """Test list_products convenience method."""
        mock_response = {"items": [], "total": 0}
        self.mock_client.searchProducts.return_value = mock_response
        
        self.operations.list_products()
        
        call_args = self.mock_client.searchProducts.call_args
        self.assertEqual(call_args[1]["q"], "*")
    
    def test_search_by_type(self):
        """Test search_by_type convenience method."""
        mock_response = {"items": [], "total": 0}
        self.mock_client.searchProducts.return_value = mock_response
        
        self.operations.search_by_type("ProductType1")
        
        call_args = self.mock_client.searchProducts.call_args
        self.assertEqual(call_args[1]["userTypeId"], "ProductType1")
    
    def test_search_modified_since(self):
        """Test search_modified_since convenience method."""
        mock_response = {"items": [], "total": 0}
        self.mock_client.searchProducts.return_value = mock_response
        
        self.operations.search_modified_since("2024-01-01T00:00:00Z")
        
        call_args = self.mock_client.searchProducts.call_args
        self.assertEqual(call_args[1]["modifiedSince"], "2024-01-01T00:00:00Z")


if __name__ == '__main__':
    unittest.main()
