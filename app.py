"""Your Weather Flask Application."""

import os, requests
from helpers import get_weather_data
from models import db, connect_db, User, City
from flask_debugtoolbar import DebugToolbarExtension
from forms import SignupForm, LoginForm, WeatherForm, BookmarkForm, RemoveBookmarkForm
from flask import Flask, request, redirect, render_template, url_for, jsonify, flash, session
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('DATABASE_URL', 'postgresql:///weather'))

# the toolbar is only enabled in debug mode: set to False to disable
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

toolbar = DebugToolbarExtension(app)
login_manager = LoginManager()

connect_db(app)

#############################################################
#####             Homepage and Error Pages              #####
#############################################################

@app.route('/', methods=['GET', 'POST'])
def index_page():
    """"Index homepage.
        Renders HTML template that includes some JS.
        Not part of JSON API! Weather add form to fetch API results."""

    form = WeatherForm()

    if form.validate_on_submit():
        city = form.city.data
        zipcode = form.zipcode.data
    return render_template('index.html', form=form)

#############################################################
#####              RESTFUL CITIES JSON API              #####
#############################################################

@app.route('/results', methods=['POST'])
def render_weather_results():
    """Render weather results from the user's search."""

    city = request.form['city']
    zipcode = ''
    countrycode = 'us'
    weather_results = get_weather_data(city)   
    return redirect(url_for('index'))


