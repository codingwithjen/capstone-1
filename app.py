"""Your Weather Flask Application."""

# from msilib import Table
import os, json, string, requests
from chevron import render
from dotenv import load_dotenv
from datetime import datetime
from models import connect_db, db, User, City
from forms import SignupForm, LoginForm, WeatherForm
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, request, redirect, render_template, url_for, jsonify, flash, session, g, abort, Markup
from sqlalchemy.exc import IntegrityError

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

load_dotenv()
connect_db(app)

#############################################################
#####             User Session Management               #####
#############################################################

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr_user to Flask global."""

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

#############################################################
# Conversion

def kelvin_to_fahrenheit(K):
    return int((K - 273.15) * 9/5 + 32)

def kelvin_to_celsius(K):
    return int(K - 273.15)

#############################################################
# Date Time

#############################################################
# Full Day, Full Month, Day, Full Year Format

def timestamp_to_datetime(ts, timezone_offset=0):
    ts = ts + timezone_offset
    return datetime.fromtimestamp(ts).strftime("%A, %B %d, %Y")

#############################################################
# Short Day, Short Month, Day Format

def day(ts, timezone_offset=0):
    ts = ts + timezone_offset
    return datetime.fromtimestamp(ts).strftime("%a")

def month(ts, timezone_offset=0):
    ts = ts + timezone_offset
    return datetime.fromtimestamp(ts).strftime("%b")

def date(ts, timezone_offset=0):
    ts = ts + timezone_offset
    return datetime.fromtimestamp(ts).strftime("%d")

#############################################################
# Weather Data for the Dashboard

def get_weather_data(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
    r = requests.get(url).json()
    return r

#############################################################
# 5-Day Forecast

def get_daily_forecast(daily_weather):

    daily_forecast = []
    for item in daily_weather[:-3]:

        # DF = "daily forecast"
        DF = {}
        DF['datetime_day'] = day(item['dt'])[:5]
        DF['datetime_month'] = month(item['dt'])[:5]
        DF['datetime_date'] = date(item['dt'])[:5]
        DF['iconcode'] = item['weather'][0]['id']
        DF['fahrenheit'] = kelvin_to_fahrenheit(item['temp']['day'])
        DF['celsius'] = kelvin_to_celsius(item['temp']['day'])
        daily_forecast.append(DF)
    return daily_forecast

#############################################################
# Search current weather on the city called

def get_weather_forecast(res, API_KEY):
    lon = res['coord']['lon']
    lat = res['coord']['lat']
    url = f'{API_BASE_URL}/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly&appid={API_KEY}'

#############################################################
    #OpenWeatherAPI Response

    forecast_res = requests.get(url).json()
    weather_forecast = {
        'current': {
            'city': res['name'].title(),
            'country': res['sys']['country'].upper(),
            'fahrenheit': kelvin_to_fahrenheit(res['main']['temp']),
            'celsius': kelvin_to_celsius(res['main']['temp']),
            'description': res['weather'][0]['description'].title(),
            'iconcode': res['weather'][0]['id'],
            'datetime': timestamp_to_datetime(forecast_res['current']['dt'])
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

    form = WeatherForm(request.form)
    return render_template('index_homepage.html', form=form)


#############################################################
#####            FETCH API WEATHER RESULTS              #####
#############################################################
@app.route('/fetch', methods=['GET', 'POST'])
def fetch():
    """API endpoint to fetch weather results."""

    city = request.form['city']
    zipcode = ''

    if not city and not zipcode:
        return jsonify({'error': 'Invalid... Please try again'})

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

    # if not g.user:
    #     flash('Access unauthorized. Please log in first in order to proceed!', 'primary')
    #     return redirect('/')

    if CURR_USER_KEY in session:
        user_id = g.user.id
        user = User.query.get_or_404(user_id)
        user = User.query.filter_by(id=user.id).first()
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
            flash('Oh snap! Username already taken. Please change a few things and try submitting again.', 'primary')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect(url_for('index_homepage'))

    else:
        return render_template('users/signup.html', form=form)

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
            flash(f'Hello, {user.username}! Welcome back! How you doin???', 'success')
            return redirect('/')
        flash('Oops! Looks like invalid crendetials have been entered. Please try again... with better, and accurate credentials!', 'primary')

    return render_template('users/login.html', form=form)

@app.route('/logout')
def logout():
    """Logs user out and redirects to index homepage."""

    do_logout()

    flash('See ya later, alligator! You have successfully logged out!', 'success')
    return redirect(url_for('login'))


#############################################################
#####                  User Dashboard                   #####
#############################################################
@app.route('/users/dashboard')
def user_dashboard():
    """Show user's dashboard that has all the bookmarks."""

    user_id = g.user.id
    user = User.query.get_or_404(user_id)

    if user:
        user_cities = City.query.filter_by(user_id=user_id).order_by(City.id.desc()).all()

        cities = []

        for city in user_cities:

            r = get_weather_data(city.name)

            city = {'name': city.name,
                    'fahrenheit': kelvin_to_fahrenheit(r['main']['temp']),
                    'celsius': kelvin_to_celsius(r['main']['temp']),
                    'description': r['weather'][0]['description'].title(),
                    'iconcode': r['weather'][0]['id'],}

            cities.append(city)

        return render_template('users/dashboard.html', user=user, cities=cities)
    else:
        return render_template('users/dashboard.html')

@app.route('/users/bookmark_city', methods=['GET', 'POST'])
def bookmark_city():
    """User can bookmark desired city and it will show up on their dashboard if they have an account."""

    if not g.user:
        flash(Markup('Access unauthorized. Please <a href="/login" class=alert-link>log in</a> first in order to proceed!'), 'primary')
        return redirect('/')

    user_id = g.user.id
    user = User.query.get_or_404(user_id)

    if user:
        city = request.form.get('city')
        user = User.query.filter_by(id=user.id).first()
        user_cities = user.cities
        if city not in [c.name for c in user_cities]:
            bookmarked_city = City(name=city, user_id=user.id)
            db.session.add(bookmarked_city)
            db.session.commit()
        flash('Oh hayyy!!! You added this city to your bookmarks!', 'success')
    return redirect(url_for('index_homepage'))

@app.route('/users/remove_city', methods=['GET', 'POST'])
def remove_city():
    """Remove and delete bookmarked city if it pips up on the homepage search when it runs via AJAX."""

    if not g.user:
        flash(Markup('Access unauthorized. Please <a href="/login" class=alert-link>log in</a> first in order to proceed!'), 'primary')
        return redirect('/')

    user_id = g.user.id
    user = User.query.get_or_404(user_id)

    if user:
        city = request.form.get('city')
        user = User.query.filter_by(id=user.id).first()
        user_cities = user.cities
        if city in [c.name for c in user_cities]:
            remove_bookmark = City.query.filter_by(name=city, user_id=user.id).first()
            db.session.delete(remove_bookmark)
            db.session.commit()
        flash('Okaaay fine... you removed that city from your bookmarks!', 'danger')
    return redirect(url_for('index_homepage'))

@app.route('/delete/<name>')
def delete_city(name):
    """Delete bookmarked city from the user's dashboard."""

    city = City.query.filter_by(name=name).first()
    db.session.delete(city)
    db.session.commit()

    flash(f'Okaaay, fine... You have successfully deleted { city.name } out of your entire existence on this app. Hehe...', 'warning')
    return redirect(url_for('user_dashboard'))

@app.route('/users/delete', methods=['POST'])
def delete_user():
    """Delete user."""

    if not g.user:
        flash(Markup('Access unauthorized. Please <a href="/login" class=alert-link>log in</a> first in order to proceed!'), 'primary')
        return redirect('/')
    
    do_logout()

    db.session.delete(g.user)
    db.session.commit()

    flash('Sad face! Your account was deleted. You will be missed!', 'primary')
    return redirect(url_for('signup'))


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

