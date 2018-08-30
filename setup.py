import os
import subprocess
import sys

from setuptools import find_packages, setup, Distribution
from setuptools.command.develop import develop
from setuptools.command.install import install

try:
    from wheel.bdist_wheel import bdist_wheel

    HAS_WHEEL = True
except ImportError:
    HAS_WHEEL = False


from uwsgi_pylib import UWSGI_LIB, UWSGI_VERSION


def install_uwsgi_as_lib():
    if not os.path.exists(UWSGI_LIB):
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--no-cache-dir",
                "--ignore-installed",
                "uWSGI=={}".format(UWSGI_VERSION),
            ],
            env={"UWSGI_AS_LIB": UWSGI_LIB},
        )


class UwsgiDevelopCommand(develop):
    def run(self):
        install_uwsgi_as_lib()
        develop.run(self)


class UwsgiInstallCommand(install):
    def run(self):
        install_uwsgi_as_lib()
        install.run(self)


if HAS_WHEEL:

    class UwsgiWheelCommand(bdist_wheel):
        def run(self):
            install_uwsgi_as_lib()
            bdist_wheel.run(self)


class UwsgiDistribution(Distribution):
    is_pure = lambda s: False

    def __init__(self, *attrs):
        Distribution.__init__(self, *attrs)
        self.cmdclass.update(
            {"install": UwsgiInstallCommand, "develop": UwsgiDevelopCommand}
        )
        if HAS_WHEEL:
            self.cmdclass["bdist_wheel"] = UwsgiWheelCommand


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
    distclass=UwsgiDistribution,
    extras_require={"test": ["pytest", "Django"]},
)
