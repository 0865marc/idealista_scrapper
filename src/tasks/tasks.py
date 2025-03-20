import logging
import logging.handlers
import os

from src.core.celery import celery_app
from src.scraper.crawler import IdealistaCrawler

logger = logging.getLogger(__name__)
handler = logging.handlers.TimedRotatingFileHandler(
    "logs/tasks.log",
    when="midnight",
    interval=1,
)
handler.setFormatter(
    logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
)
logger.addHandler(handler)
logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))


@celery_app.task
def get_properties_from_list_page(url: str) -> list[int]:
    crawler = IdealistaCrawler()
    soup = crawler.request_through_zyte(url)
    if soup is not None:
        return crawler.get_properties_from_list_page(soup)
    return []
