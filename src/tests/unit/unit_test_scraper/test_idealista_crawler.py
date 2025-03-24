import pytest
from bs4 import BeautifulSoup

from src.scraper.crawler import IdealistaCrawler


@pytest.fixture
def idealista_crawler() -> IdealistaCrawler:
    return IdealistaCrawler()


@pytest.fixture
def articles_list_soup_from_file() -> BeautifulSoup:
    with open("src/tests/unit/data/articles.html", "r") as file:
        html_content = file.read()
        return BeautifulSoup(html_content, "html.parser")


def test_crawl_properties_from_list_page(
    idealista_crawler: IdealistaCrawler,
    articles_list_soup_from_file: BeautifulSoup,
) -> None:
    properties_details = idealista_crawler.crawl_properties_from_list_page(
        articles_list_soup_from_file
    )
    assert len(properties_details) == 30
