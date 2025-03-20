from celery import Celery

celery_app = Celery("app")
celery_app.conf.update(
    broker_url="redis://redis:6379/",
    result_backend="redis://redis:6379/",
    timezone="Europe/Madrid",
    enable_utc=True,
    worker_hijack_root_logger=False,
    broker_connection_retry_on_startup=True,
)
celery_app.autodiscover_tasks(["src.tasks"])
