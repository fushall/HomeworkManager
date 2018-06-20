# coding: utf8

from flask import Blueprint as FlaskBlueprint, \
                  render_template as flask_render_template
import os.path

class Blueprint(FlaskBlueprint):

    def render_template(self, template_name, **context):
        template_name = f'/views/{self.name}/{template_name}'
        return flask_render_template(template_name, **context)

    def init_config(self, app_config):
        self.config = app_config

    @property
    def uploads_folder(self):
        return self._uploads_folder

    @uploads_folder.setter
    def uploads_folder(self, value):
        self._uploads_folder = value
