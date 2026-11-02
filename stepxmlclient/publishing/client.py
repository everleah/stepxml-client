"""Independent client for the STEP Publishing REST API."""

import logging
import os
from pathlib import Path
import tempfile
from typing import BinaryIO, Dict, Iterable, List, Optional, Tuple, Type, TypeVar, Union
from urllib.parse import quote, urlsplit, urlunsplit

import requests
from requests.auth import AuthBase

from . import xml
from .exceptions import PublishingConfigurationError, PublishingError
from .jobs import JobBackend, job_from_location, positive, wait
from .models import (
    ActualPage, DocumentDeletion, JobFile, JobStatus, PlannedPage, Publication,
    PublicationGroup, PublicationSection, PublishingJob, PublishingNode,
)

N = TypeVar("N", bound=PublishingNode)
UploadFiles = Dict[str, Tuple[str, BinaryIO, str]]


def validate_base_url(value: str) -> str:
    parts = urlsplit(value)
    if (parts.scheme not in ("http", "https") or not parts.hostname or
            parts.username is not None or parts.password is not None or
            parts.query or parts.fragment):
        raise ValueError("Publishing base URL must be an HTTP(S) URL without credentials or query")
    return value.rstrip("/")


def derive_base_url(v2_url: str) -> str:
    parts = urlsplit(validate_base_url(v2_url))
    path = parts.path.rstrip("/")
    if not path.endswith("/restapiv2"):
        raise PublishingConfigurationError(
            "Cannot derive Publishing URL; supply publishing_base_url explicitly")
    return urlunsplit(parts._replace(path=path[:-len("/restapiv2")] + "/restapi"))


def same_origin(first: str, second: str) -> bool:
    def origin(url: str) -> Tuple[str, Optional[str], int]:
        p = urlsplit(validate_base_url(url))
        return p.scheme, p.hostname, p.port or (443 if p.scheme == "https" else 80)
    return origin(first) == origin(second)


def identifier(value: str) -> str:
    if not isinstance(value, str) or not value.strip() or any(ord(c) < 32 for c in value):
        raise ValueError("Publishing IDs must be nonempty strings without control characters")
    if value in (".", ".."):
        raise ValueError("Publishing IDs cannot be path traversal segments")
    return quote(value, safe="")


class PublishingClient:
    """Publishing HTTP operations with an optional, injected job backend.

    A supplied session is borrowed and never closed or globally modified.
    Authentication, proxies and TLS can be configured on that session.
    """

    def __init__(
        self, base_url: str, *,
        session: Optional[requests.Session] = None,
        auth: Optional[Union[Tuple[str, str], AuthBase]] = None,
        context: Optional[str] = None, workspace: Optional[str] = None,
        job_backend: Optional[JobBackend] = None,
        timeout: float = 30, logger: Optional[logging.Logger] = None,
    ):
        self.base_url = validate_base_url(base_url)
        self.timeout = positive(timeout, "timeout")
        if session is not None and auth is not None:
            raise ValueError("Configure auth on the borrowed session, not on both arguments")
        self._owns_session = session is None
        self.session = session if session is not None else requests.Session()
        if auth is not None:
            self.session.auth = auth
        self.context = context
        self.workspace = workspace
        self.job_backend = job_backend
        self.logger = logger if logger is not None else logging.getLogger(__name__)

    def close(self) -> None:
        if self._owns_session:
            self.session.close()

    def __enter__(self) -> "PublishingClient":
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def _params(self, *, context: Optional[str] = None,
                workspace: Optional[str] = None,
                version: Optional[str] = None) -> Dict[str, str]:
        return {key: value for key, value in {
            "context": self.context if context is None else context,
            "workspace": self.workspace if workspace is None else workspace,
            "version": version,
        }.items() if value is not None}

    def _request(self, method: str, path: str, *, expected: Tuple[int, ...] = (200,),
                 params: Optional[Dict[str, str]] = None,
                 data: Optional[Dict[str, str]] = None,
                 files: Optional[UploadFiles] = None, stream: bool = False,
                 accept: str = "application/xml") -> requests.Response:
        operation = f"{method} {path.split('/')[0]}"
        self.logger.debug("Publishing %s", operation)
        try:
            response = self.session.request(
                method, f"{self.base_url}/{path}", params=params, data=data,
                files=files, headers={"Accept": accept}, timeout=self.timeout,
                stream=stream, allow_redirects=False,
            )
        except requests.RequestException as error:
            raise PublishingError("Publishing transport failed", operation=operation) from error
        if response.status_code not in expected:
            status = response.status_code
            response.close()
            raise PublishingError(
                f"Publishing returned HTTP {status}", status_code=status, operation=operation)
        return response

    def _read(self, path: str, tag: str, model: Type[N], **options: Optional[str]) -> N:
        with self._request("GET", path, params=self._params(**options)) as response:
            return xml.decode(xml.root(response.content, tag), model)

    def _list(self, path: str, container: str, tag: str,
              model: Type[N], params: Dict[str, str]) -> List[N]:
        with self._request("GET", path, params=params) as response:
            root = xml.root(response.content, container)
            if any(xml.local_tag(e) != tag for e in root):
                raise PublishingError(f"Unexpected elements in Publishing {container}")
            return [xml.decode(e, model) for e in xml.children(root, tag)]

    def list_publications(self, **options: Optional[str]) -> List[Publication]:
        return self._list("publications", "Publications", "Publication", Publication,
                          self._params(**options))

    def get_publication(self, publication_id: str, **options: Optional[str]) -> Publication:
        return self._read(f"publications/{identifier(publication_id)}",
                          "Publication", Publication, **options)

    def get_publication_group(self, group_id: str,
                              **options: Optional[str]) -> PublicationGroup:
        return self._read(f"publicationgroups/{identifier(group_id)}",
                          "PublicationGroup", PublicationGroup, **options)

    def get_section(self, section_id: str, **options: Optional[str]) -> PublicationSection:
        return self._read(f"sections/{identifier(section_id)}",
                          "Section", PublicationSection, **options)

    def get_section_autopage(self, section_id: str,
                            **options: Optional[str]) -> PublicationSection:
        return self._read(f"sections/{identifier(section_id)}/autopage",
                          "Section", PublicationSection, **options)

    def list_actual_pages(self, publication_id: str, *, version_id: Optional[str] = None,
                          **options: Optional[str]) -> List[ActualPage]:
        params = self._params(**options)
        if version_id is not None:
            params["versionid"] = version_id
        return self._list(f"publications/{identifier(publication_id)}/pages",
                          "Pages", "Page", ActualPage, params)

    def list_planned_pages(self, publication_id: str,
                           **options: Optional[str]) -> List[PlannedPage]:
        return self._list(f"publications/{identifier(publication_id)}/plannedpages",
                          "PlannedPages", "PlannedPage", PlannedPage, self._params(**options))

    def get_actual_page(self, publication_id: str, planned_page_id: str, *,
                        version_id: Optional[str] = None,
                        **options: Optional[str]) -> Optional[ActualPage]:
        path = (f"publications/{identifier(publication_id)}/plannedpages/"
                f"{identifier(planned_page_id)}/actualpage")
        params = self._params(**options)
        if version_id is not None:
            params["versionid"] = version_id
        with self._request("GET", path, expected=(200, 204), params=params) as response:
            if response.status_code == 204:
                return None
            return xml.decode(xml.root(response.content, "Page"), ActualPage)

    @staticmethod
    def _save(chunks: Iterable[bytes], target: Union[str, Path], *, overwrite: bool) -> Path:
        path = Path(target).absolute()
        if not path.name or path.is_dir():
            raise ValueError("Download target must be a file path")
        if path.exists() and not overwrite:
            raise FileExistsError(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".publishing-", delete=False) as f:
                temporary = Path(f.name)
                for chunk in chunks:
                    if chunk:
                        f.write(chunk)
            if overwrite:
                os.replace(temporary, path)
            else:
                # Atomic no-overwrite publication, including concurrent writers.
                os.link(temporary, path)
            return path
        except requests.RequestException as error:
            raise PublishingError("Publishing download interrupted") from error
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)

    def _download(self, path: str, target: Union[str, Path], params: Dict[str, str], *,
                  overwrite: bool) -> Path:
        with self._request("GET", path, params=params, stream=True,
                           accept="application/octet-stream") as response:
            return self._save(response.iter_content(chunk_size=1024 * 1024),
                              target, overwrite=overwrite)

    def download_actual_page_document(self, publication_id: str, page_id: str,
                                      target: Union[str, Path], *, overwrite: bool = False,
                                      **options: Optional[str]) -> Path:
        return self._download(
            f"publications/{identifier(publication_id)}/pages/{identifier(page_id)}/document",
            target, self._params(**options), overwrite=overwrite)

    def download_planned_page_document(
        self, publication_id: str, page_id: str, target: Union[str, Path], *,
        version_id: Optional[str] = None, overwrite: bool = False,
        **options: Optional[str],
    ) -> Path:
        params = self._params(**options)
        if version_id is not None:
            params["versionid"] = version_id
        return self._download(
            f"publications/{identifier(publication_id)}/plannedpages/{identifier(page_id)}/document",
            target, params, overwrite=overwrite)

    def delete_page_document(self, publication_id: str, page_id: str, *,
                             confirm_delete: bool = False,
                             **options: Optional[str]) -> DocumentDeletion:
        """Delete the DTP document, potentially including multiple actual pages."""
        if confirm_delete is not True:
            raise ValueError("Deleting all pages in the DTP document requires confirm_delete=True")
        path = f"publications/{identifier(publication_id)}/pages/{identifier(page_id)}/document"
        with self._request("DELETE", path, expected=(200, 204),
                           params=self._params(**options)) as response:
            return DocumentDeletion(deleted=response.status_code == 200,
                                    status_code=response.status_code)

    def _start(self, operation: str, data: Dict[str, str], *,
               result_field: Optional[str] = None, files: Optional[UploadFiles] = None,
               **options: Optional[str]) -> PublishingJob:
        for value in data.values():
            if not isinstance(value, str) or not value.strip():
                raise ValueError("Publishing form values must be nonempty strings")
        with self._request("POST", f"pblbackgroundprocesses/{operation}",
                           expected=(201,), params=self._params(**options), data=data,
                           files=files, accept="text/plain") as response:
            location = response.headers.get("Location")
            if not location:
                raise PublishingError("Publishing job response has no Location",
                                      operation=operation, status_code=201)
            return job_from_location(location, result_field)

    def create_indesign_package(self, page_id: str, **options: Optional[str]) -> PublishingJob:
        return self._start("CreateInDesignPackage", {"pageID": page_id},
                           result_field="ZIP", **options)

    def create_actual_page_pdf(self, page_id: str, **options: Optional[str]) -> PublishingJob:
        return self._start("GetPDFOfActualPage", {"pageID": page_id},
                           result_field="ATTACHMENT_PDF", **options)

    def create_planned_page_pdf(self, page_id: str, pdf_profile: str, version_id: str,
                               **options: Optional[str]) -> PublishingJob:
        return self._start("GetPDFOfPlannedPage",
                           {"pageID": page_id, "pdfProfile": pdf_profile, "versionID": version_id},
                           result_field="ATTACHMENT_PDF", **options)

    def create_planned_page_document(self, page_id: str, version_id: str,
                                    **options: Optional[str]) -> PublishingJob:
        return self._start("MountDocForPlan", {"pageID": page_id, "versionID": version_id}, **options)

    def upload_dtp_document(self, page_id: str, source: Union[str, Path], *,
                            confirm_overwrite: bool = False,
                            **options: Optional[str]) -> PublishingJob:
        """Replace the DTP document containing the page, including its other pages."""
        if confirm_overwrite is not True:
            raise ValueError("Replacing the DTP document requires confirm_overwrite=True")
        path = Path(source)
        with path.open("rb") as f:
            return self._start("UploadDTPDocument", {"pageID": page_id},
                               files={"file": (path.name, f, "application/octet-stream")}, **options)

    def _backend(self) -> JobBackend:
        if self.job_backend is None:
            raise PublishingConfigurationError("Job monitoring requires a configured job_backend")
        return self.job_backend

    def get_job_status(self, job: PublishingJob) -> JobStatus:
        return self._backend().get_status(job.process_id, timeout=self.timeout)

    def wait_for_job(self, job: PublishingJob, *, timeout: float = 300,
                     poll_interval: float = 2) -> JobStatus:
        return wait(self._backend(), job, timeout=timeout, poll_interval=poll_interval,
                    request_timeout=self.timeout)

    def list_job_files(self, job: PublishingJob) -> List[JobFile]:
        files = self._backend().list_files(job.process_id, timeout=self.timeout)
        if job.result_field is None:
            return files
        return [f for f in files if f.original_attachment_id == job.result_field]

    def download_job_file(self, job: PublishingJob, attachment_id: str,
                          target: Union[str, Path], *, overwrite: bool = False) -> Path:
        identifier(attachment_id)
        content = self._backend().get_file(job.process_id, attachment_id, timeout=self.timeout)
        return self._save((content,), target, overwrite=overwrite)

    def download_job_result(self, job: PublishingJob, target: Union[str, Path], *,
                            overwrite: bool = False) -> Path:
        """Download a single matching result; never guess between multiple files."""
        files = self.list_job_files(job)
        if len(files) != 1:
            raise PublishingError(
                f"Expected one Publishing result file, found {len(files)}",
                process_id=job.process_id)
        return self.download_job_file(job, files[0].id, target, overwrite=overwrite)
