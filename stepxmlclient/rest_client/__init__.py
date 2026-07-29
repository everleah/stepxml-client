"""REST API client for STEP REST API v2.

Provides comprehensive, typed access to STEP REST API operations through
organized operation groups with shared authentication.
"""

from . import exceptions
from .base import BaseOperation, handle_rest_errors
from .client import StepRestClient

__all__ = [
    'BaseOperation',
    'StepRestClient',
    'exceptions',
    'handle_rest_errors',
]
