from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, Optional, Length
# from models import User?

class SignupForm(FlaskForm):
    """Form for creating a new user profile."""

    username = StringField("Username", validators=[InputRequired(message="Please enter a desired username."), Length(min=3, max=30)],)
    email = StringField("Email", validators=[InputRequired(message="Please enter a valid email address"), Email()],)
    password = PasswordField("Password", validators=[Length(min=6, max=30)],)

class LoginForm(FlaskForm):
    """Login form for existing/registered users."""

    username = StringField("Username", validators=[InputRequired(message="Please enter your username")],)
    password = PasswordField("Password", validators=[InputRequired()],)

class WeatherForm(FlaskForm):
    """User/Anon-User to submit the city they want data from."""
    city = StringField("City", validators=[Optional()])
    zipcode = StringField("Zip Code", validators=[Optional(), Length(min=5, max=15)])

# class BookmarkForm(FlaskForm):
#     """Gives logged in user the ability to bookmark a city so
#     they don't have to resubmit search again."""

#     submit = SubmitField("Bookmark")

# class RemoveBookmarkForm(FlaskForm):
#     """"Gives logged in user the ability to remove a bookmark from
#     their dashboard."""

#     submit = SubmitField("Remove")