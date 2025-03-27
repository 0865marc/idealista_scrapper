import logging
from typing import Any, cast

from bs4 import BeautifulSoup, Tag

logger = logging.getLogger("src.tasks.tasks.idealista_scraper")


class IdealistaScraper:
    """
    Handles extractions of data from Idealista diferent pages.
    """

    def __init__(self) -> None:
        self.list_page_scraper: ListPageScraper = ListPageScraper()
        self.detail_page_scraper: DetailPageScraper = DetailPageScraper()

    def extract_properties_from_list_page(self, soup: BeautifulSoup) -> dict[int, Tag]:
        properties_tag = self.list_page_scraper.extract_properties(soup)
        return properties_tag

    def extract_property_details_from_list_page(
        self, property_id: int, properties_tag: dict[int, Tag]
    ) -> dict:
        if property_id not in properties_tag:
            return {}
        return self.list_page_scraper.extract_property_details(
            property_id, properties_tag[property_id]
        )


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
            return {}

        section_main = cast(Tag | None, div_main.find("main"))
        if section_main is None:
            logger.error("No section main found")
            return {}

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

        return properties_soup

    def extract_property_details(self, property_id: int, soup: Tag) -> dict:
        return self.HTMLParser(property_id, soup).parse()

    class HTMLParser:
        def __init__(self, property_id: int, soup: Tag) -> None:
            self.property_id = property_id
            self.soup = soup

        def parse(self) -> dict:
            try:
                return {
                    "title": self.parse_title(),
                    "price": self.parse_price(),
                    "parking": self.parse_parking()[0],
                    "parking_price": self.parse_parking()[1],
                    "description": self.parse_description(),
                }
            except ValueError as e:
                logger.error(f"Error {e} in {self.property_id}: {self.soup}")
                return {}

        def parse_title(self) -> str:
            item_info_ct = self.soup.find("div", class_="item-info-container")
            if not isinstance(item_info_ct, Tag):
                raise ValueError(
                    f"No item info container found for property {self.property_id}"
                )
            self.item_info_ct = item_info_ct

            title_element = item_info_ct.find("a", class_="item-link")
            if title_element is None:
                raise ValueError(
                    f"No title element found for property {self.property_id}"
                )
            return title_element.text.strip()

        def parse_price(self) -> int:
            price_row_div = self.item_info_ct.find("div", class_="price-row")
            if not isinstance(price_row_div, Tag):
                raise ValueError(
                    f"No price row div found for property {self.property_id}"
                )
            self.price_row_div = price_row_div

            item_price_span = price_row_div.find("span", class_="item-price")
            if not isinstance(item_price_span, Tag):
                raise ValueError(
                    f"No item price span found for property {self.property_id}"
                )

            for _content in item_price_span.contents:
                if isinstance(_content, str):
                    if _content.replace(".", "").isdigit():
                        price = int(_content.replace(".", ""))
                if not isinstance(_content, Tag):
                    logger.warning(f"Unexpected content type {_content}")
                    continue

                if _content.get("class") is None:
                    logger.warning(f"No class found for element {_content}")
                elif _content.get("class") == ["txt-big"]:
                    currency = _content.text.strip()
                    if currency == "€":
                        pass
                    else:
                        raise ValueError(f"Unknown currency {currency}")
                else:
                    logger.warning(f"Unknown price element {_content}")
            return price

        def parse_parking(self) -> tuple[bool, int]:
            parking: bool = False
            parking_price: int = 0

            parking_element = self.item_info_ct.find("span", class_="item-parking")
            if not isinstance(parking_element, Tag):
                return parking, parking_price

            for _content in parking_element.contents:
                if isinstance(_content, str):
                    if "GARAJE" in _content.upper():
                        parking = True
            return parking, parking_price

        def parse_description(self) -> str:
            description: str = ""
            item_description_ct = self.item_info_ct.find("div", class_="description")
            if not isinstance(item_description_ct, Tag):
                return description

            for _content in item_description_ct.contents:
                if isinstance(_content, str):
                    if _content.strip() == "":
                        pass
                    logger.warning(f"Unexpected str in description {_content}")
                    continue

                if not isinstance(_content, Tag):
                    logger.warning("description_ct is not Tag type")
                    continue

                if _content.get("class") is None:
                    logger.warning(f"No class found for element {_content}")
                elif _content.get("class") == ["ellipsis"]:
                    description = _content.text.strip()
                else:
                    logger.warning(f"Unknown description element {_content}")
            return " ".join(description.split())

        def parse_item_details(self) -> dict:
            item_detail_char = self.item_info_ct.find("div", class_="item-detail-char")
            if not isinstance(item_detail_char, Tag):
                return {}

            details: dict[str, Any] = {}
            floor: int | None = None
            elevator: bool = False
            rooms: int | None = None
            size: int | None = None
            for _content in item_detail_char.contents:
                if isinstance(_content, str):
                    logger.warning(f"Unexpected str in item details {_content}")
                elif not isinstance(_content, Tag):
                    logger.warning(f"Unexpected content type {_content}")
                elif _content.get("class") is None:
                    logger.warning(f"No class found for element {_content}")
                elif _content.get("class") == ["item-detail"]:
                    if "hab" in _content.text.strip().lower():
                        rooms = _content.text.strip()
                    elif "m²" in _content.text.strip().lower():
                        size = _content.text.strip()
                    elif "planta" in _content.text.strip().lower():
                        floor = _content.text.strip()
                        elevator = "ascensor" in _content.text.strip().lower()
            details = {
                "floor" : floor,
                "elevator" : elevator,
                "rooms" : rooms,
                "size" : size
            }

            return details


class DetailPageScraper:
    """
    Handles extractions of data from Idealista detail page.
    """

    def __init__(self) -> None:
        pass
