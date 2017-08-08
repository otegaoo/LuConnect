from flask_wtf import Form
from wtforms import StringField, BooleanField, validators, PasswordField
from wtforms.validators import ValidationError


def is_lincoln_email(form, field):
    string_checked = field.data.lower()
    if not string_checked.endswith("lincoln.edu"):
        raise ValidationError('Please type your Lincoln email')


class LoginForm(Form):
    email = StringField('email', [is_lincoln_email])
    student_id = StringField('id_number',
                             [validators.Length(min=6, max=6, message='Type a valid Lincoln student id number')])
    password = PasswordField('password', [validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('confirm_password', [validators.DataRequired(message='Please enter password')])
    remember_me = BooleanField('remember_me', default=False)



