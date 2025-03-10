from fastapi import APIRouter

from idealista.app.api.endpoints import properties, users

router = APIRouter()

router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(properties.router, prefix="/properties", tags=["properties"])
