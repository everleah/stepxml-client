"""Outbound integration endpoint operations for STEP REST API v2."""
import logging
from typing import Any, Optional
from ..base import BaseOperation, handle_rest_errors
from ..exceptions import NotFoundError
from ..models.integration_endpoint import IntegrationEndpointResponse

class OutboundOperations(BaseOperation):
    def __init__(self, client, logger=None, context=None, workspace=None):
        super().__init__(client, operation_name="OutboundOperations", logger=logger, context=context, workspace=workspace)

    @handle_rest_errors
    def get_outbound_endpoints(self) -> list[dict[str, Any]]:
        self._log_operation("getOutboundIntegrationEndpoints", {})
        r = self.client.getOutboundIntegrationEndpoints(**self._build_context_params())
        return r if isinstance(r, list) else []

    @handle_rest_errors
    def get_outbound_endpoint(self, ep_id: str) -> IntegrationEndpointResponse:
        self._validate_required_params({"ep_id": ep_id}, ["ep_id"])
        self._log_operation("getOutboundIntegrationEndpoint", {"id": ep_id})
        try:
            r = self.client.getOutboundIntegrationEndpoint(id=ep_id, **self._build_context_params())
        except Exception as e:
            if "404" in str(e): raise NotFoundError(ep_id, "OutboundIntegrationEndpoint")
            raise
        return IntegrationEndpointResponse(**r) if isinstance(r, dict) else r

    @handle_rest_errors
    def get_outbound_endpoint_status(self, ep_id: str) -> IntegrationEndpointResponse:
        self._validate_required_params({"ep_id": ep_id}, ["ep_id"])
        self._log_operation("getOutboundIntegrationEndpointStatus", {"id": ep_id})
        try:
            r = self.client.getOutboundIntegrationEndpointStatus(id=ep_id, **self._build_context_params())
        except Exception as e:
            if "404" in str(e): raise NotFoundError(ep_id, "OutboundIntegrationEndpoint")
            raise
        return IntegrationEndpointResponse(**r) if isinstance(r, dict) else r

    @handle_rest_errors
    def enable_outbound_endpoint(self, ep_id: str) -> IntegrationEndpointResponse:
        self._validate_required_params({"ep_id": ep_id}, ["ep_id"])
        self._log_operation("enableOutboundIntegrationEndpoint", {"id": ep_id})
        r = self.client.enableOutboundIntegrationEndpoint(id=ep_id, **self._build_context_params())
        return IntegrationEndpointResponse(**r) if isinstance(r, dict) else r

    @handle_rest_errors
    def disable_outbound_endpoint(self, ep_id: str) -> IntegrationEndpointResponse:
        self._validate_required_params({"ep_id": ep_id}, ["ep_id"])
        self._log_operation("disableOutboundIntegrationEndpoint", {"id": ep_id})
        r = self.client.disableOutboundIntegrationEndpoint(id=ep_id, **self._build_context_params())
        return IntegrationEndpointResponse(**r) if isinstance(r, dict) else r

    @handle_rest_errors
    def get_outbound_endpoint_execution_report(self, ep_id: str) -> list[dict[str, Any]]:
        self._validate_required_params({"ep_id": ep_id}, ["ep_id"])
        self._log_operation("getOutboundIntegrationEndpointExecutionReport", {"id": ep_id})
        try:
            r = self.client.getOutboundIntegrationEndpointExecutionReport(id=ep_id, **self._build_context_params())
        except Exception as e:
            if "404" in str(e): raise NotFoundError(ep_id, "OutboundIntegrationEndpoint")
            raise
        return r if isinstance(r, list) else []
