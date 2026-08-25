from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "ecommerce",
    broker=settings.REDIS_URL,
    include=["app.tasks.order"],
)

celery_app.conf.update(
    task_ignore_result=True,
    task_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    broker_connection_retry_on_startup=True,
)
