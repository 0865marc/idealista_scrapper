import logging

from idealista.scraper.redis import RedisManager

logger = logging.getLogger(__name__)


class Scraper:
    """
    This class is the main entry point for the Idealista scraper.
    """

    def __init__(self) -> None:
        self.redis_manager: RedisManager = RedisManager()
