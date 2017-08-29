from flask_wtf import Form
from flask import request
from wtforms import StringField, BooleanField, validators, PasswordField
from wtforms.validators import ValidationError
from .models import User


def is_lincoln_email(form, field):
    string_checked = field.data.lower()
    if request.form['btn'] == 'register':
        if not string_checked.endswith("@lincoln.edu"):
            raise ValidationError('Please type your Lincoln email')
    elif request.form['btn'] == 'login':
        user = User.query.filter_by(lincoln_email=request.form['lincoln_email'].lower()).first()
        if request.form['lincoln_email'].lower() != user.lincoln_email:
            raise ValidationError('Lincoln email is incorrect')
        if request.form['password'] != user.password:
            raise ValidationError('password is incorrect')


class LoginForm(Form):
    lincoln_email = StringField('email', [is_lincoln_email])
    lincoln_id = StringField('id_number',
                             [validators.Length(min=6, max=6, message='Type a valid Lincoln student id number')])
    password = PasswordField('password', [validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('confirm_password', [validators.DataRequired(message='Please enter password')])
    remember_me = BooleanField('remember_me', default=False)



