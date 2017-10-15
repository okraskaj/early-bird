import importlib

from flask import Flask
from flask_cors import CORS

from .db import db
from .config import get_config
from .flask_restful_extensions import (
    Api,
    API_RESOURCES_REGISTER,
)


def init_app(config_name=None):
    # automatically register all api resources
    importlib.import_module('app.resources')
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(get_config(config_name))
    app.api = Api(
        app,
        # catch_all_404s=True,
        # default_mediatype='application/json',
    )
    app.api.add_resources(API_RESOURCES_REGISTER)
    db.init_app(app)
    return app
