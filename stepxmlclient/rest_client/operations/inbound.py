"""Inbound Integration Endpoint operations for STEP REST API v2.

Provides high-level operations for uploading STEP-XML to Inbound Integration Endpoints
and managing their status, including enabling/disabling endpoints and retrieving execution reports.
"""

import logging
from typing import Any, Optional, Union

from ..base import BaseOperation, handle_rest_errors
from ..exceptions import NotFoundError, RestApiError, ValidationError


class InboundOperations(BaseOperation):
    """Operations for STEP Inbound Integration Endpoints (IIEP).
    
    Handles uploading STEP-XML documents to configured inbound endpoints
    and managing endpoint status and execution reports.
    
    Example:
        ```python
        from stepxmlclient.rest_client.client import StepRestClient
        from stepxmlclient.creator import Creator
        
        # Create and setup client
        client = StepRestClient(
            location_base="https://your-step.com/restapiv2",
            authorisation=auth,
            context="Context1"
        )
        
        # Generate STEP-XML
        creator = Creator(context_id="Context1")
        # ... add products, assets, etc ...
        creator.build()
        xml_bytes = creator.to_bytes()
        
        # Send to inbound endpoint
        result = client.inbound.upload_and_invoke(
            endpoint_id="my_inbound_endpoint",
            xml_data=xml_bytes,
            file_name="import_data.xml"
        )
        
        print(f"Uploaded {result.get('processId')} to endpoint")
        ```
    """
    
    def __init__(self, client, logger: Optional[logging.Logger] = None,
                 context: Optional[str] = None, workspace: Optional[str] = None):
        """Initialize inbound operations.
        
        Args:
            client: The REST API client
            logger: Optional logger instance
            context: STEP context ID for all API calls (required)
            workspace: STEP workspace ID (defaults to "Main" server-side)
        """
        super().__init__(client, operation_name="InboundOperations", logger=logger,
                         context=context, workspace=workspace)

    @handle_rest_errors
    def upload_and_invoke(self, endpoint_id: str, xml_data: Union[bytes, str],
                          file_name: Optional[str] = None) -> dict[str, Any]:
        """Upload STEP-XML to an inbound endpoint and trigger processing.
        
        Posts STEP-XML content to a configured Inbound Integration Endpoint
        with a REST receiver plugin. The endpoint is immediately invoked
        to process the uploaded data.
        
        Args:
            endpoint_id: ID of the inbound integration endpoint (required)
            xml_data: STEP-XML content as bytes or string
            file_name: Optional filename hint for the upload (e.g., "import_data.xml")
            
        Returns:
            Dictionary with response details (typically includes processId or similar)
            
        Raises:
            ValidationError: If endpoint_id is missing or endpoint not enabled
            NotFoundError: If endpoint cannot be found
            RestApiError: For other API errors
            
        Note:
            - Endpoint must have status "enabled" to invoke
            - Endpoint must have a REST-enabled receiver plugin configured
            - The endpoint will begin processing immediately
        """
        self._validate_required_params(
            {"endpoint_id": endpoint_id, "xml_data": xml_data},
            ["endpoint_id", "xml_data"]
        )

        # Convert string to bytes if needed
        if isinstance(xml_data, str):
            xml_data = xml_data.encode('utf-8')

        # Prepare query parameters (context and workspace, plus optional fileName)
        params: dict[str, Any] = {}
        if file_name:
            params["fileName"] = file_name
        params.update(self._build_context_params())

        self._log_operation("postInboundIntegrationEndpointUploadAndInvoke", {
            "endpointId": endpoint_id,
            "fileSize": len(xml_data),
            "fileName": file_name or "(not specified)"
        })

        try:
            # Use requests_openapi client method which handles path parameter substitution
            # The 'id' parameter is a path parameter and is passed separately from query params
            response = self.client.postInboundIntegrationEndpointUploadAndInvoke(
                id=endpoint_id,
                data=xml_data,
                **params
            )
            
            # Handle the response
            # Return response (requests_openapi handles JSON parsing automatically)
            if isinstance(response, dict):
                return response
            return {"success": True, "endpoint": endpoint_id}
                
        except Exception as e:
            error_str = str(e)
            if "404" in error_str:
                raise NotFoundError(endpoint_id, "InboundIntegrationEndpoint")
            elif "400" in error_str:
                if "not enabled" in error_str.lower() or "disabled" in error_str.lower():
                    raise ValidationError(
                        f"Inbound endpoint '{endpoint_id}' is not enabled. "
                        f"Enable it first using enable_endpoint()."
                    )
                elif "REST receiver" in error_str:
                    raise ValidationError(
                        f"Inbound endpoint '{endpoint_id}' does not have a REST-enabled receiver plugin. "
                        f"Configure a REST receiver in the endpoint settings."
                    )
                raise ValidationError(f"Upload failed: {error_str}")
            elif "503" in error_str:
                raise RestApiError(503, "Endpoint temporarily unavailable", details=error_str)
            raise


    @handle_rest_errors
    def list_endpoints(self) -> list[dict[str, Any]]:
        """Get all accessible inbound integration endpoints.
        
        Returns:
            List of inbound endpoint representations with ID, name, and status info
            
        Raises:
            RestApiError: For API errors
        """
        params = self._build_context_params()

        self._log_operation("getInboundIntegrationEndpoints", {})

        try:
            response = self.client.getInboundIntegrationEndpoints(**params)
        except Exception as e:
            raise RestApiError(0, f"Failed to list inbound endpoints: {str(e)}", details=str(e))

        # Convert response to list
        if isinstance(response, list):
            return response
        elif isinstance(response, dict):
            # Handle paginated response
            return response.get('results') or response.get('items') or []
        else:
            return []

    @handle_rest_errors
    def get_status(self, endpoint_id: str) -> dict[str, Any]:
        """Get the current status of an inbound endpoint.
        
        Args:
            endpoint_id: ID of the inbound integration endpoint
            
        Returns:
            Dictionary with status information (status, enabled state, etc.)
            
        Raises:
            ValidationError: If endpoint_id is missing
            NotFoundError: If endpoint cannot be found
            RestApiError: For API errors
        """
        self._validate_required_params(
            {"endpoint_id": endpoint_id},
            ["endpoint_id"]
        )

        self._log_operation("getInboundIntegrationEndpointStatus", {
            "endpointId": endpoint_id
        })

        try:
            response = self.client.getInboundIntegrationEndpointStatus(
                id=endpoint_id,
                **self._build_context_params()
            )
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(endpoint_id, "InboundIntegrationEndpoint")
            raise

        self._check_for_api_error(response, endpoint_id, "InboundIntegrationEndpoint")

        if isinstance(response, dict):
            return response
        return {"endpoint": endpoint_id}

    @handle_rest_errors
    def enable_endpoint(self, endpoint_id: str) -> dict[str, Any]:
        """Enable an inbound integration endpoint.
        
        Enables the endpoint so it can receive and process uploads.
        If endpoint has status "failed", this will resume it.
        
        Args:
            endpoint_id: ID of the inbound integration endpoint
            
        Returns:
            Response from the enable operation
            
        Raises:
            ValidationError: If endpoint_id is missing
            NotFoundError: If endpoint cannot be found
            RestApiError: For API errors
        """
        self._validate_required_params(
            {"endpoint_id": endpoint_id},
            ["endpoint_id"]
        )

        self._log_operation("postInboundIntegrationEndpointEnable", {
            "endpointId": endpoint_id
        })

        try:
            response = self.client.postInboundIntegrationEndpointEnable(
                id=endpoint_id,
                **self._build_context_params()
            )
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(endpoint_id, "InboundIntegrationEndpoint")
            raise

        self._check_for_api_error(response, endpoint_id, "InboundIntegrationEndpoint")

        if isinstance(response, dict):
            return response
        return {"success": True, "endpoint": endpoint_id, "action": "enabled"}

    @handle_rest_errors
    def disable_endpoint(self, endpoint_id: str) -> dict[str, Any]:
        """Disable an inbound integration endpoint.
        
        Disables the endpoint so it will not accept uploads or process data.
        Can be called regardless of the endpoint's current status.
        
        Args:
            endpoint_id: ID of the inbound integration endpoint
            
        Returns:
            Response from the disable operation
            
        Raises:
            ValidationError: If endpoint_id is missing
            NotFoundError: If endpoint cannot be found
            RestApiError: For API errors
        """
        self._validate_required_params(
            {"endpoint_id": endpoint_id},
            ["endpoint_id"]
        )

        self._log_operation("postInboundIntegrationEndpointDisable", {
            "endpointId": endpoint_id
        })

        try:
            response = self.client.postInboundIntegrationEndpointDisable(
                id=endpoint_id,
                **self._build_context_params()
            )
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(endpoint_id, "InboundIntegrationEndpoint")
            raise

        self._check_for_api_error(response, endpoint_id, "InboundIntegrationEndpoint")

        if isinstance(response, dict):
            return response
        return {"success": True, "endpoint": endpoint_id, "action": "disabled"}

    @handle_rest_errors
    def get_execution_report(self, endpoint_id: str) -> list[dict[str, Any]]:
        """Get the execution report for an inbound endpoint's main process.
        
        Returns detailed information about the last execution or current state.
        
        Args:
            endpoint_id: ID of the inbound integration endpoint
            
        Returns:
            List of execution report entries with details about operations performed
            
        Raises:
            ValidationError: If endpoint_id is missing
            NotFoundError: If endpoint cannot be found
            RestApiError: For API errors
        """
        self._validate_required_params(
            {"endpoint_id": endpoint_id},
            ["endpoint_id"]
        )

        self._log_operation("getInboundIntegrationEndpointExecutionReport", {
            "endpointId": endpoint_id
        })

        try:
            response = self.client.getInboundIntegrationEndpointExecutionReport(
                id=endpoint_id,
                **self._build_context_params()
            )
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(endpoint_id, "InboundIntegrationEndpoint")
            raise

        self._check_for_api_error(response, endpoint_id, "InboundIntegrationEndpoint")

        if isinstance(response, list):
            return response
        elif isinstance(response, dict):
            return response.get('results') or response.get('items') or [response]
        return []

    @handle_rest_errors
    def get_statistics(self, endpoint_id: str) -> dict[str, Any]:
        """Get statistics for an inbound integration endpoint.
        
        Returns operational statistics and metrics about the endpoint.
        
        Args:
            endpoint_id: ID of the inbound integration endpoint
            
        Returns:
            Dictionary with statistics (message counts, error counts, etc.)
            
        Raises:
            ValidationError: If endpoint_id is missing
            NotFoundError: If endpoint cannot be found
            RestApiError: For API errors
        """
        self._validate_required_params(
            {"endpoint_id": endpoint_id},
            ["endpoint_id"]
        )

        self._log_operation("getInboundIntegrationEndpointStatistics", {
            "endpointId": endpoint_id
        })

        try:
            response = self.client.getInboundIntegrationEndpointStatistics(
                id=endpoint_id,
                **self._build_context_params()
            )
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(endpoint_id, "InboundIntegrationEndpoint")
            raise

        self._check_for_api_error(response, endpoint_id, "InboundIntegrationEndpoint")

        if isinstance(response, dict):
            return response
        return {}

    @handle_rest_errors
    def get_worker_processes(self, endpoint_id: str,
                             status_filter: Optional[str] = None) -> list[str]:
        """Get background process IDs started by this endpoint.
        
        Args:
            endpoint_id: ID of the inbound integration endpoint
            status_filter: Optional filter by process status (PENDING, PROCESSING, COMPLETED, FAILED)
            
        Returns:
            List of background process IDs
            
        Raises:
            ValidationError: If endpoint_id is missing
            NotFoundError: If endpoint cannot be found
            RestApiError: For API errors
        """
        self._validate_required_params(
            {"endpoint_id": endpoint_id},
            ["endpoint_id"]
        )

        params: dict[str, Any] = self._build_context_params()
        if status_filter:
            params["status"] = status_filter

        self._log_operation("getInboundIntegrationEndpointWorkerProcesses", {
            "endpointId": endpoint_id,
            "statusFilter": status_filter
        })

        try:
            response = self.client.getInboundIntegrationEndpointWorkerProcesses(
                id=endpoint_id,
                **params
            )
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(endpoint_id, "InboundIntegrationEndpoint")
            raise

        self._check_for_api_error(response, endpoint_id, "InboundIntegrationEndpoint")

        if isinstance(response, list):
            return response
        elif isinstance(response, dict):
            return response.get('results') or response.get('items') or []
        return []
