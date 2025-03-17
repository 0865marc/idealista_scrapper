import logging
import os

from fastapi import APIRouter

from src.api.routers import properties
from src.api.routers import users
from src.tasks.tasks import get_properties_from_list_page

logger = logging.getLogger(__name__)

router = APIRouter()
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(properties.router, prefix="/properties", tags=["properties"])


@router.get("/")
def read_root():
    _properties = get_properties_from_list_page.delay(
        "https://www.idealista.com/venta-viviendas/lleida-lleida/?ordenado-por=fecha-publicacion-desc"
        )
    return {"message": "okay"}