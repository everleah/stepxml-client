"""Build, check and explicitly publish the current release to PyPI."""

import argparse
from email.parser import BytesParser
import getpass
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tarfile
import tempfile
from typing import Optional
import zipfile


ROOT = Path(__file__).resolve().parent
PYPI_URL = "https://upload.pypi.org/legacy/"
PYPI_USERNAME = "__token__"
FORBIDDEN_SUFFIXES = {".json", ".xsd", ".pem", ".key", ".pyc", ".p12", ".pfx"}


def run_module(*arguments: str, env: Optional[dict[str, str]] = None) -> None:
    subprocess.run([sys.executable, "-m", *arguments], cwd=ROOT, check=True, env=env)


def validate_members(names: list[str]) -> None:
    for name in names:
        path = PurePosixPath(name)
        if (
            path.is_absolute()
            or ".." in path.parts
            or path.suffix.lower() in FORBIDDEN_SUFFIXES
            or path.name.lower() in {".pypirc", ".env"}
            or any(part in {".git", ".venv", "__pycache__"} for part in path.parts)
        ):
            raise ValueError(f"Forbidden file in release artifact: {name}")


def check_artifacts(directory: Path) -> tuple[list[Path], str]:
    wheels = list(directory.glob("*.whl"))
    sources = list(directory.glob("*.tar.gz"))
    if len(wheels) != 1 or len(sources) != 1:
        raise ValueError("Expected exactly one wheel and one source distribution.")

    with zipfile.ZipFile(wheels[0]) as wheel:
        names = wheel.namelist()
        validate_members(names)
        metadata_names = [name for name in names if name.endswith(".dist-info/METADATA")]
        if len(metadata_names) != 1:
            raise ValueError("Expected exactly one wheel metadata file.")
        metadata = BytesParser().parsebytes(wheel.read(metadata_names[0]))
        if "stepxmlclient/__init__.py" not in names:
            raise ValueError("Wheel does not contain the stepxmlclient package.")
        if not any(name.endswith(".dist-info/licenses/LICENSE") for name in names):
            raise ValueError("Wheel does not contain the MIT license.")

    version = metadata.get("Version", "")
    if metadata.get("Name") != "stepxmlclient" or not version:
        raise ValueError("Unexpected package name or missing release version.")
    with tarfile.open(sources[0], "r:gz") as source:
        names = source.getnames()
        validate_members(names)
        roots = {PurePosixPath(name).parts[0] for name in names}
        if len(roots) != 1:
            raise ValueError("Expected a single source distribution root.")
        root = roots.pop()
        for required in ("pyproject.toml", "README.md", "LICENSE", "stepxmlclient/__init__.py"):
            if f"{root}/{required}" not in names:
                raise ValueError(f"Source distribution is missing {required}.")
        info = source.extractfile(f"{root}/PKG-INFO")
        if info is None:
            raise ValueError("Source distribution is missing package metadata.")
        with info:
            source_metadata = BytesParser().parsebytes(info.read())
        if (source_metadata.get("Name"), source_metadata.get("Version")) != (
            "stepxmlclient", version
        ):
            raise ValueError("Wheel and source distribution metadata do not match.")
    return [sources[0], wheels[0]], version


def configure_token() -> None:
    import keyring

    token = getpass.getpass("New PyPI API token (hidden input): ").strip()
    if not token.startswith("pypi-") or any(character.isspace() for character in token):
        raise ValueError("Expected a PyPI API token without whitespace.")
    keyring.set_password(PYPI_URL, PYPI_USERNAME, token)
    print("PyPI token saved in the local OS credential store, not in the repository.")


def release(publish: bool = False) -> None:
    # The default build creates the wheel from the sdist in a fresh directory.
    with tempfile.TemporaryDirectory(prefix="stepxmlclient-release-") as temporary:
        output = Path(temporary)
        run_module("build", "--outdir", str(output), str(ROOT))
        artifacts, version = check_artifacts(output)
        run_module("twine", "check", "--strict", *(str(path) for path in artifacts))
        destination = ROOT / "dist" / "pypi" / version
        destination.mkdir(parents=True, exist_ok=True)
        saved = [Path(shutil.copy2(path, destination / path.name)) for path in artifacts]
        print(f"Validated release {version}: {destination}", flush=True)
        if publish:
            import keyring

            token = keyring.get_password(PYPI_URL, PYPI_USERNAME)
            if not token:
                raise ValueError(
                    "No local PyPI token configured. Run with --configure-token first."
                )
            # Pass only these freshly checked artifacts, never a dist wildcard.
            run_module(
                "twine", "upload", "--non-interactive",
                "--repository-url", PYPI_URL, "--username", PYPI_USERNAME,
                *(str(path) for path in saved),
                env={**os.environ, "TWINE_PASSWORD": token},
            )
            print(f"Published: https://pypi.org/project/stepxmlclient/{version}/")
        else:
            print("Check only: nothing uploaded. Use --publish to publish to PyPI.")


def main(arguments: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument("--configure-token", action="store_true")
    actions.add_argument("--check-only", action="store_true")
    actions.add_argument("--publish", action="store_true")
    options = parser.parse_args(arguments)
    try:
        if options.configure_token:
            configure_token()
        else:
            release(publish=options.publish)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"Release failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
