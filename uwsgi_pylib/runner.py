#!/usr/bin/env python
import ctypes
import sys

from uwsgi_pylib import UWSGI_LIB


def run(*uwsgi_args):
    # load the uwsgi library in the global namespace
    uwsgi = ctypes.CDLL(UWSGI_LIB, mode=ctypes.RTLD_GLOBAL)
    uwsgi_binary = sys.argv[0]
    args = [uwsgi_binary, "--binary-path", uwsgi_binary] + list(uwsgi_args)

    # build command line args
    argv = (ctypes.c_char_p * (len(args) + 1))()
    for pos, arg in enumerate(args):
        try:
            argv[pos] = bytes(arg, "utf-8")
        except TypeError:
            # Python 2
            argv[pos] = arg.encode("utf-8")
    # inform the uwsgi engine, the passed environ is not safe to overwrite
    envs = (ctypes.c_char_p * 1)()
    # enter into uWSGI !!!
    uwsgi.uwsgi_init(len(args), argv, envs)


def run_from_argv():
    run(*sys.argv[2:])


if __name__ == "__main__":
    run_from_argv()
