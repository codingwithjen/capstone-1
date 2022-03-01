"""Your Weather Flask Application."""

import os, json, string, requests

from datetime import datetime
from models import connect_db, db, User, City, Bookmark
from sqlalchemy.exc import IntegrityError
from flask_debugtoolbar import DebugToolbarExtension
from forms import SignupForm, LoginForm, WeatherForm
from flask import Flask, request, redirect, render_template, url_for, jsonify, flash, session, g

# Create your own session
CURR_USER_KEY = "curr_user"

API_KEY = os.environ.get('API_SECRET_KEY')
API_BASE_URL = "https://api.openweathermap.org/"

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('DATABASE_URL', 'postgresql:///weatherflasksearch'))

# the toolbar is only enabled in debug mode: set to True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

# the toolbar is only enabled in debug mode, uncomment the line below to enable
# toolbar = DebugToolbarExtension(app)

connect_db(app)

#############################################################
#####             User Session Management               #####
#############################################################

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id

def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

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
    return datetime.fromtimestamp(ts).strftime("%x")

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
            'iconcode': res['weather'][0]['id'],
            'datetime': timestamp_to_datetime(forecast_res['current']['dt'], forecast_res['timezone_offset'])
        },
        'forecast': get_daily_forecast(forecast_res['daily'])
    }
    return weather_forecast


#############################################################
#####                     Homepage                     #####
#############################################################

@app.route('/', methods=['GET', 'POST'])
def index_homepage():
    """Index homepage.
    Renders HTML template that includes some JS.
    Not part of JSON API! Weather form to fetch API results."""

    form = WeatherForm()
    return render_template('index.html', form=form)


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
        url = f'{API_BASE_URL}/data/2.5/weather?q={city},us&appid={API_KEY}'

    # OpenWeatherAPI Response
    res = requests.get(url).json()

    if res.get('cod') != 200:
        message = res.get('message', '')
        return jsonify({'error': message})

    else:
        weather_forecast = get_weather_forecast(res, API_KEY)

    if g.user:
        user = User.query.get(session[CURR_USER_KEY])
        user_cities = user.cities
        if city.lower() in [c.name.lower() for c in user_cities]:
            weather_forecast['bookmark'] = True

    return jsonify(weather_forecast)


# Serialization

def serialize_city(cities):
    """Serialize a city SQLAlchemy obj to dictionary."""

    return {
        "id": cities.id,
        "state": cities.state_name,
        "city": cities.city_name,
    }

# Search City

@app.route('/search', methods=['GET'])
def search_city():
    """Page with listing of cities.

    Can take a 'q' param in querystring to search by that city."""

    search = request.arts.get('q')

    if not search:
        cities = City.query.all()
    else:
        users = User.query.filter(User.username.like(f"%{search}%")).all()

    return render_template('users/index.html', cities=cities)


#############################################################
#####               Sign-Up User Page                   #####
#############################################################


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handle user signup.
    Create new user and add to our database."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

    form = SignupForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
            )
            db.session.commit()

        except IntegrityError as e:
            flash('Username already taken. Please try again.', 'danger')
            return render_template('signup.html', form=form)

        do_login(user)

        return redirect(url_for('index_homepage'))

    else:
        return render_template('signup.html', form=form)


#############################################################
#####                Login/Logout Pages                 #####
#############################################################

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Produce login form or handle login."""

    form = LoginForm()

    if form.validate_on_submit():
        # authenticate will return a user or False
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            do_login(user)
            flash(f'Hello, {user.username}!', 'success')
            return redirect('/')
        flash('Invalid crendentials. Please try again.', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """Logs user out and redirects to index homepage."""

    do_logout()

    flash('You have successfully logged out.', 'success')
    return redirect(url_for('login'))


#############################################################
#####                  User Dashboard                   #####
#############################################################

@app.route('/users/<int:user_id>')
def get_dashboard(user_id):
    """Show user's dashboard."""

    user = User.query.get_or_404(user_id)

    cities = (City
                .query.filter(City.user_id == user_id)
                .limit(3)
                .all())
    bookmarks = [city.id for city in user.bookmarks]
    return render_template('users/dashboard.html', user=user, cities=cities, bookmarks=bookmarks)


# Bookmark City

# @app.route('/bookmark_city', methods=['GET', 'POST'])
# def bookmark_city():
#     """Creates bookmark for city for logged in user."""

#     if not g.user:
#         flash('Access unauthorized. Please login to proceed.', 'danger')
#         return redirect(url_for('login'))

#     user_id = g.user.id
#     user = User.query.get_or_404(user_id)

#     if user:
#         city = request.form.get['city']
#         user = User.query.filter_by(id=user_id).first()
#         user_cities = user.bookmarks
#         if city not in [c.name for c in user_cities]:
#             bookmarked_city = City(name=city, user_id=user.id)
#             db.session.add(bookmarked_city)
#             db.session.commit()
#         flash('City has been bookmarked!', 'success')

#     return redirect(url_for('get_dashboard'))

# Remove Bookmark

# @app.route('/bookmark_remove', methods=['GET', 'POST'])
# def bookmark_remove():
#     """Removes bookmark for city for logged in user."""

#     if not g.user:
#         flash('Access unauthorized. Please login to proceed.', 'danger')
#         return redirect(url_for('login'))

#     user_id = g.user.id
#     user = User.query.get_or_404(user_id)

#     if user:
#         city = request.form.get['city']
#         user = User.query.filter_by(id=user_id).first()
#         user_cities = user.bookmarks
#         if city in [c.name for c in user_cities]:
#             City.query.filter_by(name=city, user_id=user.id).delete()
#             db.session.commit()
#             flash('City has been removed from bookmarks.', 'danger')

#     return redirect(url_for('get_dashboard'))



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

