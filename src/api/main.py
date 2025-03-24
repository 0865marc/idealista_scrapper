import logging
import logging.handlers
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.api.routers.router import router
from src.db.base import create_db_and_tables

logger = logging.getLogger(__name__)
handler = logging.handlers.TimedRotatingFileHandler(
    "logs/api.log",
    when="midnight",
    interval=1,
)
handler.setFormatter(
    logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
)
logger.addHandler(handler)
logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))


app = FastAPI(
    title="Idealista API",
    description="API to consume scraped data from Idealista",
)
app.include_router(router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


# Middleware to log requests and responses
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Registra información de cada solicitud HTTP."""
    logger.info(f"Solicitud recibida: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Respuesta enviada: {response.status_code}")
    return response


@app.exception_handler(Exception)
async def handle_exceptions(request: Request, exc: Exception):
    """Maneja excepciones inesperadas y devuelve un error 500."""
    logger.error(f"Error inesperado: {exc}")
    return JSONResponse(status_code=500, content={"error": "Unexpected error"})
