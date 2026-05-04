"""Classification operations for STEP REST API v2."""

import logging
from typing import Optional, List, Dict, Any

from ..base import BaseOperation, handle_rest_errors
from ..exceptions import NotFoundError, ValidationError, RestApiError, ConflictError
from ..models.classification import (
    ClassificationResponse,
    ClassificationListResponse,
    ClassificationCreateRequest,
    ClassificationUpdateRequest,
)


class ClassificationOperations(BaseOperation):
    """Operations for STEP Classifications."""
    
    def __init__(self, client, logger: Optional[logging.Logger] = None,
                 context: Optional[str] = None, workspace: Optional[str] = None):
        """Initialize classification operations.
        
        Args:
            client: The REST API client
            logger: Optional logger instance
            context: STEP context ID for all API calls
            workspace: STEP workspace ID (defaults to "Main" server-side)
        """
        super().__init__(client, operation_name="ClassificationOperations", logger=logger,
                         context=context, workspace=workspace)
    
    @handle_rest_errors
    def get_classification(self, classification_id: str,
                          key_id: Optional[str] = None,
                          include_inherited_data: bool = False) -> ClassificationResponse:
        """Get a single classification by ID.
        
        Args:
            classification_id: The classification ID (or alternate key value if key_id is set)
            key_id: Alternate key ID to use for lookup (optional)
            include_inherited_data: Whether to include inherited attribute values (default: False)
            
        Returns:
            ClassificationResponse with classification data
            
        Raises:
            ValidationError: If classification_id is missing
            NotFoundError: If classification not found
            RestApiError: For other API errors
        """
        self._validate_required_params(
            {"classification_id": classification_id},
            ["classification_id"]
        )
        
        query_params: Dict[str, Any] = self._build_context_params()
        if key_id:
            query_params["keyId"] = key_id
        if include_inherited_data:
            query_params["includeInheritedData"] = include_inherited_data
        self._log_operation("getClassification", {"classification_id": classification_id})
        
        try:
            response = self.client.getClassification(id=classification_id, **query_params)
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(classification_id, "Classification")
            raise
        
        if isinstance(response, dict):
            return ClassificationResponse(**response)
        return response
    
    @handle_rest_errors
    def search_classifications(self, condition: dict) -> ClassificationListResponse:
        """Search classifications using a STEP condition query.
        
        Args:
            condition: A STEP condition object defining the search criteria.
                       Supported conditionTypes: 'and', 'or', 'id', 'name',
                       'textvalue', 'numericvalue', 'objecttype', 'simplebelow',
                       'lovvalue', 'hasreferenceto', 'hasdatacontainerobject'.
            
        Returns:
            ClassificationListResponse with matching classifications
            
        Raises:
            ValidationError: If condition is invalid
            RestApiError: For API errors
        """
        self._validate_required_params({"condition": condition}, ["condition"])
        body = {"condition": condition}
        self._log_operation("postClassificationsSearch", {"condition": condition})
        
        response = self.client.postClassificationsSearch(json=body, **self._build_context_params())
        
        if isinstance(response, dict):
            return ClassificationListResponse(**response)
        return response
    
    def list_classifications(self) -> ClassificationListResponse:
        """List all classifications (convenience method).
        
        Returns:
            ClassificationListResponse with all classifications
        """
        return self.search_classifications(
            condition={"conditionType": "name", "value": "*"}
        )
    
    @handle_rest_errors
    def create_classification(self, data: ClassificationCreateRequest) -> ClassificationResponse:
        """Create a new classification.
        
        Args:
            data: ClassificationCreateRequest with classification data
            
        Returns:
            ClassificationResponse with created classification
            
        Raises:
            ValidationError: If data invalid
            RestApiError: For API errors
        """
        self._validate_required_params(
            {"objectType": data.objectType, "parent": data.parent},
            ["objectType", "parent"]
        )
        create_data = data.model_dump(exclude_none=True)
        self._log_operation("postClassifications", {"objectType": data.objectType})
        
        try:
            response = self.client.postClassifications(json=create_data, **self._build_context_params())
        except Exception as e:
            if "409" in str(e):
                raise ConflictError(409, str(e))
            raise
        
        if isinstance(response, dict):
            return ClassificationResponse(**response)
        return response
    
    @handle_rest_errors
    def update_classification(self, classification_id: str,
                            updates: ClassificationUpdateRequest,
                            key_id: Optional[str] = None) -> ClassificationResponse:
        """Partially update an existing classification (PATCH).
        
        Args:
            classification_id: The classification ID (or alternate key value if key_id is set)
            updates: ClassificationUpdateRequest with fields to update
            key_id: Alternate key ID to use for lookup (optional)
            
        Returns:
            ClassificationResponse with updated classification
            
        Raises:
            ValidationError: If classification_id or data invalid
            NotFoundError: If classification not found
            RestApiError: For API errors
        """
        self._validate_required_params(
            {"classification_id": classification_id},
            ["classification_id"]
        )
        
        update_data = updates.model_dump(exclude_none=True)
        query_params = self._build_context_params()
        if key_id:
            query_params["keyId"] = key_id
        self._log_operation("patchClassification", {"classification_id": classification_id})
        
        try:
            response = self.client.patchClassification(
                id=classification_id,
                json=update_data,
                **query_params
            )
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(classification_id, "Classification")
            if "400" in str(e):
                raise ValidationError(f"Update failed: {str(e)}")
            raise
        
        if isinstance(response, dict):
            return ClassificationResponse(**response)
        return response

    @handle_rest_errors
    def replace_classification(self, classification_id: str,
                               data: ClassificationCreateRequest,
                               key_id: Optional[str] = None,
                               allow_overwrite: bool = False) -> ClassificationResponse:
        """Fully replace a classification (PUT). Creates it if it does not exist.
        
        Args:
            classification_id: The classification ID (or alternate key value if key_id is set)
            data: Complete classification data
            key_id: Alternate key ID to use for lookup (optional)
            allow_overwrite: Whether to allow overwriting an existing classification
            
        Returns:
            ClassificationResponse with replaced classification
        """
        self._validate_required_params(
            {"classification_id": classification_id},
            ["classification_id"]
        )
        
        create_data = data.model_dump(exclude_none=True)
        query_params: Dict[str, Any] = self._build_context_params()
        if key_id:
            query_params["keyId"] = key_id
        if allow_overwrite:
            query_params["allow-overwrite"] = allow_overwrite
        self._log_operation("putClassification", {"classification_id": classification_id})
        
        try:
            response = self.client.putClassification(
                id=classification_id,
                json=create_data,
                **query_params
            )
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(classification_id, "Classification")
            if "400" in str(e) or "409" in str(e):
                raise ValidationError(str(e))
            raise
        
        if isinstance(response, dict):
            return ClassificationResponse(**response)
        return response
    
    @handle_rest_errors
    def delete_classification(self, classification_id: str,
                              key_id: Optional[str] = None) -> bool:
        """Delete a classification.
        
        Args:
            classification_id: The classification ID (or alternate key value if key_id is set)
            key_id: Alternate key ID to use for lookup (optional)
            
        Returns:
            True if deletion was successful
            
        Raises:
            ValidationError: If classification_id missing
            NotFoundError: If classification not found
            RestApiError: For API errors
        """
        self._validate_required_params(
            {"classification_id": classification_id},
            ["classification_id"]
        )
        
        query_params = self._build_context_params()
        if key_id:
            query_params["keyId"] = key_id
        self._log_operation("deleteClassification", {"classification_id": classification_id})
        
        try:
            self.client.deleteClassification(id=classification_id, **query_params)
            return True
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(classification_id, "Classification")
            raise
    
    @handle_rest_errors
    def get_classification_children(self, classification_id: str,
                                    key_id: Optional[str] = None) -> List[str]:
        """Get direct children IDs of a classification (GET /classifications/{id}/children).
        
        Args:
            classification_id: The classification ID (or alternate key value if key_id is set)
            key_id: Alternate key ID to use for lookup (optional)
            
        Returns:
            List of child classification IDs
            
        Raises:
            ValidationError: If classification_id missing
            NotFoundError: If classification not found
            RestApiError: For API errors
        """
        self._validate_required_params(
            {"classification_id": classification_id},
            ["classification_id"]
        )
        
        query_params = self._build_context_params()
        if key_id:
            query_params["keyId"] = key_id
        self._log_operation("getClassificationChildren", {"classification_id": classification_id})
        
        try:
            response = self.client.getClassificationChildren(id=classification_id, **query_params)
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(classification_id, "Classification")
            raise
        
        if isinstance(response, list):
            return response
        return []
    def search_by_type(self, classification_type: str) -> ClassificationListResponse:
        """Search classifications by object type (convenience method).
        
        Args:
            classification_type: The object type ID to filter by
            
        Returns:
            ClassificationListResponse filtered by type
        """
        return self.search_classifications(
            condition={"conditionType": "objecttype", "objectType": classification_type}
        )
