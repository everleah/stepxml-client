"""Entity operations for STEP REST API v2."""

import logging
from typing import Optional, List, Dict, Any

from ..base import BaseOperation, handle_rest_errors
from ..exceptions import NotFoundError, ValidationError, RestApiError, ConflictError
from ..models.entity import (
    EntityResponse,
    EntityListResponse,
    EntityCreateRequest,
    EntityUpdateRequest,
    EntityRelationshipResponse,
)


class EntityOperations(BaseOperation):
    """Operations for STEP Entities."""
    
    def __init__(self, client, logger: Optional[logging.Logger] = None,
                 context: Optional[str] = None, workspace: Optional[str] = None):
        """Initialize entity operations.
        
        Args:
            client: The REST API client
            logger: Optional logger instance
            context: STEP context ID for all API calls
            workspace: STEP workspace ID (defaults to "Main" server-side)
        """
        super().__init__(client, operation_name="EntityOperations", logger=logger,
                         context=context, workspace=workspace)
    
    @handle_rest_errors
    def get_entity(self, entity_id: str,
                   key_id: Optional[str] = None,
                   include_inherited_data: bool = False) -> EntityResponse:
        """Get a single entity by ID.
        
        Args:
            entity_id: The entity ID (or alternate key value if key_id is set)
            key_id: Alternate key ID to use for lookup (optional)
            include_inherited_data: Whether to include inherited attribute values (default: False)
            
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
        
        query_params = self._build_context_params()
        if key_id:
            query_params["keyId"] = key_id
        if include_inherited_data:
            query_params["includeInheritedData"] = include_inherited_data
        self._log_operation("getEntity", {"entity_id": entity_id})
        
        try:
            response = self.client.getEntity(id=entity_id, **query_params)
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(entity_id, "Entity")
            raise
        
        if isinstance(response, dict):
            return EntityResponse(**response)
        return response
    
    @handle_rest_errors
    def search_entities(self, condition: dict) -> EntityListResponse:
        """Search entities using a STEP condition query.
        
        Args:
            condition: A STEP condition object defining the search criteria.
                       Supported conditionTypes: 'and', 'or', 'id', 'name',
                       'textvalue', 'numericvalue', 'objecttype', 'simplebelow',
                       'lovvalue', 'hasreferenceto', 'hasdatacontainerobject'.
            
        Returns:
            EntityListResponse with matching entities
            
        Raises:
            ValidationError: If condition is invalid
            RestApiError: For API errors
        """
        self._validate_required_params({"condition": condition}, ["condition"])
        body = {"condition": condition}
        self._log_operation("postEntitiesSearch", {"condition": condition})
        
        response = self.client.postEntitiesSearch(body=body, **self._build_context_params())
        
        if isinstance(response, dict):
            return EntityListResponse(**response)
        return response
    
    def list_entities(self) -> EntityListResponse:
        """List all entities (convenience method).
        
        Returns:
            EntityListResponse with entities
        """
        return self.search_entities(
            condition={"conditionType": "name", "value": "*"}
        )
    
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
        self._validate_required_params(
            {"objectType": data.objectType, "parent": data.parent},
            ["objectType", "parent"]
        )
        create_data = data.model_dump(exclude_none=True)
        self._log_operation("postEntities", {"objectType": data.objectType})
        
        try:
            response = self.client.postEntities(body=create_data, **self._build_context_params())
        except Exception as e:
            if "409" in str(e):
                raise ConflictError(409, str(e))
            raise
        
        if isinstance(response, dict):
            return EntityResponse(**response)
        return response
    
    @handle_rest_errors
    def update_entity(self, entity_id: str,
                     updates: EntityUpdateRequest,
                     key_id: Optional[str] = None) -> EntityResponse:
        """Partially update an existing entity (PATCH).
        
        Args:
            entity_id: The entity ID (or alternate key value if key_id is set)
            updates: EntityUpdateRequest with fields to update
            key_id: Alternate key ID to use for lookup (optional)
            
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
        
        update_data = updates.model_dump(exclude_none=True)
        query_params = self._build_context_params()
        if key_id:
            query_params["keyId"] = key_id
        self._log_operation("patchEntity", {"entity_id": entity_id})
        
        try:
            response = self.client.patchEntity(
                id=entity_id,
                body=update_data,
                **query_params
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
    def replace_entity(self, entity_id: str,
                       data: EntityCreateRequest,
                       key_id: Optional[str] = None,
                       allow_overwrite: bool = False) -> EntityResponse:
        """Fully replace an entity (PUT). Creates it if it does not exist.
        
        Args:
            entity_id: The entity ID (or alternate key value if key_id is set)
            data: Complete entity data
            key_id: Alternate key ID to use for lookup (optional)
            allow_overwrite: Whether to allow overwriting an existing entity
            
        Returns:
            EntityResponse with replaced entity
        """
        self._validate_required_params(
            {"entity_id": entity_id},
            ["entity_id"]
        )
        
        create_data = data.model_dump(exclude_none=True)
        query_params: Dict[str, Any] = self._build_context_params()
        if key_id:
            query_params["keyId"] = key_id
        if allow_overwrite:
            query_params["allow-overwrite"] = allow_overwrite
        self._log_operation("putEntity", {"entity_id": entity_id})
        
        try:
            response = self.client.putEntity(
                id=entity_id,
                body=create_data,
                **query_params
            )
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(entity_id, "Entity")
            if "400" in str(e) or "409" in str(e):
                raise ValidationError(str(e))
            raise
        
        if isinstance(response, dict):
            return EntityResponse(**response)
        return response
    
    @handle_rest_errors
    def delete_entity(self, entity_id: str,
                      key_id: Optional[str] = None) -> bool:
        """Delete an entity.
        
        Args:
            entity_id: The entity ID (or alternate key value if key_id is set)
            key_id: Alternate key ID to use for lookup (optional)
            
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
        
        query_params = self._build_context_params()
        if key_id:
            query_params["keyId"] = key_id
        self._log_operation("deleteEntity", {"entity_id": entity_id})
        
        try:
            self.client.deleteEntity(id=entity_id, **query_params)
            return True
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(entity_id, "Entity")
            raise
    
    @handle_rest_errors
    def get_entity_relationships(self, entity_id: str,
                                 reference_type_id: str,
                                 key_id: Optional[str] = None) -> EntityRelationshipResponse:
        """Get outgoing references for an entity by reference type (GET /entities/{id}/references/{referenceTypeId}).
        
        Args:
            entity_id: The entity ID (or alternate key value if key_id is set)
            reference_type_id: The reference type ID to retrieve
            key_id: Alternate key ID to use for lookup (optional)
            
        Returns:
            EntityRelationshipResponse with entity references
            
        Raises:
            ValidationError: If entity_id or reference_type_id missing
            NotFoundError: If entity not found
            RestApiError: For API errors
        """
        self._validate_required_params(
            {"entity_id": entity_id, "reference_type_id": reference_type_id},
            ["entity_id", "reference_type_id"]
        )
        
        query_params = self._build_context_params()
        if key_id:
            query_params["keyId"] = key_id
        self._log_operation("getEntities{id}References", {"entity_id": entity_id, "reference_type_id": reference_type_id})
        
        try:
            response = self.client.getEntities_id_References(id=entity_id, referenceTypeId=reference_type_id, **query_params)
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(entity_id, "Entity")
            raise
        
        if isinstance(response, dict):
            return EntityRelationshipResponse(**response)
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
            condition={"conditionType": "objecttype", "objectType": entity_type}
        )
    

