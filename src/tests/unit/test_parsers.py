from bs4 import BeautifulSoup

from src.scraper.crawler import IdealistaCrawler


def test_parse_idealista_list_page():
    idealista_crawler = IdealistaCrawler()

    with open("src/tests/unit/data/articles.html", "r") as file:
        html_content = file.read()
        soup = BeautifulSoup(html_content, "html.parser")

    articles = idealista_crawler.get_properties_from_list_page(soup)

    assert len(articles) == 30
    assert 107654102 in articles
