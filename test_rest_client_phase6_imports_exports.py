"""Phase 6: Import/Export Operations Tests

Tests for import/export job management operations and models.
Covers job creation, status tracking, downloading exports, and error handling.
"""

import unittest
import logging
from unittest.mock import Mock, MagicMock, patch, call
from datetime import datetime
from stepxmlclient.rest_client import exceptions as exc

from stepxmlclient.rest_client.models.import_export import (
    BackgroundProcessResponse,
    ExportJobCreateRequest,
)
from stepxmlclient.rest_client.operations.exports import ExportOperations
from stepxmlclient.rest_client.exceptions import (
    NotFoundError,
    ValidationError,
    RestApiError,
)


class TestImportExportModels(unittest.TestCase):
    """Tests for import/export models."""
    
    def test_job_progress_response_creation(self):
        """Test JobProgressResponse model creation."""
        progress = JobProgressResponse(
            totalItems=1000,
            processedItems=500,
            failedItems=10,
            percentComplete=50.0,
            successfulItems=None
        )
        assert progress.totalItems == 1000
        assert progress.processedItems == 500
        assert progress.failedItems == 10
        assert progress.percentComplete == 50.0
    
    def test_job_error_response_creation(self):
        """Test JobErrorResponse model creation."""
        error = JobErrorResponse(
            errorCode="INVALID_DATA",
            errorMessage="Invalid product ID",
            entityId="PROD123",
            severity="ERROR",
            timestamp=datetime.now().isoformat(),
            details=None
        )
        assert error.errorCode == "INVALID_DATA"
        assert error.errorMessage == "Invalid product ID"
        assert error.entityId == "PROD123"
    
    def test_import_job_create_request_validation(self):
        """Test ExportJobCreateRequest validation."""
        # Valid request
        request = ExportJobCreateRequest(
            entityType="Product",
            sourceType="S3",
            sourceData={"bucket": "my-bucket", "key": "products.xml"},
            updateStrategy="REPLACE",
            config=None
        )
        assert request.entityType == "Product"
        assert request.sourceType == "S3"
        
    def test_import_job_response_creation(self):
        """Test BackgroundProcessResponse model creation."""
        job = BackgroundProcessResponse(
            jobId="IMP123456",
            status="PROCESSING",
            entityType="Product",
            createdAt=datetime.now().isoformat(),
            startedAt=None,
            completedAt=None,
            updateStrategy=None,
            progress=None,
            errorMessage=None,
            config=None        
            )
        assert job.jobId == "IMP123456"
        assert job.status == "PROCESSING"
        assert job.entityType == "Product"
    
    def test_import_job_list_response(self):
        """Test ImportJobListResponse with pagination."""
        job1 = BackgroundProcessResponse(
            jobId="IMP001",
            status="COMPLETED",
            entityType="Product",
            createdAt=datetime.now().isoformat(),
            startedAt=None,
            completedAt=None,
            updateStrategy=None,
            progress=None,
            errorMessage=None,
            config=None            
        )
        job2 = BackgroundProcessResponse(
            jobId="IMP002",
            status="PROCESSING",
            entityType="Asset",
            createdAt=datetime.now().isoformat(),
            startedAt=None,
            completedAt=None,
            updateStrategy=None,
            progress=None,
            errorMessage=None,
            config=None
        )
        
        response = ImportJobListResponse(
            jobs=[job1, job2],
            totalCount=2,
            limit=20,
            offset=0
        )
        assert len(response.jobs) == 2
        assert response.totalCount == 2
    
    def test_export_job_create_request(self):
        """Test ExportJobCreateRequest validation."""
        request = ExportJobCreateRequest(
            entityType="Product",
            format="XML",
            filters={"status": "ACTIVE"},
            config=None
        )
        assert request.entityType == "Product"
        assert request.format == "XML"
    
    def test_export_job_response(self):
        """Test BackgroundProcessResponse (BackgroundProcessResponse alias) model creation.

        The STEP REST API spec defines ``BackgroundProcessIdentification`` for
        POST /export/{id} and POST /import/{id} responses.  It has only an
        optional ``id`` field matching the background-process identifier.
        """
        # Test with the spec-correct field (id)
        job = BackgroundProcessResponse(id="bg-process-0042")
        assert job.id == "bg-process-0042"

        # Pydantic ignores unknown extra fields (populate_by_name=True) – this
        # should NOT raise even though the old required fields are gone.
        job2 = BackgroundProcessResponse()
        assert job2.id is None
    
    def test_job_error_list_response(self):
        """Test JobErrorListResponse with pagination."""
        errors = [
            JobErrorResponse(
                errorCode="ERR001",
                errorMessage="Invalid data",
                entityId="PROD001",
                severity=None,
                timestamp=datetime.now().isoformat(),
                details=None
            ),
            JobErrorResponse(
                errorCode="ERR002",
                errorMessage="Duplicate entry",
                entityId="PROD002",
                severity=None,
                timestamp=datetime.now().isoformat(),
                details=None
            )
        ]
        
        response = JobErrorListResponse(
            errors=errors,
            totalCount=2,
            limit=100,
            offset=0
        )
        assert len(response.errors) == 2
        assert response.totalCount == 2




if __name__ == "__main__":
    unittest.main()
