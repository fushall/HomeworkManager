# coding: utf8


from flask import Flask, url_for, send_from_directory

from .config import DebugConfig, ReleaseConfig
from .models import db, create_data_for_test
from .models.user import UserModel
from .models.task import TaskModel

from .views import BlueprintManager
from flask_login import LoginManager

import os.path

from flask_debugtoolbar import DebugToolbarExtension



def init_flask_login(app):
    login_manager = LoginManager(app)
    login_manager.login_view = 'main.login_view'
    login_manager.login_message = app.config.get('LOGIN_MESSAGE')
    login_manager.login_message_category = app.config.get('LOGIN_MESSAGE_CATEGORY')

    @login_manager.user_loader
    def load_user(user_id):
        return UserModel.query.get(int(user_id))

    return login_manager


def create_app():
    app = Flask(__name__)

    # 向模板添加全局函数
    app.jinja_env.globals['is_str'] = lambda v: isinstance(v, str)
    app.jinja_env.globals['is_list'] = lambda v: isinstance(v, list)
    app.jinja_env.globals['is_dict'] = lambda v: isinstance(v, dict)
    app.jinja_env.globals['is_tuple'] = lambda v: isinstance(v, tuple)

    # 加载配置文件
    app.config.from_object(ReleaseConfig)
    # 修正上传文件路径
    app.uploads_folder = os.path.join(app.static_folder, app.config['UPLOADS_FOLDER'])

    # 初始化数据库
    db.init_app(app)

    # 初始化蓝本管理器
    BlueprintManager(app, db)

    # flask_login 插件
    init_flask_login(app)

    # flask_debugtoolbar 插件
    # DebugToolbarExtension(app)

    @app.shell_context_processor
    def make_shell_context():
        return dict(
            app=app,
            db=db,
            UserModel=UserModel,
            TaskModel=TaskModel,
            create_data_for_test=create_data_for_test,
        )
    return app


