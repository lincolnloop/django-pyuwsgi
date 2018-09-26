import os
import subprocess
import sys
import time

from django.test import override_settings

from django_pyuwsgi.management.commands.pyuwsgi import get_default_args

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_pyuwsgi.tests.django_settings")


def _args_to_str(args):
    """Turn a list of strings into a string that can be used as function args"""
    return ", ".join(["'{}'".format(a.replace("'", "'")) for a in args])


def run_django(*args):
    # timeout isn't supported in Python 2.7, do it the hard way...
    proc = subprocess.Popen(
        [
            sys.executable,
            "-c",
            "from django_pyuwsgi.management.commands.pyuwsgi import Command; "
            "Command().execute({})".format(_args_to_str(args)),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
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


def test_default_args():
    assert get_default_args() == [
        "--strict",
        "--need-app",
        "--module=django_pyuwsgi.tests.django_settings:application",
        "--static-map",
        "/static=/tmp/static",
    ]


@override_settings(PYUWSGI_ARGS=["--master", "--thunder-lock"])
def test_settings_args():
    assert get_default_args() == ["--master", "--thunder-lock"]
