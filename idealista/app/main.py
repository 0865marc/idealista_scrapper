import uvicorn
from fastapi import FastAPI

from idealista.app.api.router import router


class IdealistaScraper:
    def __init__(self, host: str, port: int) -> None:
        self.app = FastAPI()
        self.app.include_router(router)
        uvicorn.run(self.app, host=host, port=port)
