"""Gateway integration endpoint operations for STEP REST API v2."""
import logging
from typing import Any, Optional
from ..base import BaseOperation, handle_rest_errors
from ..exceptions import NotFoundError

class GatewayOperations(BaseOperation):
    def __init__(self, client, logger=None, context=None, workspace=None):
        super().__init__(client, operation_name="GatewayOperations", logger=logger, context=context, workspace=workspace)

    @handle_rest_errors
    def get_gateway_endpoints(self) -> list[dict[str, Any]]:
        self._log_operation("getGatewayIntegrationEndpoints", {})
        r = self.client.getGatewayIntegrationEndpoints(**self._build_context_params())
        return r if isinstance(r, list) else []

    @handle_rest_errors
    def get_gateway_endpoint(self, ep_id: str) -> dict[str, Any]:
        self._validate_required_params({"ep_id": ep_id}, ["ep_id"])
        self._log_operation("getGatewayIntegrationEndpoint", {"id": ep_id})
        try:
            r = self.client.getGatewayIntegrationEndpoint(id=ep_id, **self._build_context_params())
        except Exception as e:
            if "404" in str(e): raise NotFoundError(ep_id, "GatewayIntegrationEndpoint")
            raise
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def get_gateway_endpoint_status(self, ep_id: str) -> dict[str, Any]:
        self._validate_required_params({"ep_id": ep_id}, ["ep_id"])
        self._log_operation("getGatewayIntegrationEndpointStatus", {"id": ep_id})
        try:
            r = self.client.getGatewayIntegrationEndpointStatus(id=ep_id, **self._build_context_params())
        except Exception as e:
            if "404" in str(e): raise NotFoundError(ep_id, "GatewayIntegrationEndpoint")
            raise
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def enable_gateway_endpoint(self, ep_id: str) -> dict[str, Any]:
        self._validate_required_params({"ep_id": ep_id}, ["ep_id"])
        self._log_operation("enableGatewayIntegrationEndpoint", {"id": ep_id})
        r = self.client.enableGatewayIntegrationEndpoint(id=ep_id, **self._build_context_params())
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def disable_gateway_endpoint(self, ep_id: str) -> dict[str, Any]:
        self._validate_required_params({"ep_id": ep_id}, ["ep_id"])
        self._log_operation("disableGatewayIntegrationEndpoint", {"id": ep_id})
        r = self.client.disableGatewayIntegrationEndpoint(id=ep_id, **self._build_context_params())
        return r if isinstance(r, dict) else r
