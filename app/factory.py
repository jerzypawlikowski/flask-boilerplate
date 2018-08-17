#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.api.utlis.http import json_response

db = SQLAlchemy()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_envvar("APP_CONFIG")
    register_extensions(app)
    register_blueprints(app)
    configure_error_handlers(app)
    app.template_folder = "frontend/templates"
    app.static_folder = "frontend/static"
    return app


def register_extensions(the_app: Flask):
    """
    Register all extensions for the app
    """
    db.app = the_app
    db.init_app(the_app)


def register_blueprints(the_app: Flask):
    """
    Register all blueprints that needs to be served by the app
    """
    from app.api.blueprints.user import user_blueprint
    the_app.register_blueprint(user_blueprint, url_prefix="/api/users/")
    from app.frontend.blueprints.main import main_blueprint
    the_app.register_blueprint(main_blueprint, url_prefix="/")


def configure_error_handlers(the_app: Flask):
    """
    Error handling
    """
    @the_app.errorhandler(404)
    def handle_404(e):
        return json_response(404, response_data={"error": "Not Found"})

    @the_app.errorhandler(405)
    def handle_405(e):
        return json_response(405, response_data={"error": "Method Not Allowed"})
