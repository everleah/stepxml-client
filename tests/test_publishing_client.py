"""Offline Publishing contracts: all sixteen endpoints and XML edge cases."""

import ast
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

import requests

from stepxmlclient.publishing import (
    PublishingClient, PublishingConfigurationError, PublishingError,
)
from stepxmlclient.publishing.client import derive_base_url


def response(body=b"", status=200, **headers):
    result = requests.Response()
    result.status_code = status
    result._content = body
    result._content_consumed = True
    result.headers.update(headers)
    result.close = Mock(wraps=result.close)
    return result


class TestPublishingClient(unittest.TestCase):
    def setUp(self):
        self.session = Mock(spec=requests.Session)
        self.client = PublishingClient(
            "https://step/Proxy/restapi", session=self.session, context="C", workspace="Main")

    def assert_request(self, method, path, **expected):
        args, kwargs = self.session.request.call_args
        self.assertEqual(args, (method, "https://step/Proxy/restapi/" + path))
        self.assertEqual(kwargs["timeout"], 30)
        self.assertFalse(kwargs["allow_redirects"])
        for key, value in expected.items():
            if key == "accept":
                self.assertEqual(kwargs["headers"]["Accept"], value)
            else:
                self.assertEqual(kwargs[key], value)

    def test_all_structured_get_operations(self):
        cases = [
            ("list_publications", (), b'<Publications><Publication ID="P"/></Publications>',
             "publications", True),
            ("get_publication", ("P",), b'<Publication ID="P"/>', "publications/P", False),
            ("get_publication_group", ("G",),
             b'<PublicationGroup ID="G"><Publication ID="P"/></PublicationGroup>',
             "publicationgroups/G", False),
            ("get_section", ("S",), b'<Section ID="S"/>', "sections/S", False),
            ("get_section_autopage", ("S",), b'<Section ID="S"/>', "sections/S/autopage", False),
            ("list_actual_pages", ("P",), b'<Pages><Page ID="A"/></Pages>',
             "publications/P/pages", True),
            ("list_planned_pages", ("P",), b'<PlannedPages><PlannedPage ID="L"/></PlannedPages>',
             "publications/P/plannedpages", True),
            ("get_actual_page", ("P", "L"), b'<Page ID="A"/>',
             "publications/P/plannedpages/L/actualpage", False),
        ]
        for name, args, body, path, is_list in cases:
            with self.subTest(name=name):
                result_response = response(body)
                self.session.request.return_value = result_response
                result = getattr(self.client, name)(*args)
                self.assertEqual(len(result), 1) if is_list else self.assertIsNotNone(result.id)
                self.assert_request("GET", path, params={"context": "C", "workspace": "Main"})
                result_response.close.assert_called_once()

    def test_namespaces_templates_revisions_and_unmodeled_xml(self):
        self.session.request.return_value = response(b"""
            <p:Publication xmlns:p="urn:publishing" ID="P" UserTypeID="Type"
                           PagesPerSpread="2" DTPSystem="InDesign" Custom="keep">
              <p:Name>Catalog</p:Name>
              <p:Revision RevisionNumber="0.2" IsMajor="true"/>
              <p:PageTemplates><p:PageTemplate ID="T"/></p:PageTemplates>
              <p:ProductTemplates><p:ProductTemplate ID="PT"/></p:ProductTemplates>
              <p:PublicationTemplate ID="ROOT"/>
              <p:Versions><p:Version ID="V"/></p:Versions>
              <p:Extension>retained</p:Extension>
            </p:Publication>""")
        publication = self.client.get_publication("P")
        self.assertEqual(publication.name, "Catalog")
        self.assertEqual(publication.user_type_id, "Type")
        self.assertEqual(publication.pages_per_spread, 2)
        self.assertTrue(publication.revision.is_major)
        self.assertEqual(publication.revision.number, "0.2")
        self.assertEqual(publication.versions[0].id, "V")
        self.assertEqual(publication.page_templates[0].id, "T")
        self.assertEqual(publication.product_templates[0].id, "PT")
        self.assertEqual(publication.publication_template.id, "ROOT")
        self.assertEqual(publication.attributes["Custom"], "keep")
        self.assertIn("retained", publication.raw_xml)

    def test_section_children_and_legacy_entity_payload_preserved(self):
        self.session.request.return_value = response(b"""
          <Section ID="S" UserTypeId="section">
            <Publication ID="P"/><MasterVersion ID="V"/>
            <Pages><Page ID="A" PageNumber="iv" DTPDocumentID="D" Status="Draft"/></Pages>
            <Children><Section ID="SUB"/></Children>
            <Products><Product ID="PRODUCT"/></Products>
          </Section>""")
        section = self.client.get_section("S")
        self.assertEqual(section.publication.id, "P")
        self.assertEqual(section.master_version.id, "V")
        self.assertEqual(section.pages[0].page_number, "iv")
        self.assertEqual(section.pages[0].dtp_document_id, "D")
        self.assertEqual(section.children[0].id, "SUB")
        self.assertIn("PRODUCT", section.raw_xml)

    def test_version_parameters_are_distinct(self):
        self.session.request.return_value = response(b"<Pages/>")
        self.client.list_actual_pages("P", version_id="edition", version="table",
                                      context="Override", workspace="Approved")
        self.assertEqual(self.session.request.call_args.kwargs["params"], {
            "context": "Override", "workspace": "Approved",
            "version": "table", "versionid": "edition",
        })

    def test_unsupported_query_options_fail_before_http(self):
        for name, args in (
            ("list_publications", ()), ("list_planned_pages", ("P",)),
            ("download_actual_page_document", ("P", "A", "not-written")),
        ):
            with self.subTest(name=name), self.assertRaises(TypeError):
                getattr(self.client, name)(*args, version_id="unsupported")
        self.session.request.assert_not_called()

    def test_missing_actual_page_is_none_but_not_empty_200(self):
        self.session.request.return_value = response(status=204)
        self.assertIsNone(self.client.get_actual_page("P", "L", version_id="V"))
        self.assertEqual(self.session.request.call_args.kwargs["params"]["versionid"], "V")
        self.session.request.return_value = response()
        with self.assertRaises(PublishingError):
            self.client.get_actual_page("P", "L")

    def test_valid_empty_list(self):
        self.session.request.return_value = response(b"<Publications/>")
        self.assertEqual(self.client.list_publications(), [])

    def test_malformed_wrong_root_and_unsafe_xml_rejected(self):
        for body in (b"", b"<Publication", b"<NotPublications/>",
                     b"<Publications><Error>unauthorized</Error></Publications>",
                     b'<?xml version="1.0" encoding="not-a-codec"?><Publications/>',
                     b'<!DOCTYPE Publications [<!ENTITY x "x">]><Publications/>',
                     '<!DOCTYPE Publications><Publications/>'.encode("utf-16")):
            with self.subTest(body=body):
                self.session.request.return_value = response(body)
                with self.assertRaises(PublishingError):
                    self.client.list_publications()

    def test_invalid_typed_fields_are_not_silently_discarded(self):
        for body in (b'<Publication PagesPerSpread="invalid"/>',
                     b'<Publication><Revision IsMajor="invalid"/></Publication>'):
            self.session.request.return_value = response(body)
            with self.assertRaises(PublishingError):
                self.client.get_publication("P")

    def test_ids_are_validated_and_encoded(self):
        self.session.request.return_value = response(b'<Publication ID="P"/>')
        self.client.get_publication("A/B #1")
        self.assert_request("GET", "publications/A%2FB%20%231")
        self.session.request.reset_mock()
        for value in ("", " ", "..", ".", "a\nb", None):
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.client.get_publication(value)
        self.session.request.assert_not_called()

    def test_generation_posts(self):
        cases = [
            ("create_indesign_package", ("A",), "CreateInDesignPackage", {"pageID": "A"}, "ZIP"),
            ("create_actual_page_pdf", ("A",), "GetPDFOfActualPage",
             {"pageID": "A"}, "ATTACHMENT_PDF"),
            ("create_planned_page_pdf", ("L", "print", "V"), "GetPDFOfPlannedPage",
             {"pageID": "L", "pdfProfile": "print", "versionID": "V"}, "ATTACHMENT_PDF"),
            ("create_planned_page_document", ("L", "V"), "MountDocForPlan",
             {"pageID": "L", "versionID": "V"}, None),
        ]
        for name, args, endpoint, data, field in cases:
            with self.subTest(name=name):
                self.session.request.return_value = response(
                    status=201, Location="/restapi/bgpinstance/BGP16722/status")
                job = getattr(self.client, name)(*args, version="table")
                self.assertEqual(job.process_id, "BGP16722")
                self.assertEqual(job.result_field, field)
                self.assert_request("POST", "pblbackgroundprocesses/" + endpoint, data=data,
                                    params={"context": "C", "workspace": "Main", "version": "table"})

    def test_upload_multipart_and_confirmation(self):
        with self.assertRaises(ValueError):
            self.client.upload_dtp_document("A", "not-opened.indd")
        self.session.request.assert_not_called()
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "document.indd"
            source.write_bytes(b"INDD")

            def receive(*args, **kwargs):
                filename, stream, mime = kwargs["files"]["file"]
                self.assertEqual((filename, mime), ("document.indd", "application/octet-stream"))
                self.assertEqual(stream.read(), b"INDD")
                return response(status=201, Location="/restapi/bgpinstance/job/status")

            self.session.request.side_effect = receive
            self.client.upload_dtp_document("A", source, confirm_overwrite=True)
            self.assert_request("POST", "pblbackgroundprocesses/UploadDTPDocument", data={"pageID": "A"})
            self.assertTrue(self.session.request.call_args.kwargs["files"]["file"][1].closed)

    def test_delete_200_and_204_and_confirmation(self):
        with self.assertRaises(ValueError):
            self.client.delete_page_document("P", "A")
        self.session.request.assert_not_called()
        for status in (200, 204):
            self.session.request.return_value = response(status=status)
            result = self.client.delete_page_document("P", "A", confirm_delete=True)
            self.assertEqual(result.deleted, status == 200)
            self.assertEqual(result.status_code, status)
            self.assert_request("DELETE", "publications/P/pages/A/document")

    def test_both_document_downloads(self):
        with tempfile.TemporaryDirectory() as temporary:
            for name, segment, options in [
                ("download_actual_page_document", "pages", {}),
                ("download_planned_page_document", "plannedpages", {"version_id": "V"}),
            ]:
                with self.subTest(name=name):
                    self.session.request.return_value = response(b"\x00\xffINDD")
                    target = Path(temporary) / (segment + ".indd")
                    result = getattr(self.client, name)("P", "A", target, **options)
                    self.assertEqual(result, target)
                    self.assertEqual(result.read_bytes(), b"\x00\xffINDD")
                    self.assert_request("GET", f"publications/P/{segment}/A/document",
                                        stream=True, accept="application/octet-stream")
                    if options:
                        self.assertEqual(self.session.request.call_args.kwargs["params"]["versionid"], "V")
                    with self.assertRaises(FileExistsError):
                        getattr(self.client, name)("P", "A", target, **options)
                    getattr(self.client, name)("P", "A", target, overwrite=True, **options)
            self.assertEqual(len(list(Path(temporary).iterdir())), 2)

    def test_partial_download_cleanup_and_preserving_old_target(self):
        def broken():
            yield b"partial"
            raise requests.Timeout("interrupted")
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "old.indd"
            target.write_bytes(b"old")
            with self.assertRaises(PublishingError):
                self.client._save(broken(), target, overwrite=True)
            self.assertEqual(target.read_bytes(), b"old")
            self.assertEqual(list(Path(temporary).iterdir()), [target])

    def test_http_and_transport_errors_no_retry(self):
        for status in (301, 401, 403, 404, 409, 429, 500):
            with self.subTest(status=status):
                r = response(b"private server detail", status=status)
                self.session.request.return_value = r
                self.session.request.reset_mock()
                with self.assertRaises(PublishingError) as caught:
                    self.client.list_publications()
                self.assertEqual(caught.exception.status_code, status)
                self.assertNotIn("private", str(caught.exception))
                self.session.request.assert_called_once()
                r.close.assert_called_once()
        self.session.request.side_effect = requests.Timeout("credentials must not be logged")
        with self.assertRaises(PublishingError):
            self.client.list_publications()

    def test_invalid_forms_and_missing_location(self):
        with self.assertRaises(ValueError):
            self.client.create_planned_page_pdf("L", "", "V")
        self.session.request.assert_not_called()
        for location in (None, "/restapi/not-a-job", "/bgpinstance/%2F/status"):
            self.session.request.return_value = response(
                status=201, **({"Location": location} if location else {}))
            with self.assertRaises(PublishingError):
                self.client.create_actual_page_pdf("A")

    def test_session_ownership_and_no_global_mutation(self):
        self.client.close()
        self.session.close.assert_not_called()
        self.session.assert_not_called()
        self.assertFalse(self.session.method_calls)
        with patch("stepxmlclient.publishing.client.requests.Session") as factory:
            with PublishingClient("https://step/restapi", auth=("user", "pwd")) as client:
                self.assertEqual(client.session.auth, ("user", "pwd"))
            factory.return_value.close.assert_called_once()
        with self.assertRaises(ValueError):
            PublishingClient("https://step/restapi", session=self.session, auth=("u", "p"))

    def test_urls_and_timeout_validation(self):
        self.assertEqual(derive_base_url("https://STEP/Proxy/restapiv2/"),
                         "https://STEP/Proxy/restapi")
        with self.assertRaises(PublishingConfigurationError):
            derive_base_url("https://step/custom")
        for url in ("ftp://step/restapi", "https://user:pwd@step/restapi",
                    "https://step/restapi?context=C", "https://step/restapi#frag"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                PublishingClient(url)
        for timeout in (0, -1, float("inf"), float("nan")):
            with self.assertRaises(ValueError):
                PublishingClient("https://step/restapi", timeout=timeout)

    def test_standalone_import_does_not_import_v2(self):
        code = (
            "import sys; from stepxmlclient.publishing import PublishingClient; "
            "assert 'stepxmlclient.client' not in sys.modules; "
            "assert not any(k.startswith('stepxmlclient.rest_client') for k in sys.modules)"
        )
        subprocess.run([sys.executable, "-c", code], check=True)

    def test_new_package_syntax_supports_python39(self):
        root = Path(__file__).resolve().parents[1] / "stepxmlclient" / "publishing"
        for path in root.glob("*.py"):
            with self.subTest(path=path.name):
                ast.parse(path.read_text(encoding="utf-8"), feature_version=(3, 9))


if __name__ == "__main__":
    unittest.main()
