"""Context operations for STEP REST API v2.

Covers the /contexts endpoints introduced in v1.4.0.
"""

import logging
from typing import Any

from ..base import BaseOperation, handle_rest_errors
from ..exceptions import NotFoundError
from ..models.context import ContextResponse


class ContextOperations(BaseOperation):
    """Operations for STEP Contexts."""

    def __init__(self, client, logger: logging.Logger | None = None,
                 context: str | None = None, workspace: str | None = None):
        super().__init__(client, operation_name="ContextOperations", logger=logger,
                         context=context, workspace=workspace)

    @staticmethod
    def _coerce_context_items(payload: Any) -> list[ContextResponse]:
        """Normalize context list payloads from various response shapes."""
        if payload is None:
            return []

        if isinstance(payload, list):
            return [ContextResponse(**c) if isinstance(c, dict) else c for c in payload]

        if isinstance(payload, dict):
            for key in ("items", "data", "results", "contexts"):
                items = payload.get(key)
                if isinstance(items, list):
                    return [ContextResponse(**c) if isinstance(c, dict) else c for c in items]
            if "id" in payload:
                return [ContextResponse(**payload)]
            return []

        if hasattr(payload, "json"):
            try:
                parsed = payload.json()
            except Exception:  # noqa: BLE001
                parsed = None
            if parsed is not None:
                return ContextOperations._coerce_context_items(parsed)

        if hasattr(payload, "text"):
            try:
                import json
                parsed = json.loads(payload.text)
            except Exception:  # noqa: BLE001
                parsed = None
            if parsed is not None:
                return ContextOperations._coerce_context_items(parsed)

        return []

    @handle_rest_errors
    def get_contexts(self) -> list[ContextResponse]:
        """List all available contexts.

        Calls: GET /contexts -> getContexts

        The spec declares the response as ``type: array`` of Context objects.
        Some STEP servers / requests-openapi versions may wrap the array in a
        dict, and some transports may return a ``requests.Response`` object.
        We handle those shapes as well.
        """
        self._log_operation("getContexts", {})
        response = self.client.getContexts(**self._build_context_params())
        return self._coerce_context_items(response)

    @handle_rest_errors
    def get_context(self, context_id: str) -> ContextResponse:
        """Get a specific context by ID.

        Calls: GET /contexts/{id} -> getContext
        """
        self._validate_required_params({"context_id": context_id}, ["context_id"])
        self._log_operation("getContext", {"id": context_id})
        try:
            response = self.client.getContext(id=context_id, **self._build_context_params())
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(context_id, "Context")
            raise
        return ContextResponse(**response) if isinstance(response, dict) else response
