# coding: utf8

from flask_login.config import LOGIN_MESSAGE, LOGIN_MESSAGE_CATEGORY

from os import path
import datetime


class Config:
    """基础配置"""

    '''Flask配置'''
    # SERVER_NAME = '127.0.0.1:5000'
    SECRET_KEY = 'Hello world!'

    '''Flask-SQLAlchemy配置'''
    SQLALCHEMY_DATABASE_URI = r'mysql+pymysql://root:password@localhost:3307/class1db?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    '''Flask-Login配置'''
    LOGIN_MESSAGE = '您可以在该页面登陆到系统'
    LOGIN_MESSAGE_CATEGORY = 'info'

    # 上传文件夹/根据自己的设置更改
    UPLOADS_FOLDER = 'uploads/pictures/'

class DebugConfig(Config):
    """调试版配置"""

    '''Flask配置'''
    DEBUG = True
    # EXPLAIN_TEMPLATE_LOADING = True
    TEMPLATES_AUTO_RELOAD = True
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(seconds=45)  # session 过期时间


class ReleaseConfig(Config):
    """发行版配置"""

    '''Flask配置'''
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(minutes=30)  # session 过期时间

    '''Flask-SQLAlchemy配置'''
    SQLALCHEMY_DATABASE_URI = r'mysql+pymysql://root:password@xxx.xxx.cn/class1db?charset=utf8mb4'

