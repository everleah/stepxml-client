"""Attribute operations for STEP REST API v2."""

import logging
from typing import Any, Optional

from ..base import BaseOperation, handle_rest_errors
from ..exceptions import ConflictError, NotFoundError, ValidationError
from ..models.attribute import (
    AttributeCreateRequest,
    AttributeListResponse,
    AttributeResponse,
    AttributeUpdateRequest,
    ListOfValueResponse,
)


class AttributeOperations(BaseOperation):
    """Operations for STEP Attributes and List of Values."""
    
    def __init__(self, client, logger: Optional[logging.Logger] = None,
                 context: Optional[str] = None, workspace: Optional[str] = None):
        """Initialize attribute operations.
        
        Args:
            client: The REST API client
            logger: Optional logger instance
            context: STEP context ID for all API calls
            workspace: STEP workspace ID (defaults to "Main" server-side)
        """
        super().__init__(client, operation_name="AttributeOperations", logger=logger,
                         context=context, workspace=workspace)
    
    @handle_rest_errors
    def get_attribute(self, attribute_id: str) -> AttributeResponse:
        """Get a single attribute by ID (GET /attributes/{id}).
        
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
        
        self._log_operation("getAttribute", {"id": attribute_id})
        
        try:
            response = self.client.getAttribute(id=attribute_id, **self._build_context_params())
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(attribute_id, "Attribute")
            raise
        
        if isinstance(response, dict):
            return AttributeResponse(**response)
        return response
    
    @handle_rest_errors
    def search_attributes(self, condition: dict) -> AttributeListResponse:
        """Search attributes using a STEP condition query (POST /attributes/search).
        
        NOTE: The STEP REST API spec has a postAttributesSearch operation.
        
        Args:
            condition: A STEP condition object defining the search criteria.
            
        Returns:
            AttributeListResponse with matching attributes
        """
        self._validate_required_params({"condition": condition}, ["condition"])
        body = {"condition": condition}
        self._log_operation("postAttributesSearch", {"condition": condition})
        
        response = self.client.postAttributesSearch(json=body, **self._build_context_params())
        
        if isinstance(response, dict):
            return AttributeListResponse(**response)
        return response
    
    def list_attributes(self) -> AttributeListResponse:
        """List all attributes (convenience method using objecttype condition).
        
        Returns:
            AttributeListResponse with all attributes
        """
        return self.search_attributes(
            condition={"conditionType": "objecttype", "objectTypeId": "*"}
        )
    
    @handle_rest_errors
    def create_attribute(self, data: AttributeCreateRequest) -> AttributeResponse:
        """Create a new attribute (POST /attributes).
        
        NOTE: The STEP REST API spec has postAttributes operation.
        
        Args:
            data: AttributeCreateRequest with attribute data
            
        Returns:
            AttributeResponse with created attribute
        """
        if hasattr(data, 'model_dump'):
            create_data = data.model_dump(exclude_none=True)
        else:
            create_data = dict(data) if not isinstance(data, dict) else data
        
        self._log_operation("postAttributes", create_data)
        
        try:
            response = self.client.postAttributes(json=create_data, **self._build_context_params())
        except Exception as e:
            if "409" in str(e):
                raise ConflictError(409, str(e))
            raise
        
        if isinstance(response, dict):
            return AttributeResponse(**response)
        return response
    
    @handle_rest_errors
    def update_attribute(self, attribute_id: str,
                        updates: AttributeUpdateRequest) -> AttributeResponse:
        """Partially update an existing attribute (PATCH /attributes/{id}).
        
        Args:
            attribute_id: The attribute ID
            updates: AttributeUpdateRequest with fields to update
            
        Returns:
            AttributeResponse with updated attribute
        """
        self._validate_required_params(
            {"attribute_id": attribute_id},
            ["attribute_id"]
        )
        
        if hasattr(updates, 'model_dump'):
            update_data = updates.model_dump(exclude_none=True)
        else:
            update_data = dict(updates) if not isinstance(updates, dict) else updates
        
        self._log_operation("patchAttribute", {"id": attribute_id})
        
        try:
            response = self.client.patchAttribute(
                id=attribute_id,
                json=update_data,
                **self._build_context_params()
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
        """Delete an attribute (DELETE /attributes/{id}).
        
        Args:
            attribute_id: The attribute ID
            
        Returns:
            True if deletion was successful
        """
        self._validate_required_params(
            {"attribute_id": attribute_id},
            ["attribute_id"]
        )
        
        self._log_operation("deleteAttribute", {"id": attribute_id})
        
        try:
            self.client.deleteAttribute(id=attribute_id, **self._build_context_params())
            return True
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(attribute_id, "Attribute")
            raise
    
    @handle_rest_errors
    def get_list_of_values(self, lov_id: str) -> ListOfValueResponse:
        """Get a List of Values by ID (GET /listofvalues/{id}).
        
        Args:
            lov_id: The LOV ID
            
        Returns:
            ListOfValueResponse with LOV data
            
        Raises:
            ValidationError: If lov_id is missing
            NotFoundError: If LOV not found
            RestApiError: For other API errors
        """
        self._validate_required_params(
            {"lov_id": lov_id},
            ["lov_id"]
        )
        
        self._log_operation("getListOfValue", {"id": lov_id})
        
        try:
            response = self.client.getListOfValue(id=lov_id, **self._build_context_params())
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(lov_id, "ListOfValues")
            raise
        
        if isinstance(response, dict):
            return ListOfValueResponse(**response)
        return response
    
    @handle_rest_errors
    def search_list_of_values(self, condition: dict) -> dict[str, Any]:
        """Search List of Values using a STEP condition query (POST /listofvalues/search).
        
        Args:
            condition: A STEP condition object defining the search criteria.
            
        Returns:
            Dictionary with matching LOVs
        """
        self._validate_required_params({"condition": condition}, ["condition"])
        body = {"condition": condition}
        self._log_operation("postListOfValuesSearch", {"condition": condition})
        
        response = self.client.postListOfValuesSearch(json=body, **self._build_context_params())
        return response if isinstance(response, dict) else response
    
    def search_by_type(self, attribute_type: str) -> AttributeListResponse:
        """Search attributes by object type (convenience method).
        
        Args:
            attribute_type: The object type ID to filter by
            
        Returns:
            AttributeListResponse filtered by type
        """
        return self.search_attributes(
            condition={"conditionType": "objecttype", "objectTypeId": attribute_type}
        )
