"""REST API client for STEP REST API v2.

Provides comprehensive, typed access to STEP REST API operations through
organized operation groups with shared authentication.
"""

from .client import StepRestClient
from .base import BaseOperation, handle_rest_errors
from . import exceptions

__all__ = [
    'StepRestClient',
    'BaseOperation',
    'handle_rest_errors',
    'exceptions',
]
