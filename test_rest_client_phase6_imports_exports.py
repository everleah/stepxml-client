"""Phase 6: Import/Export Operations Tests

Tests for import/export job management operations and models.
Covers job creation, status tracking, downloading exports, and error handling.
"""

import unittest
from unittest.mock import Mock, MagicMock, patch, call
from datetime import datetime

from stepxmlclient.rest_client.models.import_export import (
    ImportJobResponse,
    ImportJobListResponse,
    ImportJobCreateRequest,
    ExportJobResponse,
    ExportJobListResponse,
    ExportJobCreateRequest,
    JobProgressResponse,
    JobErrorResponse,
    JobErrorListResponse,
)
from stepxmlclient.rest_client.operations.imports import ImportOperations
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
            percentComplete=50.0
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
            timestamp=datetime.now().isoformat()
        )
        assert error.errorCode == "INVALID_DATA"
        assert error.errorMessage == "Invalid product ID"
        assert error.entityId == "PROD123"
    
    def test_import_job_create_request_validation(self):
        """Test ImportJobCreateRequest validation."""
        # Valid request
        request = ImportJobCreateRequest(
            entityType="Product",
            sourceType="S3",
            sourceData={"bucket": "my-bucket", "key": "products.xml"},
            updateStrategy="REPLACE"
        )
        assert request.entityType == "Product"
        assert request.sourceType == "S3"
        
    def test_import_job_response_creation(self):
        """Test ImportJobResponse model creation."""
        job = ImportJobResponse(
            jobId="IMP123456",
            status="PROCESSING",
            entityType="Product",
            createdAt=datetime.now().isoformat()
        )
        assert job.jobId == "IMP123456"
        assert job.status == "PROCESSING"
        assert job.entityType == "Product"
    
    def test_import_job_list_response(self):
        """Test ImportJobListResponse with pagination."""
        job1 = ImportJobResponse(
            jobId="IMP001",
            status="COMPLETED",
            entityType="Product",
            createdAt=datetime.now().isoformat()
        )
        job2 = ImportJobResponse(
            jobId="IMP002",
            status="PROCESSING",
            entityType="Asset",
            createdAt=datetime.now().isoformat()
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
            filters={"status": "ACTIVE"}
        )
        assert request.entityType == "Product"
        assert request.format == "XML"
    
    def test_export_job_response(self):
        """Test ExportJobResponse model creation."""
        job = ExportJobResponse(
            jobId="EXP123456",
            status="COMPLETED",
            entityType="Product",
            format="XML",
            createdAt=datetime.now().isoformat()
        )
        assert job.jobId == "EXP123456"
        assert job.status == "COMPLETED"
    
    def test_job_error_list_response(self):
        """Test JobErrorListResponse with pagination."""
        errors = [
            JobErrorResponse(
                errorCode="ERR001",
                errorMessage="Invalid data",
                entityId="PROD001"
            ),
            JobErrorResponse(
                errorCode="ERR002",
                errorMessage="Duplicate entry",
                entityId="PROD002"
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


class TestImportOperations(unittest.TestCase):
    """Tests for import operations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.imports = ImportOperations(self.mock_client)
    
    def test_create_import_job_success(self):
        """Test successful import job creation."""
        # Setup
        request = ImportJobCreateRequest(
            entityType="Product",
            sourceType="S3",
            sourceData={"bucket": "my-bucket", "key": "products.xml"}
        )
        expected_response = {
            "jobId": "IMP123456",
            "status": "PENDING",
            "entityType": "Product",
            "createdAt": datetime.now().isoformat()
        }
        self.mock_client.createImportJob = Mock(return_value=expected_response)
        
        # Execute
        result = self.imports.create_import_job(request)
        
        # Assert
        assert isinstance(result, ImportJobResponse)
        assert result.jobId == "IMP123456"
        assert result.status == "PENDING"
    
    def test_get_import_job_success(self):
        """Test getting import job status."""
        # Setup
        job_id = "IMP123456"
        expected_response = {
            "jobId": job_id,
            "status": "PROCESSING",
            "entityType": "Product",
            "createdAt": datetime.now().isoformat(),
            "progress": {
                "totalItems": 1000,
                "processedItems": 500,
                "failedItems": 10,
                "percentComplete": 50.0
            }
        }
        self.mock_client.getImportJob = Mock(return_value=expected_response)
        
        # Execute
        result = self.imports.get_import_job(job_id)
        
        # Assert
        assert isinstance(result, ImportJobResponse)
        assert result.jobId == job_id
        assert result.status == "PROCESSING"
    
    def test_get_import_job_not_found(self):
        """Test get import job with invalid ID."""
        # Setup
        job_id = "INVALID_ID"
        self.mock_client.getImportJob = Mock(side_effect=Exception("404 Not Found"))
        
        # Execute & Assert
        with self.assertRaises(NotFoundError):
            self.imports.get_import_job(job_id)
    
    def test_list_import_jobs_success(self):
        """Test listing import jobs with pagination."""
        # Setup
        expected_response = {
            "jobs": [
                {
                    "jobId": "IMP001",
                    "status": "COMPLETED",
                    "entityType": "Product",
                    "createdAt": datetime.now().isoformat()
                },
                {
                    "jobId": "IMP002",
                    "status": "PROCESSING",
                    "entityType": "Asset",
                    "createdAt": datetime.now().isoformat()
                }
            ],
            "totalCount": 2,
            "limit": 20,
            "offset": 0
        }
        self.mock_client.listImportJobs = Mock(return_value=expected_response)
        
        # Execute
        result = self.imports.list_import_jobs(limit=20, offset=0)
        
        # Assert
        assert isinstance(result, ImportJobListResponse)
        assert len(result.jobs) == 2
        assert result.totalCount == 2
    
    def test_list_import_jobs_with_status_filter(self):
        """Test listing import jobs with status filter."""
        # Setup
        status_filter = "COMPLETED"
        expected_response = {
            "jobs": [
                {
                    "jobId": "IMP001",
                    "status": "COMPLETED",
                    "entityType": "Product",
                    "createdAt": datetime.now().isoformat()
                }
            ],
            "totalCount": 1,
            "limit": 20,
            "offset": 0
        }
        self.mock_client.listImportJobs = Mock(return_value=expected_response)
        
        # Execute
        result = self.imports.list_import_jobs(status_filter=status_filter)
        
        # Assert
        assert len(result.jobs) == 1
        assert result.jobs[0].status == "COMPLETED"
    
    def test_cancel_import_job_success(self):
        """Test cancelling an import job."""
        # Setup
        job_id = "IMP123456"
        self.mock_client.cancelImportJob = Mock(return_value=True)
        
        # Execute
        result = self.imports.cancel_import_job(job_id)
        
        # Assert
        assert result is True
    
    def test_get_import_job_errors(self):
        """Test retrieving import job errors."""
        # Setup
        job_id = "IMP123456"
        expected_response = {
            "errors": [
                {
                    "errorCode": "INVALID_DATA",
                    "errorMessage": "Invalid product ID",
                    "entityId": "PROD001",
                    "severity": "ERROR"
                }
            ],
            "totalCount": 1,
            "limit": 100,
            "offset": 0
        }
        self.mock_client.getImportJobErrors = Mock(return_value=expected_response)
        
        # Execute
        result = self.imports.get_import_job_errors(job_id)
        
        # Assert
        assert isinstance(result, JobErrorListResponse)
        assert len(result.errors) == 1
        assert result.errors[0].errorCode == "INVALID_DATA"
    
    def test_get_completed_imports(self):
        """Test convenience method for listing completed imports."""
        # Setup
        expected_response = {
            "jobs": [
                {
                    "jobId": "IMP001",
                    "status": "COMPLETED",
                    "entityType": "Product",
                    "createdAt": datetime.now().isoformat()
                }
            ],
            "totalCount": 1,
            "limit": 20,
            "offset": 0
        }
        self.mock_client.listImportJobs = Mock(return_value=expected_response)
        
        # Execute
        result = self.imports.get_completed_imports()
        
        # Assert
        assert len(result.jobs) == 1
        assert all(job.status == "COMPLETED" for job in result.jobs)
    
    def test_get_failed_imports(self):
        """Test convenience method for listing failed imports."""
        # Setup
        expected_response = {
            "jobs": [
                {
                    "jobId": "IMP002",
                    "status": "FAILED",
                    "entityType": "Asset",
                    "createdAt": datetime.now().isoformat(),
                    "errorMessage": "Source file not found"
                }
            ],
            "totalCount": 1,
            "limit": 20,
            "offset": 0
        }
        self.mock_client.listImportJobs = Mock(return_value=expected_response)
        
        # Execute
        result = self.imports.get_failed_imports()
        
        # Assert
        assert len(result.jobs) == 1
        assert all(job.status == "FAILED" for job in result.jobs)


class TestExportOperations(unittest.TestCase):
    """Tests for export operations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.exports = ExportOperations(self.mock_client)
    
    def test_create_export_job_success(self):
        """Test successful export job creation."""
        # Setup
        request = ExportJobCreateRequest(
            entityType="Product",
            format="XML"
        )
        expected_response = {
            "jobId": "EXP123456",
            "status": "PENDING",
            "entityType": "Product",
            "format": "XML",
            "createdAt": datetime.now().isoformat()
        }
        self.mock_client.createExportJob = Mock(return_value=expected_response)
        
        # Execute
        result = self.exports.create_export_job(request)
        
        # Assert
        assert isinstance(result, ExportJobResponse)
        assert result.jobId == "EXP123456"
        assert result.status == "PENDING"
    
    def test_get_export_job_success(self):
        """Test getting export job status."""
        # Setup
        job_id = "EXP123456"
        expected_response = {
            "jobId": job_id,
            "status": "COMPLETED",
            "entityType": "Product",
            "format": "XML",
            "createdAt": datetime.now().isoformat(),
            "completedAt": datetime.now().isoformat(),
            "progress": {
                "totalItems": 1000,
                "processedItems": 1000,
                "failedItems": 0,
                "percentComplete": 100.0
            }
        }
        self.mock_client.getExportJob = Mock(return_value=expected_response)
        
        # Execute
        result = self.exports.get_export_job(job_id)
        
        # Assert
        assert isinstance(result, ExportJobResponse)
        assert result.jobId == job_id
        assert result.status == "COMPLETED"
    
    def test_get_export_job_not_found(self):
        """Test get export job with invalid ID."""
        # Setup
        job_id = "INVALID_ID"
        self.mock_client.getExportJob = Mock(side_effect=Exception("404 Not Found"))
        
        # Execute & Assert
        with self.assertRaises(NotFoundError):
            self.exports.get_export_job(job_id)
    
    def test_list_export_jobs_success(self):
        """Test listing export jobs with pagination."""
        # Setup
        expected_response = {
            "jobs": [
                {
                    "jobId": "EXP001",
                    "status": "COMPLETED",
                    "entityType": "Product",
                    "format": "XML",
                    "createdAt": datetime.now().isoformat()
                },
                {
                    "jobId": "EXP002",
                    "status": "PROCESSING",
                    "entityType": "Asset",
                    "format": "JSON",
                    "createdAt": datetime.now().isoformat()
                }
            ],
            "totalCount": 2,
            "limit": 20,
            "offset": 0
        }
        self.mock_client.listExportJobs = Mock(return_value=expected_response)
        
        # Execute
        result = self.exports.list_export_jobs(limit=20, offset=0)
        
        # Assert
        assert isinstance(result, ExportJobListResponse)
        assert len(result.jobs) == 2
        assert result.totalCount == 2
    
    def test_list_export_jobs_with_filters(self):
        """Test listing export jobs with multiple filters."""
        # Setup
        status_filter = "COMPLETED"
        entity_type_filter = "Product"
        expected_response = {
            "jobs": [
                {
                    "jobId": "EXP001",
                    "status": "COMPLETED",
                    "entityType": "Product",
                    "format": "XML",
                    "createdAt": datetime.now().isoformat()
                }
            ],
            "totalCount": 1,
            "limit": 20,
            "offset": 0
        }
        self.mock_client.listExportJobs = Mock(return_value=expected_response)
        
        # Execute
        result = self.exports.list_export_jobs(
            status_filter=status_filter,
            entity_type_filter=entity_type_filter
        )
        
        # Assert
        assert len(result.jobs) == 1
        assert result.jobs[0].status == "COMPLETED"
        assert result.jobs[0].entityType == "Product"
    
    def test_download_export_data_success(self):
        """Test downloading exported data."""
        # Setup
        job_id = "EXP123456"
        export_data = b"<products>...</products>"
        
        # Mock the get_export_job to return completed job
        completed_job = ExportJobResponse(
            jobId=job_id,
            status="COMPLETED",
            entityType="Product",
            format="XML",
            createdAt=datetime.now().isoformat()
        )
        
        self.exports.get_export_job = Mock(return_value=completed_job)
        self.mock_client.downloadExportData = Mock(return_value=export_data)
        
        # Execute
        result = self.exports.download_export_data(job_id)
        
        # Assert
        assert result == export_data
        assert isinstance(result, bytes)
    
    def test_download_export_data_not_completed(self):
        """Test download fails for non-completed job."""
        # Setup
        job_id = "EXP123456"
        
        # Mock get_export_job to return processing job
        processing_job = ExportJobResponse(
            jobId=job_id,
            status="PROCESSING",
            entityType="Product",
            format="XML",
            createdAt=datetime.now().isoformat()
        )
        
        self.exports.get_export_job = Mock(return_value=processing_job)
        
        # Execute & Assert
        with self.assertRaises(ValidationError):
            self.exports.download_export_data(job_id)
    
    def test_download_export_data_save_to_file(self):
        """Test downloading and saving export data to file."""
        # Setup
        job_id = "EXP123456"
        export_data = b"<products>...</products>"
        
        completed_job = ExportJobResponse(
            jobId=job_id,
            status="COMPLETED",
            entityType="Product",
            format="XML",
            createdAt=datetime.now().isoformat()
        )
        
        self.exports.get_export_job = Mock(return_value=completed_job)
        self.mock_client.downloadExportData = Mock(return_value=export_data)
        
        # Execute with save_to_file
        with patch('builtins.open', create=True) as mock_open:
            result = self.exports.download_export_data(job_id, save_to_file="/tmp/export.xml")
        
        # Assert
        assert result == export_data
        mock_open.assert_called_once_with("/tmp/export.xml", 'wb')
    
    def test_get_completed_exports(self):
        """Test convenience method for listing completed exports."""
        # Setup
        expected_response = {
            "jobs": [
                {
                    "jobId": "EXP001",
                    "status": "COMPLETED",
                    "entityType": "Product",
                    "format": "XML",
                    "createdAt": datetime.now().isoformat()
                }
            ],
            "totalCount": 1,
            "limit": 20,
            "offset": 0
        }
        self.mock_client.listExportJobs = Mock(return_value=expected_response)
        
        # Execute
        result = self.exports.get_completed_exports()
        
        # Assert
        assert len(result.jobs) == 1
        assert all(job.status == "COMPLETED" for job in result.jobs)
    
    def test_export_by_entity_type(self):
        """Test convenience method for filtering by entity type."""
        # Setup
        entity_type = "Product"
        expected_response = {
            "jobs": [
                {
                    "jobId": "EXP001",
                    "status": "COMPLETED",
                    "entityType": "Product",
                    "format": "XML",
                    "createdAt": datetime.now().isoformat()
                }
            ],
            "totalCount": 1,
            "limit": 20,
            "offset": 0
        }
        self.mock_client.listExportJobs = Mock(return_value=expected_response)
        
        # Execute
        result = self.exports.export_by_entity_type(entity_type)
        
        # Assert
        assert len(result.jobs) == 1
        assert all(job.entityType == "Product" for job in result.jobs)


class TestImportExportIntegration(unittest.TestCase):
    """Integration tests for import/export workflows."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.imports = ImportOperations(self.mock_client)
        self.exports = ExportOperations(self.mock_client)
    
    def test_full_import_workflow(self):
        """Test complete import job workflow: create, check status, check errors."""
        # Create job
        create_response = {
            "jobId": "IMP123",
            "status": "PENDING",
            "entityType": "Product",
            "createdAt": datetime.now().isoformat()
        }
        self.mock_client.createImportJob = Mock(return_value=create_response)
        
        request = ImportJobCreateRequest(
            entityType="Product",
            sourceType="S3",
            sourceData={"bucket": "my-bucket", "key": "products.xml"}
        )
        created_job = self.imports.create_import_job(request)
        assert created_job.jobId == "IMP123"
        
        # Check status
        status_response = {
            "jobId": "IMP123",
            "status": "COMPLETED",
            "entityType": "Product",
            "createdAt": datetime.now().isoformat()
        }
        self.mock_client.getImportJob = Mock(return_value=status_response)
        
        job_status = self.imports.get_import_job("IMP123")
        assert job_status.status == "COMPLETED"
        
        # Check errors
        errors_response = {
            "errors": [],
            "totalCount": 0,
            "limit": 100,
            "offset": 0
        }
        self.mock_client.getImportJobErrors = Mock(return_value=errors_response)
        
        errors = self.imports.get_import_job_errors("IMP123")
        assert errors.totalCount == 0
    
    def test_full_export_workflow(self):
        """Test complete export job workflow: create, check status, download."""
        # Create export
        create_response = {
            "jobId": "EXP123",
            "status": "PENDING",
            "entityType": "Product",
            "format": "XML",
            "createdAt": datetime.now().isoformat()
        }
        self.mock_client.createExportJob = Mock(return_value=create_response)
        
        request = ExportJobCreateRequest(
            entityType="Product",
            format="XML"
        )
        created_job = self.exports.create_export_job(request)
        assert created_job.jobId == "EXP123"
        
        # Check status
        status_response = {
            "jobId": "EXP123",
            "status": "COMPLETED",
            "entityType": "Product",
            "format": "XML",
            "createdAt": datetime.now().isoformat(),
            "completedAt": datetime.now().isoformat()
        }
        self.mock_client.getExportJob = Mock(return_value=status_response)
        
        job_status = self.exports.get_export_job("EXP123")
        assert job_status.status == "COMPLETED"
        
        # Download data
        export_data = b"<products>...</products>"
        self.mock_client.downloadExportData = Mock(return_value=export_data)
        
        data = self.exports.download_export_data("EXP123")
        assert data == export_data


if __name__ == '__main__':
    unittest.main()
