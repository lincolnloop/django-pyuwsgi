# django-pyuwsgi

Run [pyuwsgi](https://pypi.org/project/pyuwsgi/) (aka uWSGI) as a Django management command.

----

[![build status](https://travis-ci.org/lincolnloop/django-pyuwsgi.svg?branch=master)](https://travis-ci.org/lincolnloop/django-pyuwsgi) [![pypi](https://img.shields.io/pypi/v/django-pyuwsgi.svg)](https://pypi.org/pypi/django-pyuwsgi) [![pyversions](https://img.shields.io/pypi/pyversions/django-pyuwsgi.svg)](https://pypi.org/pypi/django-pyuwsgi)

## Usage

1. Install:

    ```
    pip install django-pyuwsgi
    ```

2. Add to `INSTALLED_APPS`:

    ```python
    INSTALLED_APPS = [
       # ...
       "django_pyuwsgi",
       # ...
    ]
    ```
3. Run:
    
    ```
    manage.py pyuwsgi --socket=:8000 ...
    ```

## Configuration

Pyuwsgi already knows the Python interpreter and virtualenv (if applicable) to use from the Django management command environment. By default, it will run with the following flags (using `settings.WSGI_APPLICATION` to determine the module):

```
--strict --need-app --module={derived}
```

If you have `STATIC_URL` defined with a local URL, it will also add `--static-map`, derived from `STATIC_URL` and `STATIC_ROOT`.

You can pass any additional arguments uWSGI accepts in from the command line.

But uWSGI has a lot of flags, and many of them, you want every time you run the project. For that scenario, you can configure your own defaults using the optional setting, `PYUWSGI_ARGS`. Here's an example you might find helpful:

```python
PYUWSGI_ARGS = [
    "--master",
    "--strict",
    "--need-app",
    "--module".
    ":".join(WSGI_APPLICATION.rsplit(".", 1)),
    "--no-orphans",
    "--vacuum",
    "--auto-procname",
    "--enable-threads",
    "--offload-threads=4",
    "--thunder-lock",
    "--static-map",
    "=".join([STATIC_URL.rstrip("/"), STATIC_ROOT]),
    "--static-expires",
    "/* 7776000",
]
```

Don't forget to also set something like `--socket=:8000` or `--http=:8000` so your app listens on a port. Depending on your setup, it may make more sense to pass this in via the command line than hard-coding it in your settings. 

## Motivation

In some scenarios, it is beneficial to distribute a Django project with a single entrypoint for command-line interaction. This can come in handy when building Docker containers or self-contained Python apps with something like [shiv](https://github.com/linkedin/shiv).
