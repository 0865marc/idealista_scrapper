import logging
import os

from fastapi import APIRouter

from src.api.routers import properties
from src.api.routers import users
from src.tasks.tasks import wait_10_seconds

logger = logging.getLogger(__name__)

router = APIRouter()
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(properties.router, prefix="/properties", tags=["properties"])


@router.get("/")
def read_root():
    wait_10_seconds.delay()
    return {"message": "Hello"}
