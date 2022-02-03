"""Your Weather Flask Application."""

import os, json, string, requests

from datetime import datetime
from dotenv import load_dotenv
from models import db, connect_db, User, City
from sqlalchemy.exc import IntegrityError
from flask_debugtoolbar import DebugToolbarExtension
from forms import SignupForm, LoginForm, WeatherForm, BookmarkForm, RemoveForm
from flask import Flask, request, redirect, render_template, url_for, jsonify, flash
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

API_KEY = os.environ.get('API_SECRET_KEY')
API_BASE_URL = "https://api.openweathermap.org/"

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('DATABASE_URL', 'postgresql:///weather'))

# the toolbar is only enabled in debug mode: set to False to disable below
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

# the toolbar is only enabled in debug mode, uncomment the line below to enable
# toolbar = DebugToolbarExtension(app)

load_dotenv()
connect_db(app)

#############################################################
#####             User Session Management               #####
#############################################################

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.session_protection = 'strong'
login_manager.login_message_category = 'info'


# Flask-login will try and load a user BEFORE every request
@login_manager.user_loader
def load_user(user_id):
    """Return User.query.get(int(user_id)."""

    return User.query.get(int(user_id))


#############################################################
#####                Helper Decorators                  #####
#############################################################
# Conversion

def kelvin_to_fahrenheit(K):
    return int((K - 273.15) * 9/5 + 32)

def kelvin_to_celsius(K):
    return int(K - 273.15)

# Date Time

def timestamp_to_datetime(ts, timezone_offset=0):
    ts = ts + timezone_offset
    return datetime.fromtimestamp(ts).strftime("%m/%d %H:%M")

# 5-Day Forecast

def get_daily_forecast(daily_weather):

    daily_forecast = []
    for item in daily_weather[:-3]:
        # DF = "daily forecast"
        DF = {}
        DF['datetime'] = timestamp_to_datetime(item['dt'])[:5]
        DF['fahrenheit'] = kelvin_to_fahrenheit(item['feels_like']['day'])
        DF['celsius'] = kelvin_to_celsius(item['feels_like']['day'])
        daily_forecast.append(DF)
    return daily_forecast

# Search City

def get_weather_forecast(res, API_KEY):
    lon = res['coord']['lon']
    lat = res['coord']['lat']
    url = f'{API_BASE_URL}/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly&appid={API_KEY}'

    #OpenWeatherAPI Response

    forecast_res = requests.get(url).json()
    weather_forecast = {
        'current': {
            'city': res['name'].title(),
            'country': res['sys']['country'].upper(),
            'fahrenheit': kelvin_to_fahrenheit(res['main']['feels_like']),
            'celsius': kelvin_to_celsius(res['main']['feels_like']),
            'description': res['weather'][0]['description'],
            'icon': res['weather'][0]['icon'],
            'datetime': timestamp_to_datetime(forecast_res['current']['dt'], forecast_res['timezone_offset'])
        },
        'forecast': get_daily_forecast(forecast_res['daily'])
    }
    return weather_forecast


#############################################################
#####             Homepage and Error Pages              #####
#############################################################

@app.route('/', methods=['GET', 'POST'])
def index_homepage():
    """Index homepage.
    Renders HTML template that includes some JS.
    Not part of JSON API! Weather form to fetch API results."""

    form = WeatherForm()
    return render_template('index.html', title='Homepage', form=form)


# @app.errorhandler(404)
# def page_not_found(e):
#     """404 NOT FOUND page."""

#     return render_template('404.html'), 404


#############################################################
#####              RESTFUL CITIES JSON API              #####
#############################################################

@app.route('/fetch', methods=['GET', 'POST'])
def fetch():
    """API endpoint to fetch weather results."""

    city = request.form['city']
    countrycode = 'us'
    zipcode = ''


    if not city and not zipcode:
        return jsonify({'error': 'Please enter in at least one field.'})

    elif city:
        city = city.lower()
        city = string.capwords(city)
        url = f'{API_BASE_URL}/data/2.5/weather?q={city}&appid={API_KEY}'

    # OpenWeatherAPI Response
    res = requests.get(url).json()

    if res.get('cod') != 200:
        message = res.get('message', 'Invalid inquiry')
        return jsonify({'error': message})

    else:
        weather_forecast = get_weather_forecast(res, API_KEY)

    if current_user.is_authenticated:
        user = User.query.filter_by(id=current_user.id).first()
        user_cities = user.cities
        if city.lower() in [c.name.lower() for c in user_cities]:   
            weather_forecast['bookmark'] = True   

    return jsonify(weather_forecast)


#############################################################
#####               Sign-Up User Page                   #####
#############################################################


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handle user signup.
    Create new user and add to our database."""

    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = SignupForm()
    if form.validate_on_submit():
        try:
            user = User.signup(username=form.username.data,
                    email=form.email.data,
                    password=form.password.data,)
            db.session.add(user)
            # db.session.commit()

            flash(f'Welcome! Account created for {form.username.data}.'
                    f'You are now able to login', 'success')

        except IntegrityError as e:
            flash("Username already taken. Please try again.", 'danger')
            return render_template('signup.html', form=form)

        # do_login(user)

        return redirect(url_for('get_dashboard'))

    else:
        return render_template('signup.html', form=form)


#############################################################
#####                Login/Logout Pages                 #####
#############################################################

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""

    if current_user.is_authenticated:
        return redirect(url_for('get_dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            login_user(user)
            next_page = request.args.get('next')
            flash(f'Hello, {user.username}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login unsuccessful. Please try again.', 'danger')
    return render_template('login.html', form=form)     


@app.route('/logout')
def logout():
    """Handle logout of user."""

    logout_user()
    flash("You have successfully logged out", 'success')
    return redirect(url_for('login'))


#############################################################
#####                  User Dashboard                   #####
#############################################################

@app.route('/dashboard')
@login_required
def get_dashboard():
    """Render user's dashboard."""

    cities = City.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', cities=cities, title='Dashboard', form=form)

# Bookmark City

@app.route('/bookmark_city', methods=['GET', 'POST'])
def bookmark_city():
    """Creates a bookmark for signed in User."""

    if current_user.is_authenticated:
        # check if city has been bookmarked

        city = request.form.get('city')
        user = User.query.filter_by(id=current_user.id).first()
        user_cities = user.cities
        if city not in [c.name for c in user_cities]:
            bookmark_city = City(name=city, user_id=user.id)
            db.session.add(bookmark_city)
            db.session.commit()
        flash('City saved to bookmarks!', 'success')
    else:
        flash('Please login first.', 'danger')
    return redirect(url_for('index_homepage'))

@app.route('/remove_city', methods=['GET', 'POST'])
def remove_city():
    """Removes bookmarked city."""

    if current_user.id_is_authenticated:
        # Checks to see if city is bookmarked

        city = request.form.get('city')
        user = User.query.filter_by(id=current_user.id).first()
        user_cities = user.cities
        if city in [c.name for c in user_cities]:
            City.query.filter_by(name=city, user_id=current_user.id).delete()
            db.session.commit()
            flash('City removed', 'danger')
    else:
        flash('Please login first.', 'danger')
    return redirect(url_for('index_homepage'))   

##########################################################################

##########################################################################
# Turn off all caching in Flask
#   (useful for dev; in production, this kind of stuff is typically
#   handled elsewhere)
#
# https://stackoverflow.com/questions/34066804/disabling-caching-in-flask

@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req

##########################################################################

##########################################################################

if __name__ == '__main__':
    app.run(debug=True)





