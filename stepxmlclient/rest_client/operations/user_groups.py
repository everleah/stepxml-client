"""User group operations for STEP REST API v2."""

import logging
from typing import Any, Optional

from ..base import BaseOperation, handle_rest_errors
from ..exceptions import NotFoundError, ValidationError
from ..models.user import UserGroupResponse


class UserGroupOperations(BaseOperation):
    """Operations for STEP User Groups."""
    def __init__(self, client, logger=None, context=None, workspace=None):
        super().__init__(client, operation_name="UserGroupOperations", logger=logger, context=context, workspace=workspace)

    @handle_rest_errors
    def get_user_group(self, group_id: str) -> UserGroupResponse:
        self._validate_required_params({"group_id": group_id}, ["group_id"])
        self._log_operation("getUserGroup", {"id": group_id})
        try:
            r = self.client.getUserGroup(id=group_id, **self._build_context_params())
        except Exception as e:
            if "404" in str(e): raise NotFoundError(group_id, "UserGroup")
            raise
        return UserGroupResponse(**r) if isinstance(r, dict) else r

    @handle_rest_errors
    def create_or_replace_user_group(self, group_id: str, data: dict[str, Any]) -> UserGroupResponse:
        self._validate_required_params({"group_id": group_id}, ["group_id"])
        self._log_operation("createOrReplaceUserGroup", {"id": group_id})
        try:
            r = self.client.createOrReplaceUserGroup(id=group_id, json=data, **self._build_context_params())
        except Exception as e:
            if "400" in str(e): raise ValidationError(str(e))
            raise
        return UserGroupResponse(**r) if isinstance(r, dict) else r

    @handle_rest_errors
    def update_user_group(self, group_id: str, data: dict[str, Any]) -> UserGroupResponse:
        self._validate_required_params({"group_id": group_id}, ["group_id"])
        self._log_operation("updateUserGroup", {"id": group_id})
        try:
            r = self.client.updateUserGroup(id=group_id, json=data, **self._build_context_params())
        except Exception as e:
            if "404" in str(e): raise NotFoundError(group_id, "UserGroup")
            raise
        return UserGroupResponse(**r) if isinstance(r, dict) else r

    @handle_rest_errors
    def delete_user_group(self, group_id: str) -> bool:
        self._validate_required_params({"group_id": group_id}, ["group_id"])
        self._log_operation("deleteUserGroup", {"id": group_id})
        try:
            self.client.deleteUserGroup(id=group_id, **self._build_context_params())
            return True
        except Exception as e:
            if "404" in str(e): raise NotFoundError(group_id, "UserGroup")
            raise

    @handle_rest_errors
    def get_user_group_users(self, group_id: str) -> list[dict[str, Any]]:
        self._validate_required_params({"group_id": group_id}, ["group_id"])
        self._log_operation("getUserGroupUsers", {"id": group_id})
        try:
            r = self.client.getUserGroupUsers(id=group_id, **self._build_context_params())
        except Exception as e:
            if "404" in str(e): raise NotFoundError(group_id, "UserGroup")
            raise
        return r if isinstance(r, list) else []

    @handle_rest_errors
    def get_user_group_children(self, group_id: str) -> list[str]:
        self._validate_required_params({"group_id": group_id}, ["group_id"])
        self._log_operation("getUserGroupChildren", {"id": group_id})
        try:
            r = self.client.getUserGroupChildren(id=group_id, **self._build_context_params())
        except Exception as e:
            if "404" in str(e): raise NotFoundError(group_id, "UserGroup")
            raise
        return r if isinstance(r, list) else []
