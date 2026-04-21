"""Classification operations for STEP REST API v2."""

import logging
from typing import Optional, List, Dict, Any

from ..base import BaseOperation, handle_rest_errors
from ..exceptions import NotFoundError, ValidationError, RestApiError
from ..models.classification import (
    ClassificationResponse,
    ClassificationListResponse,
    ClassificationHierarchyResponse,
    ClassificationSearchRequest,
    ClassificationCreateRequest,
    ClassificationUpdateRequest,
    ClassificationValueResponse,
    ClassificationValue,
)
from ..models.common import PagedResponse


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
                          include_values: bool = False) -> ClassificationResponse:
        """Get a single classification by ID.
        
        Args:
            classification_id: The classification ID
            include_values: Whether to include classification values
            
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
        
        self._log_operation("getClassification", {
            "classificationId": classification_id,
            "includeValues": include_values
        })
        
        try:
            response = self.client.getClassification(
                classificationId=classification_id,
                includeValues=include_values,
                **self._build_context_params()
            )
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(classification_id, "Classification")
            raise
        
        if isinstance(response, dict):
            return ClassificationResponse(**response)
        return response
    
    @handle_rest_errors
    def search_classifications(self,
                              query: str = "*",
                              limit: int = 20,
                              offset: int = 0,
                              type_filter: Optional[str] = None,
                              include_values: bool = False) -> ClassificationListResponse:
        """Search classifications with optional filters.
        
        Args:
            query: Search query string (default: "*" for all)
            limit: Result limit (1-500, default: 20)
            offset: Result offset (default: 0)
            type_filter: Optional filter by classification type
            include_values: Whether to include values for each classification
            
        Returns:
            ClassificationListResponse with paginated results
            
        Raises:
            ValidationError: If parameters invalid
            RestApiError: For API errors
        """
        pagination_params = self._build_pagination_params(limit, offset)
        
        self._log_operation("searchClassifications", {
            "q": query,
            "limit": pagination_params["limit"],
            "offset": pagination_params["offset"],
            "typeFilter": type_filter,
            "includeValues": include_values
        })
        
        params = self._clean_params({
            "q": query,
            "limit": pagination_params["limit"],
            "offset": pagination_params["offset"],
            "typeFilter": type_filter,
            "includeValues": include_values
        })
        params.update(self._build_context_params())
        
        response = self.client.searchClassifications(**params)
        
        if isinstance(response, dict):
            return ClassificationListResponse(**response)
        return response
    
    @handle_rest_errors
    def list_classifications(self, limit: int = 20, offset: int = 0) -> ClassificationListResponse:
        """Convenience method to list all classifications.
        
        Args:
            limit: Result limit
            offset: Result offset
            
        Returns:
            ClassificationListResponse with all classifications
        """
        return self.search_classifications(query="*", limit=limit, offset=offset)
    
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
        # Convert Pydantic model to dict if needed
        if hasattr(data, 'model_dump'):
            create_data = data.model_dump(exclude_none=True)
        else:
            create_data = dict(data) if not isinstance(data, dict) else data
        
        self._log_operation("createClassification", create_data)
        
        try:
            response = self.client.createClassification(body=create_data, **self._build_context_params())
        except Exception as e:
            if "400" in str(e) or "409" in str(e):
                raise ValidationError(f"Create failed: {str(e)}")
            raise
        
        if isinstance(response, dict):
            return ClassificationResponse(**response)
        return response
    
    @handle_rest_errors
    def update_classification(self, classification_id: str,
                            updates: ClassificationUpdateRequest) -> ClassificationResponse:
        """Update an existing classification.
        
        Args:
            classification_id: The classification ID to update
            updates: ClassificationUpdateRequest with updated data
            
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
        
        # Convert Pydantic model to dict if needed
        if hasattr(updates, 'model_dump'):
            update_data = updates.model_dump(exclude_none=True)
        else:
            update_data = dict(updates) if not isinstance(updates, dict) else updates
        
        self._log_operation("updateClassification", {
            "classificationId": classification_id,
            "updates": update_data
        })
        
        try:
            response = self.client.updateClassification(
                classificationId=classification_id,
                body=update_data,
                **self._build_context_params()
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
    def delete_classification(self, classification_id: str) -> bool:
        """Delete a classification.
        
        Args:
            classification_id: The classification ID to delete
            
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
        
        self._log_operation("deleteClassification", {"classificationId": classification_id})
        
        try:
            self.client.deleteClassification(classificationId=classification_id, **self._build_context_params())
            return True
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(classification_id, "Classification")
            raise
    
    @handle_rest_errors
    def get_classification_hierarchy(self, classification_id: str,
                                     root_id: Optional[str] = None) -> ClassificationHierarchyResponse:
        """Get hierarchical view of a classification.
        
        Args:
            classification_id: The classification ID
            root_id: Optional root node ID for subtree (None for full hierarchy)
            
        Returns:
            ClassificationHierarchyResponse with hierarchy structure
            
        Raises:
            ValidationError: If classification_id missing
            NotFoundError: If classification or root_id not found
            RestApiError: For API errors
        """
        self._validate_required_params(
            {"classification_id": classification_id},
            ["classification_id"]
        )
        
        self._log_operation("getClassificationHierarchy", {
            "classificationId": classification_id,
            "rootId": root_id
        })
        
        params = self._clean_params({
            "rootId": root_id
        })
        
        try:
            response = self.client.getClassificationHierarchy(
                classificationId=classification_id,
                **params,
                **self._build_context_params()
            )
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(classification_id, "Classification")
            raise
        
        if isinstance(response, dict):
            return ClassificationHierarchyResponse(**response)
        return response
    
    @handle_rest_errors
    def get_classification_values(self, classification_id: str) -> ClassificationValueResponse:
        """Get all values/items in a classification.
        
        Args:
            classification_id: The classification ID
            
        Returns:
            ClassificationValueResponse with classification values
            
        Raises:
            ValidationError: If classification_id missing
            NotFoundError: If classification not found
            RestApiError: For API errors
        """
        self._validate_required_params(
            {"classification_id": classification_id},
            ["classification_id"]
        )
        
        self._log_operation("getClassificationValues", {"classificationId": classification_id})
        
        try:
            response = self.client.getClassificationValues(classificationId=classification_id, **self._build_context_params())
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(classification_id, "Classification")
            raise
        
        if isinstance(response, dict):
            return ClassificationValueResponse(**response)
        return response
    
    @handle_rest_errors
    def search_by_type(self, classification_type: str,
                       limit: int = 20, offset: int = 0) -> ClassificationListResponse:
        """Convenience method to search classifications by type.
        
        Args:
            classification_type: The classification type to filter by
            limit: Result limit
            offset: Result offset
            
        Returns:
            ClassificationListResponse filtered by type
        """
        return self.search_classifications(
            query="*",
            limit=limit,
            offset=offset,
            type_filter=classification_type
        )
    
    @handle_rest_errors
    def search_modified_since(self, timestamp: str,
                             limit: int = 20, offset: int = 0) -> ClassificationListResponse:
        """Convenience method to search classifications modified since a timestamp.
        
        Args:
            timestamp: ISO 8601 timestamp (e.g., "2025-01-01T00:00:00Z")
            limit: Result limit
            offset: Result offset
            
        Returns:
            ClassificationListResponse of modified classifications
        """
        query = f"modifiedAt >= {timestamp}"
        return self.search_classifications(query=query, limit=limit, offset=offset)
