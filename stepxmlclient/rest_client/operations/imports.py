"""Import operations for STEP REST API v2."""

import logging
from typing import Optional, List, Dict, Any

from ..base import BaseOperation, handle_rest_errors
from ..exceptions import NotFoundError, ValidationError, RestApiError
from ..models.import_export import (
    ImportJobResponse,
    ImportJobListResponse,
    ImportJobCreateRequest,
    JobErrorListResponse,
)


class ImportOperations(BaseOperation):
    """Operations for STEP data imports and bulk operations."""
    
    def __init__(self, client, logger: Optional[logging.Logger] = None):
        """Initialize import operations.
        
        Args:
            client: The REST API client
            logger: Optional logger instance
        """
        super().__init__(client, operation_name="ImportOperations", logger=logger)
    
    @handle_rest_errors
    def create_import_job(self, data: ImportJobCreateRequest) -> ImportJobResponse:
        """Create a new import job.
        
        Args:
            data: ImportJobCreateRequest with import configuration
            
        Returns:
            ImportJobResponse with job details
            
        Raises:
            ValidationError: If data invalid
            RestApiError: For API errors
        """
        # Convert Pydantic model to dict if needed
        if hasattr(data, 'model_dump'):
            create_data = data.model_dump(exclude_none=True)
        else:
            create_data = dict(data) if not isinstance(data, dict) else data
        
        self._log_operation("createImportJob", {
            "sourceType": create_data.get("sourceType"),
            "mode": create_data.get("mode")
        })
        
        try:
            response = self.client.createImportJob(json=create_data)
        except Exception as e:
            if "400" in str(e):
                raise ValidationError(f"Create import job failed: {str(e)}")
            raise
        
        if isinstance(response, dict):
            return ImportJobResponse(**response)
        return response
    
    @handle_rest_errors
    def get_import_job(self, job_id: str) -> ImportJobResponse:
        """Get status of an import job.
        
        Args:
            job_id: The import job ID
            
        Returns:
            ImportJobResponse with current job status
            
        Raises:
            ValidationError: If job_id is missing
            NotFoundError: If job not found
            RestApiError: For API errors
        """
        self._validate_required_params(
            {"job_id": job_id},
            ["job_id"]
        )
        
        self._log_operation("getImportJob", {"jobId": job_id})
        
        try:
            response = self.client.getImportJob(jobId=job_id)
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(job_id, "ImportJob")
            raise
        
        if isinstance(response, dict):
            return ImportJobResponse(**response)
        return response
    
    @handle_rest_errors
    def list_import_jobs(self,
                        status_filter: Optional[str] = None,
                        limit: int = 20,
                        offset: int = 0) -> ImportJobListResponse:
        """List import jobs with optional status filter.
        
        Args:
            status_filter: Optional filter by job status (PENDING, PROCESSING, COMPLETED, FAILED)
            limit: Result limit (1-500, default: 20)
            offset: Result offset (default: 0)
            
        Returns:
            ImportJobListResponse with list of jobs
            
        Raises:
            RestApiError: For API errors
        """
        pagination_params = self._build_pagination_params(limit, offset)
        
        self._log_operation("listImportJobs", {
            "statusFilter": status_filter,
            "limit": pagination_params["limit"],
            "offset": pagination_params["offset"]
        })
        
        params = self._clean_params({
            "statusFilter": status_filter,
            "limit": pagination_params["limit"],
            "offset": pagination_params["offset"]
        })
        
        response = self.client.listImportJobs(**params)
        
        if isinstance(response, dict):
            return ImportJobListResponse(**response)
        return response
    
    @handle_rest_errors
    def cancel_import_job(self, job_id: str) -> bool:
        """Cancel an import job.
        
        Args:
            job_id: The import job ID
            
        Returns:
            True if cancellation was successful
            
        Raises:
            ValidationError: If job_id missing
            NotFoundError: If job not found
            RestApiError: For API errors
        """
        self._validate_required_params(
            {"job_id": job_id},
            ["job_id"]
        )
        
        self._log_operation("cancelImportJob", {"jobId": job_id})
        
        try:
            self.client.cancelImportJob(jobId=job_id)
            return True
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(job_id, "ImportJob")
            raise
    
    @handle_rest_errors
    def get_import_job_errors(self, job_id: str,
                             limit: int = 100,
                             offset: int = 0) -> JobErrorListResponse:
        """Get errors from a failed import job.
        
        Args:
            job_id: The import job ID
            limit: Result limit (default: 100)
            offset: Result offset (default: 0)
            
        Returns:
            JobErrorListResponse with errors
            
        Raises:
            ValidationError: If job_id missing
            NotFoundError: If job not found
            RestApiError: For API errors
        """
        self._validate_required_params(
            {"job_id": job_id},
            ["job_id"]
        )
        
        pagination_params = self._build_pagination_params(limit, offset)
        
        self._log_operation("getImportJobErrors", {
            "jobId": job_id,
            "limit": pagination_params["limit"],
            "offset": pagination_params["offset"]
        })
        
        params = self._clean_params({
            "limit": pagination_params["limit"],
            "offset": pagination_params["offset"]
        })
        
        try:
            response = self.client.getImportJobErrors(
                jobId=job_id,
                **params
            )
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(job_id, "ImportJob")
            raise
        
        if isinstance(response, dict):
            return JobErrorListResponse(**response)
        return response
    
    @handle_rest_errors
    def get_completed_imports(self, limit: int = 20, offset: int = 0) -> ImportJobListResponse:
        """Convenience method to list completed import jobs.
        
        Args:
            limit: Result limit
            offset: Result offset
            
        Returns:
            ImportJobListResponse with completed jobs
        """
        return self.list_import_jobs(status_filter="COMPLETED", limit=limit, offset=offset)
    
    @handle_rest_errors
    def get_failed_imports(self, limit: int = 20, offset: int = 0) -> ImportJobListResponse:
        """Convenience method to list failed import jobs.
        
        Args:
            limit: Result limit
            offset: Result offset
            
        Returns:
            ImportJobListResponse with failed jobs
        """
        return self.list_import_jobs(status_filter="FAILED", limit=limit, offset=offset)
