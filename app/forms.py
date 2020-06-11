from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo

from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()],
                           render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[DataRequired()],
                             render_kw={"placeholder": "Password"})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()],
                           render_kw={"placeholder": "  Username"})
    email = StringField('Email', validators=[DataRequired(),
                        Email()],
                        render_kw={"placeholder":
                                   "Email: example@example.com"})
    password = PasswordField('Password', validators=[DataRequired()],
                             render_kw={"placeholder": "  Password"})
    password2 = PasswordField('Repeat Password', validators=[DataRequired(""),
                              EqualTo('password')],
                              render_kw={"placeholder": "Confirm password"})
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(
                'An account with this username is already in use')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(
                'An account with this email address in already in use')
