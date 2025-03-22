import logging
from typing import cast

from bs4 import BeautifulSoup, Tag

logger = logging.getLogger("src.tasks.tasks")


class IdealistaScraper:
    """
    Handles extractions of data from Idealista diferent pages.
    """

    def __init__(self) -> None:
        self.list_page_scraper: ListPageScraper = ListPageScraper()
        self.detail_page_scraper: DetailPageScraper = DetailPageScraper()

    def extract_properties(self, soup: BeautifulSoup) -> dict[int, Tag]:
        properties_tag = self.list_page_scraper.extract_properties(soup)

        properties_details = {}
        for property_id, property_tag in properties_tag.items():
            properties_details[property_id] = (
                self.list_page_scraper.extract_property_details(
                    property_id, property_tag
                )
            )
        return properties_details


class ListPageScraper:
    """
    Handles extractions of data from Idealista list page.
    """

    def __init__(self) -> None:
        pass

    def extract_properties(self, soup: BeautifulSoup) -> dict[int, Tag]:
        div_main = cast(Tag | None, soup.find("div", id="main"))
        if div_main is None:
            logger.error("No div main found")
            return []

        section_main = cast(Tag | None, div_main.find("main"))
        if section_main is None:
            logger.error("No section main found")
            return []

        properties = section_main.find_all("article", attrs={"data-element-id": True})
        properties = cast(list[Tag], properties)

        properties_soup: dict[int, Tag] = {}
        for _property in properties:
            _property_id = _property.get("data-element-id")
            if _property_id is None:
                continue

            if isinstance(_property_id, str):
                properties_soup[int(_property_id)] = _property
            elif isinstance(_property_id, list):
                # e.g. '<article data-element-id="123 456">...</article>'
                properties_soup[int(_property_id[0])] = _property
            else:
                logger.error(f"unexpected data-element-id: {_property_id}")

        logger.info(f"{properties_soup.keys()} properties from list page ")
        return properties_soup

    def extract_property_details(self, property_id: int, soup: BeautifulSoup) -> dict:
        details = {}
        item_info_ct = soup.find("div", class_="item-info-container")
        if item_info_ct is None:
            logger.error(f"No item info container found for property {property_id}")
            return {}

        details["title"] = item_info_ct.find("a", class_="item-link").text.strip()

        price_row_elements = item_info_ct.find(
            "div", class_="price-row"
        ).find_all("span", recursive=False)
        for _element in price_row_elements:
            if _element.get("class") is None:
                logger.warning(f"No class found for element {_element}")
            elif _element.get("class") == ["item-price", "h2-simulated"]:
                price_elements = _element.contents
                for _price_element in price_elements:
                    if isinstance(_price_element, str):
                        details["price"] = int(_price_element.replace(".", ""))
                        continue
                    if _price_element.get("class") is None:
                        logger.warning(f"No class found for price element {_price_element}")
                    elif _price_element.get("class") == ["txt-big"]:
                        currency = _price_element.text.strip()
                        if currency == "€":
                            details["currency"] = _price_element.text.strip()
                        else:
                            logger.warning(f"Unknown currency {currency}")

            elif _element.get("class") == ["item-parking"]:
                for _parking_element in _element.contents:
                    if isinstance(_parking_element, str):
                        if "GARAJE" in _parking_element.upper():
                            continue

                        price, currency = _parking_element.split(" ")
                        if price.replace(".", "").isdigit():
                            if currency == "€":
                                pass
                            else:
                                logger.warning(f"Unknown currency {currency}")
                            continue

                        logger.warning(f"Unknown parking element {_parking_element}")

            else:
                logger.error(f"Unknown price row element {_element}")


        _description = item_info_ct.find("div", class_="description").text.strip()
        details["description"] = " ".join(_description.split())

        return details


class DetailPageScraper:
    """
    Handles extractions of data from Idealista detail page.
    """

    def __init__(self) -> None:
        pass
