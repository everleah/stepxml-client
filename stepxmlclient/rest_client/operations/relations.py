"""Relationship operations for STEP REST API v2."""

import logging
from typing import Optional, Dict, Any

from ..base import BaseOperation, handle_rest_errors
from ..exceptions import NotFoundError, ValidationError, RestApiError
from ..models.relations import (
    RelationshipResponse,
    RelationshipListResponse,
    RelationshipCreateRequest,
    RelationshipUpdateRequest,
    RelationshipGraphResponse,
    RelationshipTypeResponse,
    CrossReferenceResponse,
    CrossReferenceListResponse,
    CrossReferenceCreateRequest,
    LinkResponse,
    LinkListResponse,
    LinkCreateRequest,
)


class RelationOperations(BaseOperation):
    """Operations for managing relationships, cross-references, and links between entities."""
    
    def __init__(self, client, logger: Optional[logging.Logger] = None):
        """Initialize relation operations.
        
        Args:
            client: The REST API client
            logger: Optional logger instance
        """
        super().__init__(client, operation_name="RelationOperations", logger=logger)
    
    # ============================================================================
    # Relationship Operations
    # ============================================================================
    
    @handle_rest_errors
    def get_relationship(self, relationship_id: str) -> RelationshipResponse:
        """Get a single relationship by ID.
        
        Args:
            relationship_id: The relationship ID
            
        Returns:
            RelationshipResponse with relationship details
            
        Raises:
            ValidationError: If relationship_id is missing
            NotFoundError: If relationship not found
            RestApiError: For API errors
        """
        self._validate_required_params(
            {"relationship_id": relationship_id},
            ["relationship_id"]
        )
        
        self._log_operation("getRelationship", {"relationshipId": relationship_id})
        
        try:
            response = self.client.getRelationship(relationshipId=relationship_id)
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(relationship_id, "Relationship")
            raise
        
        if isinstance(response, dict):
            return RelationshipResponse(**response)
        return response
    
    @handle_rest_errors
    def list_relationships(self,
                          source_id: Optional[str] = None,
                          target_id: Optional[str] = None,
                          relationship_type: Optional[str] = None,
                          limit: int = 20,
                          offset: int = 0) -> RelationshipListResponse:
        """List relationships with optional filters.
        
        Args:
            source_id: Filter by source entity ID
            target_id: Filter by target entity ID
            relationship_type: Filter by relationship type
            limit: Result limit (1-500, default: 20)
            offset: Result offset (default: 0)
            
        Returns:
            RelationshipListResponse with list of relationships
            
        Raises:
            RestApiError: For API errors
        """
        pagination_params = self._build_pagination_params(limit, offset)
        
        self._log_operation("listRelationships", {
            "sourceId": source_id,
            "targetId": target_id,
            "relationshipType": relationship_type,
            "limit": pagination_params["limit"],
            "offset": pagination_params["offset"]
        })
        
        params = self._clean_params({
            "sourceId": source_id,
            "targetId": target_id,
            "relationshipType": relationship_type,
            "limit": pagination_params["limit"],
            "offset": pagination_params["offset"]
        })
        
        response = self.client.listRelationships(**params)
        
        if isinstance(response, dict):
            return RelationshipListResponse(**response)
        return response
    
    @handle_rest_errors
    def create_relationship(self, data: RelationshipCreateRequest) -> RelationshipResponse:
        """Create a new relationship.
        
        Args:
            data: RelationshipCreateRequest with relationship details
            
        Returns:
            RelationshipResponse with created relationship
            
        Raises:
            ValidationError: If data invalid
            RestApiError: For API errors
        """
        if hasattr(data, 'model_dump'):
            create_data = data.model_dump(exclude_none=True)
        else:
            create_data = dict(data) if not isinstance(data, dict) else data
        
        self._log_operation("createRelationship", {
            "relationshipType": create_data.get("relationshipType"),
            "sourceId": create_data.get("sourceId"),
            "targetId": create_data.get("targetId")
        })
        
        try:
            response = self.client.createRelationship(body=create_data)
        except Exception as e:
            if "400" in str(e):
                raise ValidationError(f"Create relationship failed: {str(e)}")
            raise
        
        if isinstance(response, dict):
            return RelationshipResponse(**response)
        return response
    
    @handle_rest_errors
    def update_relationship(self, relationship_id: str, data: RelationshipUpdateRequest) -> RelationshipResponse:
        """Update an existing relationship.
        
        Args:
            relationship_id: The relationship ID to update
            data: RelationshipUpdateRequest with updates
            
        Returns:
            RelationshipResponse with updated relationship
            
        Raises:
            ValidationError: If data invalid
            NotFoundError: If relationship not found
            RestApiError: For API errors
        """
        self._validate_required_params(
            {"relationship_id": relationship_id},
            ["relationship_id"]
        )
        
        if hasattr(data, 'model_dump'):
            update_data = data.model_dump(exclude_none=True)
        else:
            update_data = dict(data) if not isinstance(data, dict) else data
        
        self._log_operation("updateRelationship", {
            "relationshipId": relationship_id,
            "updates": list(update_data.keys())
        })
        
        try:
            response = self.client.updateRelationship(relationshipId=relationship_id, body=update_data)
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(relationship_id, "Relationship")
            raise
        
        if isinstance(response, dict):
            return RelationshipResponse(**response)
        return response
    
    @handle_rest_errors
    def delete_relationship(self, relationship_id: str) -> bool:
        """Delete a relationship.
        
        Args:
            relationship_id: The relationship ID to delete
            
        Returns:
            True if deletion successful
            
        Raises:
            ValidationError: If relationship_id missing
            NotFoundError: If relationship not found
            RestApiError: For API errors
        """
        self._validate_required_params(
            {"relationship_id": relationship_id},
            ["relationship_id"]
        )
        
        self._log_operation("deleteRelationship", {"relationshipId": relationship_id})
        
        try:
            self.client.deleteRelationship(relationshipId=relationship_id)
            return True
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(relationship_id, "Relationship")
            raise
    
    @handle_rest_errors
    def get_relationship_types(self) -> Dict[str, RelationshipTypeResponse]:
        """Get available relationship types.
        
        Returns:
            Dictionary of relationship types
            
        Raises:
            RestApiError: For API errors
        """
        self._log_operation("getRelationshipTypes", {})
        
        response = self.client.getRelationshipTypes()
        
        if isinstance(response, dict):
            return {k: RelationshipTypeResponse(**v) if isinstance(v, dict) else v 
                    for k, v in response.items()}
        return response
    
    @handle_rest_errors
    def get_relationship_graph(self, entity_id: str, depth: int = 2) -> RelationshipGraphResponse:
        """Get relationship graph for an entity.
        
        Args:
            entity_id: The root entity ID
            depth: Graph traversal depth (default: 2)
            
        Returns:
            RelationshipGraphResponse with graph structure
            
        Raises:
            ValidationError: If entity_id missing
            NotFoundError: If entity not found
            RestApiError: For API errors
        """
        self._validate_required_params(
            {"entity_id": entity_id},
            ["entity_id"]
        )
        
        self._log_operation("getRelationshipGraph", {
            "entityId": entity_id,
            "depth": depth
        })
        
        try:
            response = self.client.getRelationshipGraph(entityId=entity_id, depth=depth)
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(entity_id, "Entity")
            raise
        
        if isinstance(response, dict):
            return RelationshipGraphResponse(**response)
        return response
    
    # ============================================================================
    # Cross-Reference Operations
    # ============================================================================
    
    @handle_rest_errors
    def get_cross_reference(self, cross_reference_id: str) -> CrossReferenceResponse:
        """Get a single cross-reference by ID.
        
        Args:
            cross_reference_id: The cross-reference ID
            
        Returns:
            CrossReferenceResponse with details
            
        Raises:
            ValidationError: If ID missing
            NotFoundError: If not found
            RestApiError: For API errors
        """
        self._validate_required_params(
            {"cross_reference_id": cross_reference_id},
            ["cross_reference_id"]
        )
        
        self._log_operation("getCrossReference", {"crossReferenceId": cross_reference_id})
        
        try:
            response = self.client.getCrossReference(crossReferenceId=cross_reference_id)
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(cross_reference_id, "CrossReference")
            raise
        
        if isinstance(response, dict):
            return CrossReferenceResponse(**response)
        return response
    
    @handle_rest_errors
    def list_cross_references(self,
                             source_id: Optional[str] = None,
                             reference_type: Optional[str] = None,
                             limit: int = 20,
                             offset: int = 0) -> CrossReferenceListResponse:
        """List cross-references with optional filters.
        
        Args:
            source_id: Filter by source entity ID
            reference_type: Filter by reference type
            limit: Result limit (1-500, default: 20)
            offset: Result offset (default: 0)
            
        Returns:
            CrossReferenceListResponse with list
            
        Raises:
            RestApiError: For API errors
        """
        pagination_params = self._build_pagination_params(limit, offset)
        
        self._log_operation("listCrossReferences", {
            "sourceId": source_id,
            "referenceType": reference_type,
            "limit": pagination_params["limit"],
            "offset": pagination_params["offset"]
        })
        
        params = self._clean_params({
            "sourceId": source_id,
            "referenceType": reference_type,
            "limit": pagination_params["limit"],
            "offset": pagination_params["offset"]
        })
        
        response = self.client.listCrossReferences(**params)
        
        if isinstance(response, dict):
            return CrossReferenceListResponse(**response)
        return response
    
    @handle_rest_errors
    def create_cross_reference(self, data: CrossReferenceCreateRequest) -> CrossReferenceResponse:
        """Create a new cross-reference.
        
        Args:
            data: CrossReferenceCreateRequest with details
            
        Returns:
            CrossReferenceResponse with created reference
            
        Raises:
            ValidationError: If data invalid
            RestApiError: For API errors
        """
        if hasattr(data, 'model_dump'):
            create_data = data.model_dump(exclude_none=True)
        else:
            create_data = dict(data) if not isinstance(data, dict) else data
        
        self._log_operation("createCrossReference", {
            "sourceId": create_data.get("sourceEntityId"),
            "referenceType": create_data.get("referenceType")
        })
        
        try:
            response = self.client.createCrossReference(body=create_data)
        except Exception as e:
            if "400" in str(e):
                raise ValidationError(f"Create cross-reference failed: {str(e)}")
            raise
        
        if isinstance(response, dict):
            return CrossReferenceResponse(**response)
        return response
    
    @handle_rest_errors
    def delete_cross_reference(self, cross_reference_id: str) -> bool:
        """Delete a cross-reference.
        
        Args:
            cross_reference_id: The cross-reference ID to delete
            
        Returns:
            True if deletion successful
            
        Raises:
            ValidationError: If ID missing
            NotFoundError: If not found
            RestApiError: For API errors
        """
        self._validate_required_params(
            {"cross_reference_id": cross_reference_id},
            ["cross_reference_id"]
        )
        
        self._log_operation("deleteCrossReference", {"crossReferenceId": cross_reference_id})
        
        try:
            self.client.deleteCrossReference(crossReferenceId=cross_reference_id)
            return True
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(cross_reference_id, "CrossReference")
            raise
    
    # ============================================================================
    # Link Operations
    # ============================================================================
    
    @handle_rest_errors
    def get_link(self, link_id: str) -> LinkResponse:
        """Get a single link by ID.
        
        Args:
            link_id: The link ID
            
        Returns:
            LinkResponse with link details
            
        Raises:
            ValidationError: If ID missing
            NotFoundError: If not found
            RestApiError: For API errors
        """
        self._validate_required_params(
            {"link_id": link_id},
            ["link_id"]
        )
        
        self._log_operation("getLink", {"linkId": link_id})
        
        try:
            response = self.client.getLink(linkId=link_id)
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(link_id, "Link")
            raise
        
        if isinstance(response, dict):
            return LinkResponse(**response)
        return response
    
    @handle_rest_errors
    def list_links(self,
                  source_id: Optional[str] = None,
                  link_type: Optional[str] = None,
                  limit: int = 20,
                  offset: int = 0) -> LinkListResponse:
        """List links with optional filters.
        
        Args:
            source_id: Filter by source entity ID
            link_type: Filter by link type
            limit: Result limit (1-500, default: 20)
            offset: Result offset (default: 0)
            
        Returns:
            LinkListResponse with list of links
            
        Raises:
            RestApiError: For API errors
        """
        pagination_params = self._build_pagination_params(limit, offset)
        
        self._log_operation("listLinks", {
            "sourceId": source_id,
            "linkType": link_type,
            "limit": pagination_params["limit"],
            "offset": pagination_params["offset"]
        })
        
        params = self._clean_params({
            "sourceId": source_id,
            "linkType": link_type,
            "limit": pagination_params["limit"],
            "offset": pagination_params["offset"]
        })
        
        response = self.client.listLinks(**params)
        
        if isinstance(response, dict):
            return LinkListResponse(**response)
        return response
    
    @handle_rest_errors
    def create_link(self, data: LinkCreateRequest) -> LinkResponse:
        """Create a new link.
        
        Args:
            data: LinkCreateRequest with link details
            
        Returns:
            LinkResponse with created link
            
        Raises:
            ValidationError: If data invalid
            RestApiError: For API errors
        """
        if hasattr(data, 'model_dump'):
            create_data = data.model_dump(exclude_none=True)
        else:
            create_data = dict(data) if not isinstance(data, dict) else data
        
        self._log_operation("createLink", {
            "sourceId": create_data.get("sourceId"),
            "linkType": create_data.get("linkType")
        })
        
        try:
            response = self.client.createLink(body=create_data)
        except Exception as e:
            if "400" in str(e):
                raise ValidationError(f"Create link failed: {str(e)}")
            raise
        
        if isinstance(response, dict):
            return LinkResponse(**response)
        return response
    
    @handle_rest_errors
    def delete_link(self, link_id: str) -> bool:
        """Delete a link.
        
        Args:
            link_id: The link ID to delete
            
        Returns:
            True if deletion successful
            
        Raises:
            ValidationError: If ID missing
            NotFoundError: If not found
            RestApiError: For API errors
        """
        self._validate_required_params(
            {"link_id": link_id},
            ["link_id"]
        )
        
        self._log_operation("deleteLink", {"linkId": link_id})
        
        try:
            self.client.deleteLink(linkId=link_id)
            return True
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(link_id, "Link")
            raise
