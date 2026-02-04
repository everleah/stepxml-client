"""Entity operations for STEP REST API v2."""

import logging
from typing import Optional, List, Dict, Any

from ..base import BaseOperation, handle_rest_errors
from ..exceptions import NotFoundError, ValidationError, RestApiError
from ..models.entity import (
    EntityResponse,
    EntityListResponse,
    EntitySearchRequest,
    EntityCreateRequest,
    EntityUpdateRequest,
    EntityRelationshipResponse,
    EntityBulkRequest,
    EntityBulkResponse,
)
from ..models.common import PagedResponse


class EntityOperations(BaseOperation):
    """Operations for STEP Entities."""
    
    def __init__(self, client, logger: Optional[logging.Logger] = None):
        """Initialize entity operations.
        
        Args:
            client: The REST API client
            logger: Optional logger instance
        """
        super().__init__(client, operation_name="EntityOperations", logger=logger)
    
    @handle_rest_errors
    def get_entity(self, entity_id: str,
                   include_attributes: bool = True,
                   include_relationships: bool = False) -> EntityResponse:
        """Get a single entity by ID.
        
        Args:
            entity_id: The entity ID
            include_attributes: Whether to include attributes (default: True)
            include_relationships: Whether to include relationships (default: False)
            
        Returns:
            EntityResponse with entity data
            
        Raises:
            ValidationError: If entity_id is missing
            NotFoundError: If entity not found
            RestApiError: For other API errors
        """
        self._validate_required_params(
            {"entity_id": entity_id},
            ["entity_id"]
        )
        
        self._log_operation("getEntity", {
            "entityId": entity_id,
            "includeAttributes": include_attributes,
            "includeRelationships": include_relationships
        })
        
        try:
            response = self.client.getEntity(
                entityId=entity_id,
                includeAttributes=include_attributes,
                includeRelationships=include_relationships
            )
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(entity_id, "Entity")
            raise
        
        if isinstance(response, dict):
            return EntityResponse(**response)
        return response
    
    @handle_rest_errors
    def search_entities(self,
                       query: str = "*",
                       limit: int = 20,
                       offset: int = 0,
                       type_filter: Optional[str] = None,
                       include_attributes: bool = True) -> EntityListResponse:
        """Search entities with optional filters.
        
        Args:
            query: Search query string (default: "*" for all)
            limit: Result limit (1-500, default: 20)
            offset: Result offset (default: 0)
            type_filter: Optional filter by entity type
            include_attributes: Whether to include attributes (default: True)
            
        Returns:
            EntityListResponse with paginated results
            
        Raises:
            ValidationError: If parameters invalid
            RestApiError: For API errors
        """
        pagination_params = self._build_pagination_params(limit, offset)
        
        self._log_operation("searchEntities", {
            "q": query,
            "limit": pagination_params["limit"],
            "offset": pagination_params["offset"],
            "typeFilter": type_filter,
            "includeAttributes": include_attributes
        })
        
        params = self._clean_params({
            "q": query,
            "limit": pagination_params["limit"],
            "offset": pagination_params["offset"],
            "typeFilter": type_filter,
            "includeAttributes": include_attributes
        })
        
        response = self.client.searchEntities(**params)
        
        if isinstance(response, dict):
            return EntityListResponse(**response)
        return response
    
    @handle_rest_errors
    def list_entities(self, limit: int = 20, offset: int = 0) -> EntityListResponse:
        """Convenience method to list all entities.
        
        Args:
            limit: Result limit
            offset: Result offset
            
        Returns:
            EntityListResponse with all entities
        """
        return self.search_entities(query="*", limit=limit, offset=offset)
    
    @handle_rest_errors
    def create_entity(self, data: EntityCreateRequest) -> EntityResponse:
        """Create a new entity.
        
        Args:
            data: EntityCreateRequest with entity data
            
        Returns:
            EntityResponse with created entity
            
        Raises:
            ValidationError: If data invalid
            RestApiError: For API errors
        """
        # Convert Pydantic model to dict if needed
        if hasattr(data, 'model_dump'):
            create_data = data.model_dump(exclude_none=True)
        else:
            create_data = dict(data) if not isinstance(data, dict) else data
        
        self._log_operation("createEntity", create_data)
        
        try:
            response = self.client.createEntity(body=create_data)
        except Exception as e:
            if "400" in str(e) or "409" in str(e):
                raise ValidationError(f"Create failed: {str(e)}")
            raise
        
        if isinstance(response, dict):
            return EntityResponse(**response)
        return response
    
    @handle_rest_errors
    def update_entity(self, entity_id: str,
                     updates: EntityUpdateRequest) -> EntityResponse:
        """Update an existing entity.
        
        Args:
            entity_id: The entity ID to update
            updates: EntityUpdateRequest with updated data
            
        Returns:
            EntityResponse with updated entity
            
        Raises:
            ValidationError: If entity_id or data invalid
            NotFoundError: If entity not found
            RestApiError: For API errors
        """
        self._validate_required_params(
            {"entity_id": entity_id},
            ["entity_id"]
        )
        
        # Convert Pydantic model to dict if needed
        if hasattr(updates, 'model_dump'):
            update_data = updates.model_dump(exclude_none=True)
        else:
            update_data = dict(updates) if not isinstance(updates, dict) else updates
        
        self._log_operation("updateEntity", {
            "entityId": entity_id,
            "updates": update_data
        })
        
        try:
            response = self.client.updateEntity(
                entityId=entity_id,
                body=update_data
            )
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(entity_id, "Entity")
            if "400" in str(e):
                raise ValidationError(f"Update failed: {str(e)}")
            raise
        
        if isinstance(response, dict):
            return EntityResponse(**response)
        return response
    
    @handle_rest_errors
    def delete_entity(self, entity_id: str) -> bool:
        """Delete an entity.
        
        Args:
            entity_id: The entity ID to delete
            
        Returns:
            True if deletion was successful
            
        Raises:
            ValidationError: If entity_id missing
            NotFoundError: If entity not found
            RestApiError: For API errors
        """
        self._validate_required_params(
            {"entity_id": entity_id},
            ["entity_id"]
        )
        
        self._log_operation("deleteEntity", {"entityId": entity_id})
        
        try:
            self.client.deleteEntity(entityId=entity_id)
            return True
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(entity_id, "Entity")
            raise
    
    @handle_rest_errors
    def get_entity_relationships(self, entity_id: str,
                                 relationship_type: Optional[str] = None,
                                 limit: int = 20,
                                 offset: int = 0) -> EntityRelationshipResponse:
        """Get relationships for an entity.
        
        Args:
            entity_id: The entity ID
            relationship_type: Optional filter by relationship type
            limit: Result limit
            offset: Result offset
            
        Returns:
            EntityRelationshipResponse with entity relationships
            
        Raises:
            ValidationError: If entity_id missing
            NotFoundError: If entity not found
            RestApiError: For API errors
        """
        self._validate_required_params(
            {"entity_id": entity_id},
            ["entity_id"]
        )
        
        pagination_params = self._build_pagination_params(limit, offset)
        
        self._log_operation("getEntityRelationships", {
            "entityId": entity_id,
            "relationshipType": relationship_type,
            "limit": pagination_params["limit"],
            "offset": pagination_params["offset"]
        })
        
        params = self._clean_params({
            "relationshipType": relationship_type,
            "limit": pagination_params["limit"],
            "offset": pagination_params["offset"]
        })
        
        try:
            response = self.client.getEntityRelationships(
                entityId=entity_id,
                **params
            )
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(entity_id, "Entity")
            raise
        
        if isinstance(response, dict):
            return EntityRelationshipResponse(**response)
        return response
    
    @handle_rest_errors
    def bulk_create_entities(self, entities: List[EntityCreateRequest]) -> EntityBulkResponse:
        """Bulk create multiple entities.
        
        Args:
            entities: List of EntityCreateRequest objects
            
        Returns:
            EntityBulkResponse with results
            
        Raises:
            ValidationError: If data invalid
            RestApiError: For API errors
        """
        # Convert Pydantic models to dicts if needed
        entity_list = []
        for entity in entities:
            if hasattr(entity, 'model_dump'):
                entity_list.append(entity.model_dump(exclude_none=True))
            else:
                entity_list.append(dict(entity) if not isinstance(entity, dict) else entity)
        
        self._log_operation("bulkCreateEntities", {"count": len(entity_list)})
        
        try:
            response = self.client.bulkCreateEntities(body={"entities": entity_list})
        except Exception as e:
            if "400" in str(e):
                raise ValidationError(f"Bulk create failed: {str(e)}")
            raise
        
        if isinstance(response, dict):
            return EntityBulkResponse(**response)
        return response
    
    @handle_rest_errors
    def bulk_update_entities(self, updates: Dict[str, EntityUpdateRequest]) -> EntityBulkResponse:
        """Bulk update multiple entities.
        
        Args:
            updates: Dictionary mapping entity IDs to EntityUpdateRequest objects
            
        Returns:
            EntityBulkResponse with results
            
        Raises:
            ValidationError: If data invalid
            RestApiError: For API errors
        """
        # Convert Pydantic models to dicts if needed
        update_list = []
        for entity_id, update_req in updates.items():
            if hasattr(update_req, 'model_dump'):
                update_data = update_req.model_dump(exclude_none=True)
            else:
                update_data = dict(update_req) if not isinstance(update_req, dict) else update_req
            update_list.append({"id": entity_id, "updates": update_data})
        
        self._log_operation("bulkUpdateEntities", {"count": len(update_list)})
        
        try:
            response = self.client.bulkUpdateEntities(body={"updates": update_list})
        except Exception as e:
            if "400" in str(e):
                raise ValidationError(f"Bulk update failed: {str(e)}")
            raise
        
        if isinstance(response, dict):
            return EntityBulkResponse(**response)
        return response
    
    @handle_rest_errors
    def search_by_type(self, entity_type: str,
                       limit: int = 20, offset: int = 0) -> EntityListResponse:
        """Convenience method to search entities by type.
        
        Args:
            entity_type: The entity type to filter by
            limit: Result limit
            offset: Result offset
            
        Returns:
            EntityListResponse filtered by type
        """
        return self.search_entities(
            query="*",
            limit=limit,
            offset=offset,
            type_filter=entity_type
        )
    
    @handle_rest_errors
    def search_modified_since(self, timestamp: str,
                             limit: int = 20, offset: int = 0) -> EntityListResponse:
        """Convenience method to search entities modified since a timestamp.
        
        Args:
            timestamp: ISO 8601 timestamp (e.g., "2025-01-01T00:00:00Z")
            limit: Result limit
            offset: Result offset
            
        Returns:
            EntityListResponse of modified entities
        """
        query = f"modifiedAt >= {timestamp}"
        return self.search_entities(query=query, limit=limit, offset=offset)
