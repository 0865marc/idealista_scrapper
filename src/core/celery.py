import os
import logging

handler = logging.handlers.TimedRotatingFileHandler(
        "logs/idealista_scraper.log", when="midnight", interval=1
    )
logging.basicConfig(
    handlers=[handler],
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

from celery import Celery  # type: ignore


celery_app = Celery('app')
celery_app.conf.broker_url = f"redis://redis:6379/"
celery_app.conf.result_backend = f"redis://redis:6379/"
celery_app.conf.update(
    timezone='Europe/Madrid',
    enable_utc=True,
)
celery_app.autodiscover_tasks(["src.tasks"])
logger = logging.getLogger(__name__)
logger.info("Celery inicializado correctamente")