from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, Length, EqualTo
from wtforms import StringField, PasswordField, SubmitField

# from models import User?

class SignupForm(FlaskForm):
    """Form for creating a new user profile."""

    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=30)],)
    email = StringField("Email", validators=[DataRequired(), Email()],)
    password = PasswordField("Password", validators=[Length(min=6, max=20)],)
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')],)
    submit = SubmitField("Sign Up")

class LoginForm(FlaskForm):
    """Login form for existing/registered users."""

    username = StringField("Username", validators=[DataRequired()],)
    password = PasswordField("Password", validators=[Length(min=6)],)
    submit = SubmitField("Login")

class WeatherForm(FlaskForm):
    """User/Anon-User to submit the city they want data from."""

    city = StringField("City", validators=[DataRequired()],)
    submit = SubmitField("Submit")

