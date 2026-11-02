# Publishing REST API

The independent Publishing client complements REST v2 with publications, sections,
planned/actual pages, DTP documents and generation jobs. It does not implement a
general publication/page CRUD API. No additional Python dependencies are required.

## Integrated use

```python
from stepxmlclient.client import BasicAuthorisation
from stepxmlclient.rest_client import StepRestClient

client = StepRestClient(
    "https://step.example/Proxy/restapiv2",
    BasicAuthorisation("user", "password"),
    context="Context1",
    workspace="Main",
)

publications = client.publishing.list_publications()
pages = client.publishing.list_actual_pages("PUBLICATION", version_id="VERSION")

job = client.publishing.create_actual_page_pdf("ACTUAL_PAGE")
status = client.publishing.wait_for_job(job, timeout=300, poll_interval=2)
client.publishing.download_job_result(job, "output.pdf")
```

Both `StepRestClient` and `StiboStepRestClient` expose a cached, lazy `.publishing`.
Accessing that property makes no request and loads no Publishing specification.
The first actual operation contacts the server. Existing v2 operations are unchanged.

The terminal `/restapiv2` is replaced with `/restapi`, preserving proxy prefixes.
For another layout supply `publishing_base_url="https://step.example/custom/publishing"`
to the main client. If the base is ambiguous, supply that URL rather than relying
on guessing. A different origin requires an explicitly configured
`publishing_client=PublishingClient(...)`; inherited credentials are not sent there.
An explicitly supplied client keeps its own configuration and job backend; the
main client does not mutate it or automatically attach a backend to it.

The subclient borrows the main client's authenticated requests session, including
TLS and proxy settings. It does not alter global headers/authentication and does
not close that session. Shared-session use is not promised to be thread-safe.
The existing main client remains responsible for its session lifecycle.

## Standalone use

```python
from stepxmlclient.publishing import PublishingClient

with PublishingClient(
    "https://step.example/restapi",
    auth=("user", "password"),
    context="Context1",
    workspace="Main",
) as publishing:
    publication = publishing.get_publication("PUBLICATION")
```

Alternatively pass a configured `requests.Session` with `session=...`; do not
also pass `auth`. Owned sessions are closed by `close()` or the context manager;
borrowed sessions are neither globally modified nor closed.

All sixteen Publishing endpoints work standalone. Job starts return
`PublishingJob(process_id, location, result_field)`. Status/wait/attachment methods
additionally require a `JobBackend`. They fail explicitly if none is configured.
The Publishing package never imports v2 operations or models.

An application with a separately configured v2 client can opt in to the bridge:

```python
from stepxmlclient.publishing import PublishingClient
from stepxmlclient.rest_client.publishing import V2PublishingJobBackend

with PublishingClient(
    "https://step.example/restapi",
    auth=("user", "password"),
    job_backend=V2PublishingJobBackend(client.background_processes),
) as publishing:
    job = publishing.create_indesign_package("ACTUAL_PAGE")
    publishing.wait_for_job(job)
    publishing.download_job_result(job, "package.zip")
```

## Publishing operations

The [Publishing detail reference](restapi/publishing.md) documents all 16
operations with exact call signatures, HTTP endpoints, parameter mappings,
response models and errors, plus the job monitoring/download helpers.
Use it for the distinction between `version`, query `versionid` and form
`versionID`, and for XML model field types such as `pages_per_spread`.
This guide focuses on setup and end-to-end workflows rather than duplicating
the per-operation reference.

## Replacement and deletion

```python
job = client.publishing.upload_dtp_document(
    "ACTUAL_PAGE", "replacement.indd", confirm_overwrite=True,
)
client.publishing.wait_for_job(job)

result = client.publishing.delete_page_document(
    "PUBLICATION", "ACTUAL_PAGE", confirm_delete=True,
)
print(result.deleted)  # 200: deleted; 204: already absent
```

**These operations can affect every page in the same DTP document.**
Without the exact boolean confirmation they fail before making a request.
Upload requires an existing actual page/document. There are no automatic retries
of Publishing POST or DELETE operations.

## Jobs and result files

- The old `Location` supplies only the process ID. Its URL is never followed.
- The main client automatically attaches the v2 backend for monitoring/downloads.
- `wait_for_job` uses a monotonic deadline. Request timeout defaults to 30 seconds;
  standalone construction accepts `timeout=...`. `client.publishing.timeout` can
  also be set before use. Polling caps each status-request timeout at time remaining.
- `succeeded` is success. `waiting`/`running` are polled. `failed`,
  `completedwitherrors`, `aborted`, `suspended`, `unexpected` and unknown statuses
  raise `PublishingJobError`, not success-shaped results.
- `get_job_status(job)` is a single status lookup without waiting.
- PDF/ZIP result selection matches v2 `originalAttachmentId` to the job's result
  field. Downloads use the actual v2 attachment `id`.
- Multiple files may share the same original field. `download_job_result`
  requires exactly one match; zero or multiple matches are explicit errors.

```python
files = client.publishing.list_job_files(job)
for index, file in enumerate(files):
    client.publishing.download_job_file(job, file.id, f"result-{index}.bin")
```

Targets are explicit local file paths, never unchecked server-supplied filenames.
Downloads do not overwrite existing files unless `overwrite=True`.
Direct DTP downloads stream to a temporary file; failed transfers leave existing
targets intact and clean up partial files. Atomic no-overwrite publication uses
filesystem hard links; unsupported filesystems report an `OSError`.
The existing v2 attachment wrapper buffers bytes, so job-result downloads are not
advertised as memory-bounded streaming.

## Errors and server prerequisites

`PublishingError` includes optional `status_code`, `operation` and `process_id`.
`PublishingConfigurationError` reports missing integration configuration;
`PublishingJobError` reports unsuccessful jobs and `PublishingTimeoutError`
reports a polling deadline. Invalid local arguments raise `ValueError`; local
file errors remain filesystem exceptions. Malformed/unexpected XML, missing
Location, HTTP errors and ambiguous files are never silently converted to success.
Publishing does not log credentials or server response bodies.

The server needs the relevant Publishing functionality, DTP integration and user
permissions. The supplied Publishing XSD is available as a local reference,
but is not enforced on responses: its empty page-list definition and missing
publication template children contradict documented examples.
Offline tests cover contracts, not installation-specific server compatibility.
Before production use verify the shared Publishing/v2 process IDs, actual
attachment-field mapping, upload's `pageID` spelling and XML variants on an
authorized STEP installation. Upload/delete tests need dedicated test documents.
