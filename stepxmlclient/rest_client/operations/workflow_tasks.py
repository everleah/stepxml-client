"""Workflow task operations for STEP REST API v2."""
import logging
from typing import Any, Optional
from ..base import BaseOperation, handle_rest_errors
from ..exceptions import NotFoundError, ValidationError

class WorkflowTaskOperations(BaseOperation):
    def __init__(self, client, logger=None, context=None, workspace=None):
        super().__init__(client, operation_name="WorkflowTaskOperations", logger=logger, context=context, workspace=workspace)

    @handle_rest_errors
    def search_workflow_tasks(self, condition: dict[str, Any]) -> dict[str, Any]:
        self._validate_required_params({"condition": condition}, ["condition"])
        self._log_operation("searchWorkflowTasks", {})
        r = self.client.searchWorkflowTasks(json={"condition": condition}, **self._build_context_params())
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def get_workflow_task(self, task_id: str) -> dict[str, Any]:
        self._validate_required_params({"task_id": task_id}, ["task_id"])
        self._log_operation("getWorkflowTask", {"id": task_id})
        try:
            r = self.client.getWorkflowTask(id=task_id, **self._build_context_params())
        except Exception as e:
            if "404" in str(e): raise NotFoundError(task_id, "WorkflowTask")
            raise
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def claim_workflow_task(self, task_id: str) -> dict[str, Any]:
        self._validate_required_params({"task_id": task_id}, ["task_id"])
        self._log_operation("claimWorkflowTask", {"id": task_id})
        r = self.client.claimWorkflowTask(id=task_id, **self._build_context_params())
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def get_workflow_task_events(self, task_id: str) -> list[dict[str, Any]]:
        self._validate_required_params({"task_id": task_id}, ["task_id"])
        self._log_operation("getWorkflowTaskEvents", {"id": task_id})
        try:
            r = self.client.getWorkflowTaskEvents(id=task_id, **self._build_context_params())
        except Exception as e:
            if "404" in str(e): raise NotFoundError(task_id, "WorkflowTask")
            raise
        return r if isinstance(r, list) else []

    @handle_rest_errors
    def trigger_workflow_task_event(self, task_id: str, data: dict[str, Any]) -> dict[str, Any]:
        self._validate_required_params({"task_id": task_id}, ["task_id"])
        self._log_operation("triggerWorkflowTaskEvent", {"id": task_id})
        r = self.client.triggerWorkflowTaskEvent(id=task_id, json=data, **self._build_context_params())
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def release_workflow_task(self, task_id: str) -> dict[str, Any]:
        self._validate_required_params({"task_id": task_id}, ["task_id"])
        self._log_operation("releaseWorkflowTask", {"id": task_id})
        r = self.client.releaseWorkflowTask(id=task_id, **self._build_context_params())
        return r if isinstance(r, dict) else r
