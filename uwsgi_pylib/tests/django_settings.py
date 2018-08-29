SECRET_KEY = "s"
WSGI_APPLICATION = "uwsgi_pylib.tests.django_settings.application"
INSTALLED_APPS = ["uwsgi_pylib"]
ROOT_URLCONF = "uwsgi_pylib.tests.django_settings"

urlpatterns = []
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
