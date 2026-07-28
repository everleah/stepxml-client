"""Entity operations for STEP REST API v2."""

import logging
from typing import Any, Optional

from ..base import BaseOperation, handle_rest_errors
from ..exceptions import ConflictError, NotFoundError, ValidationError
from ..models.entity import (
    EntityCreateRequest,
    EntityListResponse,
    EntityRelationshipResponse,
    EntityResponse,
    EntityUpdateRequest,
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
        self._log_operation("createEntitySearch", {"condition": condition})
        
        response = self.client.createEntitySearch(json=body, **self._build_context_params())
        
        if isinstance(response, dict):
            return EntityListResponse(**response)
        return response
    
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
    

    @handle_rest_errors
    def find_similar_entities(self, entity_id: str,
                              key_id: Optional[str] = None) -> dict[str, Any]:
        self._validate_required_params({"entity_id": entity_id}, ["entity_id"])
        qp = self._build_context_params()
        if key_id: qp["keyId"] = key_id
        self._log_operation("findSimilarEntities", {"id": entity_id})
        try:
            r = self.client.findSimilarEntities(id=entity_id, **qp)
        except Exception as e:
            if "404" in str(e): raise NotFoundError(entity_id, "Entity")
            raise
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def entity_match_and_merge(self, data: dict[str, Any]) -> dict[str, Any]:
        self._validate_required_params({"data": data}, ["data"])
        self._log_operation("entityMatchAndMerge", data)
        try:
            r = self.client.entityMatchAndMerge(json=data, **self._build_context_params())
        except Exception as e:
            if "400" in str(e): raise ValidationError(str(e))
            raise
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def get_entity_approval_status(self, entity_id: str,
                                   key_id: Optional[str] = None) -> dict[str, Any]:
        self._validate_required_params({"entity_id": entity_id}, ["entity_id"])
        qp = self._build_context_params()
        if key_id: qp["keyId"] = key_id
        self._log_operation("getEntityApprovalStatus", {"id": entity_id})
        try:
            r = self.client.getEntityApprovalStatus(id=entity_id, **qp)
        except Exception as e:
            if "404" in str(e): raise NotFoundError(entity_id, "Entity")
            raise
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def approve_entity(self, entity_id: str,
                       key_id: Optional[str] = None) -> dict[str, Any]:
        self._validate_required_params({"entity_id": entity_id}, ["entity_id"])
        qp = self._build_context_params()
        if key_id: qp["keyId"] = key_id
        self._log_operation("approveEntity", {"id": entity_id})
        try:
            r = self.client.approveEntity(id=entity_id, **qp)
        except Exception as e:
            if "404" in str(e): raise NotFoundError(entity_id, "Entity")
            raise
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def approve_entity_deletion(self, entity_id: str,
                                key_id: Optional[str] = None) -> dict[str, Any]:
        self._validate_required_params({"entity_id": entity_id}, ["entity_id"])
        qp = self._build_context_params()
        if key_id: qp["keyId"] = key_id
        self._log_operation("approveEntityDeletion", {"id": entity_id})
        try:
            r = self.client.approveEntityDeletion(id=entity_id, **qp)
        except Exception as e:
            if "404" in str(e): raise NotFoundError(entity_id, "Entity")
            raise
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def purge_entity(self, entity_id: str,
                     key_id: Optional[str] = None) -> dict[str, Any]:
        self._validate_required_params({"entity_id": entity_id}, ["entity_id"])
        qp = self._build_context_params()
        if key_id: qp["keyId"] = key_id
        self._log_operation("purgeEntity", {"id": entity_id})
        try:
            r = self.client.purgeEntity(id=entity_id, **qp)
        except Exception as e:
            if "404" in str(e): raise NotFoundError(entity_id, "Entity")
            raise
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def get_entity_children(self, entity_id: str,
                            key_id: Optional[str] = None) -> list[str]:
        self._validate_required_params({"entity_id": entity_id}, ["entity_id"])
        qp = self._build_context_params()
        if key_id: qp["keyId"] = key_id
        self._log_operation("getEntityChildren", {"id": entity_id})
        try:
            r = self.client.getEntityChildren(id=entity_id, **qp)
        except Exception as e:
            if "404" in str(e): raise NotFoundError(entity_id, "Entity")
            raise
        return r if isinstance(r, list) else []

    @handle_rest_errors
    def get_entity_data_containers(self, entity_id: str,
                                   key_id: Optional[str] = None) -> dict[str, Any]:
        self._validate_required_params({"entity_id": entity_id}, ["entity_id"])
        qp = self._build_context_params()
        if key_id: qp["keyId"] = key_id
        self._log_operation("getEntityDataContainers", {"id": entity_id})
        try:
            r = self.client.getEntityDataContainers(id=entity_id, **qp)
        except Exception as e:
            if "404" in str(e): raise NotFoundError(entity_id, "Entity")
            raise
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def get_entity_incoming_references(self, entity_id: str,
                                       key_id: Optional[str] = None) -> dict[str, Any]:
        self._validate_required_params({"entity_id": entity_id}, ["entity_id"])
        qp = self._build_context_params()
        if key_id: qp["keyId"] = key_id
        self._log_operation("getEntityIncomingReferences", {"id": entity_id})
        try:
            r = self.client.getEntityIncomingReferences(id=entity_id, **qp)
        except Exception as e:
            if "404" in str(e): raise NotFoundError(entity_id, "Entity")
            raise
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def get_entity_value(self, entity_id: str, attribute_id: str,
                         key_id: Optional[str] = None) -> dict[str, Any]:
        self._validate_required_params(
            {"entity_id": entity_id, "attribute_id": attribute_id},
            ["entity_id", "attribute_id"])
        qp = self._build_context_params()
        if key_id: qp["keyId"] = key_id
        self._log_operation("getEntityValueByAttributeId",
                           {"id": entity_id, "attributeId": attribute_id})
        try:
            r = self.client.getEntityValueByAttributeId(
                id=entity_id, attributeId=attribute_id, **qp)
        except Exception as e:
            if "404" in str(e): raise NotFoundError(entity_id, "Entity")
            raise
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def replace_entity_value(self, entity_id: str, attribute_id: str,
                             value: dict[str, Any],
                             key_id: Optional[str] = None) -> dict[str, Any]:
        self._validate_required_params(
            {"entity_id": entity_id, "attribute_id": attribute_id},
            ["entity_id", "attribute_id"])
        qp = self._build_context_params()
        if key_id: qp["keyId"] = key_id
        self._log_operation("replaceEntityValueByAttributeId",
                           {"id": entity_id, "attributeId": attribute_id})
        try:
            r = self.client.replaceEntityValueByAttributeId(
                id=entity_id, attributeId=attribute_id, json=value, **qp)
        except Exception as e:
            if "404" in str(e): raise NotFoundError(entity_id, "Entity")
            if "400" in str(e): raise ValidationError(str(e))
            raise
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def delete_entity_value(self, entity_id: str, attribute_id: str,
                            key_id: Optional[str] = None) -> bool:
        self._validate_required_params(
            {"entity_id": entity_id, "attribute_id": attribute_id},
            ["entity_id", "attribute_id"])
        qp = self._build_context_params()
        if key_id: qp["keyId"] = key_id
        self._log_operation("deleteEntityValueByAttributeId",
                           {"id": entity_id, "attributeId": attribute_id})
        try:
            self.client.deleteEntityValueByAttributeId(
                id=entity_id, attributeId=attribute_id, **qp)
            return True
        except Exception as e:
            if "404" in str(e): raise NotFoundError(entity_id, "Entity")
            raise


