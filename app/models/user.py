# coding: utf8
from . import db, DBMixin

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class UserModel(db.Model, DBMixin, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    number = db.Column(db.Unicode(11))
    name = db.Column(db.Unicode(5), nullable=False)

    @classmethod
    def create(cls, number, name):
        return cls(number=number, name=name)

    @classmethod
    def get(cls, number):
        return cls.query.filter_by(number=number).first()

    def is_completed_task(self, task):
        return self.get_userfile(task) is not None

    def get_userfile(self, task):
        if task and task.userfiles:
            for userfile in task.userfiles:
                if userfile.user == self:
                    return userfile


    @classmethod
    def create_data_for_test(cls):
        students = '''11111111111,张三'''
        for student in students.split('\n'):
            info = student.split(',')
            stu_number = info[0]
            stu_name = info[1]
            cls.create(stu_number, stu_name).save()
