# coding: utf8


from . import main

from flask import request

from ...models.task import TaskModel, UserFileModel
from ...models.file import FileModel

from flask import request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, ValidationError, FileField
from wtforms.validators import DataRequired, Optional, Regexp, Length, StopValidation
from flask_login import current_user


class UserFileForm(FlaskForm):
    userfile = FileField(label='userfile',
                         validators=[DataRequired()])


@main.route('/userfile/<int:task_id>/delete')
def delete_userfile(task_id):
    task = TaskModel.query.get(task_id)
    if task:
        userfile = current_user.get_userfile(task)
        if userfile:
            file = userfile.file
            userfile.delete()
            file.delete()

            flash('删除成功！你可以上传新的作品啦')
    else:
        flash('文件不存在，删除失败')
    return redirect(url_for('main.task_view', task_id=task_id))

@main.route('/task/<int:task_id>', methods=['GET', 'POST'])
def task_view(task_id):
    form = UserFileForm()
    task = TaskModel.query.get(task_id)
    if request.method == 'GET':

        return main.render_template('task.html', task=task, form=form)
    else:
        if form.validate_on_submit():
            userfile_file = form.userfile.data
            try:
                userfile = FileModel.savefile(file=userfile_file,
                                              folder=main.uploads_folder,
                                              url_prefix=url_for('static', filename=main.config['UPLOADS_FOLDER']))

                UserFileModel.create(user=current_user,
                                     task=task,
                                     file=userfile)
                return redirect(url_for('main.task_view', task_id=task_id))
            except FileExistsError as err:
                flash(err)
            except TypeError as err:
                flash(err)
        return main.render_template('task.html', task=task, form=form)