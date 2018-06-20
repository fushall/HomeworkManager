# coding: utf8

from . import main

from ...models.file import FileModel
from ...models.task import TaskModel

from werkzeug.utils import secure_filename
from flask import request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, FileField
from wtforms.validators import DataRequired, Optional, Regexp, Length, StopValidation
from flask_login import login_required, current_user

import datetime

class PostForm(FlaskForm):
    title = StringField(label='title',
                        validators=[DataRequired()])
    content = TextAreaField(label='text',
                            validators=[DataRequired()])
    picture = FileField(label='picture',
                        validators=[DataRequired()])


@main.route('/post', methods=['GET', 'POST'])
@login_required
def post_view():
    form = PostForm()
    if request.method == 'GET':
        return main.render_template('post.html', form=form)
    else:
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            picture_file = form.picture.data
            try:
                picture = FileModel.savefile(file=picture_file,
                                             folder=main.uploads_folder,
                                             url_prefix=url_for('static', filename=main.config['UPLOADS_FOLDER']))
                task = TaskModel.create(title=title,
                                        content=content,
                                        picture=picture,
                                        user=current_user,
                                        created_at=datetime.datetime.now())
                flash('成功发布任务！')
                return redirect(url_for('main.task_view', task_id=task.id))
            except FileExistsError as err:
                flash(err)
            except TypeError as err:
                flash(err)


        return main.render_template('post.html', form=form)
