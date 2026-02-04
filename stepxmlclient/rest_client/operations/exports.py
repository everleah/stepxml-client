"""Export operations for STEP REST API v2."""

import logging
from typing import Optional

from ..base import BaseOperation, handle_rest_errors
from ..exceptions import NotFoundError, ValidationError, RestApiError
from ..models.import_export import (
    ExportJobResponse,
    ExportJobListResponse,
    ExportJobCreateRequest,
)


class ExportOperations(BaseOperation):
    """Operations for STEP data exports and data retrieval."""
    
    def __init__(self, client, logger: Optional[logging.Logger] = None):
        """Initialize export operations.
        
        Args:
            client: The REST API client
            logger: Optional logger instance
        """
        super().__init__(client, operation_name="ExportOperations", logger=logger)
    
    @handle_rest_errors
    def create_export_job(self, data: ExportJobCreateRequest) -> ExportJobResponse:
        """Create a new export job.
        
        Args:
            data: ExportJobCreateRequest with export configuration
            
        Returns:
            ExportJobResponse with job details
            
        Raises:
            ValidationError: If data invalid
            RestApiError: For API errors
        """
        # Convert Pydantic model to dict if needed
        if hasattr(data, 'model_dump'):
            create_data = data.model_dump(exclude_none=True)
        else:
            create_data = dict(data) if not isinstance(data, dict) else data
        
        self._log_operation("createExportJob", {
            "entityType": create_data.get("entityType"),
            "format": create_data.get("format")
        })
        
        try:
            response = self.client.createExportJob(body=create_data)
        except Exception as e:
            if "400" in str(e):
                raise ValidationError(f"Create export job failed: {str(e)}")
            raise
        
        if isinstance(response, dict):
            return ExportJobResponse(**response)
        return response
    
    @handle_rest_errors
    def get_export_job(self, job_id: str) -> ExportJobResponse:
        """Get status of an export job.
        
        Args:
            job_id: The export job ID
            
        Returns:
            ExportJobResponse with current job status
            
        Raises:
            ValidationError: If job_id is missing
            NotFoundError: If job not found
            RestApiError: For API errors
        """
        self._validate_required_params(
            {"job_id": job_id},
            ["job_id"]
        )
        
        self._log_operation("getExportJob", {"jobId": job_id})
        
        try:
            response = self.client.getExportJob(jobId=job_id)
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(job_id, "ExportJob")
            raise
        
        if isinstance(response, dict):
            return ExportJobResponse(**response)
        return response
    
    @handle_rest_errors
    def list_export_jobs(self,
                        status_filter: Optional[str] = None,
                        entity_type_filter: Optional[str] = None,
                        limit: int = 20,
                        offset: int = 0) -> ExportJobListResponse:
        """List export jobs with optional filters.
        
        Args:
            status_filter: Optional filter by job status (PENDING, PROCESSING, COMPLETED, FAILED)
            entity_type_filter: Optional filter by entity type
            limit: Result limit (1-500, default: 20)
            offset: Result offset (default: 0)
            
        Returns:
            ExportJobListResponse with list of jobs
            
        Raises:
            RestApiError: For API errors
        """
        pagination_params = self._build_pagination_params(limit, offset)
        
        self._log_operation("listExportJobs", {
            "statusFilter": status_filter,
            "entityTypeFilter": entity_type_filter,
            "limit": pagination_params["limit"],
            "offset": pagination_params["offset"]
        })
        
        params = self._clean_params({
            "statusFilter": status_filter,
            "entityTypeFilter": entity_type_filter,
            "limit": pagination_params["limit"],
            "offset": pagination_params["offset"]
        })
        
        response = self.client.listExportJobs(**params)
        
        if isinstance(response, dict):
            return ExportJobListResponse(**response)
        return response
    
    @handle_rest_errors
    def download_export_data(self, job_id: str, save_to_file: Optional[str] = None) -> bytes:
        """Download exported data from a completed export job.
        
        Args:
            job_id: The export job ID
            save_to_file: Optional file path to save data to
            
        Returns:
            Exported data as bytes
            
        Raises:
            ValidationError: If job_id missing
            NotFoundError: If job not found or data not available
            RestApiError: For API errors
        """
        self._validate_required_params(
            {"job_id": job_id},
            ["job_id"]
        )
        
        self._log_operation("downloadExportData", {"jobId": job_id})
        
        try:
            # Get the export job first to verify it exists and is completed
            job = self.get_export_job(job_id)
            
            if job.status != "COMPLETED":
                raise ValidationError(f"Export job {job_id} is not completed (status: {job.status})")
            
            # Download the data
            response = self.client.downloadExportData(jobId=job_id)
            
            # Handle the response - could be bytes or content
            if isinstance(response, bytes):
                data = response
            elif hasattr(response, 'content'):
                data = response.content
            else:
                data = bytes(response)
            
            # Optionally save to file
            if save_to_file:
                with open(save_to_file, 'wb') as f:
                    f.write(data)
                self._log_operation("exportDataSaved", {"file": save_to_file, "size": len(data)})
            
            return data
            
        except (FileNotFoundError, OSError, IOError) as e:
            # Let file system errors pass through
            raise
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(job_id, "ExportJob")
            raise
    
    @handle_rest_errors
    def get_completed_exports(self, limit: int = 20, offset: int = 0) -> ExportJobListResponse:
        """Convenience method to list completed export jobs.
        
        Args:
            limit: Result limit
            offset: Result offset
            
        Returns:
            ExportJobListResponse with completed jobs
        """
        return self.list_export_jobs(status_filter="COMPLETED", limit=limit, offset=offset)
    
    @handle_rest_errors
    def export_by_entity_type(self, entity_type: str,
                             export_format: str = "XML",
                             limit: int = 20,
                             offset: int = 0) -> ExportJobListResponse:
        """Convenience method to list export jobs for a specific entity type.
        
        Args:
            entity_type: The entity type to filter by (Product, Asset, Classification, Entity)
            export_format: Export format to filter by (optional)
            limit: Result limit
            offset: Result offset
            
        Returns:
            ExportJobListResponse filtered by entity type
        """
        return self.list_export_jobs(
            entity_type_filter=entity_type,
            limit=limit,
            offset=offset
        )
