"""Batch operations for STEP REST API v2."""

from typing import Any

from ..base import BaseOperation, handle_rest_errors
from ..models.batch import BatchResponse


class BatchOperations(BaseOperation):
    """Operations for STEP Batch execution."""
    def __init__(self, client, logger=None, context=None, workspace=None):
        super().__init__(client, operation_name="BatchOperations", logger=logger, context=context, workspace=workspace)

    @handle_rest_errors
    def execute_batch_operation(self, data: dict[str, Any]) -> BatchResponse:
        """Execute a batch of operations.

        Calls: POST /batch/execute -> executeBatchOperation
        """
        self._validate_required_params({"data": data}, ["data"])
        self._log_operation("executeBatchOperation", {})
        r = self._call_operation("executeBatchOperation", json=data, **self._build_context_params())
        return BatchResponse(**r) if isinstance(r, dict) else r
