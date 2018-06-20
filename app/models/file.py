# coding: utf8

from . import db, DBMixin

from werkzeug.utils import secure_filename

import hashlib
import datetime
import os.path
import os


class FileModel(db.Model, DBMixin):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(250))
    path = db.Column(db.Unicode(250))
    url = db.Column(db.Unicode(250))
    sha1 = db.Column(db.Unicode(40))
    size = db.Column(db.Integer)

    created_at = db.Column(db.DateTime)

    @classmethod
    def create(cls, name, path, url, sha1, created_at, size):
        return cls(name=name,
                   path=path,
                   url=url,
                   sha1=sha1,
                   created_at=created_at,
                   size=size)

    def deletefile(self):
        os.remove(self.path)

    def delete(self):
        self.deletefile()
        super().delete()

    @classmethod
    def savefile(cls, file, folder, url_prefix):
        now = datetime.datetime.now()
        filename = file.filename
        filebytes = file.read()
        file.seek(0)
        size = len(filebytes)

        if size > 1 * 1024 * 1024:
            raise TypeError('文件太大，建议不超过1m')

        sha1 = hashlib.sha1(filebytes).hexdigest()

        url = os.path.join(url_prefix, sha1)
        print(url_prefix, sha1, url)
        if cls.query.filter_by(sha1=sha1).first():
            raise FileExistsError(f'{filename} 已经存在，请勿重复上传')
        else:
            path = os.path.join(folder, sha1)
            file.save(path)
            return cls.create(name=filename,
                              path=path,
                              url=url,
                              sha1=sha1,
                              created_at=now,
                              size=size).save()
