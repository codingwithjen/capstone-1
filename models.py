"""Database models for Weather Flask Application."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# DO NOT MODIFY
def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

# Create the User Model
class User(db.Model):
    """Users in our database."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=True, nullable=False)
    cities = db.relationship("City", backref="user", lazy=True)

    def __repr__(self):
        return f<"User #{self.id}: {self.username}, {self.email} >"


# Create the City Model

class City(db.Model):
    """City Model."""

    __tablename__ = "cities"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)

    def serialize(self):
        """Returns a dict representation of city, which we can turn into JSON."""

        return {
            "id": self.id,
            "name": self.name,
        }

    def __repr__(self):
        return f"<City {self.id} name={self.name} >"

