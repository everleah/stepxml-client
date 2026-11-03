from pathlib import Path
import shutil

from setuptools import setup
from setuptools.command.build_py import build_py


class BuildPy(build_py):
    """Include optional local specifications without adding them to Git."""

    def run(self):
        super().run()
        root = Path(__file__).resolve().parent
        destination = Path(self.build_lib) / "stepxmlclient"
        for name in ("openapi.json", "openapi_pub.json"):
            source = root / name
            target = destination / name
            if source.is_file():
                self.mkpath(str(destination))
                shutil.copyfile(source, target)
            elif not (root / "stepxmlclient" / name).is_file() and target.is_file():
                target.unlink()


setup(cmdclass={"build_py": BuildPy})
