"""
WSGI config for piepi project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "piepi.settings_docker")

application = get_wsgi_application()

from django.contrib.auth import get_user_model  # noqa: E402
from dotenv import load_dotenv  # noqa: E402

load_dotenv()
user_model = get_user_model()

if not user_model.objects.all().exists():
    username = os.getenv("DJANGO_SUPERUSER_USERNAME", "admin")
    email = os.getenv("DJANGO_SUPERUSER_EMAIL")
    password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "admin")
    user_model.objects.create_superuser(username, email, password)
