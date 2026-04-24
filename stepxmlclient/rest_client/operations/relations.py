"""Reference (relation) operations for STEP REST API v2.

In the STEP REST API, references are modeled as sub-resources on entity types:
  GET/PUT/DELETE /products/{id}/references/{referenceTypeId}/{targetId}
  GET/PUT/DELETE /assets/{id}/references/{referenceTypeId}/{targetId}
  GET/PUT/DELETE /classifications/{id}/references/{referenceTypeId}/{targetId}
  GET/PUT/DELETE /entities/{id}/references/{referenceTypeId}/{targetId}
  GET /reference-types/{id}

There is no standalone "relationship" or "cross-reference" resource in the spec.
"""

import logging
from typing import Optional, Dict, Any, Literal

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

# Supported entity types for reference operations
EntityType = Literal["products", "assets", "classifications", "entities"]

# Map entity type to operation-ID prefix (singular capitalised)
_OP_PREFIX = {
    "products": "Product",
    "assets": "Asset",
    "classifications": "Classification",
    "entities": "Entity",
}

# Map entity type to plural capitalised form used in list-reference operation IDs
# e.g. getProducts{id}References, getEntities{id}References
_OP_PLURAL = {
    "products": "Products",
    "assets": "Assets",
    "classifications": "Classifications",
    "entities": "Entities",
}


class RelationOperations(BaseOperation):
    """Operations for managing references between STEP entities.

    The STEP REST API models references as sub-resources attached to a source entity.
    All methods require specifying the ``entity_type`` ('products', 'assets',
    'classifications', or 'entities') of the *source* object.
    """

    def __init__(self, client, logger: Optional[logging.Logger] = None,
                 context: Optional[str] = None, workspace: Optional[str] = None):
        """Initialize relation operations.
        
        Args:
            client: The REST API client
            logger: Optional logger instance
            context: STEP context ID for all API calls
            workspace: STEP workspace ID (defaults to "Main" server-side)
        """
        super().__init__(client, operation_name="RelationOperations", logger=logger,
                         context=context, workspace=workspace)

    # ============================================================================
    # Reference Operations
    # ============================================================================

    @handle_rest_errors
    def list_references(self, entity_type: EntityType,
                        entity_id: str,
                        reference_type_id: str,
                        key_id: Optional[str] = None) -> RelationshipListResponse:
        """List all outgoing references of a given type for a source entity.

        Calls: GET /{entity_type}/{id}/references/{referenceTypeId}

        Args:
            entity_type: Source entity type ('products', 'assets', 'classifications', 'entities')
            entity_id: Source entity ID (or alternate key value if key_id is set)
            reference_type_id: The reference type ID to list
            key_id: Alternate key ID for the source entity (optional)

        Returns:
            RelationshipListResponse with list of references
        """
        self._validate_required_params(
            {"entity_id": entity_id, "reference_type_id": reference_type_id},
            ["entity_id", "reference_type_id"]
        )

        plural = _OP_PLURAL.get(entity_type)
        if not plural:
            raise ValidationError(f"Invalid entity_type: {entity_type!r}. Must be one of {list(_OP_PLURAL)}")
        # Spec operationId uses literal braces: e.g. getProducts{id}References
        op_id = "get" + plural + "{id}References"

        query_params = self._build_context_params()
        if key_id:
            query_params["keyId"] = key_id
        self._log_operation(op_id, {"entity_id": entity_id, "reference_type_id": reference_type_id})

        try:
            op_func = getattr(self.client, op_id)
            response = op_func(id=entity_id, referenceTypeId=reference_type_id, **query_params)
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(entity_id, prefix)
            raise

        if isinstance(response, dict):
            return RelationshipListResponse(**response)
        return response

    @handle_rest_errors
    def get_reference(self, entity_type: EntityType,
                      entity_id: str,
                      reference_type_id: str,
                      target_id: str,
                      key_id: Optional[str] = None,
                      target_key_id: Optional[str] = None,
                      include_inherited_data: bool = False) -> RelationshipResponse:
        """Get a single outgoing reference.

        Calls: GET /{entity_type}/{id}/references/{referenceTypeId}/{targetId}

        Args:
            entity_type: Source entity type
            entity_id: Source entity ID (or alternate key if key_id is set)
            reference_type_id: The reference type ID
            target_id: Target entity ID (or alternate key if target_key_id is set)
            key_id: Alternate key ID for source entity (optional)
            target_key_id: Alternate key ID for target entity (optional)
            include_inherited_data: Whether to include inherited attribute values (default: False)

        Returns:
            RelationshipResponse with reference details
        """
        self._validate_required_params(
            {"entity_id": entity_id, "reference_type_id": reference_type_id, "target_id": target_id},
            ["entity_id", "reference_type_id", "target_id"]
        )

        prefix = _OP_PREFIX.get(entity_type, "Product")
        op_id = f"get{prefix}Reference"

        query_params: Dict[str, Any] = self._build_context_params()
        if key_id:
            query_params["keyId"] = key_id
        if target_key_id:
            query_params["targetKeyId"] = target_key_id
        if include_inherited_data:
            query_params["includeInheritedData"] = include_inherited_data
        self._log_operation(op_id, {"entity_id": entity_id, "reference_type_id": reference_type_id, "target_id": target_id})

        try:
            op_func = getattr(self.client, op_id)
            response = op_func(id=entity_id, referenceTypeId=reference_type_id, targetId=target_id, **query_params)
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(entity_id, prefix)
            raise

        if isinstance(response, dict):
            return RelationshipResponse(**response)
        return response

    @handle_rest_errors
    def put_reference(self, entity_type: EntityType,
                      entity_id: str,
                      reference_type_id: str,
                      target_id: str,
                      data: Optional[Dict[str, Any]] = None,
                      key_id: Optional[str] = None,
                      target_key_id: Optional[str] = None,
                      allow_overwrite: bool = False) -> RelationshipResponse:
        """Create or replace an outgoing reference (PUT).

        Calls: PUT /{entity_type}/{id}/references/{referenceTypeId}/{targetId}

        Args:
            entity_type: Source entity type
            entity_id: Source entity ID (or alternate key if key_id is set)
            reference_type_id: The reference type ID
            target_id: Target entity ID (or alternate key if target_key_id is set)
            data: Optional body with reference attribute values
            key_id: Alternate key ID for source entity (optional)
            target_key_id: Alternate key ID for target entity (optional)
            allow_overwrite: Whether to allow overwriting an existing reference

        Returns:
            RelationshipResponse with created/replaced reference
        """
        self._validate_required_params(
            {"entity_id": entity_id, "reference_type_id": reference_type_id, "target_id": target_id},
            ["entity_id", "reference_type_id", "target_id"]
        )

        prefix = _OP_PREFIX.get(entity_type, "Product")
        op_id = f"put{prefix}Reference"

        query_params: Dict[str, Any] = self._build_context_params()
        if key_id:
            query_params["keyId"] = key_id
        if target_key_id:
            query_params["targetKeyId"] = target_key_id
        if allow_overwrite:
            query_params["allow-overwrite"] = allow_overwrite
        self._log_operation(op_id, {"entity_id": entity_id, "reference_type_id": reference_type_id, "target_id": target_id})

        try:
            op_func = getattr(self.client, op_id)
            if data:
                response = op_func(id=entity_id, referenceTypeId=reference_type_id, targetId=target_id, body=data, **query_params)
            else:
                response = op_func(id=entity_id, referenceTypeId=reference_type_id, targetId=target_id, **query_params)
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(entity_id, prefix)
            if "400" in str(e):
                raise ValidationError(str(e))
            raise

        if isinstance(response, dict):
            return RelationshipResponse(**response)
        return response

    @handle_rest_errors
    def delete_reference(self, entity_type: EntityType,
                         entity_id: str,
                         reference_type_id: str,
                         target_id: str,
                         key_id: Optional[str] = None,
                         target_key_id: Optional[str] = None) -> bool:
        """Delete an outgoing reference.

        Calls: DELETE /{entity_type}/{id}/references/{referenceTypeId}/{targetId}

        Args:
            entity_type: Source entity type
            entity_id: Source entity ID (or alternate key if key_id is set)
            reference_type_id: The reference type ID
            target_id: Target entity ID (or alternate key if target_key_id is set)
            key_id: Alternate key ID for source entity (optional)
            target_key_id: Alternate key ID for target entity (optional)

        Returns:
            True if deletion was successful
        """
        self._validate_required_params(
            {"entity_id": entity_id, "reference_type_id": reference_type_id, "target_id": target_id},
            ["entity_id", "reference_type_id", "target_id"]
        )

        prefix = _OP_PREFIX.get(entity_type, "Product")
        op_id = f"delete{prefix}Reference"

        query_params = self._build_context_params()
        if key_id:
            query_params["keyId"] = key_id
        if target_key_id:
            query_params["targetKeyId"] = target_key_id
        self._log_operation(op_id, {"entity_id": entity_id, "reference_type_id": reference_type_id, "target_id": target_id})

        try:
            op_func = getattr(self.client, op_id)
            op_func(id=entity_id, referenceTypeId=reference_type_id, targetId=target_id, **query_params)
            return True
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(entity_id, prefix)
            raise

    @handle_rest_errors
    def get_incoming_references(self, entity_type: EntityType,
                                entity_id: str,
                                reference_type_id: str,
                                key_id: Optional[str] = None) -> RelationshipListResponse:
        """List incoming references of a given type for a target entity.

        Calls: GET /{entity_type}/{id}/incoming-references/{referenceTypeId}

        Args:
            entity_type: Target entity type
            entity_id: Target entity ID (or alternate key if key_id is set)
            reference_type_id: The reference type ID to list
            key_id: Alternate key ID for the target entity (optional)

        Returns:
            RelationshipListResponse with list of incoming references
        """
        self._validate_required_params(
            {"entity_id": entity_id, "reference_type_id": reference_type_id},
            ["entity_id", "reference_type_id"]
        )

        prefix = _OP_PREFIX.get(entity_type, "Product")
        op_id = f"get{prefix}IncomingReference"

        query_params = self._build_context_params()
        if key_id:
            query_params["keyId"] = key_id
        self._log_operation(op_id, {"entity_id": entity_id, "reference_type_id": reference_type_id})

        try:
            op_func = getattr(self.client, op_id)
            response = op_func(id=entity_id, referenceTypeId=reference_type_id, **query_params)
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(entity_id, prefix)
            raise

        if isinstance(response, dict):
            return RelationshipListResponse(**response)
        return response

    # ============================================================================
    # Reference Type Lookup
    # ============================================================================

    @handle_rest_errors
    def get_reference_type(self, reference_type_id: str) -> RelationshipTypeResponse:
        """Get a reference type definition by ID (GET /reference-types/{id}).

        Args:
            reference_type_id: The reference type ID

        Returns:
            RelationshipTypeResponse with reference type details
        """
        self._validate_required_params(
            {"reference_type_id": reference_type_id},
            ["reference_type_id"]
        )

        query_params = self._build_context_params()
        self._log_operation("getReferenceType", {"reference_type_id": reference_type_id})

        try:
            response = self.client.getReferenceType(id=reference_type_id, **query_params)
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(reference_type_id, "ReferenceType")
            raise

        if isinstance(response, dict):
            return RelationshipTypeResponse(**response)
        return response
