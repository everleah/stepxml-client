"""Product operations for STEP REST API.

Provides CRUD and search operations for products.
"""

from typing import Optional, List, Dict, Any
import logging

import requests_openapi as roa

from ..base import BaseOperation, handle_rest_errors
from ..models.common import PagedResponse, PageInfo
from ..models.product import (
    ProductResponse,
    ProductListResponse,
    ProductSearchRequest,
    ProductCreateRequest,
    ProductUpdateRequest,
)
from .. import exceptions as exc


class ProductOperations(BaseOperation):
    """Product CRUD and search operations.
    
    Provides methods for:
    - Retrieving single products
    - Searching and listing products
    - Creating new products
    - Updating existing products
    - Deleting products
    - Accessing product attributes and values
    """
    
    def __init__(self, client: roa.Client, logger: logging.Logger = None):
        """Initialize ProductOperations.
        
        Args:
            client: The requests-openapi Client instance
            logger: Logger instance (optional)
        """
        super().__init__(client, operation_name="ProductOperations", logger=logger)
    
    @handle_rest_errors
    def get_product(self, product_id: str, 
                   include_attributes: bool = True,
                   include_values: bool = True) -> ProductResponse:
        """Retrieve a single product by ID.
        
        Args:
            product_id: The product ID to retrieve
            include_attributes: Whether to include product attributes
            include_values: Whether to include product values
            
        Returns:
            ProductResponse with product data
            
        Raises:
            NotFoundError: If product not found
            RestApiError: For other API errors
        """
        self._validate_required_params(
            {"product_id": product_id},
            ["product_id"]
        )
        
        params = {
            "productId": product_id,
            "includeAttributes": include_attributes,
            "includeValues": include_values,
        }
        self._log_operation("getProduct", params)
        
        try:
            response = self.client.getProduct(**params)
        except Exception as e:
            if "404" in str(e) or "not found" in str(e).lower():
                raise exc.NotFoundError(product_id, "Product")
            raise
        
        # Convert response to ProductResponse if needed
        if isinstance(response, dict):
            return ProductResponse(**response)
        return response
    
    @handle_rest_errors
    def search_products(self, query: str = "*",
                       user_type_id: Optional[str] = None,
                       modified_since: Optional[str] = None,
                       limit: int = 20,
                       offset: int = 0,
                       include_attributes: bool = True,
                       include_values: bool = True) -> ProductListResponse:
        """Search for products with optional filters.
        
        Args:
            query: Free-text search query (default: "*" for all)
            user_type_id: Filter by user type ID
            modified_since: ISO 8601 timestamp - only products modified after this date
            limit: Maximum results to return (1-1000, default: 20)
            offset: Result offset for pagination (default: 0)
            include_attributes: Whether to include attributes (default: True)
            include_values: Whether to include values (default: True)
            
        Returns:
            ProductListResponse with paginated results
            
        Raises:
            ValidationError: If parameters are invalid
            RestApiError: For API errors
        """
        # Validate pagination parameters
        pagination_params = self._build_pagination_params(limit, offset)
        
        params = {
            "q": query,
            "limit": pagination_params["limit"],
            "offset": pagination_params["offset"],
            "includeAttributes": include_attributes,
            "includeValues": include_values,
        }
        
        # Add optional filters
        if user_type_id:
            params["userTypeId"] = user_type_id
        if modified_since:
            params["modifiedSince"] = modified_since
        
        # Clean parameters
        params = self._clean_params(params)
        self._log_operation("searchProducts", params)
        
        # Call API
        response = self.client.searchProducts(**params)
        
        # Handle response and build list response
        if isinstance(response, dict):
            items = response.get("items", [])
            total = response.get("total")
        else:
            items = getattr(response, "items", [])
            total = getattr(response, "total", None)
        
        # Convert items to ProductResponse objects
        product_items = [
            ProductResponse(**item) if isinstance(item, dict) else item
            for item in items
        ]
        
        page_info = self._build_page_info(
            limit=pagination_params["limit"],
            offset=pagination_params["offset"],
            total=total
        )
        
        return ProductListResponse(
            items=product_items,
            total=total,
            limit=pagination_params["limit"],
            offset=pagination_params["offset"],
            has_more=page_info.has_more
        )
    
    @handle_rest_errors
    def create_product(self, product_data: ProductCreateRequest) -> ProductResponse:
        """Create a new product.
        
        Args:
            product_data: ProductCreateRequest with product data
            
        Returns:
            ProductResponse with created product data
            
        Raises:
            ValidationError: If product data is invalid
            ConflictError: If product ID already exists
            RestApiError: For other API errors
        """
        # Validate that ID is present
        self._validate_required_params(
            {"id": product_data.id},
            ["id"]
        )
        
        # Convert request to dict for API call
        product_dict = product_data.model_dump(exclude_none=True)
        self._log_operation("createProduct", {"productId": product_data.id})
        
        try:
            response = self.client.createProduct(body=product_dict)
        except Exception as e:
            if "409" in str(e) or "conflict" in str(e).lower():
                raise exc.ConflictError(409, f"Product {product_data.id} already exists")
            if "400" in str(e):
                raise exc.ValidationError(str(e))
            raise
        
        # Convert response to ProductResponse
        if isinstance(response, dict):
            return ProductResponse(**response)
        return response
    
    @handle_rest_errors
    def update_product(self, product_id: str,
                      updates: ProductUpdateRequest) -> ProductResponse:
        """Update an existing product.
        
        Args:
            product_id: The product ID to update
            updates: ProductUpdateRequest with updates
            
        Returns:
            ProductResponse with updated product data
            
        Raises:
            NotFoundError: If product not found
            ValidationError: If updates are invalid
            RestApiError: For other API errors
        """
        # Validate product ID
        self._validate_required_params(
            {"product_id": product_id},
            ["product_id"]
        )
        
        # Convert updates to dict
        updates_dict = updates.model_dump(exclude_none=True)
        self._log_operation("updateProduct", {"productId": product_id})
        
        try:
            response = self.client.updateProduct(
                productId=product_id,
                body=updates_dict
            )
        except Exception as e:
            if "404" in str(e):
                raise exc.NotFoundError(product_id, "Product")
            if "400" in str(e):
                raise exc.ValidationError(str(e))
            raise
        
        # Convert response to ProductResponse
        if isinstance(response, dict):
            return ProductResponse(**response)
        return response
    
    @handle_rest_errors
    def delete_product(self, product_id: str) -> bool:
        """Delete a product.
        
        Args:
            product_id: The product ID to delete
            
        Returns:
            True if deletion was successful
            
        Raises:
            NotFoundError: If product not found
            RestApiError: For other API errors
        """
        self._validate_required_params(
            {"product_id": product_id},
            ["product_id"]
        )
        
        self._log_operation("deleteProduct", {"productId": product_id})
        
        try:
            self.client.deleteProduct(productId=product_id)
            return True
        except Exception as e:
            if "404" in str(e):
                raise exc.NotFoundError(product_id, "Product")
            raise
    
    @handle_rest_errors
    def get_product_attributes(self, product_id: str) -> List[Dict[str, Any]]:
        """Get all attributes for a product.
        
        Args:
            product_id: The product ID
            
        Returns:
            List of attribute dictionaries
            
        Raises:
            NotFoundError: If product not found
            RestApiError: For API errors
        """
        self._validate_required_params(
            {"product_id": product_id},
            ["product_id"]
        )
        
        self._log_operation("getProductAttributes", {"productId": product_id})
        
        try:
            response = self.client.getProductAttributes(productId=product_id)
        except Exception as e:
            if "404" in str(e):
                raise exc.NotFoundError(product_id, "Product")
            raise
        
        # Handle response
        if isinstance(response, dict):
            return response.get("items", [])
        elif isinstance(response, list):
            return response
        else:
            return getattr(response, "items", [])
    
    @handle_rest_errors
    def get_product_values(self, product_id: str) -> List[Dict[str, Any]]:
        """Get all values (variants/SKUs) for a product.
        
        Args:
            product_id: The product ID
            
        Returns:
            List of value/variant dictionaries
            
        Raises:
            NotFoundError: If product not found
            RestApiError: For API errors
        """
        self._validate_required_params(
            {"product_id": product_id},
            ["product_id"]
        )
        
        self._log_operation("getProductValues", {"productId": product_id})
        
        try:
            response = self.client.getProductValues(productId=product_id)
        except Exception as e:
            if "404" in str(e):
                raise exc.NotFoundError(product_id, "Product")
            raise
        
        # Handle response
        if isinstance(response, dict):
            return response.get("items", [])
        elif isinstance(response, list):
            return response
        else:
            return getattr(response, "items", [])
    
    def list_products(self, limit: int = 20, offset: int = 0,
                     include_attributes: bool = True,
                     include_values: bool = True) -> ProductListResponse:
        """List all products (convenience method).
        
        Args:
            limit: Max results per page
            offset: Result offset
            include_attributes: Whether to include attributes
            include_values: Whether to include values
            
        Returns:
            ProductListResponse with paginated results
        """
        return self.search_products(
            query="*",
            limit=limit,
            offset=offset,
            include_attributes=include_attributes,
            include_values=include_values
        )
    
    def search_by_type(self, user_type_id: str,
                      limit: int = 20,
                      offset: int = 0) -> ProductListResponse:
        """Search products by user type (convenience method).
        
        Args:
            user_type_id: User type to filter by
            limit: Max results per page
            offset: Result offset
            
        Returns:
            ProductListResponse with paginated results
        """
        return self.search_products(
            query="*",
            user_type_id=user_type_id,
            limit=limit,
            offset=offset
        )
    
    def search_modified_since(self, modified_since: str,
                             limit: int = 20,
                             offset: int = 0) -> ProductListResponse:
        """Search products modified after a specific timestamp (convenience method).
        
        Args:
            modified_since: ISO 8601 timestamp
            limit: Max results per page
            offset: Result offset
            
        Returns:
            ProductListResponse with paginated results
        """
        return self.search_products(
            query="*",
            modified_since=modified_since,
            limit=limit,
            offset=offset
        )
