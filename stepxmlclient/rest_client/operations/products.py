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
    
    def __init__(self, client: roa.Client, logger: Optional[logging.Logger] = None,
                 context: Optional[str] = None, workspace: Optional[str] = None):
        """Initialize ProductOperations.
        
        Args:
            client: The requests-openapi Client instance
            logger: Logger instance (optional)
            context: STEP context ID for all API calls
            workspace: STEP workspace ID (defaults to "Main" server-side)
        """
        super().__init__(client, operation_name="ProductOperations", logger=logger,
                         context=context, workspace=workspace)
    
    @handle_rest_errors
    def get_product(self, product_id: str,
                   key_id: Optional[str] = None,
                   include_inherited_data: bool = False) -> ProductResponse:
        """Retrieve a single product by ID.
        
        Args:
            product_id: The product ID (or alternate key value if key_id is set)
            key_id: Alternate key ID to use for lookup (optional)
            include_inherited_data: Whether to include inherited attribute values (default: False)
            
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
        
        params: Dict[str, Any] = {"id": product_id}
        if key_id:
            params["keyId"] = key_id
        if include_inherited_data:
            params["includeInheritedData"] = include_inherited_data
        params.update(self._build_context_params())
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
    def search_products(self, condition: dict) -> ProductListResponse:
        """Search for products using a STEP condition query.
        
        Args:
            condition: A STEP condition object defining the search criteria.
                       Supported conditionTypes: 'and', 'or', 'id', 'name',
                       'textvalue', 'numericvalue', 'objecttype', 'simplebelow',
                       'lovvalue', 'hasreferenceto', 'hasdatacontainerobject'.
                       Example: {"conditionType": "objecttype", "objectTypeId": "MyType"}
            
        Returns:
            ProductListResponse with matching products
            
        Raises:
            ValidationError: If condition is invalid
            RestApiError: For API errors
        """
        self._validate_required_params({"condition": condition}, ["condition"])
        body = {"condition": condition}
        self._log_operation("postProductsSearch", {"condition": condition})
        
        response = self.client.postProductsSearch(body=body, **self._build_context_params())
        
        if isinstance(response, dict):
            items = response.get("items", [])
            total = response.get("total")
        else:
            items = getattr(response, "items", [])
            total = getattr(response, "total", None)
        
        product_items = [
            ProductResponse(**item) if isinstance(item, dict) else item
            for item in items
        ]
        
        return ProductListResponse(
            items=product_items,
            total=total,
            limit=max(len(product_items), 1),
            offset=0,
            has_more=False
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
        self._log_operation("postProducts", {"productId": product_data.id})
        
        try:
            response = self.client.postProducts(body=product_dict, **self._build_context_params())
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
                      updates: ProductUpdateRequest,
                      key_id: Optional[str] = None) -> ProductResponse:
        """Partially update an existing product (PATCH).
        
        Args:
            product_id: The product ID (or alternate key value if key_id is set)
            updates: ProductUpdateRequest with fields to update
            key_id: Alternate key ID to use for lookup (optional)
            
        Returns:
            ProductResponse with updated product data
            
        Raises:
            NotFoundError: If product not found
            ValidationError: If updates are invalid
            RestApiError: For other API errors
        """
        self._validate_required_params(
            {"product_id": product_id},
            ["product_id"]
        )
        
        updates_dict = updates.model_dump(exclude_none=True)
        params = {"id": product_id}
        if key_id:
            params["keyId"] = key_id
        params.update(self._build_context_params())
        self._log_operation("patchProduct", {"id": product_id})
        
        try:
            response = self.client.patchProduct(
                body=updates_dict,
                **params
            )
        except Exception as e:
            if "404" in str(e):
                raise exc.NotFoundError(product_id, "Product")
            if "400" in str(e):
                raise exc.ValidationError(str(e))
            raise
        
        if isinstance(response, dict):
            return ProductResponse(**response)
        return response

    @handle_rest_errors
    def replace_product(self, product_id: str,
                        product_data: ProductCreateRequest,
                        key_id: Optional[str] = None,
                        allow_overwrite: bool = False) -> ProductResponse:
        """Fully replace a product (PUT). Creates it if it does not exist.
        
        Args:
            product_id: The product ID (or alternate key value if key_id is set)
            product_data: Complete product data to replace with
            key_id: Alternate key ID to use for lookup (optional)
            allow_overwrite: Whether to allow overwriting an existing product
            
        Returns:
            ProductResponse with replaced product data
            
        Raises:
            NotFoundError: If product not found and allow_overwrite is False
            ValidationError: If data is invalid
            RestApiError: For other API errors
        """
        self._validate_required_params(
            {"product_id": product_id},
            ["product_id"]
        )
        
        product_dict = product_data.model_dump(exclude_none=True)
        params: Dict[str, Any] = {"id": product_id}
        if key_id:
            params["keyId"] = key_id
        if allow_overwrite:
            params["allow-overwrite"] = allow_overwrite
        params.update(self._build_context_params())
        self._log_operation("putProduct", {"id": product_id})
        
        try:
            response = self.client.putProduct(
                body=product_dict,
                **params
            )
        except Exception as e:
            if "404" in str(e):
                raise exc.NotFoundError(product_id, "Product")
            if "400" in str(e) or "409" in str(e):
                raise exc.ValidationError(str(e))
            raise
        
        if isinstance(response, dict):
            return ProductResponse(**response)
        return response
    
    @handle_rest_errors
    def delete_product(self, product_id: str,
                       key_id: Optional[str] = None) -> bool:
        """Delete a product.
        
        Args:
            product_id: The product ID (or alternate key value if key_id is set)
            key_id: Alternate key ID to use for lookup (optional)
            
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
        
        params = {"id": product_id}
        if key_id:
            params["keyId"] = key_id
        params.update(self._build_context_params())
        self._log_operation("deleteProduct", {"id": product_id})
        
        try:
            self.client.deleteProduct(**params)
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
        
        # NOTE: There is no bulk 'get all attributes' operation in the STEP REST API spec.
        # Use get_product() and inspect the returned values, or use get_product_value()
        # for a specific attribute (getProductValue: GET /products/{id}/values/{attributeId}).
        self._log_operation("getProductValue", {"id": product_id})
        
        try:
            response = self.client.getProductValue(id=product_id, **self._build_context_params())
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
        
        # NOTE: There is no bulk 'get all values' operation in the STEP REST API spec.
        # Use get_product() for the full product object including values.
        self._log_operation("getProductValue", {"id": product_id})
        
        try:
            response = self.client.getProductValue(id=product_id, **self._build_context_params())
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
    
    def search_by_type(self, user_type_id: str) -> ProductListResponse:
        """Search products by object type (convenience method).
        
        Args:
            user_type_id: Object type ID to filter by
            
        Returns:
            ProductListResponse with matching products
        """
        return self.search_products(
            condition={"conditionType": "objecttype", "objectTypeId": user_type_id}
        )
    
    def search_by_id(self, product_id: str) -> ProductListResponse:
        """Search products by ID condition (convenience method).
        
        Args:
            product_id: Product ID or pattern to search for
            
        Returns:
            ProductListResponse with matching products
        """
        return self.search_products(
            condition={"conditionType": "id", "id": product_id}
        )
