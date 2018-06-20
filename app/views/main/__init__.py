# coding: utf8

from ...flask_exts import Blueprint

main = Blueprint('main', __name__)

from . import index, login, post, task
