"""Context operations for STEP REST API v2.

Covers the /contexts endpoints introduced in v1.4.0.
"""

import logging
from typing import Any, Optional

from ..base import BaseOperation, handle_rest_errors
from ..exceptions import NotFoundError


class ContextOperations(BaseOperation):
    """Operations for STEP Contexts."""

    def __init__(self, client, logger: Optional[logging.Logger] = None,
                 context: Optional[str] = None, workspace: Optional[str] = None):
        super().__init__(client, operation_name="ContextOperations", logger=logger,
                         context=context, workspace=workspace)

    @handle_rest_errors
    def get_contexts(self) -> list[dict[str, Any]]:
        """List all available contexts.

        Calls: GET /contexts -> getContexts
        """
        self._log_operation("getContexts", {})
        response = self.client.getContexts(**self._build_context_params())
        if isinstance(response, list):
            return response
        if isinstance(response, dict):
            return response.get("items", [])
        return []

    @handle_rest_errors
    def get_context(self, context_id: str) -> dict[str, Any]:
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
        return response if isinstance(response, dict) else response
