SECRET_KEY = "s"
WSGI_APPLICATION = "django_pyuwsgi.tests.django_settings.application"
INSTALLED_APPS = ["django_pyuwsgi"]
ROOT_URLCONF = "django_pyuwsgi.tests.django_settings"
STATIC_URL = "/static/"
STATIC_ROOT = "/tmp/static"

urlpatterns = []
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
