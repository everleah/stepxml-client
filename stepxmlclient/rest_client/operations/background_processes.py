"""Background process operations for STEP REST API v2."""
import logging
from typing import Any, Optional
from ..base import BaseOperation, handle_rest_errors
from ..exceptions import NotFoundError
from ..models.background_process import BackgroundProcessResponse

class BackgroundProcessOperations(BaseOperation):
    def __init__(self, client, logger=None, context=None, workspace=None):
        super().__init__(client, operation_name="BackgroundProcessOperations", logger=logger, context=context, workspace=workspace)

    @handle_rest_errors
    def get_background_process(self, process_id: str) -> BackgroundProcessResponse:
        self._validate_required_params({"process_id": process_id}, ["process_id"])
        self._log_operation("getBackgroundProcess", {"id": process_id})
        try:
            r = self.client.getBackgroundProcess(id=process_id, **self._build_context_params())
        except Exception as e:
            if "404" in str(e): raise NotFoundError(process_id, "BackgroundProcess")
            raise
        return BackgroundProcessResponse(**r) if isinstance(r, dict) else r

    @handle_rest_errors
    def get_execution_report(self, process_id: str) -> list[dict[str, Any]]:
        self._validate_required_params({"process_id": process_id}, ["process_id"])
        self._log_operation("getBackgroundProcessExecutionReport", {"id": process_id})
        try:
            r = self.client.getBackgroundProcessExecutionReport(id=process_id, **self._build_context_params())
        except Exception as e:
            if "404" in str(e): raise NotFoundError(process_id, "BackgroundProcess")
            raise
        return r if isinstance(r, list) else []

    @handle_rest_errors
    def get_attachments_metadata(self, process_id: str) -> list[dict[str, Any]]:
        self._validate_required_params({"process_id": process_id}, ["process_id"])
        self._log_operation("getBackgroundProcessAttachmentsMetadata", {"id": process_id})
        try:
            r = self.client.getBackgroundProcessAttachmentsMetadata(id=process_id, **self._build_context_params())
        except Exception as e:
            if "404" in str(e): raise NotFoundError(process_id, "BackgroundProcess")
            raise
        return r if isinstance(r, list) else []

    @handle_rest_errors
    def get_attachment_metadata(self, process_id: str, attachment_id: str) -> BackgroundProcessResponse:
        self._validate_required_params({"process_id": process_id, "attachment_id": attachment_id}, ["process_id", "attachment_id"])
        self._log_operation("getBackgroundProcessAttachmentMetadata", {"id": process_id, "attachmentId": attachment_id})
        try:
            r = self.client.getBackgroundProcessAttachmentMetadata(id=process_id, attachmentId=attachment_id, **self._build_context_params())
        except Exception as e:
            if "404" in str(e): raise NotFoundError(process_id, "BackgroundProcess")
            raise
        return BackgroundProcessResponse(**r) if isinstance(r, dict) else r

    @handle_rest_errors
    def get_attachment_content(self, process_id: str, attachment_id: str) -> bytes:
        self._validate_required_params({"process_id": process_id, "attachment_id": attachment_id}, ["process_id", "attachment_id"])
        self._log_operation("getBackgroundProcessAttachmentContent", {"id": process_id, "attachmentId": attachment_id})
        try:
            r = self.client.getBackgroundProcessAttachmentContent(id=process_id, attachmentId=attachment_id, **self._build_context_params())
        except Exception as e:
            if "404" in str(e): raise NotFoundError(process_id, "BackgroundProcess")
            raise
        return r

    @handle_rest_errors
    def get_process_types(self) -> list[dict[str, Any]]:
        self._log_operation("getBackgroundProcessTypes", {})
        r = self.client.getBackgroundProcessTypes(**self._build_context_params())
        return r if isinstance(r, list) else []

    @handle_rest_errors
    def get_processes_of_type(self, type_id: str) -> list[dict[str, Any]]:
        self._validate_required_params({"type_id": type_id}, ["type_id"])
        self._log_operation("getBackgroundProcessesOfType", {"typeId": type_id})
        try:
            r = self.client.getBackgroundProcessesOfType(typeId=type_id, **self._build_context_params())
        except Exception as e:
            if "404" in str(e): raise NotFoundError(type_id, "BackgroundProcessType")
            raise
        return r if isinstance(r, list) else []
