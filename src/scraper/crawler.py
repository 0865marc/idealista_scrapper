import logging
import os
import time
import uuid
from base64 import b64decode
from typing import Literal, cast

import redis
import redis.client
import requests
from bs4 import BeautifulSoup, Tag

logger = logging.getLogger("src.tasks.tasks")


class Crawler:
    def __init__(self, domain: Literal["idealista", "fotocasa"]) -> None:
        self.REDIS_HOST: str = os.getenv("REDIS_HOST", "redis")
        self.REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
        self.MAX_WORKERS: int = int(os.getenv("MAX_WORKERS", 2))
        self.RETRY_DELAY: int = int(os.getenv("RETRY_DELAY", 1))  # seconds
        self.TIMEOUT: int = int(os.getenv("TIMEOUT", 30))  # seconds
        self.SEMAPHORE_KEY: str = "zyte_api_semaphore"
        self.ACTIVE_WORKERS_KEY: str = "zyte_api_active_workers"

        self.redis_client = redis.Redis(host=self.REDIS_HOST, port=self.REDIS_PORT)
        self.worker_id = str(uuid.uuid4())

    def request_through_zyte(self, url: str) -> BeautifulSoup|None:
        logger.info(f"Worker {self.worker_id} requesting {url} through Zyte")
        has_slot = False

        while not has_slot:
            with self.redis_client.pipeline() as pipe:
                has_slot = self.acquire_slot(pipe)

        try:
            response: requests.Response = requests.post(
                "https://api.zyte.com/v1/extract",
                auth=("", ""),  ## GET it from env
                json={"url": url, "httpResponseBody": True},
            )
            if response.status_code != 200:
                logger.error(
                    f"Zyte response code: {response.status_code} | {response.json()}"
                    )
                return None

            response_body = b64decode(response.json()["httpResponseBody"])
            soup = BeautifulSoup(response_body, "html.parser")
            return soup

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
                logger.info(f"Slot acquired ({current_count + 1}/{self.MAX_WORKERS})")  # noqa: E501
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

    def crawl_properties(self, soup: BeautifulSoup) -> dict[int, dict]:
        properties_id = self.get_properties_from_list_page(soup)

        properties_details: dict[int, dict] = {}
        for property_id in properties_id:
            properties_details[property_id] = self.get_property_details(property_id)
        return properties_details

    def get_properties_from_list_page(self, soup: BeautifulSoup) -> list[int]:
        div_main = cast(Tag | None, soup.find("div", id="main"))
        if div_main is None:
            logger.error("No div main found")
            return []

        section_main = cast(Tag | None, div_main.find("main"))
        if section_main is None:
            logger.error("No section main found")
            return []

        articles = section_main.find_all("article", attrs={"data-element-id": True})
        articles = cast(list[Tag], articles)

        articles_id: list[int] = []
        for _article in articles:
            _article_id = _article.get("data-element-id")
            if _article_id is None:
                continue

            if isinstance(_article_id, str):
                articles_id.append(int(_article_id))
            elif isinstance(_article_id, list):
                # e.g. '<article data-element-id="123 456">...</article>'
                articles_id.append(int(_article_id[0]))
                logger.warning(f"strange data-element-id: {_article_id}")
            else:
                logger.error(f"unexpected data-element-id: {_article_id}")

        logger.info(f"{articles_id} properties from list page ")
        return articles_id

    def get_property_details(self, property_id: int) -> dict:
        return {}
