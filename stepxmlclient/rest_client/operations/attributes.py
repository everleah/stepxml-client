"""Attribute operations for STEP REST API v2."""

import logging
from typing import Optional, List, Dict, Any

from ..base import BaseOperation, handle_rest_errors
from ..exceptions import NotFoundError, ValidationError, RestApiError
from ..models.attribute import (
    AttributeResponse,
    AttributeListResponse,
    ListOfValueResponse,
    AttributeSearchRequest,
    AttributeCreateRequest,
    AttributeUpdateRequest,
    ListOfValueItem,
)


class AttributeOperations(BaseOperation):
    """Operations for STEP Attributes and List of Values."""
    
    def __init__(self, client, logger: Optional[logging.Logger] = None):
        """Initialize attribute operations.
        
        Args:
            client: The REST API client
            logger: Optional logger instance
        """
        super().__init__(client, operation_name="AttributeOperations", logger=logger)
    
    @handle_rest_errors
    def get_attribute(self, attribute_id: str) -> AttributeResponse:
        """Get a single attribute by ID.
        
        Args:
            attribute_id: The attribute ID
            
        Returns:
            AttributeResponse with attribute data
            
        Raises:
            ValidationError: If attribute_id is missing
            NotFoundError: If attribute not found
            RestApiError: For other API errors
        """
        self._validate_required_params(
            {"attribute_id": attribute_id},
            ["attribute_id"]
        )
        
        self._log_operation("getAttribute", {"attributeId": attribute_id})
        
        try:
            response = self.client.getAttribute(attributeId=attribute_id)
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(attribute_id, "Attribute")
            raise
        
        if isinstance(response, dict):
            return AttributeResponse(**response)
        return response
    
    @handle_rest_errors
    def search_attributes(self,
                         query: str = "*",
                         limit: int = 20,
                         offset: int = 0,
                         type_filter: Optional[str] = None) -> AttributeListResponse:
        """Search attributes with optional filters.
        
        Args:
            query: Search query string (default: "*" for all)
            limit: Result limit (1-500, default: 20)
            offset: Result offset (default: 0)
            type_filter: Optional filter by attribute type
            
        Returns:
            AttributeListResponse with paginated results
            
        Raises:
            ValidationError: If parameters invalid
            RestApiError: For API errors
        """
        pagination_params = self._build_pagination_params(limit, offset)
        
        self._log_operation("searchAttributes", {
            "q": query,
            "limit": pagination_params["limit"],
            "offset": pagination_params["offset"],
            "typeFilter": type_filter
        })
        
        params = self._clean_params({
            "q": query,
            "limit": pagination_params["limit"],
            "offset": pagination_params["offset"],
            "typeFilter": type_filter
        })
        
        response = self.client.searchAttributes(**params)
        
        if isinstance(response, dict):
            return AttributeListResponse(**response)
        return response
    
    @handle_rest_errors
    def list_attributes(self, limit: int = 20, offset: int = 0) -> AttributeListResponse:
        """Convenience method to list all attributes.
        
        Args:
            limit: Result limit
            offset: Result offset
            
        Returns:
            AttributeListResponse with all attributes
        """
        return self.search_attributes(query="*", limit=limit, offset=offset)
    
    @handle_rest_errors
    def create_attribute(self, data: AttributeCreateRequest) -> AttributeResponse:
        """Create a new attribute.
        
        Args:
            data: AttributeCreateRequest with attribute data
            
        Returns:
            AttributeResponse with created attribute
            
        Raises:
            ValidationError: If data invalid
            RestApiError: For API errors
        """
        # Convert Pydantic model to dict if needed
        if hasattr(data, 'model_dump'):
            create_data = data.model_dump(exclude_none=True)
        else:
            create_data = dict(data) if not isinstance(data, dict) else data
        
        self._log_operation("createAttribute", create_data)
        
        try:
            response = self.client.createAttribute(body=create_data)
        except Exception as e:
            if "400" in str(e) or "409" in str(e):
                raise ValidationError(f"Create failed: {str(e)}")
            raise
        
        if isinstance(response, dict):
            return AttributeResponse(**response)
        return response
    
    @handle_rest_errors
    def update_attribute(self, attribute_id: str,
                        updates: AttributeUpdateRequest) -> AttributeResponse:
        """Update an existing attribute.
        
        Args:
            attribute_id: The attribute ID to update
            updates: AttributeUpdateRequest with updated data
            
        Returns:
            AttributeResponse with updated attribute
            
        Raises:
            ValidationError: If attribute_id or data invalid
            NotFoundError: If attribute not found
            RestApiError: For API errors
        """
        self._validate_required_params(
            {"attribute_id": attribute_id},
            ["attribute_id"]
        )
        
        # Convert Pydantic model to dict if needed
        if hasattr(updates, 'model_dump'):
            update_data = updates.model_dump(exclude_none=True)
        else:
            update_data = dict(updates) if not isinstance(updates, dict) else updates
        
        self._log_operation("updateAttribute", {
            "attributeId": attribute_id,
            "updates": update_data
        })
        
        try:
            response = self.client.updateAttribute(
                attributeId=attribute_id,
                body=update_data
            )
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(attribute_id, "Attribute")
            if "400" in str(e):
                raise ValidationError(f"Update failed: {str(e)}")
            raise
        
        if isinstance(response, dict):
            return AttributeResponse(**response)
        return response
    
    @handle_rest_errors
    def delete_attribute(self, attribute_id: str) -> bool:
        """Delete an attribute.
        
        Args:
            attribute_id: The attribute ID to delete
            
        Returns:
            True if deletion was successful
            
        Raises:
            ValidationError: If attribute_id missing
            NotFoundError: If attribute not found
            RestApiError: For API errors
        """
        self._validate_required_params(
            {"attribute_id": attribute_id},
            ["attribute_id"]
        )
        
        self._log_operation("deleteAttribute", {"attributeId": attribute_id})
        
        try:
            self.client.deleteAttribute(attributeId=attribute_id)
            return True
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(attribute_id, "Attribute")
            raise
    
    @handle_rest_errors
    def get_list_of_values(self, lov_id: str) -> ListOfValueResponse:
        """Get a List of Values by ID.
        
        Args:
            lov_id: The LOV ID
            
        Returns:
            ListOfValueResponse with LOV items
            
        Raises:
            ValidationError: If lov_id is missing
            NotFoundError: If LOV not found
            RestApiError: For other API errors
        """
        self._validate_required_params(
            {"lov_id": lov_id},
            ["lov_id"]
        )
        
        self._log_operation("getListOfValues", {"lovId": lov_id})
        
        try:
            response = self.client.getListOfValues(lovId=lov_id)
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(lov_id, "ListOfValues")
            raise
        
        if isinstance(response, dict):
            return ListOfValueResponse(**response)
        return response
    
    @handle_rest_errors
    def search_list_of_values(self,
                             query: str = "*",
                             limit: int = 20,
                             offset: int = 0) -> Dict[str, Any]:
        """Search List of Values with optional filters.
        
        Args:
            query: Search query string (default: "*" for all)
            limit: Result limit (1-500, default: 20)
            offset: Result offset (default: 0)
            
        Returns:
            Dictionary with list of LOVs
            
        Raises:
            RestApiError: For API errors
        """
        pagination_params = self._build_pagination_params(limit, offset)
        
        self._log_operation("searchListOfValues", {
            "q": query,
            "limit": pagination_params["limit"],
            "offset": pagination_params["offset"]
        })
        
        params = self._clean_params({
            "q": query,
            "limit": pagination_params["limit"],
            "offset": pagination_params["offset"]
        })
        
        response = self.client.searchListOfValues(**params)
        return response if isinstance(response, dict) else response
    
    @handle_rest_errors
    def search_by_type(self, attribute_type: str,
                      limit: int = 20, offset: int = 0) -> AttributeListResponse:
        """Convenience method to search attributes by type.
        
        Args:
            attribute_type: The attribute type to filter by
            limit: Result limit
            offset: Result offset
            
        Returns:
            AttributeListResponse filtered by type
        """
        return self.search_attributes(
            query="*",
            limit=limit,
            offset=offset,
            type_filter=attribute_type
        )
