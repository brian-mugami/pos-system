from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, PasswordField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import EmailField
from wtforms.validators import EqualTo


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[validators.DataRequired()])
    last_name = StringField('Last Name', validators=[validators.DataRequired()])
    email = EmailField('Email', validators=[validators.DataRequired()])
    phone_no = IntegerField('Phone Number', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[validators.DataRequired(), EqualTo('password')])
    submit = SubmitField('Create')


class LoginForm(FlaskForm):
    phone_no = IntegerField('Phone Number', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    submit = SubmitField('Login')


class ForgotPasswordForm(FlaskForm):
    email = EmailField('Email')
    phone_no = IntegerField('Phone Number', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[validators.DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset')
