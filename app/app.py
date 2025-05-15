"""
File: app.py
Description: Sets up directories, resets cache of static/template files, and
configures all routes (rendering templates, function calls, etc.).
"""

# Imports
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from .routes import router
import os

# Get directory paths
BASE_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIRECTORY = os.path.join(BASE_DIRECTORY, "templates")
STATIC_DIRECTORY = os.path.join(BASE_DIRECTORY, "static")

# Resets the cache of static files
class ResetCacheStaticFiles(StaticFiles):
    async def response(self, path: str, scope):
        """
        Given a directory path and type, it will reset the cached files to
        update any changes made to them
        """
        response: FileResponse = await super().response(path, scope)
        response.headers["Cache-Control"] = "no-store"
        return response


def create_app():
    """
    Create a FastAPI app with necessary static files and API routes
    """
    app = FastAPI()
    app.mount("/static", ResetCacheStaticFiles(directory=STATIC_DIRECTORY), name="static") # Set static files path (reset cache)
    app.include_router(router) # Get API routes

    return app