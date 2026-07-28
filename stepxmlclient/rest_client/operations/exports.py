"""Export and Import operations for STEP REST API v2."""

import logging
from typing import Any, Optional

from ..base import BaseOperation, handle_rest_errors
from ..exceptions import NotFoundError, ValidationError
from ..models.import_export import (
    BackgroundProcessResponse,
    ExportJobCreateRequest,
)


class ExportOperations(BaseOperation):
    """Operations for STEP data exports and imports."""

    def __init__(self, client, logger: Optional[logging.Logger] = None,
                 context: Optional[str] = None, workspace: Optional[str] = None):
        """Initialize export operations.

        Args:
            client: The REST API client
            logger: Optional logger instance
            context: STEP context ID for all API calls
            workspace: STEP workspace ID (defaults to "Main" server-side)
        """
        super().__init__(client, operation_name="ExportOperations", logger=logger,
                         context=context, workspace=workspace)

    @handle_rest_errors
    def create_export_job(self, export_configuration_id: str,
                          data: Optional[ExportJobCreateRequest] = None,
                          use_request_context_workspace: Optional[bool] = None) -> BackgroundProcessResponse:
        """Trigger an export using a pre-configured export configuration (POST /export/{exportConfigurationId}).

        Args:
            export_configuration_id: The ID of the export configuration to use (required)
            data: Optional request body with additional export parameters
            use_request_context_workspace: If True, use the workspace from the request context

        Returns:
            ExportJobResponse with job details

        Raises:
            ValidationError: If export_configuration_id is missing or data is invalid
            RestApiError: For API errors
        """
        self._validate_required_params(
            {"export_configuration_id": export_configuration_id},
            ["export_configuration_id"]
        )

        if data is not None:
            if hasattr(data, 'model_dump'):
                create_data = data.model_dump(exclude_none=True)
            else:
                create_data = dict(data) if not isinstance(data, dict) else data
        else:
            create_data = None

        query_params: dict = self._build_context_params()
        if use_request_context_workspace is not None:
            query_params["useRequestContextWorkspace"] = use_request_context_workspace

        self._log_operation("startExport", {"exportConfigurationId": export_configuration_id})

        try:
            if create_data:
                response = self.client.startExport(exportConfigurationId=export_configuration_id, json=create_data, **query_params)
            else:
                response = self.client.startExport(exportConfigurationId=export_configuration_id, **query_params)
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(export_configuration_id, "ExportConfiguration")
            if "400" in str(e):
                raise ValidationError(f"Export failed: {str(e)}")
            raise

        self._check_for_api_error(response, export_configuration_id, "ExportConfiguration")
        if isinstance(response, dict):
            return BackgroundProcessResponse(**response)
        return response

    @handle_rest_errors
    def create_import_job(self, import_configuration_id: str,
                          data: Optional[object] = None,
                          process_description: Optional[str] = None) -> BackgroundProcessResponse:
        """Trigger an import using a pre-configured import configuration (POST /import/{importConfigurationId}).

        Args:
            import_configuration_id: The ID of the import configuration to use (required)
            data: Optional request body with import payload
            process_description: Optional human-readable description for the import process

        Returns:
            BackgroundProcessResponse with job/process details

        Raises:
            ValidationError: If import_configuration_id is missing or data is invalid
            RestApiError: For API errors
        """
        self._validate_required_params(
            {"import_configuration_id": import_configuration_id},
            ["import_configuration_id"]
        )

        query_params = self._build_context_params()
        if process_description:
            query_params["processDescription"] = process_description

        self._log_operation("startImport", {"importConfigurationId": import_configuration_id})

        try:
            if data is not None:
                # Binary data: convert to bytes if needed
                if isinstance(data, str):
                    binary_data = data.encode('utf-8')
                elif isinstance(data, bytes):
                    binary_data = data
                else:
                    # For Pydantic models or dicts, convert to JSON bytes
                    import json
                    
                    from pydantic import BaseModel
                    if isinstance(data, BaseModel):
                        binary_data = json.dumps(data.model_dump(exclude_none=True)).encode('utf-8')
                    else:
                        binary_data = json.dumps(data).encode('utf-8')
                
                response = self.client.startImport(
                    importConfigurationId=import_configuration_id,
                    data=binary_data,
                    **query_params
                )
                response_dict: dict[str, Any] = response if isinstance(response, dict) else {"success": True}
            else:
                response = self.client.startImport(
                    importConfigurationId=import_configuration_id,
                    **query_params
                )
                response_dict: dict[str, Any] = response if isinstance(response, dict) else {"success": True}
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(import_configuration_id, "ImportConfiguration")
            if "400" in str(e):
                raise ValidationError(f"Import failed: {e!s}")
            raise

        self._check_for_api_error(response_dict, import_configuration_id, "ImportConfiguration")
        if isinstance(response_dict, dict):
            return BackgroundProcessResponse(**response_dict)
        return response_dict
    
