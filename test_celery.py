import os
from celery import Celery  # type: ignore

class CeleryManager:
    def __init__(self) -> None:
        self.celery_app = Celery('idealista')
        self.setup_celery()

    def setup_celery(self) -> None:
        redis_host = os.getenv('REDIS_HOST', 'localhost')
        redis_port = os.getenv('REDIS_PORT', '6379')
        redis_db = os.getenv('REDIS_DB', '0')
        
        self.celery_app.conf.broker_url = f"redis://{redis_host}:{redis_port}/{redis_db}"
        self.celery_app.conf.result_backend = f"redis://{redis_host}:{redis_port}/{redis_db}"

        self.celery_app.conf.update(
            timezone='Europe/Madrid',
            enable_utc=True,
        )

    def start_celery(self) -> None:
        # Inicia el worker desde código
        from celery.bin import worker
        worker_instance = worker.worker(app=self.celery_app)
        worker_instance.run(loglevel='INFO')

celery_manager = CeleryManager()
celery_app = celery_manager.celery_app