"""Collection group operations for STEP REST API v2."""

from typing import Any

from ..base import BaseOperation, handle_rest_errors
from ..exceptions import NotFoundError
from ..models.collection import CollectionGroupResponse


class CollectionGroupOperations(BaseOperation):
    """Operations for STEP Collection Groups."""
    def __init__(self, client, logger=None, context=None, workspace=None):
        super().__init__(client, operation_name="CollectionGroupOperations", logger=logger, context=context, workspace=workspace)

    @handle_rest_errors
    def get_collection_group(self, group_id: str) -> CollectionGroupResponse:
        self._validate_required_params({"group_id": group_id}, ["group_id"])
        self._log_operation("getCollectionGroup", {"id": group_id})
        try:
            r = self.client.getCollectionGroup(id=group_id, **self._build_context_params())
        except Exception as e:
            if "404" in str(e): raise NotFoundError(group_id, "CollectionGroup")
            raise
        return CollectionGroupResponse(**r) if isinstance(r, dict) else r

    @handle_rest_errors
    def get_collection_group_children(self, group_id: str) -> list[str]:
        self._validate_required_params({"group_id": group_id}, ["group_id"])
        self._log_operation("getCollectionGroupChildren", {"id": group_id})
        try:
            r = self.client.getCollectionGroupChildren(id=group_id, **self._build_context_params())
        except Exception as e:
            if "404" in str(e): raise NotFoundError(group_id, "CollectionGroup")
            raise
        return r if isinstance(r, list) else []

    @handle_rest_errors
    def get_collection_group_collections(self, group_id: str) -> list[dict[str, Any]]:
        self._validate_required_params({"group_id": group_id}, ["group_id"])
        self._log_operation("getCollectionGroupCollections", {"id": group_id})
        try:
            r = self.client.getCollectionGroupCollections(id=group_id, **self._build_context_params())
        except Exception as e:
            if "404" in str(e): raise NotFoundError(group_id, "CollectionGroup")
            raise
        return r if isinstance(r, list) else []
