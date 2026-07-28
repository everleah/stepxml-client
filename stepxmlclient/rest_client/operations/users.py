"""User operations for STEP REST API v2.

Covers the /users endpoints introduced in v1.4.0.
"""

import logging
from typing import Any, Optional

from ..base import BaseOperation, handle_rest_errors
from ..exceptions import NotFoundError, ValidationError
from ..models.user import UserResponse


class UserOperations(BaseOperation):
    """Operations for STEP Users."""

    def __init__(self, client, logger: Optional[logging.Logger] = None,
                 context: Optional[str] = None, workspace: Optional[str] = None):
        super().__init__(client, operation_name="UserOperations", logger=logger,
                         context=context, workspace=workspace)

    @handle_rest_errors
    def get_user(self, user_id: str) -> UserResponse:
        """Get a user by ID.
        Calls: GET /users/{id} -> getUser
        """
        self._validate_required_params({"user_id": user_id}, ["user_id"])
        self._log_operation("getUser", {"id": user_id})
        try:
            r = self.client.getUser(id=user_id, **self._build_context_params())
        except Exception as e:
            if "404" in str(e): raise NotFoundError(user_id, "User")
            raise
        return UserResponse(**r) if isinstance(r, dict) else r

    @handle_rest_errors
    def create_or_replace_user(self, user_id: str, data: dict[str, Any]) -> UserResponse:
        """Create or fully replace a user.
        Calls: PUT /users/{id} -> createOrReplaceUser
        """
        self._validate_required_params({"user_id": user_id}, ["user_id"])
        self._log_operation("createOrReplaceUser", {"id": user_id})
        try:
            r = self.client.createOrReplaceUser(id=user_id, json=data, **self._build_context_params())
        except Exception as e:
            if "400" in str(e): raise ValidationError(str(e))
            raise
        return UserResponse(**r) if isinstance(r, dict) else r

    @handle_rest_errors
    def update_user(self, user_id: str, data: dict[str, Any]) -> UserResponse:
        """Partially update a user.
        Calls: PATCH /users/{id} -> updateUser
        """
        self._validate_required_params({"user_id": user_id}, ["user_id"])
        self._log_operation("updateUser", {"id": user_id})
        try:
            r = self.client.updateUser(id=user_id, json=data, **self._build_context_params())
        except Exception as e:
            if "404" in str(e): raise NotFoundError(user_id, "User")
            if "400" in str(e): raise ValidationError(str(e))
            raise
        return UserResponse(**r) if isinstance(r, dict) else r

    @handle_rest_errors
    def delete_user(self, user_id: str) -> bool:
        """Delete a user.
        Calls: DELETE /users/{id} -> deleteUser
        """
        self._validate_required_params({"user_id": user_id}, ["user_id"])
        self._log_operation("deleteUser", {"id": user_id})
        try:
            self.client.deleteUser(id=user_id, **self._build_context_params())
            return True
        except Exception as e:
            if "404" in str(e): raise NotFoundError(user_id, "User")
            raise

    @handle_rest_errors
    def randomize_password(self, user_id: str) -> UserResponse:
        """Randomize a user's password.
        Calls: POST /users/{id}/randomize-password -> randomizeStepPassword
        """
        self._validate_required_params({"user_id": user_id}, ["user_id"])
        self._log_operation("randomizeStepPassword", {"id": user_id})
        try:
            r = self.client.randomizeStepPassword(id=user_id, **self._build_context_params())
        except Exception as e:
            if "404" in str(e): raise NotFoundError(user_id, "User")
            raise
        return UserResponse(**r) if isinstance(r, dict) else r

    @handle_rest_errors
    def add_user_to_group(self, user_id: str, group_data: dict[str, Any]) -> UserResponse:
        """Add a user to a group.
        Calls: POST /users/{id}/add-to-group -> addUserToGroup
        """
        self._validate_required_params({"user_id": user_id}, ["user_id"])
        self._log_operation("addUserToGroup", {"id": user_id})
        try:
            r = self.client.addUserToGroup(id=user_id, json=group_data, **self._build_context_params())
        except Exception as e:
            if "404" in str(e): raise NotFoundError(user_id, "User")
            raise
        return UserResponse(**r) if isinstance(r, dict) else r

    @handle_rest_errors
    def remove_user_from_group(self, user_id: str, group_data: dict[str, Any]) -> UserResponse:
        """Remove a user from a group.
        Calls: POST /users/{id}/remove-from-group -> removeUserFromGroup
        """
        self._validate_required_params({"user_id": user_id}, ["user_id"])
        self._log_operation("removeUserFromGroup", {"id": user_id})
        try:
            r = self.client.removeUserFromGroup(id=user_id, json=group_data, **self._build_context_params())
        except Exception as e:
            if "404" in str(e): raise NotFoundError(user_id, "User")
            raise
        return UserResponse(**r) if isinstance(r, dict) else r
