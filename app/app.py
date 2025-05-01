from flask import Flask
import os
from app.routes import routes

BASE_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIRECTORY = os.path.join(BASE_DIRECTORY, "templates")
STATIC_DIRECTORY = os.path.join(BASE_DIRECTORY, "static")

def create_app():
    app = Flask(__name__, template_folder=TEMPLATES_DIRECTORY, static_folder=STATIC_DIRECTORY)
    app.register_blueprint(routes)
    return app