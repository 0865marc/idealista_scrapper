import uvicorn
from fastapi import FastAPI

from idealista.app.api.router import router


class IdealistaScraper:
    def __init__(self) -> None:
        self.app = FastAPI()
        self.app.include_router(router)

    def initialize_app(self, host: str, port: int) -> None:
        uvicorn.run(self.app, host=host, port=port)
