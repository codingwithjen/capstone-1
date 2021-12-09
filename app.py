"""Your Weather Flask Application."""

import os, requests
from helpers import get_weather_data
from sqlalchemy.exc import IntegrityError
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
login_manager.init_app(app)
login_manager.login_view = 'login'

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


#############################################################
#####               Sign-Up User Page                   #####
#############################################################

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handle user signup.
    Create new user and add to DB. Redirect to home page.
    If form not valid, present form.
    If the there already is a user with that username: flash message
    and re-present form."""

    if current_user.is_authenticated:
        return redirect(url_for('index'))  

    form = SignupForm()
    if form.validate_on_submit():
        try:
            user = User(username=form.username.data,
                    email=form.email.data,
                    password=hashed_pwd,
                    )

            db.session.commit()
            flash(f'Account created for {form.username.data}! '
                    f'You are now able to login.', 'success')

        except IntegrityError as e:
            flash("Username already taken", 'danger')
            return render_template('/signup.html', form=form)

    else:
        return render_template('login.html', form=form)


#############################################################
#####                Login/Logout Pages                 #####
#############################################################

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            login_user(user, remember=form.remember.data)
            flash('You have successfully logged in!', 'success')
            return redirect(url_for('get_dashboard')) 
        else:
            flash('Invalid credentials!', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    logout_user()
    flash("You have successfully logged out!", 'success')
    return redirect(url_for('login'))


#############################################################
#####                  User Dashboard                   #####
#############################################################

@app.route('/dashboard')
@login_required
def get_dashboard():
    """User dashboard."""

    cities = City.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', title='Account', cities=cities)


@app.route('/bookmark_city', methods=['GET', 'POST'])
def bookmark_city():
    """Enables user to bookmark a city/search."""

    if current_user.is_authenticated:
        city = request.form.get('city')
        user = User.query.filter_by(id=current_user.id).first()
        user_cities = user.cities
        if city not in [c.name for c in user_cities]:
            bookmarked_city = City(name=city, user_id=user.id)
            db.session.add(bookmarked_city)
            db.session.commit()
        flash('{city.name} saved!', 'success')
    else:
        flash('Please login first.', 'danger')
    return redirect(url_for('index'))


@app.route('/delete/<name>')
def remove_city(name):
    """Delete city."""

    if current_user.is_authenticated:
        city = request.form.get('city')
        user = User.query.filter_by(id=current_user.id).first()
        user_cities = user.cities
        if city in [c.name for c in user_cities]:
            City.query.filter_by(name=city, user_id=current_user.id)
            db.session.delete(city)
            db.session.commit()
            flash(f'Succesfully deleted and removed {city.name}!', 'success')
        else:
            flash('Please login!', 'danger')
    return redirect(url_for('get_dashboard'))


#############################################################
#####                                                   #####
#############################################################

if __name__ == '__main__':
    app.run(debug=True)