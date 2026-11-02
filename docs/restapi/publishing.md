# Publishing REST API

> **Subclient:** `client.publishing` | **Standalone import:** `from stepxmlclient.publishing import PublishingClient`
>
> **Source:** [`stepxmlclient/publishing/client.py`](../../stepxmlclient/publishing/client.py)

Publishing is a **separate API**, normally under `/restapi`, not an additional
REST v2 operation group. Its 16 endpoints are not included in the v2 totals of
200 operationIds and 22 tag groups. Both main clients expose the lazy subclient;
the standalone client needs no v2 configuration for these endpoints.

See [Publishing usage](../PUBLISHING_USAGE.md) for authentication, URL overrides,
session ownership and integrated/standalone setup.
See [Publishing state](../PUBLISHING_STATE.md) for specification limitations
and installation-specific checks still requiring an authorized STEP server.

## Conventions and parameters

All endpoint paths below are relative to the configured Publishing base URL.
`**options` in signatures accepts only these common optional keyword arguments:

| Python option | HTTP query name | Behavior |
|---|---|---|
| `context` | `context` | Explicit string overrides the client's context; omitted/`None` inherits it |
| `workspace` | `workspace` | Explicit string overrides the client's workspace; omitted/`None` inherits it |
| `version` | `version` | Publication version applied to table output; omitted/`None` is not sent |

These are not interchangeable with `version_id`, the edition selector offered
by specific methods. Its exact query/form spelling is listed below.
The typed methods do not accept arbitrary `format` or `xslt` transformations.
Path IDs must be nonempty strings without control characters; they are URL-encoded.

Structured GET responses use XML (`Accept: application/xml`).
Empty list containers return `[]`; malformed XML, unexpected roots or unexpected
list children raise an error. Empty HTTP 200 responses are not treated as absence.
Only `get_actual_page` interprets HTTP 204 as `None`.

## Operations

### Publications and sections

| Method signature | HTTP endpoint | Result |
|---|---|---|
| `list_publications(**options)` | GET `/publications` | `list[Publication]` from `Publications/Publication` |
| `get_publication(publication_id, **options)` | GET `/publications/{id}` | `Publication` |
| `get_publication_group(group_id, **options)` | GET `/publicationgroups/{id}` | `PublicationGroup`, including its publications |
| `get_section(section_id, **options)` | GET `/sections/{id}` | `PublicationSection` |
| `get_section_autopage(section_id, **options)` | GET `/sections/{id}/autopage` | `PublicationSection` |

All five expect HTTP 200. No `autopage` call occurs implicitly; this method
only exposes the dedicated GET endpoint. These endpoints do not provide
general publication/section creation or update operations.

### Actual and planned pages

| Method signature | HTTP endpoint | Result |
|---|---|---|
| `list_actual_pages(publication_id, *, version_id=None, **options)` | GET `/publications/{id}/pages` | HTTP 200: `list[ActualPage]` from `Pages/Page` |
| `list_planned_pages(publication_id, **options)` | GET `/publications/{id}/plannedpages` | HTTP 200: `list[PlannedPage]` |
| `get_actual_page(publication_id, planned_page_id, *, version_id=None, **options)` | GET `/publications/{id}/plannedpages/{pageid}/actualpage` | HTTP 200: `ActualPage`; HTTP 204: `None` |

`version_id`, when supplied, is sent as the query parameter **`versionid`**.
It is not supported by `list_planned_pages`.
`planned_page_id` refers to a planned page, not an actual-page ID.

### Stored DTP documents

| Method signature | HTTP endpoint | Result |
|---|---|---|
| `download_actual_page_document(publication_id, page_id, target, *, overwrite=False, **options)` | GET `/publications/{id}/pages/{pageid}/document` | HTTP 200: saved absolute `Path` |
| `download_planned_page_document(publication_id, page_id, target, *, version_id=None, overwrite=False, **options)` | GET `/publications/{id}/plannedpages/{pageid}/document` | HTTP 200: saved absolute `Path` |
| `delete_page_document(publication_id, page_id, *, confirm_delete=False, **options)` | DELETE `/publications/{id}/pages/{pageid}/document` | `DocumentDeletion(deleted, status_code)` |

The planned-page download sends `version_id` as query **`versionid`**.
Downloads request `application/octet-stream`; a missing document (HTTP 404) is
an error, not an empty file. `target` is an explicit local file path (`str` or
`Path`), not a directory or a server-supplied filename.

DELETE requires the exact boolean **`confirm_delete=True`** before any HTTP
request is made. It deletes the DTP document containing the actual page:
**other actual pages in the same document can be deleted as well**.
HTTP 200 means `deleted=True`; HTTP 204 means already absent (`deleted=False`).

### Generation jobs

All four methods below POST to `/pblbackgroundprocesses/{operation}` with
`application/x-www-form-urlencoded` data. Common options remain query
parameters. The response must be HTTP 201 with a valid `Location` header.

| Method signature | Operation path suffix | Form fields | Job result field |
|---|---|---|---|
| `create_indesign_package(page_id, **options)` | `CreateInDesignPackage` | `pageID` | `ZIP` |
| `create_actual_page_pdf(page_id, **options)` | `GetPDFOfActualPage` | `pageID` | `ATTACHMENT_PDF` |
| `create_planned_page_pdf(page_id, pdf_profile, version_id, **options)` | `GetPDFOfPlannedPage` | `pageID`, `pdfProfile`, `versionID` | `ATTACHMENT_PDF` |
| `create_planned_page_document(page_id, version_id, **options)` | `MountDocForPlan` | `pageID`, `versionID` | `None` |

All return `PublishingJob`; they start work but do not wait for completion.
Form fields must contain nonempty strings. Here `version_id` is required and
maps to **`versionID`**, not query `versionid` or common option `version`.

Package/actual-PDF methods take an actual-page ID; planned-PDF/mount methods
take a planned-page ID. An InDesign package may contain every actual page in
the same DTP document. Mount creates the stored DTP document: after successful
completion, use the planned-page document download rather than expecting a
PDF/ZIP attachment.

### DTP replacement upload

```python
upload_dtp_document(page_id, source, *, confirm_overwrite=False, **options)
```

- POST `/pblbackgroundprocesses/UploadDTPDocument`.
- `source`: path (`str` or `Path`) to a local file, opened in binary mode.
- Multipart form fields: **`pageID`** and **`file`**. The file part uses the
  local basename and `application/octet-stream`; requests supplies the boundary.
- Requires **`confirm_overwrite=True`**; otherwise no request/file open occurs.
- Returns `PublishingJob` with `result_field=None` after HTTP 201 plus `Location`.
- Requires an existing actual page; it replaces that page's entire DTP document,
  potentially overwriting multiple actual pages.

The implementation follows the specification prose's `pageID`; the vendor curl
example instead spells it `pageId`. This discrepancy still needs server verification.
There are no automatic retries of Publishing POST or DELETE requests.

## Response models

Models are exported from `stepxmlclient.publishing`.

| Model | Fields / mapping |
|---|---|
| `PublishingNode` | Optional `id`, `title`, `name`, `user_type_id`, `context`, `workspace`, `revision`; `attributes` retains original attributes and `raw_xml` retains the node XML |
| `Revision` | Optional `created`, `last_modified`, `modified_by`, `number`, `is_major` |
| `Publication` | Node fields plus `parent_id`, `dtp_system`, `pages_per_spread`, `versions`, `page_templates`, `product_templates`, `publication_template` |
| `PublicationGroup` | Node fields plus `publications` |
| `PublicationSection` | Node fields plus `publication`, `master_version`, `pages`, recursive `children` |
| `ActualPage` | Node fields plus `page_number`, `status`, `dtp_document_id` |
| `PlannedPage` | Node fields plus `page_number`, `status`, `section_id` |
| `PublishingJob` | `process_id`, original `location`, optional `result_field` |
| `JobStatus` | `process_id`, `status`, optional `progress`, `number_of_errors`, `number_of_warnings` |
| `JobFile` | Actual attachment `id`, optional `name`, `mime_type`, `original_attachment_id` |
| `DocumentDeletion` | `deleted: bool`, `status_code: int` |

Versions, templates and master versions use `PublishingNode`.
Collections default to empty lists; absent optional scalar/node fields are `None`.
`pages_per_spread` is **`str | None`**, matching XSD/OpenAPI: `"02"` remains
`"02"`, and an empty string is distinct from an absent attribute. Page numbers,
page statuses and revision timestamps are also strings, not numbers/enums/datetimes.
`Revision.is_major` is an optional boolean.

The decoder accepts unnamespaced and namespaced XML and both `UserTypeId` and
legacy `UserTypeID`. Embedded products/assets/classifications remain in `raw_xml`,
not v2 entity models. Publishing XML is not a STEP-XML exchange document.
The XSD is not enforced wholesale: its empty page-list definition and omitted
publication template children contradict documented examples.

## Job monitoring and result helpers

These helpers are **not additional Publishing endpoints**. They require an
injected `JobBackend`, automatically provided by both main clients. Standalone
clients without a backend can start jobs but cannot monitor or fetch attachments.
The default bridge delegates to [v2 Background Processes](background_processes.md).

| Method signature | Backend operation / result |
|---|---|
| `get_job_status(job)` | One status lookup; returns `JobStatus` |
| `wait_for_job(job, *, timeout=300, poll_interval=2)` | Polls status; returns successful `JobStatus` |
| `list_job_files(job)` | Lists attachment metadata; returns `list[JobFile]` |
| `download_job_file(job, attachment_id, target, *, overwrite=False)` | Downloads the specified actual attachment ID; returns saved `Path` |
| `download_job_result(job, target, *, overwrite=False)` | Lists results and downloads exactly one match; returns saved `Path` |

`job` is a `PublishingJob`. The process ID is extracted from a Location such as
`/restapi/bgpinstance/BGP_16722/status`; that legacy URL is **never requested**.
With the v2 backend, monitoring uses `/background-processes/{id}` and attachment
metadata/content use `/background-processes/{id}/attachments` and
`/background-processes/{id}/attachments/{attachmentId}/content`, relative to v2.

`wait_for_job` uses a monotonic total deadline. `timeout` and `poll_interval`
must be finite and positive; each status-request timeout is capped at the
remaining wait time. `waiting` and `running` continue polling; only `succeeded`
returns normally. `completedwitherrors`, `failed`, `suspended`, `aborted`,
`unexpected`, unknown status values and process-ID mismatches raise job errors.

`list_job_files` filters `original_attachment_id` against `job.result_field`
when set (`ZIP` or `ATTACHMENT_PDF`); otherwise it lists all attachments.
The **actual `JobFile.id`** is used for downloading. Multiple attachments can
share the same original field: `download_job_result` raises on zero or multiple
matches instead of choosing one. An explicit `download_job_file` neither filters
nor waits for job completion; call `wait_for_job` first when appropriate.

## Errors and file handling

| Condition | Behavior |
|---|---|
| HTTP outside the operation's accepted statuses, including redirects | `PublishingError`, with HTTP `status_code` |
| Transport failure, malformed XML/fields, missing or invalid job Location | `PublishingError` |
| No job backend or invalid main-client Publishing configuration | `PublishingConfigurationError` |
| Unsuccessful/unknown job status or mismatched process identity while waiting | `PublishingJobError` |
| Overall wait deadline exceeded | `PublishingTimeoutError` |
| Missing destructive confirmation, invalid IDs/forms/timeouts | `ValueError` |
| Unsupported common keyword option | `TypeError` |
| Existing target without overwrite / local filesystem failure | `FileExistsError` / `OSError` |

`PublishingError` exposes optional `status_code`, `operation` and `process_id`;
not every error populates all three. v2 backend failures are translated into
Publishing errors. Credentials and server response bodies are not logged.

HTTP request timeout defaults to 30 seconds; standalone construction accepts
`timeout=...`, and the subclient exposes `.timeout`. It is separate from the
overall `wait_for_job` deadline. Publishing redirects are not followed.
Downloads default to `overwrite=False`. Direct DTP downloads stream through
a temporary file; failed transfers clean up partial files and preserve existing
targets. Atomic no-overwrite publication uses filesystem hard links, so unsupported
filesystems report `OSError`. v2 attachment downloads buffer bytes and are not
memory-bounded streaming downloads.

## Examples

The following read/download example is complete apart from replacing server,
credentials and IDs with authorized values:

```python
from stepxmlclient.publishing import PublishingClient

with PublishingClient(
    "https://step.example/restapi",
    auth=("user", "password"),
    context="Context1",
    workspace="Main",
) as publishing:
    publication = publishing.get_publication("PUBLICATION")
    pages = publishing.list_planned_pages(publication.id)
    if pages:
        page = publishing.get_actual_page(
            publication.id, pages[0].id, version_id="VERSION",
        )
        if page is not None:
            publishing.download_actual_page_document(
                publication.id, page.id, "stored-document.indd",
            )
```

For complete generation/monitor/download and explicitly confirmed replacement/
deletion examples, see the [Publishing usage guide](../PUBLISHING_USAGE.md).
