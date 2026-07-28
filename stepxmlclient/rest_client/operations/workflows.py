"""Workflow operations for STEP REST API v2."""
import logging
from typing import Any, Optional
from ..base import BaseOperation, handle_rest_errors
from ..exceptions import NotFoundError, ValidationError
from ..models.workflow import WorkflowResponse

class WorkflowOperations(BaseOperation):
    def __init__(self, client, logger=None, context=None, workspace=None):
        super().__init__(client, operation_name="WorkflowOperations", logger=logger, context=context, workspace=workspace)

    @handle_rest_errors
    def get_workflow_ids(self) -> list[str]:
        self._log_operation("getWorkflowIds", {})
        r = self.client.getWorkflowIds(**self._build_context_params())
        return r if isinstance(r, list) else []

    @handle_rest_errors
    def get_workflow(self, workflow_id: str) -> WorkflowResponse:
        self._validate_required_params({"workflow_id": workflow_id}, ["workflow_id"])
        self._log_operation("getWorkflow", {"id": workflow_id})
        try:
            r = self.client.getWorkflow(id=workflow_id, **self._build_context_params())
        except Exception as e:
            if "404" in str(e): raise NotFoundError(workflow_id, "Workflow")
            raise
        return WorkflowResponse(**r) if isinstance(r, dict) else r

    @handle_rest_errors
    def create_workflow_instance(self, workflow_id: str, data: dict[str, Any]) -> WorkflowResponse:
        self._validate_required_params({"workflow_id": workflow_id}, ["workflow_id"])
        self._log_operation("createWorkflowInstance", {"id": workflow_id})
        try:
            r = self.client.createWorkflowInstance(id=workflow_id, json=data, **self._build_context_params())
        except Exception as e:
            if "400" in str(e): raise ValidationError(str(e))
            raise
        return WorkflowResponse(**r) if isinstance(r, dict) else r

    @handle_rest_errors
    def delete_workflow_instance(self, workflow_id: str, instance_id: str) -> bool:
        self._validate_required_params({"workflow_id": workflow_id, "instance_id": instance_id}, ["workflow_id", "instance_id"])
        self._log_operation("deleteWorkflowInstance", {"id": workflow_id, "instanceId": instance_id})
        try:
            self.client.deleteWorkflowInstance(id=workflow_id, instanceId=instance_id, **self._build_context_params())
            return True
        except Exception as e:
            if "404" in str(e): raise NotFoundError(workflow_id, "Workflow")
            raise
