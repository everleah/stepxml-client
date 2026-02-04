"""Phase 0 - Foundation tests for REST API client infrastructure.

Tests for core Pydantic models, exceptions, and base operation class.
"""

import unittest
from typing import List

from stepxmlclient.rest_client import exceptions as exc
from stepxmlclient.rest_client.models import (
    PageInfo,
    PagedResponse,
    ErrorDetail,
    ErrorResponse,
    ApiResponse,
    SearchFilter,
    SearchRequest,
)
from stepxmlclient.rest_client.base import BaseOperation
import logging


class TestPageInfo(unittest.TestCase):
    """Tests for PageInfo model."""
    
    def test_page_info_creation(self):
        """Test basic PageInfo creation."""
        page = PageInfo(offset=0, limit=20, total=100)
        self.assertEqual(page.offset, 0)
        self.assertEqual(page.limit, 20)
        self.assertEqual(page.total, 100)
        self.assertTrue(page.has_more)  # 0 + 20 < 100, so more results exist
    
    def test_page_info_has_more(self):
        """Test has_more calculation."""
        page = PageInfo(offset=0, limit=20, total=100)
        self.assertTrue(page.has_more)
        
        page = PageInfo(offset=80, limit=20, total=100)
        self.assertFalse(page.has_more)
    
    def test_page_info_defaults(self):
        """Test PageInfo default values."""
        page = PageInfo()
        self.assertEqual(page.offset, 0)
        self.assertEqual(page.limit, 20)
        self.assertIsNone(page.total)
        self.assertFalse(page.has_more)
    
    def test_page_info_validation_limit(self):
        """Test PageInfo limit validation."""
        with self.assertRaises(ValueError):
            PageInfo(limit=0)  # Must be >= 1
        
        with self.assertRaises(ValueError):
            PageInfo(limit=1001)  # Must be <= 1000
    
    def test_page_info_validation_offset(self):
        """Test PageInfo offset validation."""
        with self.assertRaises(ValueError):
            PageInfo(offset=-1)  # Must be >= 0


class TestErrorDetail(unittest.TestCase):
    """Tests for ErrorDetail model."""
    
    def test_error_detail_creation(self):
        """Test ErrorDetail creation."""
        detail = ErrorDetail(
            code="REQUIRED_FIELD",
            message="Field is required",
            field="name"
        )
        self.assertEqual(detail.code, "REQUIRED_FIELD")
        self.assertEqual(detail.message, "Field is required")
        self.assertEqual(detail.field, "name")
    
    def test_error_detail_with_details(self):
        """Test ErrorDetail with additional details."""
        detail = ErrorDetail(
            code="VALIDATION_ERROR",
            message="Invalid value",
            details={"min": 1, "max": 100, "actual": 150}
        )
        self.assertIsNotNone(detail.details)
        self.assertEqual(detail.details["max"], 100)


class TestErrorResponse(unittest.TestCase):
    """Tests for ErrorResponse model."""
    
    def test_error_response_creation(self):
        """Test ErrorResponse creation."""
        response = ErrorResponse(
            error_code="VALIDATION_FAILED",
            error_message="Request validation failed",
            status=400
        )
        self.assertEqual(response.error_code, "VALIDATION_FAILED")
        self.assertEqual(response.status, 400)
    
    def test_error_response_with_details(self):
        """Test ErrorResponse with error details."""
        details = [
            ErrorDetail(code="REQUIRED", message="Field required", field="name"),
            ErrorDetail(code="INVALID_FORMAT", message="Invalid format", field="email"),
        ]
        response = ErrorResponse(
            error_code="VALIDATION_FAILED",
            error_message="Multiple validation errors",
            status=400,
            error_details=details
        )
        self.assertEqual(len(response.error_details), 2)


class TestApiResponse(unittest.TestCase):
    """Tests for ApiResponse model."""
    
    def test_api_response_creation(self):
        """Test ApiResponse creation."""
        data = {"id": 123, "name": "Test Product"}
        response = ApiResponse(data=data, success=True)
        self.assertEqual(response.data["id"], 123)
        self.assertTrue(response.success)
    
    def test_api_response_with_metadata(self):
        """Test ApiResponse with metadata."""
        response = ApiResponse(
            data={"id": 123},
            metadata={"version": "1.0"},
            success=True
        )
        self.assertIsNotNone(response.metadata)
        self.assertEqual(response.metadata["version"], "1.0")


class TestPagedResponse(unittest.TestCase):
    """Tests for PagedResponse model."""
    
    def test_paged_response_creation(self):
        """Test PagedResponse creation."""
        items = [{"id": 1}, {"id": 2}]
        pagination = PageInfo(offset=0, limit=20, total=100)
        response = PagedResponse(items=items, pagination=pagination)
        
        self.assertEqual(len(response.items), 2)
        self.assertEqual(response.pagination.total, 100)
    
    def test_paged_response_empty(self):
        """Test PagedResponse with no items."""
        response = PagedResponse(items=[])
        self.assertEqual(len(response.items), 0)


class TestSearchFilter(unittest.TestCase):
    """Tests for SearchFilter model."""
    
    def test_search_filter_creation(self):
        """Test SearchFilter creation."""
        filter = SearchFilter(field="status", value="active", operator="eq")
        self.assertEqual(filter.field, "status")
        self.assertEqual(filter.operator, "eq")
    
    def test_search_filter_defaults(self):
        """Test SearchFilter default operator."""
        filter = SearchFilter(field="name", value="test")
        self.assertEqual(filter.operator, "eq")


class TestSearchRequest(unittest.TestCase):
    """Tests for SearchRequest model."""
    
    def test_search_request_creation(self):
        """Test SearchRequest creation."""
        request = SearchRequest(query="test", limit=50)
        self.assertEqual(request.query, "test")
        self.assertEqual(request.limit, 50)
        self.assertEqual(request.offset, 0)
    
    def test_search_request_with_filters(self):
        """Test SearchRequest with filters."""
        filters = [
            SearchFilter(field="status", value="active"),
            SearchFilter(field="category", value="products"),
        ]
        request = SearchRequest(query="test", filters=filters)
        self.assertEqual(len(request.filters), 2)


class TestExceptions(unittest.TestCase):
    """Tests for exception classes."""
    
    def test_rest_client_error(self):
        """Test RestClientError."""
        error = exc.RestClientError("Test error")
        self.assertIsInstance(error, Exception)
    
    def test_authentication_error(self):
        """Test AuthenticationError."""
        error = exc.AuthenticationError("Invalid credentials")
        self.assertIsInstance(error, exc.RestClientError)
    
    def test_authorization_error(self):
        """Test AuthorizationError."""
        error = exc.AuthorizationError("Access denied")
        self.assertIsInstance(error, exc.RestClientError)
    
    def test_not_found_error(self):
        """Test NotFoundError."""
        error = exc.NotFoundError("PROD123", "Product")
        self.assertEqual(error.status_code, 404)
        self.assertEqual(error.error_code, "NOT_FOUND")
        self.assertEqual(error.resource_id, "PROD123")
    
    def test_validation_error(self):
        """Test ValidationError."""
        errors = ["Field A is required", "Field B is invalid"]
        error = exc.ValidationError(errors)
        self.assertEqual(error.validation_errors, errors)
    
    def test_conflict_error(self):
        """Test ConflictError."""
        error = exc.ConflictError(409, "Resource already exists")
        self.assertEqual(error.status_code, 409)
    
    def test_rate_limit_error(self):
        """Test RateLimitError."""
        error = exc.RateLimitError(retry_after=60)
        self.assertEqual(error.status_code, 429)
        self.assertEqual(error.retry_after, 60)
    
    def test_server_error(self):
        """Test ServerError."""
        error = exc.ServerError(500, "Internal server error")
        self.assertEqual(error.status_code, 500)
    
    def test_timeout_error(self):
        """Test TimeoutError."""
        error = exc.TimeoutError("Request timed out")
        self.assertIsInstance(error, exc.RestClientError)
    
    def test_operation_error(self):
        """Test OperationError."""
        error = exc.OperationError("Operation failed")
        self.assertIsInstance(error, exc.RestClientError)


class TestBaseOperation(unittest.TestCase):
    """Tests for BaseOperation base class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.logger = logging.getLogger(__name__)
        # Create a mock client (we don't test actual HTTP here)
        self.mock_client = None
    
    def test_base_operation_creation(self):
        """Test BaseOperation initialization."""
        # We can't fully test without a real client, but we can test initialization
        # This test ensures the class structure is correct
        self.assertTrue(hasattr(BaseOperation, '_log_operation'))
        self.assertTrue(hasattr(BaseOperation, '_process_response'))
        self.assertTrue(hasattr(BaseOperation, '_build_pagination_params'))
        self.assertTrue(hasattr(BaseOperation, '_build_page_info'))
        self.assertTrue(hasattr(BaseOperation, '_call_operation'))
        self.assertTrue(hasattr(BaseOperation, '_validate_required_params'))
        self.assertTrue(hasattr(BaseOperation, '_clean_params'))
    
    def test_build_pagination_params(self):
        """Test pagination parameter building."""
        # Create instance without client for testing
        op = object.__new__(BaseOperation)
        
        params = op._build_pagination_params(limit=50, offset=100)
        self.assertEqual(params['limit'], 50)
        self.assertEqual(params['offset'], 100)
    
    def test_build_pagination_params_clamping(self):
        """Test pagination parameter clamping."""
        op = object.__new__(BaseOperation)
        
        # Test limit clamping
        params = op._build_pagination_params(limit=2000, offset=100)
        self.assertEqual(params['limit'], 1000)  # Clamped to max
        
        params = op._build_pagination_params(limit=0, offset=100)
        self.assertEqual(params['limit'], 1)  # Clamped to min
    
    def test_build_pagination_params_offset_clamping(self):
        """Test offset clamping."""
        op = object.__new__(BaseOperation)
        
        params = op._build_pagination_params(limit=20, offset=-10)
        self.assertEqual(params['offset'], 0)  # Clamped to 0
    
    def test_build_page_info(self):
        """Test PageInfo building."""
        op = object.__new__(BaseOperation)
        
        page_info = op._build_page_info(limit=20, offset=0, total=100)
        self.assertEqual(page_info.limit, 20)
        self.assertEqual(page_info.offset, 0)
        self.assertEqual(page_info.total, 100)
        self.assertTrue(page_info.has_more)
    
    def test_build_page_info_no_more(self):
        """Test PageInfo when no more results."""
        op = object.__new__(BaseOperation)
        
        page_info = op._build_page_info(limit=20, offset=80, total=100)
        self.assertFalse(page_info.has_more)
    
    def test_clean_params(self):
        """Test parameter cleaning."""
        op = object.__new__(BaseOperation)
        
        params = {
            'name': 'test',
            'description': None,
            'limit': 20,
            'offset': None,
        }
        cleaned = op._clean_params(params)
        
        self.assertEqual(len(cleaned), 2)
        self.assertIn('name', cleaned)
        self.assertIn('limit', cleaned)
        self.assertNotIn('description', cleaned)
        self.assertNotIn('offset', cleaned)
    
    def test_validate_required_params_success(self):
        """Test successful parameter validation."""
        op = object.__new__(BaseOperation)
        op.logger = logging.getLogger(__name__)
        
        params = {'id': '123', 'name': 'test'}
        # Should not raise
        op._validate_required_params(params, ['id', 'name'])
    
    def test_validate_required_params_missing(self):
        """Test validation with missing parameters."""
        op = object.__new__(BaseOperation)
        op.logger = logging.getLogger(__name__)
        
        params = {'id': '123'}
        with self.assertRaises(exc.ValidationError):
            op._validate_required_params(params, ['id', 'name'])
    
    def test_validate_required_params_none_values(self):
        """Test validation with None parameter values."""
        op = object.__new__(BaseOperation)
        op.logger = logging.getLogger(__name__)
        
        params = {'id': '123', 'name': None}
        with self.assertRaises(exc.ValidationError):
            op._validate_required_params(params, ['id', 'name'])


if __name__ == '__main__':
    unittest.main()
