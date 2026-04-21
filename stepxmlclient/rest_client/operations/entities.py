"""Entity operations for STEP REST API v2."""

import logging
from typing import Optional, List, Dict, Any

from ..base import BaseOperation, handle_rest_errors
from ..exceptions import NotFoundError, ValidationError, RestApiError, ConflictError
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
        
        params: Dict[str, Any] = {"id": entity_id}
        if key_id:
            params["keyId"] = key_id
        if include_inherited_data:
            params["includeInheritedData"] = include_inherited_data
        params.update(self._build_context_params())
        self._log_operation("getEntity", params)
        
        try:
            response = self.client.getEntity(**params)
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
    
    @handle_rest_errors
    def list_entities(self) -> EntityListResponse:
        """List all entities by object type (convenience method).
        
        Returns:
            EntityListResponse with entities
        """
        return self.search_entities(
            condition={"conditionType": "objecttype", "objectTypeId": "*"}
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
        # Convert Pydantic model to dict if needed
        if hasattr(data, 'model_dump'):
            create_data = data.model_dump(exclude_none=True)
        else:
            create_data = dict(data) if not isinstance(data, dict) else data
        
        self._log_operation("postEntities", create_data)
        
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
        
        if hasattr(updates, 'model_dump'):
            update_data = updates.model_dump(exclude_none=True)
        else:
            update_data = dict(updates) if not isinstance(updates, dict) else updates
        
        params = {"id": entity_id}
        if key_id:
            params["keyId"] = key_id
        params.update(self._build_context_params())
        self._log_operation("patchEntity", {"id": entity_id})
        
        try:
            response = self.client.patchEntity(
                body=update_data,
                **params
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
        
        if hasattr(data, 'model_dump'):
            create_data = data.model_dump(exclude_none=True)
        else:
            create_data = dict(data) if not isinstance(data, dict) else data
        
        params: Dict[str, Any] = {"id": entity_id}
        if key_id:
            params["keyId"] = key_id
        if allow_overwrite:
            params["allow-overwrite"] = allow_overwrite
        params.update(self._build_context_params())
        self._log_operation("putEntity", {"id": entity_id})
        
        try:
            response = self.client.putEntity(
                body=create_data,
                **params
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
        
        params = {"id": entity_id}
        if key_id:
            params["keyId"] = key_id
        params.update(self._build_context_params())
        self._log_operation("deleteEntity", {"id": entity_id})
        
        try:
            self.client.deleteEntity(**params)
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
        
        params = {"id": entity_id, "referenceTypeId": reference_type_id}
        if key_id:
            params["keyId"] = key_id
        params.update(self._build_context_params())
        self._log_operation("getEntities{id}References", params)
        
        try:
            response = self.client.getEntities_id_References(**params)
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
        
        NOTE: No bulk create operation exists in the STEP REST API spec.
        Individual entities should be created via create_entity() (postEntities).
        This method is kept for backward compatibility but may not work with real API.
        
        Args:
            entities: List of EntityCreateRequest objects
            
        Returns:
            EntityBulkResponse with results
        """
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
            condition={"conditionType": "objecttype", "objectTypeId": entity_type}
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
