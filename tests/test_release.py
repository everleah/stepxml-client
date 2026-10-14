"""Offline regression tests for PyPI packaging and publication safeguards."""

import contextlib
import io
from pathlib import Path
import subprocess
import tarfile
import tempfile
from unittest import TestCase
from unittest.mock import patch
import zipfile

import publish_pypi as release


def make_artifacts(directory, extra_wheel=None, extra_source=None, source_version="1.0.0"):
    metadata = (
        b"Metadata-Version: 2.4\nName: stepxmlclient\nVersion: 1.0.0\n"
        b"License-Expression: MIT\n\n"
    )
    wheel = directory / "stepxmlclient-1.0.0-py3-none-any.whl"
    with zipfile.ZipFile(wheel, "w") as archive:
        archive.writestr("stepxmlclient/__init__.py", "")
        archive.writestr("stepxmlclient-1.0.0.dist-info/METADATA", metadata)
        archive.writestr("stepxmlclient-1.0.0.dist-info/licenses/LICENSE", "MIT")
        if extra_wheel:
            archive.writestr(extra_wheel, "not for publication")
    source = directory / "stepxmlclient-1.0.0.tar.gz"
    files = {
        "pyproject.toml": b"",
        "README.md": b"",
        "LICENSE": b"MIT",
        "stepxmlclient/__init__.py": b"",
        "PKG-INFO": metadata.replace(b"Version: 1.0.0", f"Version: {source_version}".encode()),
    }
    if extra_source:
        files[extra_source] = b"not for publication"
    with tarfile.open(source, "w:gz") as archive:
        for name, content in files.items():
            info = tarfile.TarInfo(f"stepxmlclient-1.0.0/{name}")
            info.size = len(content)
            archive.addfile(info, io.BytesIO(content))
    return [source, wheel]


class TestReleaseArtifacts(TestCase):
    def test_accepts_matching_distributions(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            expected = make_artifacts(directory)
            artifacts, version = release.check_artifacts(directory)
            self.assertEqual(artifacts, expected)
            self.assertEqual(version, "1.0.0")

    def test_rejects_forbidden_files_in_either_archive(self):
        for location in ("extra_source", "extra_wheel"):
            for name in (
                "stepxmlclient/openapi.json", "STEP.xsd", ".pypirc", ".env",
                "private.key", "secret.pem", ".venv/token", "../outside.py",
            ):
                with self.subTest(location=location, name=name):
                    with tempfile.TemporaryDirectory() as temporary:
                        directory = Path(temporary)
                        make_artifacts(directory, **{location: name})
                        with self.assertRaisesRegex(ValueError, "Forbidden file"):
                            release.check_artifacts(directory)

    def test_rejects_multiple_wheels(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            make_artifacts(directory)
            (directory / "stale.whl").touch()
            with self.assertRaisesRegex(ValueError, "exactly one wheel"):
                release.check_artifacts(directory)

    def test_rejects_mismatched_versions(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            make_artifacts(directory, source_version="0.9.0")
            with self.assertRaisesRegex(ValueError, "do not match"):
                release.check_artifacts(directory)


class TestReleaseWorkflow(TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        root_patch = patch.object(release, "ROOT", self.root)
        root_patch.start()
        self.addCleanup(root_patch.stop)
        self.calls = []
        self.stdout = contextlib.redirect_stdout(io.StringIO())
        self.stdout.__enter__()
        self.addCleanup(self.stdout.__exit__, None, None, None)

    def fake_module(self, *arguments, **kwargs):
        self.calls.append((arguments, kwargs))
        if arguments[0] == "build":
            make_artifacts(Path(arguments[arguments.index("--outdir") + 1]))

    def test_default_only_checks_and_retains_artifacts(self):
        with patch.object(release, "run_module", side_effect=self.fake_module):
            self.assertEqual(release.main([]), 0)
        self.assertEqual(len(self.calls), 2)
        self.assertEqual(self.calls[0][0][0], "build")
        self.assertNotIn("--wheel", self.calls[0][0])
        self.assertEqual(self.calls[1][0][:3], ("twine", "check", "--strict"))
        self.assertEqual(len(list((self.root / "dist" / "pypi" / "1.0.0").iterdir())), 2)

    def test_uploads_only_new_artifacts_using_local_keyring(self):
        (self.root / "dist").mkdir()
        (self.root / "dist" / "old.whl").touch()
        with patch.object(release, "run_module", side_effect=self.fake_module):
            with patch("keyring.get_password", return_value="test-local-credential") as get:
                release.release(publish=True)
        get.assert_called_once_with(release.PYPI_URL, release.PYPI_USERNAME)
        arguments, kwargs = self.calls[-1]
        self.assertEqual(arguments[:3], ("twine", "upload", "--non-interactive"))
        self.assertIn(release.PYPI_URL, arguments)
        self.assertNotIn("--skip-existing", arguments)
        self.assertNotIn("test-local-credential", arguments)
        self.assertEqual(kwargs["env"]["TWINE_PASSWORD"], "test-local-credential")
        paths = [Path(argument) for argument in arguments[-2:]]
        self.assertEqual({path.suffix for path in paths}, {".gz", ".whl"})
        self.assertTrue(all(path.parent == self.root / "dist" / "pypi" / "1.0.0" for path in paths))
        self.assertTrue(all(path.is_file() for path in paths))
        self.assertFalse(any("*" in argument for argument in arguments))

    def test_missing_token_prevents_upload(self):
        with patch.object(release, "run_module", side_effect=self.fake_module):
            with patch("keyring.get_password", return_value=None):
                with self.assertRaisesRegex(ValueError, "--configure-token"):
                    release.release(publish=True)
        self.assertEqual(len(self.calls), 2)

    def test_failed_check_prevents_upload(self):
        def fail_check(*arguments, **kwargs):
            self.fake_module(*arguments, **kwargs)
            if arguments[:2] == ("twine", "check"):
                raise subprocess.CalledProcessError(1, ["twine", "check"])

        with patch.object(release, "run_module", side_effect=fail_check):
            with self.assertRaises(subprocess.CalledProcessError):
                release.release(publish=True)
        self.assertEqual(len(self.calls), 2)

    def test_configure_saves_token_only_to_keyring(self):
        with patch("getpass.getpass", return_value="pypi-test-credential"):
            with patch("keyring.set_password") as save:
                release.configure_token()
        save.assert_called_once_with(
            release.PYPI_URL, release.PYPI_USERNAME, "pypi-test-credential"
        )
        self.assertEqual(list(self.root.iterdir()), [])

    def test_invalid_token_is_not_saved(self):
        with patch("getpass.getpass", return_value="invalid"):
            with patch("keyring.set_password") as save:
                with self.assertRaisesRegex(ValueError, "PyPI API token"):
                    release.configure_token()
        save.assert_not_called()

    def test_subprocess_failure_sets_nonzero_exit_code(self):
        with patch.object(release, "release", side_effect=subprocess.CalledProcessError(1, ["build"])):
            with contextlib.redirect_stderr(io.StringIO()) as stderr:
                self.assertEqual(release.main(["--check-only"]), 1)
        self.assertIn("Release failed", stderr.getvalue())
