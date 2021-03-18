# /users/forms.py
from wtforms import StringField, PasswordField, SubmitField # form rendering
from flask_wtf import FlaskForm # integrate Flask + WTForms
from wtforms.validators import DataRequired, Email, EqualTo # form validation
from wtforms import ValidationError # raise validation errors
from flask_wtf.file import FileField, FileAllowed # ability to upload file for avatar

from flask_login import current_user # proxy for logged-in user
from ..models import User

# build login form for registered users
class LoginForm(FlaskForm):
    email = StringField('Email',validators = [DataRequired(),Email()])
    password = PasswordField('Password',validators = [DataRequired()])
    submit = SubmitField('Log In')

# build registration form for new users
class RegistrationForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    username = StringField('UserName',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('pass_confirm',message='Passwords must match!')])
    pass_confirm = PasswordField('Confirm Password',validators=[DataRequired()])
    submit = SubmitField('Register!')

    # Confirm email is unique
    def validate_email(self, email):
        if User.query.filter_by(email=self.email.data).first():
            raise ValidationError('Email has been registered already')

    # Confirm username is unique
    def validate_username(self, username):
        if User.query.filter_by(username=self.username.data).first():
            raise ValidationError('Username has been registered already')

# build form to update user
class UpdateUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    username = StringField('Username', validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    # Confirm email is unique
    def validate_email(self, email):
        if current_user.email == self.email.data:
            return
        if User.query.filter_by(email=self.email.data).first():
            raise ValidationError('Email has been registered already')

    # Confirm username is unique
    def validate_username(self, username):
        if current_user.username == self.username.data:
            return
        if User.query.filter_by(username=self.username.data).first():
            raise ValidationError('Username has been registered already')
