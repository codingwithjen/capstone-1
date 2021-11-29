from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, EqualTo, Email, Optional, Length

class SignupForm(FlaskForm):
    """Form for creating a new user profile."""

class LoginForm(FlaskForm):
    """Login form for existing/registered users."""

class WeatherForm(FlaskForm):
    """User/Anon-User to submit the city they want data from."""
    city = StringField("City", validators=[Optional()])
    zipcode = StringField("Zip Code", validators=[Optional(), Length(min=5, max=15)])
    # submit = SubmitField("Submit")

class BookmarkForm(FlaskForm):
    """Gives logged in user the ability to bookmark a city so
    they don't have to resubmit search again."""

    submit = SubmitField("Bookmark")

class RemoveBookmarkForm(FlaskForm):
    """"Gives logged in user the ability to remove a bookmark from
    their dashboard."""

    submit = SubmitField("Remove")