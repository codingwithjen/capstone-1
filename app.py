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
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

# toolbar = DebugToolbarExtension(app)
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
def index_weather_results():
    """Render weather results from homepage."""

    weather_data = []

    for city in cities:
        r = get_weather_data(city.name)
        print(r)

        weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],

        }
        weather_data.append(weather)
    
    return redirect(url_for('index', weather_data=weather_data))

    # city = request.form['city']
    # zipcode = ''
    # countrycode = 'us'
    # weather_results = get_weather_data(city)   
    # return redirect(url_for('index'))

#############################################################
#####        Authenticated User's Dashboard             #####
#############################################################

# @app.route('/results', methods=['POST'])
# def get


#############################################################
#####               Sign-Up User Page                   #####
#############################################################

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = SignupForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pwd)

        db.session.add(user)
        db.session.commit()

        flash(f'Account created for {form.username.data}!' f)