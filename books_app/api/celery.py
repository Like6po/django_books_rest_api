from celery import Celery

from books_app.settings import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

app = Celery("tasks",
             broker=CELERY_BROKER_URL,
             backend=CELERY_RESULT_BACKEND)

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
