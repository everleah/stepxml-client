"""Base operation class for REST API operations.

Provides common functionality for all operation classes including error handling,
pagination, logging, and request/response processing.
"""

import logging
from functools import wraps
from typing import Any, Callable, Dict, Optional, TypeVar

import requests
import requests_openapi as roa

from . import exceptions as exc
from .models.common import PageInfo

T = TypeVar('T')


def handle_rest_errors(func: Callable) -> Callable:
    """Decorator to handle common REST API errors.
    
    Converts HTTP errors to appropriate exception types.
    Allows FileNotFoundError and other file system exceptions to pass through.

    Also detects STEP API error responses returned as dicts when
    requests_openapi does not raise an exception for non-2xx HTTP responses.
    The STEP REST API returns error payloads with the form
    ``{"httpStatus": <int>, "message": "...", "httpReason": "..."}``.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            # Detect STEP error responses returned as plain dicts instead of
            # raised exceptions (requests_openapi may not call raise_for_status).
            if isinstance(result, dict) and 'httpStatus' in result:
                status = result.get('httpStatus', 0)
                message = result.get('message') or result.get('httpReason', 'API error')
                if status == 401:
                    raise exc.AuthenticationError(f"Authentication failed: {message}")
                elif status == 403:
                    raise exc.AuthorizationError(f"Access denied: {message}")
                elif status == 404:
                    raise exc.NotFoundError(None, details=result)
                elif status == 409:
                    raise exc.ConflictError(status, message)
                elif status == 429:
                    raise exc.RateLimitError(details=result)
                elif 500 <= status < 600:
                    raise exc.ServerError(status, message)
                elif 400 <= status < 500:
                    raise exc.RestApiError(status, message)
            return result
        except requests.exceptions.RequestException as e:
            # Handle requests library exceptions
            if hasattr(e, 'response') and e.response is not None:
                status = e.response.status_code
                try:
                    error_data = e.response.json()
                except Exception:
                    error_data = {"message": e.response.text}
                
                error_msg = error_data.get('error_message') or error_data.get('message', str(e))
                error_code = error_data.get('error_code')
                
                if status == 401:
                    raise exc.AuthenticationError(f"Authentication failed: {error_msg}")
                elif status == 403:
                    raise exc.AuthorizationError(f"Access denied: {error_msg}")
                elif status == 404:
                    raise exc.NotFoundError(None, details=error_data)
                elif status == 409:
                    raise exc.ConflictError(status, error_msg, error_code=error_code)
                elif status == 429:
                    retry_after = e.response.headers.get('Retry-After')
                    raise exc.RateLimitError(retry_after=retry_after, details=error_data)
                elif 500 <= status < 600:
                    raise exc.ServerError(status, error_msg, error_code=error_code)
                else:
                    raise exc.RestApiError(status, error_msg, error_code=error_code)
            else:
                raise exc.RestClientError(f"Request failed: {str(e)}")
        except (FileNotFoundError, OSError):
            # Let file system errors pass through unchanged
            raise
        except Exception as e:
            if isinstance(e, exc.RestClientError):
                raise
            raise exc.RestClientError(f"Unexpected error: {e!s}")
    
    return wrapper


class BaseOperation:
    """Base class for REST API operation groups.
    
    Provides common functionality for all operation classes:
    - Error handling
    - Pagination helpers
    - Logging
    - Response processing
    
    Attributes:
        client: The requests_openapi.Client instance
        logger: Logger instance for this operation group
        operation_name: Name of this operation group (for logging)
        context: STEP context ID passed to every API call
        workspace: STEP workspace ID passed to every API call (defaults to "Main" server-side)
    """
    
    def __init__(self, client: roa.Client, operation_name: str | None = None, 
                 logger: Optional[logging.Logger] = None,
                 context: str | None = None, workspace: str | None = None):
        """Initialize base operation.
        
        Args:
            client: The requests-openapi Client instance
            operation_name: Name of this operation group (defaults to class name)
            logger: Logger instance (defaults to class logger)
            context: STEP context ID to use for all API calls (required by STEP REST API)
            workspace: STEP workspace ID (server defaults to "Main" if not supplied)
        """
        self.client = client
        self.operation_name = operation_name or self.__class__.__name__
        self.context = context
        self.workspace = workspace
        
        if logger is None:
            self.logger = logging.getLogger(f"{self.__class__.__module__}.{self.operation_name}")
        else:
            self.logger = logger
    
    def _build_context_params(self) -> Dict[str, Any]:
        """Build context and workspace parameters for API calls.
        
        Returns:
            Dictionary containing context and/or workspace keys if set.
        """
        params: Dict[str, Any] = {}
        if self.context is not None:
            params['context'] = self.context
        if self.workspace is not None:
            params['workspace'] = self.workspace
        return params

    def _check_for_api_error(self, response: Any, resource_id: str | None = None,
                              resource_type: str | None = None) -> None:
        """Detect STEP error responses returned as dicts instead of raised exceptions.

        The STEP REST API may return an error body like
        ``{"httpStatus": 404, "message": "...", "httpReason": "..."}`` on a
        transport-level 200 when using requests_openapi without raise_for_status.
        This method raises the appropriate library exception in those cases.

        Args:
            response: The API response (dict, list, or object)
            resource_id: Resource ID for error messages
            resource_type: Resource type name for error messages

        Raises:
            AuthenticationError: If httpStatus is 401
            AuthorizationError: If httpStatus is 403
            NotFoundError: If httpStatus is 404
            ConflictError: If httpStatus is 409
            RestApiError: For other 4xx/5xx status codes
        """
        if not isinstance(response, dict) or 'httpStatus' not in response:
            return
        status = response.get('httpStatus', 0)
        message = response.get('message') or response.get('httpReason', 'API error')
        if status == 401:
            raise exc.AuthenticationError(f"Authentication failed: {message}")
        elif status == 403:
            raise exc.AuthorizationError(f"Access denied: {message}")
        elif status == 404:
            raise exc.NotFoundError(resource_id, resource_type)
        elif status == 409:
            raise exc.ConflictError(status, message)
        elif 400 <= status < 600:
            raise exc.RestApiError(status, message)

    def _check_response_status(self, response: Any, resource_id: str | None = None,
                                resource_type: str | None = None) -> None:
        """Check response for HTTP error status codes returned without raising an exception.
        
        Some STEP endpoints (e.g. binary content) return an HTTP error response body
        (e.g. an HTML 404 page) with a non-error HTTP status from the transport layer.
        This method inspects the underlying response object and raises the appropriate
        exception when an error status is detected.
        
        Args:
            response: The API response object
            resource_id: Resource ID for error messages
            resource_type: Resource type name for error messages
            
        Raises:
            NotFoundError: If status is 404
            RestApiError: For other 4xx/5xx status codes
        """
        # First check for STEP error dicts (JSON body with httpStatus field)
        self._check_for_api_error(response, resource_id, resource_type)

        raw_response = getattr(response, '_response', None) or getattr(response, 'response', None)
        status_code = (
            getattr(raw_response, 'status_code', None)
            or getattr(response, 'status_code', None)
        )
        if status_code is not None and isinstance(status_code, int) and status_code >= 400:
            if status_code == 404:
                raise exc.NotFoundError(resource_id, resource_type)
            raise exc.RestApiError(status_code, f"HTTP {status_code} for {resource_type} {resource_id}")

    def _log_operation(self, operation_id: str, params: Optional[Dict[str, Any]] = None) -> None:
        """Log an API operation.
        
        Args:
            operation_id: The OpenAPI operation ID
            params: Request parameters
        """
        self.logger.debug(
            f"Calling {self.operation_name}.{operation_id}",
            extra={"params": params}
        )

    @staticmethod
    def _coerce_list_payload(payload: Any) -> list[Any]:
        """Normalize list-like API payloads from various response shapes.

        Supports:
        - native lists
        - dicts with common wrapper keys such as items/results/data/values
        - response-like objects exposing json() or text
        - single-object payloads, which are returned as a one-item list
        """
        if payload is None:
            return []

        if isinstance(payload, list):
            return payload

        if isinstance(payload, dict):
            for key in ("items", "results", "data", "values"):
                value = payload.get(key)
                if isinstance(value, list):
                    return value
            if payload:
                return [payload]
            return []

        if hasattr(payload, "json"):
            try:
                parsed = payload.json()
            except Exception:
                parsed = None
            if parsed is not None:
                return BaseOperation._coerce_list_payload(parsed)

        if hasattr(payload, "text"):
            try:
                import json
                parsed = json.loads(payload.text)
            except Exception:
                parsed = None
            if parsed is not None:
                return BaseOperation._coerce_list_payload(parsed)

        return []
    
    def _process_response(self, response: Any) -> Any:
        """Process API response (hook for subclasses).
        
        Override this method in subclasses to add custom response processing.
        
        Args:
            response: Raw API response
            
        Returns:
            Processed response
        """
        return response
    
    def _build_pagination_params(self, limit: int = 20, offset: int = 0) -> Dict[str, Any]:
        """Build pagination parameters for requests.
        
        Args:
            limit: Number of items per page
            offset: Result offset
            
        Returns:
            Dictionary of pagination parameters
        """
        return {
            "limit": max(1, min(limit, 1000)),  # Clamp between 1 and 1000
            "offset": max(0, offset)
        }
    
    def _build_page_info(self, limit: int, offset: int, 
                        total: Optional[int] = None) -> PageInfo:
        """Build PageInfo object from pagination parameters.
        
        Args:
            limit: Items per page
            offset: Current offset
            total: Total items (if known)
            
        Returns:
            PageInfo instance
        """
        return PageInfo(
            limit=limit,
            offset=offset,
            total=total
        )
    
    def _get_paginated_results(self, operation_id: str, params: Optional[Dict[str, Any]] = None,
                              item_key: str = "items",
                              total_key: str = "total") -> tuple:
        """Execute paginated API call and extract items and total count.
        
        Args:
            operation_id: OpenAPI operation ID to call
            params: Request parameters (should include limit and offset)
            item_key: Key in response containing items list
            total_key: Key in response containing total count
            
        Returns:
            Tuple of (items, total) where total may be None if not in response
        """
        self._log_operation(operation_id, params)
        
        operation = getattr(self.client, operation_id)
        response = operation(**(params or {}))
        
        # Handle different response formats
        if isinstance(response, dict):
            items = response.get(item_key, [])
            total = response.get(total_key)
        else:
            # Handle object responses
            items = getattr(response, item_key, [])
            total = getattr(response, total_key, None)
        
        return items, total
    
    @handle_rest_errors
    def _call_operation(self, operation_id: str, **params) -> Any:
        """Call an OpenAPI operation with error handling.
        
        Args:
            operation_id: OpenAPI operation ID to call
            **params: Operation parameters
            
        Returns:
            Operation response
        """
        self._log_operation(operation_id, params)
        
        operation = getattr(self.client, operation_id)
        response = operation(**params)
        
        return self._process_response(response)
    
    def _validate_required_params(self, params: Dict[str, Any], 
                                  required: list) -> None:
        """Validate that required parameters are present.
        
        Args:
            params: Parameters to validate
            required: List of required parameter names
            
        Raises:
            ValidationError: If required parameters are missing
        """
        missing = [p for p in required if p not in params or params[p] is None]
        if missing:
            raise exc.ValidationError(f"Missing required parameters: {missing}")
    
    def _clean_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Remove None values from parameters.
        
        Args:
            params: Parameters to clean
            
        Returns:
            Cleaned parameters
        """
        return {k: v for k, v in params.items() if v is not None}
