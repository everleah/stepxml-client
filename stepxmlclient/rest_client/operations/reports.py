"""Reporting operations for STEP REST API v2."""
from typing import Any, Optional

from ..base import BaseOperation, handle_rest_errors


class ReportOperations(BaseOperation):
    def __init__(self, client, logger=None, context=None, workspace=None):
        super().__init__(client, operation_name="ReportOperations", logger=logger, context=context, workspace=workspace)

    @handle_rest_errors
    def start_historic_changes_report(self, report_id: str, data: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        self._validate_required_params({"report_id": report_id}, ["report_id"])
        self._log_operation("startHistoricChangesReport", {"reportID": report_id})
        kwargs: dict[str, Any] = {"id": report_id}
        kwargs.update(self._build_context_params())
        if data is not None:
            kwargs["json"] = data
        r = self.client.startHistoricChangesReport(**kwargs)
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def clean_up_historic_changes_report(self, report_id: str) -> dict[str, Any]:
        self._validate_required_params({"report_id": report_id}, ["report_id"])
        self._log_operation("cleanUpHistoricChangesReport", {"reportID": report_id})
        r = self.client.cleanUpHistoricChangesReport(id=report_id, **self._build_context_params())
        return r if isinstance(r, dict) else r
