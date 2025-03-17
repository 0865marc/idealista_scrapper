import os
import logging

from celery import Celery  # type: ignore


logger = logging.getLogger("src.tasks.celery")

celery_app = Celery('app')
celery_app.conf.broker_url = f"redis://redis:6379/"
celery_app.conf.result_backend = f"redis://redis:6379/"
celery_app.conf.update(
    timezone='Europe/Madrid',
    enable_utc=True,
    worker_hijack_root_logger=False,
    broker_connection_retry_on_startup=True
)
celery_app.autodiscover_tasks(["src.tasks"])
logger.info("Celery inicializado correctamente")
logger.debug("Celery inicializado correctamente")
