# coding: utf8

from . import main
from ...models.user import UserModel

from flask import request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Optional, Regexp, Length, StopValidation
from flask_login import login_user, logout_user


class LoginForm(FlaskForm):
    number = StringField(label='stu_number',
                         validators=[DataRequired(message='你需要填写学号'),
                                     Regexp('^\d{11}', message='学号格式不正确'),
                                     Length(min=11, max=11, message='手机号必须是11位阿拉伯数字')])
    name = StringField(label='stu_name',
                       validators=[DataRequired(message='必须填写姓名')])
    remember = BooleanField(label='下次自动登录',
                            validators=[Optional()])

    def validate_name(self, field):
        stu_number = self.number.data
        stu_name = field.data
        remember = self.remember.data

        user = UserModel.get(stu_number)
        if user:
            if stu_name == user.name:
                login_user(user, remember)
            else:
                raise StopValidation('学号和姓名没有对上啊')
        else:
            raise StopValidation('学号好像不对啊')


@main.route('/login', methods=['GET', 'POST'])
def login_view():
    login_form = LoginForm()

    if request.method == 'GET':
        return main.render_template('login.html', form=login_form)
    else:
        if login_form.validate_on_submit():
            flash('登进来啦！你可以发布任务或者完成某个任务')
            return redirect(url_for('main.index_view'))
        print(login_form.errors)
        return main.render_template('login.html', form=login_form)


@main.route('/logout')
def logout_view():
    logout_user()
    return redirect(url_for('main.index_view'))
