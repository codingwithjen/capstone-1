"""Your Weather Flask Application."""

import os, requests
from secrets import API_SECRET_KEY
from flask import Flask, request, jsonify, render_template
from models import db, connect_db, User, City

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URL'] = 'postgresql:///weather'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"

connect_db(app)

#############################################################
#####             Homepage and Error Pages              #####
#############################################################

@app.route("/")
def index_page():
    """Renders HTML template that include some JS - NOT PART OF JSON API!"""

    form = WeatherForm()
    return render_template("index.html", form=form)

#############################################################
#####              RESTFUL CITIES JSON API              #####
#############################################################

@app.route("/api/cities")
def list_cities():
    """Returns JSON with all cities."""

    all_cities = [city.serialize() for city in City.query.all()]
    return jsonify(cities=all_cities) 

@app.route("/api/cities/<int:id>")
def get_cities(id):
    city = City.query.get_or_404(id)
    return jsonify(city=city.serialize())

@app.route("/api/cities", methods=["POST"])
def search_city():
    new_city = City(name=request.json["name"])
    db.session.add(new_city)
    db.session.commit()
    response_json = jsonify(city=new_city.serialize())
    return (response_json, 201)

@app.route("/api/cities/<int:id>", methods=["PATCH"])
def update_dashboard(id):
    city = City.query.get_or_404(id)
    request.json
    city.name = request.json.get("name", city.name)
    db.session.commit()
    return jsonify(city=city.serialize())

@app.route("/api/cities/<int:id>", methods=["DELETE"])
def delete_city(id):
    city = City.query.get_or_404(id)
    db.session.delete(city)
    db.session.commit()
    return jsonify(message="deleted")


# https://coderedirect.com/questions/332614/sqlalchemy-exc-operationalerror-sqlite3-operationalerror-no-such-table