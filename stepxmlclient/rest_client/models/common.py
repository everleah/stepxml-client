"""Common REST API models and utilities.

Provides shared Pydantic models for pagination, error responses, and generic
API response envelopes used across all REST operations.
"""

from typing import TypeVar, Generic, Optional, Any, List, Dict
from pydantic import BaseModel, Field, computed_field, ConfigDict

T = TypeVar('T')


class PageInfo(BaseModel):
    """Pagination metadata for paginated responses.
    
    Attributes:
        offset: Current offset in result set
        limit: Number of results per page
        total: Total number of items available (if known)
        has_more: Whether more results are available (computed)
    """
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "offset": 0,
                "limit": 20,
                "total": 150,
                "has_more": True
            }
        }
    )
    
    offset: int = Field(0, ge=0, description="Current offset in result set")
    limit: int = Field(20, ge=1, le=1000, description="Number of results per page")
    total: Optional[int] = Field(None, ge=0, description="Total number of items available")
    
    @computed_field
    @property
    def has_more(self) -> bool:
        """Calculate if more results are available."""
        if self.total is None:
            return False
        return (self.offset + self.limit) < self.total


class PagedResponse(BaseModel, Generic[T]):
    """Generic paginated response wrapper.
    
    Wraps list results with pagination metadata.
    
    Attributes:
        items: List of items in this page
        pagination: Pagination metadata
    """
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "items": [],
                "pagination": {
                    "offset": 0,
                    "limit": 20,
                    "total": 100,
                    "has_more": True
                }
            }
        }
    )
    
    items: List[T] = Field(default_factory=list, description="Items in this page")
    pagination: Optional[PageInfo] = Field(None, description="Pagination metadata")


class ErrorDetail(BaseModel):
    """Individual error detail in an error response.
    
    Attributes:
        code: Machine-readable error code
        message: Human-readable error message
        field: Field name if error is field-specific
        details: Additional context-specific details
    """
    
    code: str = Field(..., description="Machine-readable error code")
    message: str = Field(..., description="Human-readable error message")
    field: Optional[str] = Field(None, description="Field name if field-specific")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional details")


class ErrorResponse(BaseModel):
    """Standard API error response.
    
    Attributes:
        error_code: Primary error code
        error_message: Primary error message
        status: HTTP status code
        timestamp: ISO 8601 timestamp of error occurrence
        request_id: Unique request identifier for debugging
        error_details: List of detailed error information
    """
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "error_code": "VALIDATION_ERROR",
                "error_message": "Request validation failed",
                "status": 400,
                "timestamp": "2024-02-04T10:30:00Z",
                "request_id": "req-12345",
                "error_details": [
                    {
                        "code": "REQUIRED_FIELD",
                        "message": "Field 'name' is required",
                        "field": "name"
                    }
                ]
            }
        }
    )
    
    error_code: str = Field(..., description="Primary error code")
    error_message: str = Field(..., description="Primary error message")
    status: int = Field(..., ge=400, le=599, description="HTTP status code")
    timestamp: Optional[str] = Field(None, description="ISO 8601 timestamp")
    request_id: Optional[str] = Field(None, description="Unique request identifier")
    error_details: Optional[List[ErrorDetail]] = Field(None, description="Detailed error info")


class ApiResponse(BaseModel, Generic[T]):
    """Generic API response envelope.
    
    Standard wrapper for single-item API responses.
    
    Attributes:
        data: Response data of generic type T
        metadata: Optional metadata about the response
        success: Whether the operation was successful
        timestamp: ISO 8601 timestamp of response
    """
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "data": {},
                "success": True,
                "timestamp": "2024-02-04T10:30:00Z"
            }
        }
    )
    
    data: Optional[T] = Field(None, description="Response data")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Response metadata")
    success: bool = Field(True, description="Operation success flag")
    timestamp: Optional[str] = Field(None, description="ISO 8601 timestamp")


class SearchFilter(BaseModel):
    """Search filter specification.
    
    Attributes:
        field: Field name to filter on
        value: Filter value
        operator: Comparison operator (eq, ne, gt, lt, contains, in, etc.)
    """
    
    field: str = Field(..., description="Field name")
    value: Any = Field(..., description="Filter value")
    operator: str = Field("eq", description="Comparison operator")


class SearchRequest(BaseModel):
    """Generic search request.
    
    Attributes:
        query: Free-text search query
        filters: List of search filters
        limit: Maximum results to return
        offset: Offset for pagination
        sort: Sort specification (field:asc|desc)
    """
    
    query: Optional[str] = Field(None, description="Free-text search query")
    filters: Optional[List[SearchFilter]] = Field(None, description="Search filters")
    limit: int = Field(20, ge=1, le=1000, description="Maximum results")
    offset: int = Field(0, ge=0, description="Result offset")
    sort: Optional[str] = Field(None, description="Sort specification")


# Type aliases for common response types
SuccessResponse = ApiResponse[Dict[str, Any]]
ListResponse = PagedResponse[Dict[str, Any]]
