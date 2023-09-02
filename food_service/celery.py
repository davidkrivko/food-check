import os
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "food_service.settings")

app = Celery("app")

app.config_from_object("django.conf:settings", namespace="CELERY")
