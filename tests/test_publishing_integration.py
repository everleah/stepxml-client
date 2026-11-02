"""Offline end-to-end integration using real requests-openapi and a fake HTTP adapter."""

import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock
from urllib.parse import parse_qs, urlsplit

import requests

from stepxmlclient.client import BasicAuthorisation, StiboStepRestClient
from stepxmlclient.publishing import PublishingClient, PublishingConfigurationError, PublishingError
from stepxmlclient.rest_client import StepRestClient
from tests.test_publishing_client import response


def local_spec():
    paths = {}
    for path, operation, binary in (
        ("/background-processes/{id}", "getBackgroundProcess", False),
        ("/background-processes/{id}/attachments", "getBackgroundProcessAttachmentsMetadata", False),
        ("/background-processes/{id}/attachments/{attachmentId}/content",
         "getBackgroundProcessAttachmentContent", True),
    ):
        params = [{"name": "id", "in": "path", "required": True, "schema": {"type": "string"}}]
        if "{attachmentId}" in path:
            params.append({"name": "attachmentId", "in": "path", "required": True,
                           "schema": {"type": "string"}})
        params.extend({"name": key, "in": "query", "schema": {"type": "string"}}
                      for key in ("context", "workspace"))
        paths[path] = {"get": {
            "operationId": operation, "parameters": params,
            "responses": {"200": {"description": "synthetic fixture",
                                  "content": {("application/octet-stream" if binary
                                               else "application/json"): {
                                      "schema": {"type": "string" if binary else "object"}}}}},
        }}
    return {"openapi": "3.0.3", "info": {"title": "Synthetic test", "version": "1"},
            "servers": [{"url": "/restapiv2"}], "paths": paths}


class OfflineAdapter(requests.adapters.BaseAdapter):
    def __init__(self):
        self.calls = []
        self.status = 200
        self.job_status = "succeeded"
        self.result_field = "ATTACHMENT_PDF"

    def send(self, request, **kwargs):
        self.calls.append((request, kwargs))
        path = urlsplit(request.url).path
        if request.method == "POST":
            self.result_field = "ZIP" if path.endswith("/CreateInDesignPackage") else "ATTACHMENT_PDF"
            result = response(status=201, Location="/restapi/bgpinstance/BGP_16722/status")
        elif path.endswith("/content"):
            content = b"PK\x00\xff" if self.result_field == "ZIP" else b"%PDF\x00\xff"
            result = response(content, status=self.status)
        elif path.endswith("/attachments"):
            result = response(json.dumps([
                {"id": "REAL_ID", "originalAttachmentId": self.result_field,
                 "name": "print.pdf", "mimeType": "application/pdf"}
            ]).encode(), status=self.status)
        elif "/background-processes/" in path:
            result = response(json.dumps({
                "id": "BGP_16722", "status": self.job_status, "numberOfWarnings": 2,
                "numberOfErrors": 0, "executionTimeMillis": 50,
                "backgroundProcessType": "Publishing",
            }).encode(), status=self.status)
        else:
            result = response(b'<Publications><Publication ID="P"/></Publications>')
        result.request = request
        result.url = request.url
        return result

    def close(self):
        pass


class TestPublishingIntegration(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.spec = Path(self.temporary.name) / "synthetic.json"
        self.spec.write_text(json.dumps(local_spec()), encoding="utf-8")

    def make_client(self, cls=StepRestClient, **options):
        client = cls(
            "https://STEP/Proxy/restapiv2", BasicAuthorisation("user", "pwd"),
            openapi_file=str(self.spec), context="C", workspace="Approved", **options)
        self.adapter = OfflineAdapter()
        client.client.requestor.mount("https://", self.adapter)
        self.addCleanup(client.client.requestor.close)
        return client

    def test_lazy_cached_property_and_no_requests_for_both_entry_points(self):
        for cls in (StepRestClient, StiboStepRestClient):
            with self.subTest(cls=cls):
                client = self.make_client(cls)
                self.assertEqual(self.adapter.calls, [])
                publishing = client.publishing
                self.assertIs(publishing, client.publishing)
                self.assertEqual(self.adapter.calls, [])
                self.assertEqual(publishing.base_url, "https://STEP/Proxy/restapi")
                self.assertIs(publishing.session, client.client.requestor)
                self.assertEqual((publishing.context, publishing.workspace), ("C", "Approved"))
                if isinstance(client, StepRestClient):
                    self.assertIs(publishing.job_backend.operations, client.background_processes)

    def test_full_pdf_workflow_with_real_transport_and_no_legacy_status_request(self):
        client = self.make_client()
        session = client.client.requestor
        original_headers = session.headers.copy()
        self.assertEqual(client.publishing.list_publications()[0].id, "P")
        job = client.publishing.create_actual_page_pdf("A")
        status = client.publishing.wait_for_job(job)
        self.assertEqual(status.number_of_warnings, 2)
        self.assertEqual(status.number_of_errors, 0)
        target = Path(self.temporary.name) / "result.pdf"
        client.publishing.download_job_result(job, target)
        self.assertEqual(target.read_bytes(), b"%PDF\x00\xff")
        self.assertEqual(session.headers, original_headers)
        paths = []
        for request, kwargs in self.adapter.calls:
            paths.append(urlsplit(request.url).path)
            self.assertEqual(request.headers["Authorization"], "Basic dXNlcjpwd2Q=")
            params = parse_qs(urlsplit(request.url).query)
            self.assertEqual(params, {"context": ["C"], "workspace": ["Approved"]})
            self.assertGreater(kwargs["timeout"], 0)
        self.assertFalse(any("/bgpinstance/" in path for path in paths))
        self.assertTrue(paths[-1].endswith("/BGP_16722/attachments/REAL_ID/content"))

    def test_real_form_and_multipart_encoding(self):
        client = self.make_client()
        client.publishing.create_planned_page_pdf("L", "print", "V")
        request = self.adapter.calls[-1][0]
        self.assertEqual(request.headers["Content-Type"], "application/x-www-form-urlencoded")
        self.assertEqual(parse_qs(request.body), {
            "pageID": ["L"], "pdfProfile": ["print"], "versionID": ["V"]})
        source = Path(self.temporary.name) / "test.indd"
        source.write_bytes(b"INDD")
        client.publishing.upload_dtp_document("A", source, confirm_overwrite=True)
        request = self.adapter.calls[-1][0]
        self.assertTrue(request.headers["Content-Type"].startswith("multipart/form-data;"))
        self.assertIn(b'name="pageID"', request.body)
        self.assertIn(b'name="file"; filename="test.indd"', request.body)

    def test_zip_generation_monitoring_and_download(self):
        client = self.make_client()
        job = client.publishing.create_indesign_package("A")
        self.assertEqual(job.result_field, "ZIP")
        client.publishing.wait_for_job(job)
        target = Path(self.temporary.name) / "package.zip"
        client.publishing.download_job_result(job, target)
        self.assertEqual(target.read_bytes(), b"PK\x00\xff")

    def test_override_origin_and_explicit_client(self):
        client = self.make_client(publishing_base_url="https://step/Custom/publishing")
        self.assertEqual(client.publishing.base_url, "https://step/Custom/publishing")
        client = self.make_client(publishing_base_url="https://other/restapi")
        with self.assertRaises(PublishingConfigurationError):
            _ = client.publishing
        independent = PublishingClient("https://other/restapi", auth=("other", "secret"))
        self.addCleanup(independent.close)
        client = self.make_client(publishing_client=independent)
        self.assertIs(client.publishing, independent)

    def test_borrowed_session_retains_proxy_tls_and_lifecycle(self):
        client = self.make_client()
        session = client.client.requestor
        session.proxies["https"] = "http://proxy.invalid"
        session.verify = False
        session.close = Mock()
        publishing = client.publishing
        publishing.close()
        session.close.assert_not_called()
        self.assertFalse(publishing.session.verify)
        self.assertEqual(publishing.session.proxies["https"], "http://proxy.invalid")

    def test_http_failure_in_each_v2_stage_is_not_empty_success(self):
        client = self.make_client()
        job = client.publishing.create_actual_page_pdf("A")
        self.adapter.status = 404
        for call in (
            lambda: client.publishing.get_job_status(job),
            lambda: client.publishing.list_job_files(job),
            lambda: client.publishing.download_job_file(
                job, "REAL_ID", Path(self.temporary.name) / "never-created"),
        ):
            with self.assertRaises(PublishingError):
                call()
        self.assertFalse((Path(self.temporary.name) / "never-created").exists())


if __name__ == "__main__":
    unittest.main()
