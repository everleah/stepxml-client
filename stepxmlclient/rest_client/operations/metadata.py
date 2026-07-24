"""Metadata operations for STEP REST API v2."""

import logging
from typing import Optional

from ..base import BaseOperation, handle_rest_errors
from ..exceptions import RestApiError
from ..models.metadata import (
    SystemMetadataResponse,
    ContextListResponse,
    ContextResponse,
    QualifierListResponse,
    QualifierResponse,
    DimensionListResponse,
    DimensionResponse,
    UserTypeListResponse,
    UserTypeResponse,
    WorkspaceListResponse,
    WorkspaceResponse,
)


class MetadataOperations(BaseOperation):
    """Operations for STEP system metadata and configuration."""
    
    def __init__(self,  
                 client, 
                 logger: Optional[logging.Logger] = None, 
                 context: Optional[str] = None, 
                 workspace: Optional[str] = None):
        """Initialize metadata operations.
        
        Args:
            client: The REST API client
            logger: Optional logger instance
        """
        super().__init__(client, 
                         operation_name="MetadataOperations", 
                         logger=logger, context=context, workspace=workspace)
    
    @handle_rest_errors
    def get_system_info(self) -> SystemMetadataResponse:
        """Get system information and capabilities.
        
        Returns:
            SystemMetadataResponse with system metadata
            
        Raises:
            RestApiError: For API errors
        """
        self._log_operation("getSystemInfo", {})
        
        response = self.client.getSystemInfo()
        
        if isinstance(response, dict):
            return SystemMetadataResponse(**response)
        return response
    
    @handle_rest_errors
    def list_contexts(self, limit: int = 100, offset: int = 0) -> ContextListResponse:
        """List all available contexts.
        
        Args:
            limit: Result limit
            offset: Result offset
            
        Returns:
            ContextListResponse with available contexts
            
        Raises:
            RestApiError: For API errors
        """
        pagination_params = self._build_pagination_params(limit, offset)
        
        self._log_operation("listContexts", {
            "limit": pagination_params["limit"],
            "offset": pagination_params["offset"]
        })
        
        params = self._clean_params({
            "limit": pagination_params["limit"],
            "offset": pagination_params["offset"]
        })
        
        response = self.client.listContexts(**params)
        
        if isinstance(response, dict):
            return ContextListResponse(**response)
        return response
    
    @handle_rest_errors
    def get_context(self, context_id: str) -> ContextResponse:
        """Get a specific context by ID.
        
        Args:
            context_id: The context ID
            
        Returns:
            ContextResponse with context details
            
        Raises:
            RestApiError: For API errors
        """
        self._log_operation("getContext", {"contextId": context_id})
        
        response = self.client.getContext(contextId=context_id)
        
        if isinstance(response, dict):
            return ContextResponse(**response)
        return response
    
    @handle_rest_errors
    def list_qualifiers(self, limit: int = 100, offset: int = 0) -> QualifierListResponse:
        """List all available qualifiers.
        
        Args:
            limit: Result limit
            offset: Result offset
            
        Returns:
            QualifierListResponse with available qualifiers
            
        Raises:
            RestApiError: For API errors
        """
        pagination_params = self._build_pagination_params(limit, offset)
        
        self._log_operation("listQualifiers", {
            "limit": pagination_params["limit"],
            "offset": pagination_params["offset"]
        })
        
        params = self._clean_params({
            "limit": pagination_params["limit"],
            "offset": pagination_params["offset"]
        })
        
        response = self.client.listQualifiers(**params)
        
        if isinstance(response, dict):
            return QualifierListResponse(**response)
        return response
    
    @handle_rest_errors
    def get_qualifier(self, qualifier_id: str) -> QualifierResponse:
        """Get a specific qualifier by ID.
        
        Args:
            qualifier_id: The qualifier ID
            
        Returns:
            QualifierResponse with qualifier details
            
        Raises:
            RestApiError: For API errors
        """
        self._log_operation("getQualifier", {"qualifierId": qualifier_id})
        
        response = self.client.getQualifier(qualifierId=qualifier_id)
        
        if isinstance(response, dict):
            return QualifierResponse(**response)
        return response
    
    @handle_rest_errors
    def list_dimensions(self, limit: int = 100, offset: int = 0) -> DimensionListResponse:
        """List all available dimensions.
        
        Args:
            limit: Result limit
            offset: Result offset
            
        Returns:
            DimensionListResponse with available dimensions
            
        Raises:
            RestApiError: For API errors
        """
        pagination_params = self._build_pagination_params(limit, offset)
        
        self._log_operation("listDimensions", {
            "limit": pagination_params["limit"],
            "offset": pagination_params["offset"]
        })
        
        params = self._clean_params({
            "limit": pagination_params["limit"],
            "offset": pagination_params["offset"]
        })
        
        response = self.client.listDimensions(**params)
        
        if isinstance(response, dict):
            return DimensionListResponse(**response)
        return response
    
    @handle_rest_errors
    def get_dimension(self, dimension_id: str) -> DimensionResponse:
        """Get a specific dimension by ID.
        
        Args:
            dimension_id: The dimension ID
            
        Returns:
            DimensionResponse with dimension details
            
        Raises:
            RestApiError: For API errors
        """
        self._log_operation("getDimension", {"dimensionId": dimension_id})
        
        response = self.client.getDimension(dimensionId=dimension_id)
        
        if isinstance(response, dict):
            return DimensionResponse(**response)
        return response
    
    @handle_rest_errors
    def list_user_types(self, limit: int = 100, offset: int = 0) -> UserTypeListResponse:
        """List all available user types.
        
        Args:
            limit: Result limit
            offset: Result offset
            
        Returns:
            UserTypeListResponse with available user types
            
        Raises:
            RestApiError: For API errors
        """
        pagination_params = self._build_pagination_params(limit, offset)
        
        self._log_operation("listUserTypes", {
            "limit": pagination_params["limit"],
            "offset": pagination_params["offset"]
        })
        
        params = self._clean_params({
            "limit": pagination_params["limit"],
            "offset": pagination_params["offset"]
        })
        
        response = self.client.listUserTypes(**params)
        
        if isinstance(response, dict):
            return UserTypeListResponse(**response)
        return response
    
    @handle_rest_errors
    def get_user_type(self, user_type_id: str) -> UserTypeResponse:
        """Get a specific user type by ID.
        
        Args:
            user_type_id: The user type ID
            
        Returns:
            UserTypeResponse with user type details
            
        Raises:
            RestApiError: For API errors
        """
        self._log_operation("getUserType", {"userTypeId": user_type_id})
        
        response = self.client.getUserType(userTypeId=user_type_id)
        
        if isinstance(response, dict):
            return UserTypeResponse(**response)
        return response
    
    @handle_rest_errors
    def list_workspaces(self, limit: int = 100, offset: int = 0) -> WorkspaceListResponse:
        """List all available workspaces.
        
        Args:
            limit: Result limit
            offset: Result offset
            
        Returns:
            WorkspaceListResponse with available workspaces
            
        Raises:
            RestApiError: For API errors
        """
        pagination_params = self._build_pagination_params(limit, offset)
        
        self._log_operation("listWorkspaces", {
            "limit": pagination_params["limit"],
            "offset": pagination_params["offset"]
        })
        
        params = self._clean_params({
            "limit": pagination_params["limit"],
            "offset": pagination_params["offset"]
        })
        
        response = self.client.listWorkspaces(**params)
        
        if isinstance(response, dict):
            return WorkspaceListResponse(**response)
        return response
    
    @handle_rest_errors
    def get_workspace(self, workspace_id: str) -> WorkspaceResponse:
        """Get a specific workspace by ID.
        
        Args:
            workspace_id: The workspace ID
            
        Returns:
            WorkspaceResponse with workspace details
            
        Raises:
            RestApiError: For API errors
        """
        self._log_operation("getWorkspace", {"workspaceId": workspace_id})
        
        response = self.client.getWorkspace(workspaceId=workspace_id)
        
        if isinstance(response, dict):
            return WorkspaceResponse(**response)
        return response
