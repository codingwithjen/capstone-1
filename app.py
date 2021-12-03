"""Your Weather Flask Application."""

import os, requests
from helpers import get_results
from models import db, connect_db, User, City
from flask_debugtoolbar import DebugToolbarExtension
from forms import SignupForm, LoginForm, WeatherForm, BookmarkForm, RemoveBookmarkForm
from flask import Flask, request, redirect, render_template, url_for, jsonify, flash, session, g

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config["SQLALCHEMY_DATABASE_URI"] = (os.environ.get("DATABASE_URL", "postgresql:///weather"))
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "c0rg1$rul3!")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = True
debug = DebugToolbarExtension(app)

connect_db(app)

#############################################################
#####             User signup/login/logout              #####
#############################################################

@app.before_request
def add_user_to_g():
    """Add user to Flask's global g variable."""

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
#####             Homepage and Error Pages              #####
#############################################################

@app.route('/', methods=['GET', 'POST'])
def index():
    """Renders HTML template that include some JS - NOT PART OF JSON API! Weather add form; fetch API results."""

    form = WeatherForm()

    if form.validate_on_submit():
        city = form.city.data
        zipcode = form.zipcode.data
        return redirect("/results")
    else:
        return render_template("index.html", form=form)

# @app.errorhandler(404)
# def page_not_found(e):
#     """404 NOT FOUND page."""

#     return render_template("404.html"), 404

#############################################################
#####              RESTFUL CITIES JSON API              #####
#############################################################

@app.route('/results', methods=['GET', 'POST'])
def get_weather_results():
    """Fetch weather results from the city value submitted into the Weather Form by user."""

    city = request.args["city"]
    zipcode = ''
    countrycode = "us"
    weather_results = get_results(city)
    return render_template('dashboard.html', weather_results=weather_results)



# @app.route("/api/cities")
# def list_cities():
#     """Returns JSON with all cities."""

#     all_cities = [city.serialize() for city in City.query.all()]
#     return jsonify(cities=all_cities)

# @app.route("/api/cities/<int:id>")
# def get_cities(id):
#     city = City.query.get_or_404(id)
#     return jsonify(city=city.serialize())

# @app.route("/api/cities", methods=["POST"])
# def search_city():
#     new_city = City(name=request.json["name"])
#     db.session.add(new_city)
#     db.session.commit()
#     response_json = jsonify(city=new_city.serialize())
#     return (response_json, 201)

# @app.route("/api/cities/<int:id>", methods=["PATCH"])
# def update_dashboard(id):
#     city = City.query.get_or_404(id)
#     request.json
#     city.name = request.json.get("name", city.name)
#     db.session.commit()
#     return jsonify(city=city.serialize())

# @app.route("/api/cities/<int:id>", methods=["DELETE"])
# def delete_city(id):
#     city = City.query.get_or_404(id)
#     db.session.delete(city)
#     db.session.commit()
#     return jsonify(message="deleted")


# https://coderedirect.com/questions/332614/sqlalchemy-exc-operationalerror-sqlite3-operationalerror-no-such-table