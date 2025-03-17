import logging
import requests
from base64 import b64decode
import os

from bs4 import BeautifulSoup

from src.core.celery import celery_app


logger = logging.getLogger(__name__)
handler = logging.handlers.TimedRotatingFileHandler(
    "logs/tasks/tasks.log",
    when="midnight", 
    interval=1,
)
handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                      datefmt="%Y-%m-%d %H:%M:%S",)
    )
logger.addHandler(handler)
logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))


@celery_app.task
def get_properties_from_list_page(url: str) -> list[int]:
    logger.info(f"Getting properties from list page {url}")
    response: requests.Response = requests.post(
        "https://api.zyte.com/v1/extract",
        auth=("", ""), ## GET it from env
        json={
            "url": url,
            "httpResponseBody": True
        }
    )
    logger.info(f"Zyte esponse code: {response.status_code}")

    response_body: bytes = b64decode(response.json()["httpResponseBody"])
    soup = BeautifulSoup(response_body, "html.parser")
    div_main = soup.find("div", id="main")
    section_main = div_main.find("main")
    articles = section_main.find_all("article", attrs={"data-element-id": True})
    articles_id = [
        _a.get("data-element-id") for _a in articles
    ]
    logger.info(f"{articles_id} properties from list page {url}")
    return articles_id


