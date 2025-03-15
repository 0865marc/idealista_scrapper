import time 
from src.core.celery import celery_app

import logging

logger = logging.getLogger(__name__)

@celery_app.task
def wait_10_seconds():
    logger.warning("Waiting 10 seconds")
    print(logger.handlers)
    time.sleep(10)
    logger.warning("Done waiting")
    return "Done"



