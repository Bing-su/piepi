import os
import sys

from django.apps import AppConfig


class ServerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "server"

    def ready(self):
        if "migrate" in sys.argv:
            return

        from django.contrib.auth import get_user_model

        user_model = get_user_model()

        if not user_model.objects.all().exists():
            username = os.getenv("DJANGO_SUPERUSER_USERNAME", "admin")
            email = os.getenv("DJANGO_SUPERUSER_EMAIL")
            password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "admin")
            user_model.objects.create_superuser(username, email, password)
