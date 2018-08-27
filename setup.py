import os
import subprocess
import sys

from setuptools import find_packages, setup
from setuptools.command.develop import develop
from setuptools.command.install import install

from uwsgi_pylib import UWSGI_LIB, UWSGI_VERSION


def install_uwsgi_as_lib():
    if os.path.exists(UWSGI_LIB):
        return
    os.environ["UWSGI_AS_LIB"] = UWSGI_LIB
    print("Building {}...".format(UWSGI_LIB))
    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--no-cache-dir",
            "--ignore-installed",
            "uWSGI=={}".format(UWSGI_VERSION),
        ]
    )


def build_uwsgi_lib(command_subclass):
    orig_run = command_subclass.run

    def install_uwsgi_and_run(self):
        install_uwsgi_as_lib()
        orig_run(self)

    command_subclass.run = install_uwsgi_and_run
    return command_subclass


@build_uwsgi_lib
class UwsgiDevelopCommand(develop):
    pass


@build_uwsgi_lib
class UwsgiInstallCommand(install):
    pass


try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

    @build_uwsgi_lib
    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            _bdist_wheel.finalize_options(self)
            # Flag wheels as platform dependent
            self.root_is_pure = False


except ImportError:
    bdist_wheel = None

README = open(os.path.join(os.path.dirname(__file__), "README.md")).read()

setup(
    name="uWSGI-pylib",
    version=UWSGI_VERSION,
    description="uWSGI as a Python module",
    long_description=README,
    long_description_content_type="text/markdown",
    keywords=["uwsgi", "entrypoint"],
    packages=find_packages(),
    license="MIT",
    include_package_data=True,
    package_data={"uwsgi_pylib": [UWSGI_LIB]},
    cmdclass={
        "install": UwsgiInstallCommand,
        "develop": UwsgiDevelopCommand,
        "bdist_wheel": bdist_wheel,
    },
)
