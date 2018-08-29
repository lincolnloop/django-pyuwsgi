import subprocess
import sys
import time

import pytest

from ..runner import run


def _args_to_str(args):
    """Turn a list of strings into a string that can be used as function args"""
    return ", ".join(["'{}'".format(a.replace("'", "'")) for a in args])


def run(*args):
    """uWSGI exits the process after a run so we need to run in subprocess"""
    return subprocess.check_output(
        [
            sys.executable,
            "-c",
            "from uwsgi_pylib.runner import run; " "run({})".format(_args_to_str(args)),
        ],
        stderr=subprocess.STDOUT,
    )


def run_django(*args):
    # timeout isn't supported in Python 2.7, do it the hard way...
    pytest.importorskip("django")
    proc = subprocess.Popen(
        [
            sys.executable,
            "-c",
            "from uwsgi_pylib.management.commands.uwsgi import Command; "
            "Command().execute({})".format(_args_to_str(args)),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env={"DJANGO_SETTINGS_MODULE": "uwsgi_pylib.tests.django_settings"},
    )
    time.sleep(1)
    proc.kill()
    return proc



def test_help():
    assert "show this help" in run("--help").decode("utf-8")


def test_need_app():
    try:
        run("--need-app", "-s", "127.0.0.1:0")
        assert False
    except subprocess.CalledProcessError as e:
        assert "no app loaded. GAME OVER" in e.output.decode("utf-8")


def test_django():
    """Start a Django HTTP server and then kill it"""
    proc = run_django("--http-socket=127.0.0.1:0")
    assert "WSGI app 0 (mountpoint='') ready in" in proc.communicate()[0].decode("utf-8")
