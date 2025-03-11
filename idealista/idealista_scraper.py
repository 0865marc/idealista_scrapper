from idealista.app.main import IdealistaAPI
from idealista.scraper.main import Scraper


class IdealistaScraper:
    """
    This class is the main entry point for the Idealista scraper.
    It starts & manages the API(/app) and the scraper(/scraper).
    """

    def __init__(self, host: str, port: int) -> None:
        self.scraper = Scraper()
        self.api = IdealistaAPI(host, port)

    def start(self) -> None:
        self.api.start() # TODO: this blocks the main thread
