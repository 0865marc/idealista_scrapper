from src.api.main import app
#from src.core.logging import setup_logging
from src.core.celery import celery_app
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

def main() -> None:
    print("this should only print once")
    app.start(celery_app)

if __name__ == "__main__":
    main()
