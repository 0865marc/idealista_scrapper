import logging
import logging.handlers

from idealista.app.main import IdealistaScraper

logger = logging.getLogger(__name__)
handler = logging.handlers.TimedRotatingFileHandler("idealista_scraper.log", when="midnight", interval=1)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

def main() -> None:
    IdealistaScraper(host="0.0.0.0", port=8000) # TODO: this blocks the main thread
    logger.info("Idealista scraper started")


if __name__ == "__main__":
    main()
