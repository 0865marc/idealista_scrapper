# import logging


# def setup_logging():
#     handler = logging.handlers.TimedRotatingFileHandler(
#         "logs/idealista_scraper.log", when="midnight", interval=1
#     )
#     logging.basicConfig(
#         handlers=[handler],
#         level=logging.INFO,
#         format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
#         datefmt="%Y-%m-%d %H:%M:%S",
#     )