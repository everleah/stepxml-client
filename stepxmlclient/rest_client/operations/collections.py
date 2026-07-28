"""Collection operations for STEP REST API v2."""

import logging
from typing import Any, Optional

from ..base import BaseOperation, handle_rest_errors
from ..exceptions import NotFoundError, ValidationError


class CollectionOperations(BaseOperation):
    """Operations for STEP Collections."""
    def __init__(self, client, logger=None, context=None, workspace=None):
        super().__init__(client, operation_name="CollectionOperations", logger=logger, context=context, workspace=workspace)

    @handle_rest_errors
    def create_collection(self, data: dict[str, Any]) -> dict[str, Any]:
        self._log_operation("createCollection", data)
        try:
            r = self.client.createCollection(json=data, **self._build_context_params())
        except Exception as e:
            if "409" in str(e): raise ValidationError(str(e))
            raise
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def get_collection(self, collection_id: str) -> dict[str, Any]:
        self._validate_required_params({"collection_id": collection_id}, ["collection_id"])
        self._log_operation("getCollection", {"id": collection_id})
        try:
            r = self.client.getCollection(id=collection_id, **self._build_context_params())
        except Exception as e:
            if "404" in str(e): raise NotFoundError(collection_id, "Collection")
            raise
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def create_or_replace_collection(self, collection_id: str, data: dict[str, Any]) -> dict[str, Any]:
        self._validate_required_params({"collection_id": collection_id}, ["collection_id"])
        self._log_operation("createOrReplaceCollection", {"id": collection_id})
        try:
            r = self.client.createOrReplaceCollection(id=collection_id, json=data, **self._build_context_params())
        except Exception as e:
            if "400" in str(e): raise ValidationError(str(e))
            raise
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def delete_collection(self, collection_id: str) -> bool:
        self._validate_required_params({"collection_id": collection_id}, ["collection_id"])
        self._log_operation("deleteCollection", {"id": collection_id})
        try:
            self.client.deleteCollection(id=collection_id, **self._build_context_params())
            return True
        except Exception as e:
            if "404" in str(e): raise NotFoundError(collection_id, "Collection")
            raise

    @handle_rest_errors
    def get_collection_content(self, collection_id: str) -> dict[str, Any]:
        self._validate_required_params({"collection_id": collection_id}, ["collection_id"])
        self._log_operation("getCollectionContent", {"id": collection_id})
        try:
            r = self.client.getCollectionContent(id=collection_id, **self._build_context_params())
        except Exception as e:
            if "404" in str(e): raise NotFoundError(collection_id, "Collection")
            raise
        return r if isinstance(r, dict) else r
