# Publishing implementation state

## Implemented

- Independent `stepxmlclient.publishing.PublishingClient`, with requests,
  Pydantic and standard-library XML; no new dependencies.
- All 16 documented operations: 10 GET, 5 POST and 1 DELETE.
- Typed publications/groups, sections, versions/templates, actual/planned pages,
  revisions and job/file results; unmodeled XML retained.
- Lazy `.publishing` on both main clients with borrowed authentication/session,
  context/workspace inheritance and explicit URL/client overrides.
- Injected job backend and separate v2 adapter; Publishing imports no v2 code.
- v2 status polling with deadlines, result-field mapping to real attachment IDs,
  multiple-file listing and explicit/single-result downloads.
- Explicit confirmation for DTP replacement and deletion.
- HTTP/error/shape validation, streamed direct DTP downloads and partial cleanup.
- Offline endpoint, XML, job, transport and release safeguards tests.

## Reference limitations

The local Publishing OpenAPI and WADL describe the same 16 operations.
OpenAPI has malformed parameter declarations, incomplete page-list/upload
schemas, and response tables that omit documented 200/204 alternatives and
the job Location header. Upload prose uses `pageID`, while its curl example
uses `pageId`; the implementation follows the prose.
The locally supplied, Git-ignored `openapi_pub.json` is optionally included in
wheel and sdist, but is not needed by Publishing at runtime or by offline tests.
WADL and XSD remain excluded from releases.

The supplied Publishing XSD is self-contained and compiles successfully. It
confirms unnamespaced XML, optional node/revision fields, direct Publication
children in groups, Versions/Version nesting and recursive Children/Section.
`PagesPerSpread` is `xs:string`, not an integer: `pages_per_spread` preserves
the string, including leading zeroes, empty and nonnumeric values. Page numbers,
statuses and revision timestamps are also strings, not enums/datetime values.

The XSD does not resolve every discrepancy: `actualPageList` is empty, rejecting
the populated Pages shown in WADL examples; publication template children shown
in those examples are also absent from `publicationSO`. Therefore it is a
reference for model alignment, not an unconditional runtime validation gate.
The decoder continues to support documented page/template content and tolerates
namespaced variants. The XSD defines no HTTP/upload/job/attachment contracts,
so those integration uncertainties remain unchanged.

No legacy v1 job-monitoring API is implemented. Background-process identity is
shared with v2 according to the integration requirement. The local v2 contract
documents status, attachment metadata and binary-content endpoints, but
cross-API job visibility and the concrete `ZIP`/`ATTACHMENT_PDF` mapping have
not been verified against a live server.

## Boundaries

- No general publication/planned-page create/update CRUD beyond the supplied API.
- No modification of STEP-XML parser, creator or XML entity models.
- No arbitrary `format`/`xslt` transformations in typed methods.
- No implicit job start, destructive action, legacy-Location request or POST retry.
- No automatic selection of the first of several matching result files.
- v2 attachment content is buffered; only direct DTP downloads stream.
- Shared requests sessions are not guaranteed thread-safe.

## Verification

```powershell
python -m unittest discover -s tests -p "test_publishing_*.py"
python -m unittest tests.test_rest_client_phase8_background_processes tests.test_release
```

Live acceptance requires an authorized installation: read publications/pages,
generate PDF and ZIP, inspect the same process ID through v2, confirm attachment
metadata, and download the actual files. Test replacement/deletion only against
explicitly authorized disposable documents.

See [Publishing usage](PUBLISHING_USAGE.md).
