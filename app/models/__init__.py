# coding: utf8

from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()


class DBMixin:
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()


from .user import UserModel

def create_data_for_test(app):

    with app.app_context():
        db.drop_all()
        db.create_all()

        models = [
            UserModel
        ]
        for model in models:
            model.create_data_for_test()
