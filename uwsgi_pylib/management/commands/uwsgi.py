from django.conf import settings
from django.core.management import BaseCommand
from uwsgi_pylib import runner


class Command(BaseCommand):
    """
    This bypasses any Django handling of the command and sends all arguments straight
    to uWSGI.
    """

    help = "Start uWSGI server"

    def run_from_argv(self, argv):
        # project.wsgi.application -> project.wsgi:application
        wsgi_module = ":".join(settings.WSGI_APPLICATION.rsplit(".", 1))
        default_args = ["--strict", "--need-app", "--module", wsgi_module]
        if (settings.STATIC_URL or "").startswith("/"):
            default_args.extend(
                [
                    "--static-map",
                    "{}={}".format(
                        settings.STATIC_URL.rstrip("/"), settings.STATIC_ROOT
                    ),
                ]
            )
        args = default_args + argv[2:]
        runner.run(*args)

    def execute(self, *args, **options):
        self.run_from_argv(["manage.py", "uwsgi"] + list(args))