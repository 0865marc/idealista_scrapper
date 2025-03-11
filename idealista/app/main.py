import uvicorn
from fastapi import FastAPI

from idealista.app.api.router import router


class IdealistaAPI:
    """
    This class is the main entry point for the Idealista API. Built on top of FastAPI.
    """

    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port

        self.app = FastAPI()
        self.app.include_router(router)

    def start(self) -> None:
        uvicorn.run(self.app, host=self.host, port=self.port)
