import os

from celery import Celery  # type: ignore


class CeleryManager:
    def __init__(self) -> None:
        self.celery_app = Celery('idealista')

    def setup_celery(self) -> None:
        self.celery_app.conf.broker_url = f"redis://{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}/{os.getenv('REDIS_DB')}"
        self.celery_app.conf.result_backend = f"redis://{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}/{os.getenv('REDIS_DB')}"

        self.celery_app.conf.update(
            timezone='Europe/Madrid',
            enable_utc=True,
        )
