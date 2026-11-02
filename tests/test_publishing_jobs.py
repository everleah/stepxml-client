"""Backend-neutral Publishing jobs and deterministic polling."""

from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

from stepxmlclient.publishing import (
    JobFile, JobStatus, PublishingClient, PublishingConfigurationError,
    PublishingError, PublishingJob, PublishingJobError, PublishingTimeoutError,
)
from stepxmlclient.publishing.jobs import job_from_location


class TestPublishingJobs(unittest.TestCase):
    def setUp(self):
        self.backend = Mock()
        self.client = PublishingClient("https://step/restapi", job_backend=self.backend)
        self.addCleanup(self.client.close)
        self.job = PublishingJob(
            process_id="BGP_16722", location="/restapi/bgpinstance/BGP_16722/status",
            result_field="ATTACHMENT_PDF")

    def test_locations_only_supply_identity(self):
        for location in (
            "/restapi/bgpinstance/BGP_16722/status",
            "restapi/bgpinstance/BGP_16722/status/",
            "https://other.invalid/restapi/bgpinstance/BGP_16722/status?x=y",
        ):
            self.assertEqual(job_from_location(location).process_id, "BGP_16722")
        for location in ("/bgpinstance//status", "/bgpinstance/%2e%2e/status",
                         "ftp://server/bgpinstance/id/status", "/bgpinstance/a%5Cb/status",
                         "https://[", "https:///bgpinstance/id/status"):
            with self.subTest(location=location), self.assertRaises(PublishingError):
                job_from_location(location)

    def test_wait_success_uses_v2_identity_and_bounded_timeout(self):
        clock = [0.0]
        self.backend.get_status.side_effect = [
            JobStatus(process_id=self.job.process_id, status=status)
            for status in ("waiting", "running", "succeeded")
        ]
        with patch("stepxmlclient.publishing.jobs.time.monotonic", side_effect=lambda: clock[0]), \
                patch("stepxmlclient.publishing.jobs.time.sleep",
                      side_effect=lambda delay: clock.__setitem__(0, clock[0] + delay)):
            result = self.client.wait_for_job(self.job, timeout=5, poll_interval=1)
        self.assertEqual(result.status, "succeeded")
        self.assertEqual(self.backend.get_status.call_count, 3)
        self.assertEqual(self.backend.get_status.call_args.kwargs["timeout"], 3)

    def test_all_non_success_terminal_and_unknown_statuses_raise(self):
        for status in ("completedwitherrors", "failed", "suspended", "aborted",
                       "unexpected", "future-status"):
            with self.subTest(status=status):
                self.backend.get_status.return_value = JobStatus(
                    process_id=self.job.process_id, status=status)
                with self.assertRaises(PublishingJobError) as caught:
                    self.client.wait_for_job(self.job)
                self.assertEqual(caught.exception.process_id, self.job.process_id)

    def test_total_deadline_and_late_success(self):
        clock = [0.0]
        self.backend.get_status.return_value = JobStatus(
            process_id=self.job.process_id, status="running")
        with patch("stepxmlclient.publishing.jobs.time.monotonic", side_effect=lambda: clock[0]), \
                patch("stepxmlclient.publishing.jobs.time.sleep",
                      side_effect=lambda delay: clock.__setitem__(0, clock[0] + delay)):
            with self.assertRaises(PublishingTimeoutError):
                self.client.wait_for_job(self.job, timeout=2, poll_interval=10)
        self.backend.get_status.assert_called_once()
        clock[0] = 0

        def late(process_id, **kwargs):
            clock[0] = 3
            return JobStatus(process_id=process_id, status="succeeded")

        self.backend.get_status.side_effect = late
        with patch("stepxmlclient.publishing.jobs.time.monotonic", side_effect=lambda: clock[0]):
            with self.assertRaises(PublishingTimeoutError):
                self.client.wait_for_job(self.job, timeout=2)

    def test_invalid_polling_options_and_process_mismatch(self):
        for options in ({"timeout": 0}, {"poll_interval": 0}, {"timeout": float("inf")}):
            with self.assertRaises(ValueError):
                self.client.wait_for_job(self.job, **options)
        self.backend.get_status.assert_not_called()
        self.backend.get_status.return_value = JobStatus(process_id="OTHER", status="succeeded")
        with self.assertRaises(PublishingJobError):
            self.client.wait_for_job(self.job)

    def test_standalone_without_backend_can_start_but_cannot_monitor(self):
        client = PublishingClient("https://step/restapi")
        self.addCleanup(client.close)
        for call in (
            lambda: client.get_job_status(self.job), lambda: client.wait_for_job(self.job),
            lambda: client.list_job_files(self.job),
            lambda: client.download_job_file(self.job, "ATT", "unused.pdf"),
        ):
            with self.assertRaises(PublishingConfigurationError):
                call()

    def test_attachment_mapping_and_real_id(self):
        self.backend.list_files.return_value = [
            JobFile(id="actual-42", original_attachment_id="ATTACHMENT_PDF", name="result.pdf"),
            JobFile(id="actual-43", original_attachment_id="ZIP", name="result.zip"),
        ]
        self.backend.get_file.return_value = b"%PDF-1.7\x00\xff"
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "result.pdf"
            self.client.download_job_result(self.job, target)
            self.assertEqual(target.read_bytes(), b"%PDF-1.7\x00\xff")
        self.backend.get_file.assert_called_once_with(
            "BGP_16722", "actual-42", timeout=30)

    def test_ambiguous_and_missing_attachments_are_errors(self):
        for files in ([], [
            JobFile(id="a", original_attachment_id="ATTACHMENT_PDF"),
            JobFile(id="b", original_attachment_id="ATTACHMENT_PDF"),
        ]):
            self.backend.list_files.return_value = files
            with self.assertRaises(PublishingError):
                self.client.download_job_result(self.job, "unused.pdf")
        self.backend.get_file.assert_not_called()

    def test_explicit_download_and_no_result_field_lists_all(self):
        files = [JobFile(id="a", original_attachment_id="LOG")]
        self.backend.list_files.return_value = files
        job = self.job.model_copy(update={"result_field": None})
        self.assertEqual(self.client.list_job_files(job), files)
        self.backend.get_file.return_value = b"log"
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "a"
            self.client.download_job_file(job, "a", target)
            with self.assertRaises(FileExistsError):
                self.client.download_job_file(job, "a", target)


if __name__ == "__main__":
    unittest.main()
