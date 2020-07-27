from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from wtforms_validators import AlphaNumeric

from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()],
                           render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[DataRequired()],
                             render_kw={"placeholder": "Password"})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),
                           AlphaNumeric(message="Alphanumeric only")],
                           render_kw={"placeholder": "Username"})
    email = StringField('Email', validators=[DataRequired(),
                        Email()],
                        render_kw={"placeholder":
                                   "Email: example@example.com"})
    password = PasswordField('Password', validators=[DataRequired(),
                             Length(min=8),
                             AlphaNumeric(message="Alphanumeric only")],
                             render_kw={"placeholder": "Password"})
    password2 = PasswordField('Repeat Password', validators=[DataRequired(""),
                              EqualTo('password', message="Passwords must match")],
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


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()],
                        render_kw={"placeholder": "Email"})
    submit = SubmitField('Request password reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')


class ChangeProfileInformationForm(FlaskForm):
    username = StringField('New Username', validators=[AlphaNumeric(message="Alphanumeric only")],
                           render_kw={"placeholder": "Username"})
    email = StringField('New Email', validators=[Email()],
                        render_kw={"placeholder":
                                   "Email: example@example.com"})
    email_confirm = StringField('Please enter your new email again', validators=[EqualTo(email, "Email addresses do not match")])
    password = StringField("Please enter your password to confirm these changes",
                           validators=[DataRequired(),
                           Length(min=8),
                           AlphaNumeric(message="Alphanumeric only")],
                           render_kw={"placeholder": "Password"})
    submit = SubmitField("Confirm Account Detail Changes")



    