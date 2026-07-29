"""Product operations for STEP REST API.

Provides CRUD and search operations for products.
"""

import logging
from typing import Any, Optional

import requests_openapi as roa

from .. import exceptions as exc
from ..base import BaseOperation, handle_rest_errors
from ..models.product import (
    ProductCreateRequest,
    ProductListResponse,
    ProductResponse,
    ProductUpdateRequest,
)


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
        
        query_params: dict[str, Any] = self._build_context_params()
        if key_id:
            query_params["keyId"] = key_id
        if include_inherited_data:
            query_params["includeInheritedData"] = include_inherited_data
        self._log_operation("getProduct", {"product_id": product_id})
        
        try:
            response = self.client.getProduct(id=product_id, **query_params)
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
                       Example: {"conditionType": "objecttype", "objectType": "MyType"}
            
        Returns:
            ProductListResponse with matching products
            
        Raises:
            ValidationError: If condition is invalid
            RestApiError: For API errors
        """
        self._validate_required_params({"condition": condition}, ["condition"])
        body = {"condition": condition}
        self._log_operation("createProductSearch", {"condition": condition})
        
        response = self.client.createProductSearch(json=body, **self._build_context_params())
        
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
        # POST /products requires objectType and parent. ID is auto-generated server-side.
        self._validate_required_params(
            {
                "objectType": product_data.objectType,
                "parent": product_data.parent,
            },
            ["objectType", "parent"]
        )
        
        # Convert request to dict for API call
        product_dict = product_data.model_dump(exclude_none=True)
        self._log_operation("createProduct", {"objectType": product_data.objectType, "parent": product_data.parent})
        
        try:
            response = self.client.createProduct(json=product_dict, **self._build_context_params())
        except Exception as e:
            if "409" in str(e) or "conflict" in str(e).lower():
                raise exc.ConflictError(409, "Product conflict while creating product")
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
        query_params = self._build_context_params()
        if key_id:
            query_params["keyId"] = key_id
        self._log_operation("updateProduct", {"product_id": product_id})
        
        try:
            response = self.client.updateProduct(
                id=product_id,
                json=updates_dict,
                **query_params
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
        query_params: dict[str, Any] = self._build_context_params()
        if key_id:
            query_params["keyId"] = key_id
        if allow_overwrite:
            query_params["allow-overwrite"] = allow_overwrite
        self._log_operation("createOrReplaceProduct", {"product_id": product_id})
        
        try:
            response = self.client.createOrReplaceProduct(
                id=product_id,
                json=product_dict,
                **query_params
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
        
        query_params = self._build_context_params()
        if key_id:
            query_params["keyId"] = key_id
        self._log_operation("deleteProduct", {"product_id": product_id})
        
        try:
            self.client.deleteProduct(id=product_id, **query_params)
            return True
        except Exception as e:
            if "404" in str(e):
                raise exc.NotFoundError(product_id, "Product")
            raise
    
    def search_by_type(self, user_type_id: str) -> ProductListResponse:
        """Search products by object type (convenience method).
        
        Args:
            user_type_id: Object type ID to filter by
            
        Returns:
            ProductListResponse with matching products
        """
        return self.search_products(
            condition={"conditionType": "objecttype", "objectType": user_type_id}
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

    # ------------------------------------------------------------------
    # Approval & lifecycle (v1.4.0)
    # ------------------------------------------------------------------

    @handle_rest_errors
    def get_product_approval_status(self, product_id: str,
                                    key_id: Optional[str] = None) -> dict[str, Any]:
        self._validate_required_params({"product_id": product_id}, ["product_id"])
        qp = self._build_context_params()
        if key_id: qp["keyId"] = key_id
        self._log_operation("getProductApprovalStatus", {"id": product_id})
        try:
            r = self.client.getProductApprovalStatus(id=product_id, **qp)
        except Exception as e:
            if "404" in str(e): raise exc.NotFoundError(product_id, "Product")
            raise
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def approve_product(self, product_id: str,
                        key_id: Optional[str] = None) -> dict[str, Any]:
        self._validate_required_params({"product_id": product_id}, ["product_id"])
        qp = self._build_context_params()
        if key_id: qp["keyId"] = key_id
        self._log_operation("approveProduct", {"id": product_id})
        try:
            r = self.client.approveProduct(id=product_id, **qp)
        except Exception as e:
            if "404" in str(e): raise exc.NotFoundError(product_id, "Product")
            raise
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def approve_product_deletion(self, product_id: str,
                                 key_id: Optional[str] = None) -> dict[str, Any]:
        self._validate_required_params({"product_id": product_id}, ["product_id"])
        qp = self._build_context_params()
        if key_id: qp["keyId"] = key_id
        self._log_operation("approveProductDeletion", {"id": product_id})
        try:
            r = self.client.approveProductDeletion(id=product_id, **qp)
        except Exception as e:
            if "404" in str(e): raise exc.NotFoundError(product_id, "Product")
            raise
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def purge_product(self, product_id: str,
                      key_id: Optional[str] = None) -> dict[str, Any]:
        self._validate_required_params({"product_id": product_id}, ["product_id"])
        qp = self._build_context_params()
        if key_id: qp["keyId"] = key_id
        self._log_operation("purgeProduct", {"id": product_id})
        try:
            r = self.client.purgeProduct(id=product_id, **qp)
        except Exception as e:
            if "404" in str(e): raise exc.NotFoundError(product_id, "Product")
            raise
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def get_product_children(self, product_id: str,
                             key_id: Optional[str] = None) -> list[str]:
        self._validate_required_params({"product_id": product_id}, ["product_id"])
        qp = self._build_context_params()
        if key_id: qp["keyId"] = key_id
        self._log_operation("getProductChildren", {"id": product_id})
        try:
            r = self.client.getProductChildren(id=product_id, **qp)
        except Exception as e:
            if "404" in str(e): raise exc.NotFoundError(product_id, "Product")
            raise
        return r if isinstance(r, list) else []

    @handle_rest_errors
    def get_product_data_containers(self, product_id: str,
                                    key_id: Optional[str] = None) -> dict[str, Any]:
        self._validate_required_params({"product_id": product_id}, ["product_id"])
        qp = self._build_context_params()
        if key_id: qp["keyId"] = key_id
        self._log_operation("getProductDataContainers", {"id": product_id})
        try:
            r = self.client.getProductDataContainers(id=product_id, **qp)
        except Exception as e:
            if "404" in str(e): raise exc.NotFoundError(product_id, "Product")
            raise
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def get_product_incoming_references(self, product_id: str,
                                        key_id: Optional[str] = None) -> dict[str, Any]:
        self._validate_required_params({"product_id": product_id}, ["product_id"])
        qp = self._build_context_params()
        if key_id: qp["keyId"] = key_id
        self._log_operation("getProductIncomingReferences", {"id": product_id})
        try:
            r = self.client.getProductIncomingReferences(id=product_id, **qp)
        except Exception as e:
            if "404" in str(e): raise exc.NotFoundError(product_id, "Product")
            raise
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def get_product_value(self, product_id: str, attribute_id: str,
                          key_id: Optional[str] = None) -> dict[str, Any]:
        self._validate_required_params(
            {"product_id": product_id, "attribute_id": attribute_id},
            ["product_id", "attribute_id"])
        qp = self._build_context_params()
        if key_id: qp["keyId"] = key_id
        self._log_operation("getProductValueByAttributeId",
                           {"id": product_id, "attributeId": attribute_id})
        try:
            r = self.client.getProductValueByAttributeId(
                id=product_id, attributeId=attribute_id, **qp)
        except Exception as e:
            if "404" in str(e): raise exc.NotFoundError(product_id, "Product")
            raise
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def replace_product_value(self, product_id: str, attribute_id: str,
                              value: dict[str, Any],
                              key_id: Optional[str] = None) -> dict[str, Any]:
        self._validate_required_params(
            {"product_id": product_id, "attribute_id": attribute_id},
            ["product_id", "attribute_id"])
        qp = self._build_context_params()
        if key_id: qp["keyId"] = key_id
        self._log_operation("replaceProductValueByAttributeId",
                           {"id": product_id, "attributeId": attribute_id})
        try:
            r = self.client.replaceProductValueByAttributeId(
                id=product_id, attributeId=attribute_id, json=value, **qp)
        except Exception as e:
            if "404" in str(e): raise exc.NotFoundError(product_id, "Product")
            if "400" in str(e): raise exc.ValidationError(str(e))
            raise
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def delete_product_value(self, product_id: str, attribute_id: str,
                             key_id: Optional[str] = None) -> bool:
        self._validate_required_params(
            {"product_id": product_id, "attribute_id": attribute_id},
            ["product_id", "attribute_id"])
        qp = self._build_context_params()
        if key_id: qp["keyId"] = key_id
        self._log_operation("deleteProductValueByAttributeId",
                           {"id": product_id, "attributeId": attribute_id})
        try:
            self.client.deleteProductValueByAttributeId(
                id=product_id, attributeId=attribute_id, **qp)
            return True
        except Exception as e:
            if "404" in str(e): raise exc.NotFoundError(product_id, "Product")
            raise

