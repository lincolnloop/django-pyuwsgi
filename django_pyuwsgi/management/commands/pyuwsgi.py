from __future__ import absolute_import

from django.conf import settings
from django.core.management import BaseCommand

import pyuwsgi


def get_default_args():
    """Load pyuwsgi args from settings or use our defaults"""
    try:
        return settings.PYUWSGI_ARGS
    except AttributeError:
        defaults = [
            "--strict",
            "--need-app",
            # project.wsgi.application -> project.wsgi:application
            "--module={}".format(":".join(settings.WSGI_APPLICATION.rsplit(".", 1))),
        ]
        if (settings.STATIC_URL or "").startswith("/"):
            defaults.extend(
                [
                    "--static-map",
                    "{}={}".format(
                        settings.STATIC_URL.rstrip("/"), settings.STATIC_ROOT
                    ),
                ]
            )
        return defaults


class Command(BaseCommand):
    """
    This bypasses any Django handling of the command and sends all arguments straight
    to pyuwsgi.
    """

    help = "Start pyuwsgi server"

    def run_from_argv(self, argv):
        args = get_default_args() + argv[2:]
        pyuwsgi.run(*args)

    def execute(self, *args, **options):
        self.run_from_argv(["manage.py", "pyuwsgi"] + list(args))
