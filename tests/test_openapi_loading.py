"""Offline tests for local specifications and authenticated server bootstrap."""

import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch
from urllib.parse import urlsplit

import requests
import requests_openapi
from requests.adapters import BaseAdapter

from stepxmlclient.client import BasicAuthorisation, StiboStepRestClient
from stepxmlclient.rest_client import StepRestClient


SPEC = {
    "openapi": "3.0.3",
    "info": {"title": "Synthetic bootstrap test", "version": "1"},
    "servers": [{"url": "/not-the-configured-server"}],
    "paths": {
        "/probe": {"get": {
            "operationId": "getProbe",
            "responses": {"200": {"description": "OK"}},
        }},
    },
}


class BootstrapAdapter(BaseAdapter):
    def __init__(self):
        self.calls = []
        self.status = 200
        self.spec_body = json.dumps(SPEC).encode()

    def send(self, request, **kwargs):
        self.calls.append((request, kwargs))
        is_spec = urlsplit(request.url).path.endswith("/specification/openapi.json")
        status = self.status
        if request.headers.get("Authorization") != "Basic dXNlcjpwd2Q=":
            status = 401
        result = requests.Response()
        result.request = request
        result.url = request.url
        result.status_code = status
        result._content = self.spec_body if is_spec else b'{"ok":true}'
        result.headers["Content-Type"] = "application/json"
        if status == 302:
            result.headers["Location"] = "https://other.invalid/specification/openapi.json"
        return result

    def close(self):
        pass


class TestOpenApiLoading(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.cache = self.directory / "cache.json"
        self.session = requests.Session()
        self.session.trust_env = False
        self.addCleanup(self.session.close)
        self.adapter = BootstrapAdapter()
        self.session.mount("https://", self.adapter)
        self.client_factory = Mock(wraps=requests_openapi.Client)
        self.session_patch = patch("stepxmlclient.client.roa.Client",
                                   side_effect=lambda **kwargs: self.client_factory(
                                       requestor=self.session, **kwargs))
        self.session_patch.start()
        self.addCleanup(self.session_patch.stop)
        unsafe_fetch = patch("requests_openapi.core.requests.get",
                             side_effect=requests.HTTPError("Unauthenticated specification fetch"))
        unsafe_fetch.start()
        self.addCleanup(unsafe_fetch.stop)
        bundled = patch.object(StiboStepRestClient, "_get_bundled_openapi_file", return_value=None)
        bundled.start()
        self.addCleanup(bundled.stop)
        cache = patch.object(StiboStepRestClient, "_OPENAPI_CACHE_FILE", str(self.cache))
        cache.start()
        self.addCleanup(cache.stop)

    def create(self, cls=StiboStepRestClient, **options):
        return cls("https://step.invalid/Proxy/restapiv2",
                   BasicAuthorisation("user", "pwd"), **options)

    def write_spec(self, name):
        path = self.directory / name
        path.write_text(json.dumps(SPEC), encoding="utf-8")
        return path

    def test_remote_spec_and_operations_use_same_authenticated_session(self):
        for cls in (StiboStepRestClient, StepRestClient):
            with self.subTest(cls=cls):
                self.adapter.calls.clear()
                client = self.create(cls, proxies={"https": "http://proxy.invalid"}, nocert=True)
                self.assertIs(client.client.requestor, self.session)
                self.assertEqual(len(self.adapter.calls), 1)
                request, options = self.adapter.calls[0]
                self.assertEqual(request.headers["Authorization"], "Basic dXNlcjpwd2Q=")
                self.assertEqual(request.url,
                                 "https://step.invalid/Proxy/restapiv2/specification/openapi.json")
                self.assertFalse(options["verify"])
                self.assertEqual(options["proxies"]["https"], "http://proxy.invalid")
                self.assertGreater(options["timeout"], 0)
                result = client.client.getProbe()
                result.raise_for_status()
                self.assertEqual(result.json(), {"ok": True})
                self.assertEqual(self.adapter.calls[-1][0].url,
                                 "https://step.invalid/Proxy/restapiv2/probe")
                self.assertIs(client.publishing.session, self.session)
        self.assertFalse(self.cache.exists())

    def test_explicit_file_has_priority_over_cache_and_no_bootstrap_request(self):
        local = self.write_spec("explicit.json")
        self.cache.write_text("invalid cache must not be read", encoding="utf-8")
        client = self.create(openapi_file=str(local), cache_openapi=True)
        self.assertTrue(callable(client.client.getProbe))
        self.assertEqual(self.adapter.calls, [])

    def test_cache_has_priority_and_no_bootstrap_request(self):
        self.write_spec("cache.json")
        client = self.create(cache_openapi=True)
        self.assertTrue(callable(client.client.getProbe))
        self.assertEqual(self.adapter.calls, [])

    def test_existing_bundled_source_remains_compatible(self):
        bundled = self.write_spec("legacy-bundled.json")
        with patch.object(StiboStepRestClient, "_get_bundled_openapi_file",
                          return_value=str(bundled)):
            self.create()
        self.assertEqual(self.adapter.calls, [])

    def test_remote_cache_is_saved_only_when_enabled(self):
        self.create(cache_openapi=True)
        self.assertEqual(json.loads(self.cache.read_text(encoding="utf-8")), SPEC)
        self.assertEqual(len(self.adapter.calls), 1)
        self.adapter.calls.clear()
        self.create(cache_openapi=True)
        self.assertEqual(self.adapter.calls, [])

    def test_missing_explicit_file_without_cache_fails_without_network(self):
        with self.assertRaises(FileNotFoundError):
            self.create(openapi_file=str(self.directory / "missing.json"))
        self.assertEqual(self.adapter.calls, [])

    def test_missing_explicit_file_with_cache_retains_server_fallback(self):
        self.create(openapi_file=str(self.directory / "missing.json"), cache_openapi=True)
        self.assertTrue(self.cache.exists())

    def test_http_errors_and_redirects_do_not_create_cache_or_retry(self):
        for status in (401, 403, 404, 500, 302, 204):
            with self.subTest(status=status):
                self.adapter.calls.clear()
                self.adapter.status = status
                with self.assertRaises(requests.HTTPError):
                    self.create(cache_openapi=True)
                self.assertEqual(len(self.adapter.calls), 1)
                self.assertFalse(self.cache.exists())

    def test_invalid_remote_json_is_not_cached(self):
        for body in (b"not json", b'{"not":"an OpenAPI specification"}'):
            with self.subTest(body=body):
                self.adapter.spec_body = body
                with self.assertRaises(ValueError):
                    self.create(cache_openapi=True)
                self.assertFalse(self.cache.exists())

    def test_transport_timeout_is_not_cached_or_retried(self):
        with patch.object(self.adapter, "send", side_effect=requests.Timeout("bootstrap timeout")) as send:
            with self.assertRaises(requests.Timeout):
                self.create(cache_openapi=True)
            send.assert_called_once()
        self.assertFalse(self.cache.exists())

    def test_invalid_requestor_response_is_an_explicit_error(self):
        with patch.object(self.session, "request", return_value=None):
            with self.assertRaisesRegex(TypeError, "must return a requests.Response"):
                self.create(cache_openapi=True)
        self.assertFalse(self.cache.exists())

    def test_custom_authorisation_hooks_run_once_and_local_hooks_see_spec(self):
        events = []
        session = self.session

        class CustomAuthorisation:
            def adapt_client(self, client):
                events.append("adapt")
                client.requestor.auth = ("user", "pwd")

            def do_authorisation(self, client):
                events.append("authorise")
                client.requestor.headers["X-Custom-Auth"] = "configured"

        client = StiboStepRestClient("https://step.invalid/restapiv2", CustomAuthorisation())
        self.assertEqual(events, ["adapt", "authorise"])
        self.assertEqual(self.adapter.calls[0][0].headers["X-Custom-Auth"], "configured")
        self.assertIs(client.client.requestor, session)
        events.clear()
        local = self.write_spec("local.json")

        class SchemaAuthorisation(CustomAuthorisation):
            def adapt_client(self, client):
                self_probe = client.getProbe
                assert callable(self_probe)
                super().adapt_client(client)

        StiboStepRestClient("https://step.invalid/restapiv2", SchemaAuthorisation(),
                           openapi_file=str(local))
        self.assertEqual(events, ["adapt", "authorise"])


if __name__ == "__main__":
    unittest.main()
