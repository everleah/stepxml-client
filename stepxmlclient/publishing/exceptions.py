"""Errors raised by the independent Publishing client."""

from typing import Optional


class PublishingError(Exception):
    """Publishing HTTP, transport or response-contract failure."""

    def __init__(self, message: str, *, status_code: Optional[int] = None,
                 operation: Optional[str] = None,
                 process_id: Optional[str] = None):
        super().__init__(message)
        self.status_code = status_code
        self.operation = operation
        self.process_id = process_id


class PublishingConfigurationError(PublishingError):
    """The requested integration has not been configured."""


class PublishingJobError(PublishingError):
    """A background process did not complete successfully."""


class PublishingTimeoutError(PublishingJobError):
    """The job exceeded the caller's waiting deadline."""
