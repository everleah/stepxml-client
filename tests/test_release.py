"""Offline regression tests for PyPI packaging and publication safeguards."""

import contextlib
import io
from pathlib import Path
import shutil
import subprocess
import sys
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
                "stepxmlclient/credentials.json", "STEP.xsd", "wadl_pub.xml",
                "stepxmlclient/wadl_pub.xml", ".pypirc", ".env",
                "private.key", "secret.pem", ".venv/token", "../outside.py",
                "other/openapi.json", "stepxmlclient/nested/openapi_pub.json",
            ):
                with self.subTest(location=location, name=name):
                    with tempfile.TemporaryDirectory() as temporary:
                        directory = Path(temporary)
                        make_artifacts(directory, **{location: name})
                        with self.assertRaisesRegex(ValueError, "Forbidden file"):
                            release.check_artifacts(directory)

    def test_accepts_only_named_optional_specifications(self):
        for name in ("openapi.json", "openapi_pub.json"):
            for source_name in (name, f"stepxmlclient/{name}"):
                with self.subTest(name=name, source_name=source_name):
                    with tempfile.TemporaryDirectory() as temporary:
                        directory = Path(temporary)
                        make_artifacts(directory, extra_wheel=f"stepxmlclient/{name}",
                                       extra_source=source_name)
                        release.check_artifacts(directory)

    def test_rejects_root_specifications_in_wheel(self):
        for name in ("openapi.json", "openapi_pub.json"):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as temporary:
                directory = Path(temporary)
                make_artifacts(directory, extra_wheel=name)
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


class TestOptionalSpecificationBuild(TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        for name in ("pyproject.toml", "setup.py", "MANIFEST.in", "README.md", "LICENSE"):
            shutil.copyfile(release.ROOT / name, self.root / name)
        self.package = self.root / "stepxmlclient"
        self.package.mkdir()
        (self.package / "__init__.py").write_text("", encoding="utf-8")

    def build(self, output, wheel_only=False):
        arguments = [sys.executable, "-m", "build", "--no-isolation", "--outdir", str(output)]
        if wheel_only:
            arguments.append("--wheel")
        result = subprocess.run(arguments, cwd=self.root, text=True,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.assertEqual(result.returncode, 0, result.stdout)
        return next(output.glob("*.whl"))

    def test_sdist_to_wheel_with_both_either_or_no_specifications(self):
        for names in ((), ("openapi.json",), ("openapi_pub.json",),
                      ("openapi.json", "openapi_pub.json")):
            with self.subTest(names=names):
                for name in release.OPTIONAL_SPECIFICATIONS:
                    (self.root / name).unlink(missing_ok=True)
                    (self.package / name).unlink(missing_ok=True)
                for name in names:
                    (self.root / name).write_bytes(b'{"synthetic":"root"}')
                    (self.package / name).write_bytes(b'{"synthetic":"older package copy"}')
                (self.package / "credentials.json").write_text("excluded", encoding="utf-8")
                output = self.root / ("output-" + str(len(list(self.root.glob("output-*")))))
                wheel = self.build(output)
                release.check_artifacts(output)
                with zipfile.ZipFile(wheel) as archive:
                    for name in release.OPTIONAL_SPECIFICATIONS:
                        member = f"stepxmlclient/{name}"
                        self.assertEqual(member in archive.namelist(), name in names)
                        if name in names:
                            self.assertEqual(archive.read(member), b'{"synthetic":"root"}')
                    self.assertNotIn("stepxmlclient/credentials.json", archive.namelist())
                with tarfile.open(next(output.glob("*.tar.gz")), "r:gz") as archive:
                    root = archive.getnames()[0].split("/")[0]
                    for name in release.OPTIONAL_SPECIFICATIONS:
                        self.assertEqual(f"{root}/{name}" in archive.getnames(), name in names)

    def test_package_local_spec_and_stale_direct_wheel_output(self):
        for name in release.OPTIONAL_SPECIFICATIONS:
            (self.package / name).write_bytes(b'{"synthetic":"package"}')
        wheel = self.build(self.root / "first", wheel_only=True)
        with zipfile.ZipFile(wheel) as archive:
            for name in release.OPTIONAL_SPECIFICATIONS:
                self.assertEqual(archive.read(f"stepxmlclient/{name}"),
                                 b'{"synthetic":"package"}')
                (self.package / name).unlink()
        wheel = self.build(self.root / "second", wheel_only=True)
        with zipfile.ZipFile(wheel) as archive:
            for name in release.OPTIONAL_SPECIFICATIONS:
                self.assertNotIn(f"stepxmlclient/{name}", archive.namelist())


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
