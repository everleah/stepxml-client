"""System information operations for STEP REST API v2.

Covers the /system-information endpoint introduced in v1.4.0.
"""

import logging
from typing import Any, Optional

from ..base import BaseOperation, handle_rest_errors


class SystemInformationOperations(BaseOperation):
    """Operations for STEP system information."""

    def __init__(self, client, logger: Optional[logging.Logger] = None,
                 context: Optional[str] = None, workspace: Optional[str] = None):
        super().__init__(client, operation_name="SystemInformationOperations", logger=logger,
                         context=context, workspace=workspace)

    @handle_rest_errors
    def get_system_information(self) -> dict[str, Any]:
        """Get system information and capabilities.

        Calls: GET /system-information -> getSystemInformation
        """
        self._log_operation("getSystemInformation", {})
        response = self.client.getSystemInformation(**self._build_context_params())
        return response if isinstance(response, dict) else response
