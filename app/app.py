from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse
from .routes import router
import os

BASE_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIRECTORY = os.path.join(BASE_DIRECTORY, "templates")
STATIC_DIRECTORY = os.path.join(BASE_DIRECTORY, "static")

class ResetCacheStaticFiles(StaticFiles):
    async def response(self, path: str, scope):
        response: FileResponse = await super().response(path, scope)
        response.headers["Cache-Control"] = "no-store"
        return response

def create_app():
    app = FastAPI()

    print("==> STATIC FOLDER =", STATIC_DIRECTORY)

    # Mount static files
    app.mount("/static", ResetCacheStaticFiles(directory=STATIC_DIRECTORY), name="static")

    # Include API routes
    app.include_router(router)

    return app