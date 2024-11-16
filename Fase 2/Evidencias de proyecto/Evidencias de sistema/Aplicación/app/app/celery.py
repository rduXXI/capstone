# proyecto/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Configurar el entorno Django para Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
app = Celery("app")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
