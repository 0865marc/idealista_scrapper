import logging
import logging.handlers

from dotenv import load_dotenv

from idealista.idealista_scraper import IdealistaScraper

load_dotenv()

logger = logging.getLogger()
handler = logging.handlers.TimedRotatingFileHandler(
    "logs/idealista_scraper.log", when="midnight", interval=1
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def main() -> None:
    logger.error("TESTING")
    idealista_scrapper = IdealistaScraper(host="0.0.0.0", port=8000)

    logger.info("Idealista scraper started")

    idealista_scrapper.start()


if __name__ == "__main__":
    main()
