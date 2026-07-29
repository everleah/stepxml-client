"""Attribute and type-definition operations for STEP REST API v2.

Covers Attributes, Lists of Values, Data Container Types, Data Type Groups,
Object Types, Reference Types, Units, and Unique Keys per the OpenAPI spec.
"""

import logging
from typing import Any, Optional

from ..base import BaseOperation, handle_rest_errors
from ..exceptions import NotFoundError
from ..models.attribute import (
    AttributeResponse,
    ListOfValueResponse,
)


class AttributeOperations(BaseOperation):
    """Operations for STEP Attributes and type definitions.

    Note: The STEP REST API v2 (v1.4.0) only provides GET access for attribute
    and type-definition resources. There is no create, update, or delete for
    attributes via the REST API.
    """

    def __init__(self, client, logger: Optional[logging.Logger] = None,
                 context: str | None = None, workspace: str | None = None):
        super().__init__(client, operation_name="AttributeOperations", logger=logger,
                         context=context, workspace=workspace)

    # ------------------------------------------------------------------
    # Attributes (tag: Attributes)
    # ------------------------------------------------------------------

    @handle_rest_errors
    def get_attribute(self, attribute_id: str) -> AttributeResponse:
        """Get a single attribute definition by ID.

        Calls: GET /attributes/{id} → getAttribute

        Args:
            attribute_id: The attribute ID

        Returns:
            AttributeResponse with attribute definition

        Raises:
            ValidationError: If attribute_id is missing
            NotFoundError: If attribute not found
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

    # ------------------------------------------------------------------
    # Lists Of Values (tag: Lists Of Values)
    # ------------------------------------------------------------------

    @handle_rest_errors
    def get_list_of_values(self, lov_id: str) -> ListOfValueResponse:
        """Get a List of Values by ID.

        Calls: GET /lists-of-values/{id} → getListOfValuess

        Args:
            lov_id: The LOV ID

        Returns:
            ListOfValueResponse with LOV data

        Raises:
            ValidationError: If lov_id is missing
            NotFoundError: If LOV not found
        """
        self._validate_required_params(
            {"lov_id": lov_id},
            ["lov_id"]
        )
        self._log_operation("getListOfValuess", {"id": lov_id})

        try:
            response = self.client.getListOfValuess(id=lov_id, **self._build_context_params())
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(lov_id, "ListOfValues")
            raise

        if isinstance(response, dict):
            return ListOfValueResponse(**response)
        return response

    @handle_rest_errors
    def get_list_of_values_entries(self, lov_id: str) -> list[dict[str, Any]]:
        """Get the value entries for a List of Values.

        Calls: GET /lists-of-values/{id}/value-entries → getListOfValuessEntries

        Args:
            lov_id: The LOV ID

        Returns:
            List of value entry dictionaries

        Raises:
            ValidationError: If lov_id is missing
            NotFoundError: If LOV not found
        """
        self._validate_required_params(
            {"lov_id": lov_id},
            ["lov_id"]
        )
        self._log_operation("getListOfValuessEntries", {"id": lov_id})

        try:
            response = self.client.getListOfValuessEntries(id=lov_id, **self._build_context_params())
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(lov_id, "ListOfValues")
            raise

        if isinstance(response, list):
            return response
        if isinstance(response, dict):
            return response.get("items", [])
        return []

    # ------------------------------------------------------------------
    # Type definitions (various tags — read-only single GET each)
    # ------------------------------------------------------------------

    @handle_rest_errors
    def get_data_container_type(self, type_id: str) -> dict[str, Any]:
        """Get a data container type definition by ID.

        Calls: GET /data-container-types/{id} → getDataContainerType
        """
        self._validate_required_params({"type_id": type_id}, ["type_id"])
        self._log_operation("getDataContainerType", {"id": type_id})
        try:
            response = self.client.getDataContainerType(id=type_id, **self._build_context_params())
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(type_id, "DataContainerType")
            raise
        return response if isinstance(response, dict) else response

    @handle_rest_errors
    def get_data_type_group(self, group_id: str) -> dict[str, Any]:
        """Get a data type group definition by ID.

        Calls: GET /data-type-groups/{id} → getDataTypeGroup
        """
        self._validate_required_params({"group_id": group_id}, ["group_id"])
        self._log_operation("getDataTypeGroup", {"id": group_id})
        try:
            response = self.client.getDataTypeGroup(id=group_id, **self._build_context_params())
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(group_id, "DataTypeGroup")
            raise
        return response if isinstance(response, dict) else response

    @handle_rest_errors
    def get_object_type(self, type_id: str) -> dict[str, Any]:
        """Get an object type definition by ID.

        Calls: GET /object-types/{id} → getObjectType
        """
        self._validate_required_params({"type_id": type_id}, ["type_id"])
        self._log_operation("getObjectType", {"id": type_id})
        try:
            response = self.client.getObjectType(id=type_id, **self._build_context_params())
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(type_id, "ObjectType")
            raise
        return response if isinstance(response, dict) else response

    @handle_rest_errors
    def get_object_type_children(self, type_id: str) -> list[str]:
        """Get child object types for a given object type.

        Calls: GET /object-types/{id}/children → getObjectTypeChildren
        """
        self._validate_required_params({"type_id": type_id}, ["type_id"])
        self._log_operation("getObjectTypeChildren", {"id": type_id})
        try:
            response = self.client.getObjectTypeChildren(id=type_id, **self._build_context_params())
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(type_id, "ObjectType")
            raise
        if isinstance(response, list):
            return response
        return []

    @handle_rest_errors
    def get_reference_type(self, reference_type_id: str) -> dict[str, Any]:
        """Get a reference type definition by ID.

        Calls: GET /reference-types/{id} → getReferenceType
        """
        self._validate_required_params({"reference_type_id": reference_type_id}, ["reference_type_id"])
        self._log_operation("getReferenceType", {"id": reference_type_id})
        try:
            response = self.client.getReferenceType(id=reference_type_id, **self._build_context_params())
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(reference_type_id, "ReferenceType")
            raise
        return response if isinstance(response, dict) else response

    @handle_rest_errors
    def get_unit(self, unit_id: str) -> dict[str, Any]:
        """Get a unit definition by ID.

        Calls: GET /units/{id} → getUnit
        """
        self._validate_required_params({"unit_id": unit_id}, ["unit_id"])
        self._log_operation("getUnit", {"id": unit_id})
        try:
            response = self.client.getUnit(id=unit_id, **self._build_context_params())
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(unit_id, "Unit")
            raise
        return response if isinstance(response, dict) else response

    @handle_rest_errors
    def get_unique_key(self, key_id: str) -> dict[str, Any]:
        """Get a unique key definition by ID.

        Calls: GET /unique-keys/{id} → getUniqueKey
        """
        self._validate_required_params({"key_id": key_id}, ["key_id"])
        self._log_operation("getUniqueKey", {"id": key_id})
        try:
            response = self.client.getUniqueKey(id=key_id, **self._build_context_params())
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(key_id, "UniqueKey")
            raise
        return response if isinstance(response, dict) else response
