import os

from setuptools import find_packages, setup


README = open(os.path.join(os.path.dirname(__file__), "README.md")).read()

setup(
    name="django-pyuwsgi",
    version="1.1.1",
    description="uWSGI as a Django management command",
    author="Peter Baumgartner",
    author_email="pete@lincolnloop.com",
    url="https://github.com/lincolnloop/django-pyuwsgi",
    long_description=README,
    long_description_content_type="text/markdown",
    keywords=["uwsgi", "django", "pyuwsgi"],
    packages=find_packages(),
    license="MIT",
    install_requires=["pyuwsgi>=2.0.17.2b3", "Django"],
    extras_require={"test": ["pytest"]},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Framework :: Django",
    ],
)
