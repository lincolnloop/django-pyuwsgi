# django-pyuwsgi

Run pyuwsgi (aka uWSGI) as a Django management command.

----

[![build status](https://travis-ci.org/lincolnloop/django-pyuwsgi.svg?branch=master)](https://travis-ci.org/lincolnloop/django-pyuwsgi)

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

Don't worry about setting the module you want to run or virtualenv/home, that will already be handled for you via the `WSGI_APPLICATION` setting and your current Python interpreter. If you've configured your static files to be served from a local URL, they'll be setup too.

## Motivation

In some scenarios, it is beneficial to distribute a Django project with a single entrypoint for command-line interaction. This can come in handy when building Docker containers or self-contained Python apps with something like [shiv](https://github.com/linkedin/shiv).
