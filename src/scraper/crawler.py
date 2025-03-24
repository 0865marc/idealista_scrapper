import logging
import os
import time
import uuid
from base64 import b64decode
from typing import Literal

import redis
import redis.client
import requests
from bs4 import BeautifulSoup

from src.scraper.idealista_scraper import IdealistaScraper

logger = logging.getLogger("src.tasks.tasks")


class Crawler:
    """
    Handles the basics mecahnics of crawling a website.
    Right now it's only used for Idealista, but could be extended to other websites.
    """

    def __init__(self, webpage: Literal["idealista", "fotocasa"]) -> None:
        self.webpage = webpage
        self.REDIS_HOST: str = os.getenv("REDIS_HOST", "redis")
        self.REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
        self.MAX_WORKERS: int = int(os.getenv("MAX_WORKERS", 2))
        self.RETRY_DELAY: int = int(os.getenv("RETRY_DELAY", 1))  # seconds
        self.TIMEOUT: int = int(os.getenv("TIMEOUT", 30))  # seconds
        self.SEMAPHORE_KEY: str = "zyte_api_semaphore"
        self.ACTIVE_WORKERS_KEY: str = "zyte_api_active_workers"

        self.redis_client = redis.Redis(host=self.REDIS_HOST, port=self.REDIS_PORT)
        self.worker_id = str(uuid.uuid4())

    def request_through_zyte(self, url: str) -> BeautifulSoup | None:
        logger.info(f"Worker {self.worker_id} requesting {url} through Zyte")
        has_slot = False

        while not has_slot:
            with self.redis_client.pipeline() as pipe:
                has_slot = self.acquire_slot(pipe)

        try:
            res: requests.Response = requests.post(
                "https://api.zyte.com/v1/extract",
                auth=("7cdea51c9eaa4846afdb1641070b23e4", ""),  ## GET it from env
                json={"url": url, "httpResponseBody": True},
            )
            match res.status_code:
                case 200:
                    response_body = b64decode(res.json()["httpResponseBody"])
                    soup = BeautifulSoup(response_body, "html.parser")
                    return soup
                case 401:
                    logger.error("Zyte API key is empty/invalid")
                    return None
                case _:
                    logger.error(
                        f"Zyte response code: {res.status_code} | {res.json()}"
                    )
                    return None

        finally:
            with self.redis_client.pipeline() as pipe:
                self.release_slot(pipe)

    def acquire_slot(self, pipe: redis.client.Pipeline) -> bool:
        try:
            pipe.watch(self.SEMAPHORE_KEY)  # raises WatchError if value changes

            redis_value = self.redis_client.get(self.SEMAPHORE_KEY) or 0
            if isinstance(redis_value, bytes):
                current_count = int(redis_value.decode("utf-8"))
            elif isinstance(redis_value, int):
                current_count = 0
            else:
                logger.warning(f"Unexpected value for semaphore: {redis_value}")
                current_count = self.MAX_WORKERS

            if current_count < self.MAX_WORKERS:
                pipe.multi()
                pipe.incr(self.SEMAPHORE_KEY)
                pipe.hset(self.ACTIVE_WORKERS_KEY, self.worker_id, str(time.time()))

                pipe.execute()
                logger.info(f"Slot acquired ({current_count + 1}/{self.MAX_WORKERS})")
                return True
            else:
                # No available slot, wait and retry
                pipe.unwatch()
                logger.info(f"No available slot, waiting {self.RETRY_DELAY}")
                time.sleep(self.RETRY_DELAY)
                return False

        except redis.WatchError as e:
            logger.info(f"Redis watch error. Trying again... {e}")
            time.sleep(self.RETRY_DELAY)
            return False

    def release_slot(self, pipe: redis.client.Pipeline) -> None:
        pipe.decr(self.SEMAPHORE_KEY)
        pipe.hdel(self.ACTIVE_WORKERS_KEY, self.worker_id)
        pipe.execute()
        logger.info(f"Slot released ({self.worker_id})")


class IdealistaCrawler(Crawler):
    def __init__(self) -> None:
        super().__init__("idealista")
        self.scraper: IdealistaScraper = IdealistaScraper()

    def crawl_properties_from_list_page(self, soup: BeautifulSoup) -> dict[int, dict]:
        properties_soup = self.scraper.extract_properties_from_list_page(soup)

        properties_details: dict[int, dict] = {}
        for property_id in properties_soup.keys():
            properties_details[property_id] = (
                self.scraper.extract_property_details_from_list_page(
                    property_id, properties_soup
                )
            )
        return properties_details
