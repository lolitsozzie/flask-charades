from flask import Flask

from demo.extensions import db, migrate
from .blueprints import demo_bp


def create_app(config=None, app_name=None):
    """
    Create a Flask app.
    :param config: A Config type object for configuring the application.
    :param app_name: The name of the app.
    :return: The Flask app instance.
    """
    if config is None:
        raise Exception('No configuration passed to create_app().')
    if app_name is None:
        app_name = 'demo'

    app = Flask(app_name)

    configure_app(app, config)
    configure_extensions(app)
    configure_blueprints(app)
    return app


def configure_app(app: Flask, config):
    """
    Configure the app.
    :param app: A Flask app.
    :param config: A config object.
    """
    app.config.from_object(config)


def configure_extensions(app: Flask):
    """
    Initialize flask extensions with init_app.
    """
    db.init_app(app)
    migrate.init_app(app, db)


def configure_blueprints(app: Flask):
    """
    Configure blueprints.
    """
    app.register_blueprint(demo_bp)

