from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length, Optional
from wtforms_validators import AlphaNumeric

from app.models import User, ItemType


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
    username = StringField('New Username', validators=[Optional(), AlphaNumeric(message="Alphanumeric only")],
                           render_kw={"placeholder": "New username"})
    email = StringField('New Email', validators=[Optional(), Email()],
                        render_kw={"placeholder":
                                   "New email: example@example.com"})
    email_confirm = StringField('Please enter your new email again', validators=[Optional(), EqualTo('email', "Email addresses do not match")],
                                render_kw={"placeholder": "Confirm your new email"})
    password = PasswordField("Please enter your password to confirm these changes",
                           validators=[DataRequired()],
                           render_kw={"placeholder": "Enter your password to confirm profile changes"})
    submit = SubmitField("Confirm Account Detail Changes")

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


class UploadNewItemForm(FlaskForm):
    item_types = ItemType.query.filter_by(ItemType.name).all()
    name = StringField('Item Name', validators=[DataRequired()], render_kw={"placeholder": "Item Name"})
    item_type = SelectField('Item Type', choices=item_types)
    small_image = FileField()
    