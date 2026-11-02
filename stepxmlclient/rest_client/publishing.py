"""Optional bridge from Publishing jobs to existing REST v2 operations."""

from typing import List

from pydantic import ValidationError

from ..publishing import JobFile, JobStatus, PublishingError
from .exceptions import RestClientError
from .operations.background_processes import BackgroundProcessOperations


class V2PublishingJobBackend:
    def __init__(self, operations: BackgroundProcessOperations):
        self.operations = operations

    def get_status(self, process_id: str, *, timeout: float) -> JobStatus:
        try:
            result = self.operations.get_background_process(process_id, timeout=timeout)
        except RestClientError as error:
            raise PublishingError("REST v2 job status request failed", process_id=process_id,
                                  status_code=getattr(error, "status_code", None)) from error
        if result.id != process_id or not result.status:
            raise PublishingError("REST v2 returned an invalid job identity or status",
                                  process_id=process_id)
        return JobStatus(
            process_id=process_id, status=result.status, progress=result.progress,
            number_of_errors=result.number_of_errors,
            number_of_warnings=result.number_of_warnings,
        )

    def list_files(self, process_id: str, *, timeout: float) -> List[JobFile]:
        try:
            items = self.operations.get_attachments_metadata(process_id, timeout=timeout)
        except RestClientError as error:
            raise PublishingError("REST v2 attachment list request failed", process_id=process_id,
                                  status_code=getattr(error, "status_code", None)) from error
        try:
            files = [JobFile.model_validate({
                "id": item.get("id"), "name": item.get("name"),
                "mime_type": item.get("mimeType"),
                "original_attachment_id": item.get("originalAttachmentId"),
            }) for item in items]
        except ValidationError as error:
            raise PublishingError("Invalid REST v2 attachment metadata",
                                  process_id=process_id) from error
        if any(not f.id.strip() for f in files):
            raise PublishingError("REST v2 attachment has an empty ID", process_id=process_id)
        return files

    def get_file(self, process_id: str, attachment_id: str, *, timeout: float) -> bytes:
        try:
            return self.operations.get_attachment_content(process_id, attachment_id, timeout=timeout)
        except RestClientError as error:
            raise PublishingError("REST v2 attachment download failed", process_id=process_id,
                                  status_code=getattr(error, "status_code", None)) from error
