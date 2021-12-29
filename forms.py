from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Email, Optional, Length
# from models import User?

class SignupForm(FlaskForm):
    """Form for creating a new user profile."""

    username = StringField("Username", validators=[InputRequired(message="Please enter a username."), Length(min=3, max=30)],)
    email = StringField("Email", validators=[InputRequired(), Email(message="Invalid email.")],)
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=30)],)

class LoginForm(FlaskForm):
    """Login form for existing/registered users."""

    username = StringField("Username", validators=[InputRequired(message="Please enter your username"), Length(min=3, max=30)],)
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=30)],)
    remember = BooleanField("Remember Me")

class WeatherForm(FlaskForm):
    """User/Anon-User to submit the city they want data from."""

    city = StringField("City", validators=[Optional()])
    zipcode = StringField("Zip Code", validators=[Optional(), Length(min=5, max=15)])
