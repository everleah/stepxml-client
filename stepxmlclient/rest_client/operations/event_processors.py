"""Event processor operations for STEP REST API v2."""
import logging
from typing import Any, Optional
from ..base import BaseOperation, handle_rest_errors
from ..exceptions import NotFoundError

class EventProcessorOperations(BaseOperation):
    def __init__(self, client, logger=None, context=None, workspace=None):
        super().__init__(client, operation_name="EventProcessorOperations", logger=logger, context=context, workspace=workspace)

    @handle_rest_errors
    def get_event_processors(self) -> list[dict[str, Any]]:
        self._log_operation("getEventProcessors", {})
        r = self.client.getEventProcessors(**self._build_context_params())
        return r if isinstance(r, list) else []

    @handle_rest_errors
    def get_event_processor(self, ep_id: str) -> dict[str, Any]:
        self._validate_required_params({"ep_id": ep_id}, ["ep_id"])
        self._log_operation("getEventProcessor", {"id": ep_id})
        try:
            r = self.client.getEventProcessor(id=ep_id, **self._build_context_params())
        except Exception as e:
            if "404" in str(e): raise NotFoundError(ep_id, "EventProcessor")
            raise
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def get_event_processor_status(self, ep_id: str) -> dict[str, Any]:
        self._validate_required_params({"ep_id": ep_id}, ["ep_id"])
        self._log_operation("getEventProcessorStatus", {"id": ep_id})
        try:
            r = self.client.getEventProcessorStatus(id=ep_id, **self._build_context_params())
        except Exception as e:
            if "404" in str(e): raise NotFoundError(ep_id, "EventProcessor")
            raise
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def get_event_processor_execution_report(self, ep_id: str) -> list[dict[str, Any]]:
        self._validate_required_params({"ep_id": ep_id}, ["ep_id"])
        self._log_operation("getEventProcessorExecutionReport", {"id": ep_id})
        try:
            r = self.client.getEventProcessorExecutionReport(id=ep_id, **self._build_context_params())
        except Exception as e:
            if "404" in str(e): raise NotFoundError(ep_id, "EventProcessor")
            raise
        return r if isinstance(r, list) else []

    @handle_rest_errors
    def enable_event_processor(self, ep_id: str) -> dict[str, Any]:
        self._validate_required_params({"ep_id": ep_id}, ["ep_id"])
        self._log_operation("enableEventProcessor", {"id": ep_id})
        r = self.client.enableEventProcessor(id=ep_id, **self._build_context_params())
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def disable_event_processor(self, ep_id: str) -> dict[str, Any]:
        self._validate_required_params({"ep_id": ep_id}, ["ep_id"])
        self._log_operation("disableEventProcessor", {"id": ep_id})
        r = self.client.disableEventProcessor(id=ep_id, **self._build_context_params())
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def invoke_event_processor(self, ep_id: str, data: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        self._validate_required_params({"ep_id": ep_id}, ["ep_id"])
        self._log_operation("invokeEventProcessor", {"id": ep_id})
        kwargs = {"id": ep_id, **self._build_context_params()}
        if data: kwargs["json"] = data
        r = self.client.invokeEventProcessor(**kwargs)
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def get_event_queue_status(self, ep_id: str) -> dict[str, Any]:
        self._validate_required_params({"ep_id": ep_id}, ["ep_id"])
        self._log_operation("getEventProcessorEventQueueStatus", {"id": ep_id})
        r = self.client.getEventProcessorEventQueueStatus(id=ep_id, **self._build_context_params())
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def get_event_queue_unread_count(self, ep_id: str) -> dict[str, Any]:
        self._validate_required_params({"ep_id": ep_id}, ["ep_id"])
        self._log_operation("getEventProcessorNumberOfUnreadEventsInEventQueue", {"id": ep_id})
        r = self.client.getEventProcessorNumberOfUnreadEventsInEventQueue(id=ep_id, **self._build_context_params())
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def enable_event_queue(self, ep_id: str) -> dict[str, Any]:
        self._validate_required_params({"ep_id": ep_id}, ["ep_id"])
        self._log_operation("enableEventQueue", {"id": ep_id})
        r = self.client.enableEventQueue(id=ep_id, **self._build_context_params())
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def disable_event_queue(self, ep_id: str) -> dict[str, Any]:
        self._validate_required_params({"ep_id": ep_id}, ["ep_id"])
        self._log_operation("disableEventQueue", {"id": ep_id})
        r = self.client.disableEventQueue(id=ep_id, **self._build_context_params())
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def get_event_processor_statistics(self, ep_id: str) -> dict[str, Any]:
        self._validate_required_params({"ep_id": ep_id}, ["ep_id"])
        self._log_operation("getEventProcessorStatistics", {"id": ep_id})
        r = self.client.getEventProcessorStatistics(id=ep_id, **self._build_context_params())
        return r if isinstance(r, dict) else r
