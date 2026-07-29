"""Data type group operations for STEP REST API v2."""

from typing import Any

from ..base import BaseOperation, handle_rest_errors
from ..exceptions import NotFoundError
from ..models.data_type_group import DataTypeGroupResponse


class DataTypeGroupOperations(BaseOperation):
    """Operations for STEP Data Type Groups."""
    def __init__(self, client, logger=None, context=None, workspace=None):
        super().__init__(client, operation_name="DataTypeGroupOperations", logger=logger, context=context, workspace=workspace)

    @handle_rest_errors
    def get_data_type_group(self, group_id: str) -> DataTypeGroupResponse:
        self._validate_required_params({"group_id": group_id}, ["group_id"])
        self._log_operation("getDataTypeGroup", {"id": group_id})
        try:
            r = self.client.getDataTypeGroup(id=group_id, **self._build_context_params())
        except Exception as e:
            if "404" in str(e): raise NotFoundError(group_id, "DataTypeGroup")
            raise
        return DataTypeGroupResponse(**r) if isinstance(r, dict) else r

    @handle_rest_errors
    def get_data_type_group_children(self, group_id: str) -> list[str]:
        self._validate_required_params({"group_id": group_id}, ["group_id"])
        self._log_operation("getDataTypeGroupChildren", {"id": group_id})
        try:
            r = self.client.getDataTypeGroupChildren(id=group_id, **self._build_context_params())
        except Exception as e:
            if "404" in str(e): raise NotFoundError(group_id, "DataTypeGroup")
            raise
        return r if isinstance(r, list) else []

    @handle_rest_errors
    def get_data_type_group_attributes(self, group_id: str) -> list[dict[str, Any]]:
        self._validate_required_params({"group_id": group_id}, ["group_id"])
        self._log_operation("getDataTypeGroupAttributes", {"id": group_id})
        try:
            r = self.client.getDataTypeGroupAttributes(id=group_id, **self._build_context_params())
        except Exception as e:
            if "404" in str(e): raise NotFoundError(group_id, "DataTypeGroup")
            raise
        return r if isinstance(r, list) else []

    @handle_rest_errors
    def get_data_type_group_data_container_types(self, group_id: str) -> list[dict[str, Any]]:
        self._validate_required_params({"group_id": group_id}, ["group_id"])
        self._log_operation("getDataTypeGroupDataContainerTypes", {"id": group_id})
        try:
            r = self.client.getDataTypeGroupDataContainerTypes(id=group_id, **self._build_context_params())
        except Exception as e:
            if "404" in str(e): raise NotFoundError(group_id, "DataTypeGroup")
            raise
        return r if isinstance(r, list) else []

    @handle_rest_errors
    def get_data_type_group_reference_types(self, group_id: str) -> list[dict[str, Any]]:
        self._validate_required_params({"group_id": group_id}, ["group_id"])
        self._log_operation("getDataTypeGroupReferenceTypes", {"id": group_id})
        try:
            r = self.client.getDataTypeGroupReferenceTypes(id=group_id, **self._build_context_params())
        except Exception as e:
            if "404" in str(e): raise NotFoundError(group_id, "DataTypeGroup")
            raise
        return r if isinstance(r, list) else []
