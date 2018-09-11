import os

from setuptools import find_packages, setup


README = open(os.path.join(os.path.dirname(__file__), "README.md")).read()

setup(
    name="django-pyuwsgi",
    version="1.0.0",
    description="uWSGI as a Django management command",
    long_description=README,
    long_description_content_type="text/markdown",
    keywords=["uwsgi", "django", "pyuwsgi"],
    packages=find_packages(),
    license="MIT",
    install_requires=["pyuwsgi", "Django"],
    extras_require={"test": ["pytest"]},
)
