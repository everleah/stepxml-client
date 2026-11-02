"""Backend-neutral background process monitoring."""

import math
import time
from typing import List, Optional, Protocol
from urllib.parse import unquote, urlsplit

from .exceptions import PublishingError, PublishingJobError, PublishingTimeoutError
from .models import JobFile, JobStatus, PublishingJob


class JobBackend(Protocol):
    def get_status(self, process_id: str, *, timeout: float) -> JobStatus: ...

    def list_files(self, process_id: str, *, timeout: float) -> List[JobFile]: ...

    def get_file(self, process_id: str, attachment_id: str, *, timeout: float) -> bytes: ...


def positive(value: float, name: str) -> float:
    if not math.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be finite and greater than zero")
    return value


def job_from_location(location: str, result_field: Optional[str] = None) -> PublishingJob:
    try:
        parts = urlsplit(location)
    except ValueError as error:
        raise PublishingError("Invalid Publishing job Location") from error
    path = parts.path.rstrip("/").split("/")
    if (parts.scheme not in ("", "http", "https") or
            (parts.scheme and not parts.netloc) or
            len(path) < 3 or path[-3] != "bgpinstance" or path[-1] != "status"):
        raise PublishingError("Invalid Publishing job Location")
    process_id = unquote(path[-2])
    if (not process_id.strip() or process_id in (".", "..") or
            any(ord(c) < 32 or c in "/\\?#" for c in process_id)):
        raise PublishingError("Invalid Publishing process ID")
    return PublishingJob(process_id=process_id, location=location, result_field=result_field)


def wait(backend: JobBackend, job: PublishingJob, *, timeout: float,
         poll_interval: float, request_timeout: float) -> JobStatus:
    deadline = time.monotonic() + positive(timeout, "timeout")
    positive(poll_interval, "poll_interval")
    positive(request_timeout, "request_timeout")
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise PublishingTimeoutError("Publishing job timed out", process_id=job.process_id)
        status = backend.get_status(job.process_id, timeout=min(request_timeout, remaining))
        if time.monotonic() >= deadline:
            raise PublishingTimeoutError("Publishing job timed out", process_id=job.process_id)
        if status.process_id != job.process_id:
            raise PublishingJobError("Background process ID mismatch", process_id=job.process_id)
        if status.status == "succeeded":
            return status
        if status.status not in ("waiting", "running"):
            raise PublishingJobError(
                f"Publishing job ended with status {status.status}", process_id=job.process_id)
        time.sleep(min(poll_interval, max(0, deadline - time.monotonic())))
