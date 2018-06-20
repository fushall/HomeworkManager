# coding: utf8

from .main import main
import os.path

db = None


class BlueprintManager:

    def __init__(self, app=None, database=None):
        self.app = None
        self.db = None

        self.init_app(app)
        self.init_db(database)

    def init_db(self, database):
        assert database is not None

        self.db = database

    def init_app(self, app):
        assert app is not None

        self.app = app
        blueprints = [
            main
        ]
        for blueprint in blueprints:
            blueprint.init_config(self.app.config)
            blueprint.uploads_folder = app.uploads_folder
            self.app.register_blueprint(
                blueprint
            )


