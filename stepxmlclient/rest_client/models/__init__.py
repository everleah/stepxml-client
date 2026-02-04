"""REST API models for STEP REST API v2.

Provides Pydantic models for request/response handling and validation.
"""

from .common import (
    PageInfo,
    PagedResponse,
    ErrorDetail,
    ErrorResponse,
    ApiResponse,
    SearchFilter,
    SearchRequest,
    SuccessResponse,
    ListResponse,
)
from .product import (
    ProductResponse,
    ProductListResponse,
    ProductSearchRequest,
    ProductCreateRequest,
    ProductUpdateRequest,
    ProductAttribute,
    ProductValue,
    CrossReference,
)

__all__ = [
    'PageInfo',
    'PagedResponse',
    'ErrorDetail',
    'ErrorResponse',
    'ApiResponse',
    'SearchFilter',
    'SearchRequest',
    'SuccessResponse',
    'ListResponse',
    'ProductResponse',
    'ProductListResponse',
    'ProductSearchRequest',
    'ProductCreateRequest',
    'ProductUpdateRequest',
    'ProductAttribute',
    'ProductValue',
    'CrossReference',
]
