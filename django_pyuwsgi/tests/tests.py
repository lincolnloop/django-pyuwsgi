import subprocess
import sys
import time

import pytest


def _args_to_str(args):
    """Turn a list of strings into a string that can be used as function args"""
    return ", ".join(["'{}'".format(a.replace("'", "'")) for a in args])


def run_django(*args):
    # timeout isn't supported in Python 2.7, do it the hard way...
    proc = subprocess.Popen(
        [
            sys.executable,
            "-c",
            "from django_pyuwsgi.management.commands.uwsgi import Command; "
            "Command().execute({})".format(_args_to_str(args)),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env={"DJANGO_SETTINGS_MODULE": "django_pyuwsgi.tests.django_settings"},
    )
    time.sleep(1)
    proc.kill()
    return proc


def test_django():
    """Start a Django HTTP server and then kill it"""
    proc = run_django("--http-socket=127.0.0.1:0")
    assert "WSGI app 0 (mountpoint='') ready in" in proc.communicate()[0].decode(
        "utf-8"
    )
