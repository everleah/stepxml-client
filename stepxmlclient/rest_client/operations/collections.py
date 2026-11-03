"""Collection operations for STEP REST API v2."""

from typing import Any

from ..base import BaseOperation, handle_rest_errors
from ..models.collection import CollectionResponse


class CollectionOperations(BaseOperation):
    """Operations for STEP Collections."""
    def __init__(self, client, logger=None, context=None, workspace=None):
        super().__init__(client, operation_name="CollectionOperations", logger=logger, context=context, workspace=workspace)

    @handle_rest_errors
    def create_collection(self, data: dict[str, Any]) -> CollectionResponse:
        self._log_operation("createCollection", data)
        r = self._call_operation("createCollection", json=data, **self._build_context_params())
        return CollectionResponse(**r) if isinstance(r, dict) else r

    @handle_rest_errors
    def get_collection(self, collection_id: str) -> CollectionResponse:
        self._validate_required_params({"collection_id": collection_id}, ["collection_id"])
        self._log_operation("getCollection", {"id": collection_id})
        r = self._call_operation("getCollection", id=collection_id, **self._build_context_params())
        return CollectionResponse(**r) if isinstance(r, dict) else r

    @handle_rest_errors
    def create_or_replace_collection(self, collection_id: str, data: dict[str, Any]) -> CollectionResponse:
        self._validate_required_params({"collection_id": collection_id}, ["collection_id"])
        self._log_operation("createOrReplaceCollection", {"id": collection_id})
        r = self._call_operation("createOrReplaceCollection", id=collection_id, json=data, **self._build_context_params())
        return CollectionResponse(**r) if isinstance(r, dict) else r

    @handle_rest_errors
    def delete_collection(self, collection_id: str) -> bool:
        self._validate_required_params({"collection_id": collection_id}, ["collection_id"])
        self._log_operation("deleteCollection", {"id": collection_id})
        self._call_operation("deleteCollection", id=collection_id, **self._build_context_params())
        return True

    @handle_rest_errors
    def get_collection_content(self, collection_id: str) -> CollectionResponse:
        self._validate_required_params({"collection_id": collection_id}, ["collection_id"])
        self._log_operation("getCollectionContent", {"id": collection_id})
        r = self._call_operation("getCollectionContent", id=collection_id, **self._build_context_params())
        return CollectionResponse(**r) if isinstance(r, dict) else r
