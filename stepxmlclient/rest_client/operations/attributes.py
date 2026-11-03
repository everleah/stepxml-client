"""Attribute and type-definition operations for STEP REST API v2.

Covers Attributes, Lists of Values, Data Container Types, Data Type Groups,
Object Types, Reference Types, Units, and Unique Keys per the OpenAPI spec.
"""

import logging
from typing import Any, Optional

from ..base import BaseOperation, handle_rest_errors
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

        response = self._call_operation("getAttribute", id=attribute_id, **self._build_context_params())

        if isinstance(response, dict):
            return AttributeResponse(**response)
        return response

    # ------------------------------------------------------------------
    # Lists Of Values (tag: Lists Of Values)
    # ------------------------------------------------------------------

    @handle_rest_errors
    def get_list_of_values(self, lov_id: str) -> ListOfValueResponse:
        """Get a List of Values by ID.

        Calls: GET /lists-of-values/{id} → getListOfValues

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
        self._log_operation("getListOfValues", {"id": lov_id})

        response = self._call_operation("getListOfValues", id=lov_id, **self._build_context_params())

        if isinstance(response, dict):
            return ListOfValueResponse(**response)
        return response

    @handle_rest_errors
    def get_list_of_values_entries(self, lov_id: str) -> list[dict[str, Any]]:
        """Get the value entries for a List of Values.

        Calls: GET /lists-of-values/{id}/value-entries → getListOfValuesEntries

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
        self._log_operation("getListOfValuesEntries", {"id": lov_id})

        response = self._call_operation("getListOfValuesEntries", id=lov_id, **self._build_context_params())

        return self._coerce_list_payload(response)

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
        response = self._call_operation("getDataContainerType", id=type_id, **self._build_context_params())
        return response if isinstance(response, dict) else response

    @handle_rest_errors
    def get_data_type_group(self, group_id: str) -> dict[str, Any]:
        """Get a data type group definition by ID.

        Calls: GET /data-type-groups/{id} → getDataTypeGroup
        """
        self._validate_required_params({"group_id": group_id}, ["group_id"])
        self._log_operation("getDataTypeGroup", {"id": group_id})
        response = self._call_operation("getDataTypeGroup", id=group_id, **self._build_context_params())
        return response if isinstance(response, dict) else response

    @handle_rest_errors
    def get_object_type(self, type_id: str) -> dict[str, Any]:
        """Get an object type definition by ID.

        Calls: GET /object-types/{id} → getObjectType
        """
        self._validate_required_params({"type_id": type_id}, ["type_id"])
        self._log_operation("getObjectType", {"id": type_id})
        response = self._call_operation("getObjectType", id=type_id, **self._build_context_params())
        return response if isinstance(response, dict) else response

    @handle_rest_errors
    def get_object_type_children(self, type_id: str) -> list[str]:
        """Get child object types for a given object type.

        Calls: GET /object-types/{id}/children → getObjectTypeChildren
        """
        self._validate_required_params({"type_id": type_id}, ["type_id"])
        self._log_operation("getObjectTypeChildren", {"id": type_id})
        response = self._call_operation("getObjectTypeChildren", id=type_id, **self._build_context_params())
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
        response = self._call_operation("getReferenceType", id=reference_type_id, **self._build_context_params())
        return response if isinstance(response, dict) else response

    @handle_rest_errors
    def get_unit(self, unit_id: str) -> dict[str, Any]:
        """Get a unit definition by ID.

        Calls: GET /units/{id} → getUnit
        """
        self._validate_required_params({"unit_id": unit_id}, ["unit_id"])
        self._log_operation("getUnit", {"id": unit_id})
        response = self._call_operation("getUnit", id=unit_id, **self._build_context_params())
        return response if isinstance(response, dict) else response

    @handle_rest_errors
    def get_unique_key(self, key_id: str) -> dict[str, Any]:
        """Get a unique key definition by ID.

        Calls: GET /unique-keys/{id} → getUniqueKey
        """
        self._validate_required_params({"key_id": key_id}, ["key_id"])
        self._log_operation("getUniqueKey", {"id": key_id})
        response = self._call_operation("getUniqueKey", id=key_id, **self._build_context_params())
        return response if isinstance(response, dict) else response
