import logging
import os

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from celery import Celery

from src.api.routers.router import router


logger = logging.getLogger(__name__)
handler = logging.handlers.TimedRotatingFileHandler(
    "logs/api/api.log",
    when="midnight", 
    interval=1,
)
handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                      datefmt="%Y-%m-%d %H:%M:%S",)
    )
logger.addHandler(handler)
logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))


app = FastAPI(
    title="Idealista API",
    description="API to consume scraped data from Idealista",
)
app.include_router(router)

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


