"""Base operation class for REST API operations.

Provides common functionality for all operation classes including error handling,
pagination, logging, and request/response processing.
"""

import logging
from functools import wraps
from typing import Any, Callable, Dict, NoReturn, Optional, TypeVar

import requests
import requests_openapi as roa

from . import exceptions as exc
from .models.common import PageInfo

T = TypeVar('T')


def _read_json_response(response: requests.Response) -> Any:
    try:
        return response.json()
    except ValueError as error:
        raise exc.RestClientError(f"Invalid JSON response: {error}") from error


def _raise_api_error(status: int, payload: Any, *, response: Any = None,
                     resource_id: str | None = None,
                     resource_type: str | None = None) -> None:
    if status < 400:
        return
    details = payload if isinstance(payload, dict) else {"message": payload}
    message = "; ".join(dict.fromkeys(
        str(details[key]) for key in ("error_message", "message", "httpReason", "detail")
        if details.get(key)
    )) or f"HTTP {status}"
    error_code = details.get("error_code")
    if status == 401:
        raise exc.AuthenticationError(message, details=details)
    if status == 403:
        raise exc.AuthorizationError(message, details=details)
    if status == 404:
        raise exc.NotFoundError(resource_id, resource_type, details=details, error_message=message)
    if status == 429:
        headers = getattr(response, "headers", {})
        raise exc.RateLimitError(retry_after=headers.get("Retry-After"), details=details,
                                 error_message=message)
    error_type = exc.ConflictError if status == 409 else (
        exc.ServerError if status >= 500 else exc.RestApiError
    )
    raise error_type(status, message, error_code=error_code, details=details)


def _check_response(response: Any, resource_id: str | None = None,
                    resource_type: str | None = None) -> None:
    raw_response = getattr(response, "_response", None)
    if raw_response is None:
        raw_response = getattr(response, "response", None)
    if raw_response is None:
        raw_response = response
    status = getattr(raw_response, "status_code", None)
    if isinstance(status, int) and status >= 400:
        payload = None
        read_json = getattr(raw_response, "json", None)
        if callable(read_json):
            try:
                payload = read_json()
            except ValueError:
                payload = getattr(raw_response, "text", None)
        if payload is None:
            payload = getattr(raw_response, "text", None) or getattr(raw_response, "reason", None)
        _raise_api_error(status, payload, response=raw_response,
                         resource_id=resource_id, resource_type=resource_type)
    if isinstance(response, dict):
        status = response.get("httpStatus")
        if isinstance(status, str) and status.isdecimal():
            status = int(status)
        if isinstance(status, int):
            _raise_api_error(status, response, resource_id=resource_id,
                             resource_type=resource_type)


def _raise_request_error(error: requests.exceptions.RequestException,
                         resource_id: str | None = None) -> NoReturn:
    if error.response is not None:
        try:
            _check_response(error.response, resource_id)
        finally:
            error.response.close()
    if isinstance(error, requests.exceptions.Timeout):
        raise exc.TimeoutError(f"Request timed out: {error}") from error
    raise exc.RestClientError(f"Request failed: {error}") from error


def handle_rest_errors(func: Callable) -> Callable:
    """Decorator to handle common REST API errors.
    
    Converts HTTP errors to appropriate exception types.
    Allows FileNotFoundError and other file system exceptions to pass through.

    Also detects HTTP responses and STEP error dictionaries when
    requests_openapi does not raise an exception for non-2xx HTTP responses.
    The STEP REST API returns error payloads with the form
    ``{"httpStatus": <int>, "message": "...", "httpReason": "..."}``.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            _check_response(result)
            return result
        except requests.exceptions.RequestException as e:
            _raise_request_error(e)
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
        _check_response(response, resource_id, resource_type)

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
        _check_response(response, resource_id, resource_type)

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
        """Check errors and decode HTTP JSON before operation-specific processing."""
        if isinstance(response, requests.Response):
            try:
                self._check_response_status(response)
                if not response.content:
                    return None
                payload = _read_json_response(response)
                self._check_for_api_error(payload)
                return payload
            finally:
                response.close()
        self._check_response_status(response)
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
        
        response = self._call_operation(operation_id, **(params or {}))
        
        # Handle different response formats
        if isinstance(response, list):
            items = response
            total = None
        elif isinstance(response, dict):
            items = response.get(item_key, [])
            total = response.get(total_key)
        else:
            items = getattr(response, item_key, None)
            total = getattr(response, total_key, None)
        if not isinstance(items, list):
            raise exc.RestClientError("List response must be an array or an object containing an items array")
        
        return items, total
    
    def _call_operation(self, operation_id: str, *, _raw_response: bool = False,
                        **params) -> Any:
        """Call an OpenAPI operation with error handling.
        
        Args:
            operation_id: OpenAPI operation ID to call
            _raw_response: Preserve a checked binary HTTP response for the caller
            **params: Operation parameters
            
        Returns:
            Operation response
        """
        self._log_operation(operation_id, params)
        
        operation = getattr(self.client, operation_id)
        try:
            response = operation(**params)
        except requests.exceptions.RequestException as error:
            _raise_request_error(error, params.get("id"))
        try:
            self._check_response_status(response, params.get("id"))
            if _raw_response and isinstance(response, requests.Response):
                if "json" in response.headers.get("Content-Type", "").lower() and response.content:
                    self._check_for_api_error(_read_json_response(response), params.get("id"))
        except exc.RestClientError:
            if isinstance(response, requests.Response):
                response.close()
            raise
        if _raw_response:
            return response
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
