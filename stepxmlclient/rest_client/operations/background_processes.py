"""Background process operations for STEP REST API v2."""

from typing import Any, Optional
from urllib.parse import quote

import requests

from ..base import BaseOperation, handle_rest_errors
from ..exceptions import NotFoundError, RestClientError
from ..models.background_process import BackgroundProcessResponse


class BackgroundProcessOperations(BaseOperation):
    def __init__(self, client, logger=None, context=None, workspace=None):
        super().__init__(client, operation_name="BackgroundProcessOperations", logger=logger, context=context, workspace=workspace)

    def _json_payload(self, response: Any) -> Any:
        if isinstance(response, requests.Response):
            try:
                response.raise_for_status()
                payload = response.json()
            finally:
                response.close()
        else:
            payload = response
        self._check_for_api_error(payload)
        return payload

    @handle_rest_errors
    def get_background_process(self, process_id: str, *,
                               timeout: Optional[float] = None) -> BackgroundProcessResponse:
        self._validate_required_params({"process_id": process_id}, ["process_id"])
        self._log_operation("getBackgroundProcess", {"id": process_id})
        try:
            params = self._build_context_params()
            if timeout is not None:
                params["_timeout"] = timeout
            r = self._call_operation("getBackgroundProcess", id=quote(process_id, safe=""), **params)
        except RestClientError:
            raise
        except Exception as e:
            if "404" in str(e): raise NotFoundError(process_id, "BackgroundProcess")
            raise
        r = self._json_payload(r)
        if isinstance(r, BackgroundProcessResponse):
            return r
        if not isinstance(r, dict):
            raise RestClientError("Background process response must be an object")
        return BackgroundProcessResponse.model_validate(r)

    @handle_rest_errors
    def get_execution_report(self, process_id: str) -> list[dict[str, Any]]:
        self._validate_required_params({"process_id": process_id}, ["process_id"])
        self._log_operation("getBackgroundProcessExecutionReport", {"id": process_id})
        try:
            r = self._call_operation("getBackgroundProcessExecutionReport", id=process_id, **self._build_context_params())
        except RestClientError:
            raise
        except Exception as e:
            if "404" in str(e): raise NotFoundError(process_id, "BackgroundProcess")
            raise
        return r if isinstance(r, list) else []

    @handle_rest_errors
    def get_attachments_metadata(self, process_id: str, *,
                                 timeout: Optional[float] = None) -> list[dict[str, Any]]:
        self._validate_required_params({"process_id": process_id}, ["process_id"])
        self._log_operation("getBackgroundProcessAttachmentsMetadata", {"id": process_id})
        try:
            params = self._build_context_params()
            if timeout is not None:
                params["_timeout"] = timeout
            r = self._call_operation("getBackgroundProcessAttachmentsMetadata",
                id=quote(process_id, safe=""), **params)
        except RestClientError:
            raise
        except Exception as e:
            if "404" in str(e): raise NotFoundError(process_id, "BackgroundProcess")
            raise
        r = self._json_payload(r)
        if not isinstance(r, list) or not all(isinstance(item, dict) for item in r):
            raise RestClientError("Background process attachments response must be an array of objects")
        return r

    @handle_rest_errors
    def get_attachment_metadata(self, process_id: str, attachment_id: str) -> BackgroundProcessResponse:
        self._validate_required_params({"process_id": process_id, "attachment_id": attachment_id}, ["process_id", "attachment_id"])
        self._log_operation("getBackgroundProcessAttachmentMetadata", {"id": process_id, "attachmentId": attachment_id})
        try:
            r = self._call_operation("getBackgroundProcessAttachmentMetadata", id=process_id, attachmentId=attachment_id, **self._build_context_params())
        except RestClientError:
            raise
        except Exception as e:
            if "404" in str(e): raise NotFoundError(process_id, "BackgroundProcess")
            raise
        return BackgroundProcessResponse(**r) if isinstance(r, dict) else r

    @handle_rest_errors
    def get_attachment_content(self, process_id: str, attachment_id: str, *,
                               timeout: Optional[float] = None) -> bytes:
        self._validate_required_params({"process_id": process_id, "attachment_id": attachment_id}, ["process_id", "attachment_id"])
        self._log_operation("getBackgroundProcessAttachmentContent", {"id": process_id, "attachmentId": attachment_id})
        try:
            params = self._build_context_params()
            if timeout is not None:
                params["_timeout"] = timeout
            r = self._call_operation("getBackgroundProcessAttachmentContent", _raw_response=True,
                id=quote(process_id, safe=""),
                attachmentId=quote(attachment_id, safe=""), **params)
        except RestClientError:
            raise
        except Exception as e:
            if "404" in str(e): raise NotFoundError(process_id, "BackgroundProcess")
            raise
        if isinstance(r, requests.Response):
            try:
                r.raise_for_status()
                return r.content
            finally:
                r.close()
        self._check_for_api_error(r, process_id, "BackgroundProcess")
        if not isinstance(r, bytes):
            raise RestClientError("Background process attachment response must contain bytes")
        return r

    @handle_rest_errors
    def get_process_types(self) -> list[dict[str, Any]]:
        self._log_operation("getBackgroundProcessTypes", {})
        r = self._call_operation("getBackgroundProcessTypes", **self._build_context_params())
        return r if isinstance(r, list) else []

    @handle_rest_errors
    def get_processes_of_type(self, type_id: str) -> list[dict[str, Any]]:
        self._validate_required_params({"type_id": type_id}, ["type_id"])
        self._log_operation("getBackgroundProcessesOfType", {"typeId": type_id})
        try:
            r = self._call_operation("getBackgroundProcessesOfType", typeId=type_id, **self._build_context_params())
        except RestClientError:
            raise
        except Exception as e:
            if "404" in str(e): raise NotFoundError(type_id, "BackgroundProcessType")
            raise
        return r if isinstance(r, list) else []
