# uWSGI-pylib

Run uWSGI as a Python module.

----

⚠️ This is experimental!

## Usage

1. Install (this will take some time as uWSGI is compiled)

    ```
    pip install uWSGI-pylib
    ```

2. Import and run

    ```python
    from uwsgi_pylib import runner
    runner.run("--socket=:8000",
               "--module=mywsgi:app")
 
    ```
    
    Any uWSGI options will be accepted as arguments.
    
### Django Management Command

For convenience, a Django management command wrapper is included. Simply add `uwsgi_pylib` to your `INSTALLED_APPS` and run:

```python
manage.py uwsgi --socket=:8000 ...
```

This uses the `WSGI_APPLICATION` setting to determine what module to run and will also serve your static files if you have them set to be served from a local URL.

## Motivation

uWSGI isn't really a Python module. Running `pip install uWSGI` will build a binary you can run via `uwsgi`, but doesn't provide something you can run from within a Python module.

In some scenarios, however, you want to run uWSGI as a Python module. For example, if you are trying to distribute an application with a single entrypoint for command-line interaction. This may be helpful when building Docker containers or building self-contained Python apps with something like [shiv](https://github.com/linkedin/shiv).


## How it Works


This takes advantage of some undocumented parts of uWSGI to build and run it as a ctypes compatible shared library instead of the normal executable. This process is described by the developer in [unbit/uwsgi#564](https://github.com/unbit/uwsgi/issues/564#issuecomment-37719925).

### Creating the Shared Library

By setting the environment variable `UWSGI_AS_LIB`, we can force `pip install uwsgi` to output a shared library. In `setup.py` we override the install commands to build the library for your architecture and include it in the package.

### Running the Shared Library as a Python Module

The shared library is loaded via the `ctypes` library and executed using an exported function `uwsgi_init`.
