# coding: utf8
from . import db, DBMixin
from .user import UserModel

import datetime
import os
import os.path
import shutil
import zipfile

class UserFileModel(db.Model, DBMixin):
    __tablename__ = 'userfiles'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('UserModel', backref='userfiles')

    file_id = db.Column(db.Integer, db.ForeignKey('files.id'))
    file = db.relationship('FileModel')

    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))
    task = db.relationship('TaskModel', backref='userfiles')

    @classmethod
    def create(cls, user, task, file):
        return cls(user=user,
                   task=task,
                   file=file).save()


class TaskModel(db.Model, DBMixin):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.UnicodeText)
    content = db.Column(db.UnicodeText)

    picture_id = db.Column(db.Integer, db.ForeignKey('files.id'))
    picture = db.relationship('FileModel')

    created_at = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('UserModel', backref='tasks')

    @property
    def userfile_count(self):
        count = len(self.userfiles) if self.userfiles else 0
        return count

    def not_completed_users(self):
        users = UserModel.query.all()

        for userfile in self.userfiles:
            if userfile.user in users:
                users.remove(userfile.user)
        return users

    def user_is_not_completed(self, user):
        return user in self.not_completed_users()

    def zip_userfiles(self, dist_folder):
        try:
            os.makedirs(dist_folder)
        except FileExistsError:
            print('目录已经存在，请勿重复创建')

        _zipfile = zipfile.ZipFile(os.path.join(dist_folder, self.title + '.zip'), mode='w')
        for userfile in self.userfiles:
            sub_dir = userfile.user.number + ' ' + userfile.user.name
            arcname = os.path.join(sub_dir, userfile.file.name)
            print(arcname)
            _zipfile.write(userfile.file.path, arcname=arcname)
        _zipfile.close()



    @classmethod
    def create(cls, title, content, picture, user, created_at=datetime.datetime.now()):
        return cls(title=title,
                   content=content,
                   picture=picture,
                   user=user,
                   created_at=created_at).save()
