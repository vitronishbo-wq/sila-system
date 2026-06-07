"""Canonical Celery app bootstrap for `app.core`."""

from apps.backend.app.core.settings import settings
from celery import Celery

app = Celery("sila")
app.conf.broker_url = getattr(settings, "CELERY_BROKER_URL", "redis://redis:6379/0")
app.conf.result_backend = "redis://redis:6379/1"
app.conf.task_serializer = "json"
app.conf.result_serializer = "json"
app.conf.accept_content = ["json"]
app.conf.timezone = "UTC"
app.conf.enable_utc = True
app.conf.task_acks_late = True
app.conf.worker_prefetch_multiplier = 1
app.conf.task_default_rate_limit = "100/m"
app.autodiscover_tasks(["apps.backend.app.domain.notifications.tasks"])
