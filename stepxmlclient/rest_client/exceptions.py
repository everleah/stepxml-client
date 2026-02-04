"""REST API client exceptions.

Provides REST-specific exception classes for error handling in rest_client operations.
"""


class RestClientError(Exception):
    """Base exception for REST API client errors."""
    
    pass


class RestApiError(RestClientError):
    """Exception raised for API response errors.
    
    Attributes:
        status_code: HTTP status code from the API response
        error_message: Error message from the API
        error_code: API-specific error code if available
        details: Additional error details from response body
    """
    
    def __init__(self, status_code, error_message, error_code=None, details=None):
        self.status_code = status_code
        self.error_message = error_message
        self.error_code = error_code
        self.details = details
        message = f"API Error ({status_code}): {error_message}"
        if error_code:
            message += f" [Code: {error_code}]"
        super().__init__(message)


class AuthenticationError(RestClientError):
    """Exception raised for authentication failures."""
    
    pass


class AuthorizationError(RestClientError):
    """Exception raised for authorization failures (insufficient permissions)."""
    
    pass


class NotFoundError(RestApiError):
    """Exception raised when a requested resource is not found (HTTP 404)."""
    
    def __init__(self, resource_id, resource_type=None, details=None):
        message = f"Resource not found"
        if resource_type:
            message += f": {resource_type}"
        if resource_id:
            message += f" (ID: {resource_id})"
        super().__init__(404, message, error_code="NOT_FOUND", details=details)
        self.resource_id = resource_id
        self.resource_type = resource_type


class ValidationError(RestClientError):
    """Exception raised for request validation errors."""
    
    def __init__(self, validation_errors):
        self.validation_errors = validation_errors
        message = f"Validation error: {validation_errors}"
        super().__init__(message)


class ConflictError(RestApiError):
    """Exception raised for resource conflicts (HTTP 409)."""
    
    pass


class RateLimitError(RestApiError):
    """Exception raised when rate limit is exceeded (HTTP 429)."""
    
    def __init__(self, retry_after=None, details=None):
        super().__init__(429, "Rate limit exceeded", error_code="RATE_LIMITED", details=details)
        self.retry_after = retry_after


class ServerError(RestApiError):
    """Exception raised for server errors (HTTP 5xx)."""
    
    pass


class TimeoutError(RestClientError):
    """Exception raised when request times out."""
    
    pass


class OperationError(RestClientError):
    """Exception raised for operation-specific errors."""
    
    pass
