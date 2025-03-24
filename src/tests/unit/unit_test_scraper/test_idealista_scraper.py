import pytest
from bs4 import BeautifulSoup, Tag

from src.scraper.idealista_scraper import IdealistaScraper


@pytest.fixture
def idealista_scraper() -> IdealistaScraper:
    return IdealistaScraper()


@pytest.fixture
def articles_list_soup_from_file() -> BeautifulSoup:
    with open("src/tests/unit/data/articles.html", "r") as file:
        html_content = file.read()
        return BeautifulSoup(html_content, "html.parser")


@pytest.fixture
def extracted_articles_from_list_page(
    idealista_scraper: IdealistaScraper, articles_list_soup_from_file: BeautifulSoup
) -> dict[int, Tag]:
    return idealista_scraper.extract_properties_from_list_page(
        articles_list_soup_from_file
    )


def test_extract_properties_from_list_page(
    extracted_articles_from_list_page: dict[int, Tag],
) -> None:
    assert len(extracted_articles_from_list_page) == 30
    assert 107654102 in extracted_articles_from_list_page


def test_extract_property_details_from_list_page(
    idealista_scraper: IdealistaScraper,
    extracted_articles_from_list_page: dict[int, Tag],
) -> None:
    # Property 107654102
    details = idealista_scraper.extract_property_details_from_list_page(
        107654102, extracted_articles_from_list_page
    )
    assert details["title"] == "Casa o chalet independiente en Ciutat Jardí, Lleida"
    assert details["price"] == 525000
    assert (
        details["description"]
        == "En breve presentamos chalet unifamiliar de 220m2 con parcela de 820m2, en las cercanías del CLUB DE TENNIS LLEIDA. Ideal para familias, que valoren tranquilidad, cerca del colegio Espiga y del Club. Llamanos para inscribirte en la lista para visitar dicho inmueble."  # noqa: E501
    )

    # Property 107651666
    details = idealista_scraper.extract_property_details_from_list_page(
        107651666, extracted_articles_from_list_page
    )
    assert details["title"] == "Piso en Albert Porqueras, Mariola, Lleida"
    assert details["price"] == 140000
    assert details["parking"] is True
    assert details["parking_price"] == 0
    assert (
        details["description"]
        == "¿Te imaginas tu vivienda en propiedad en Lérida? ¡Testa Homes lo hace posible! *La vivienda y fotos publicadas corresponden a una vivienda tipo, para más información consulte a su gestor comercial. Vivienda sin amueblar. Suelos de tarima y armarios empotrados. Cocina amueblada con encimera, horno, fregadero y campan"  # noqa: E501
    )
