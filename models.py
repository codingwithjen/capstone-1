"""Database models for Weather Flask Application."""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
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

    @classmethod
    def register(cls, username, pwd):
        """Register user with hashed password and return user."""

        hashed = bcrypt.generate_password_hash(pwd)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user with username and hashed password."""
        return cls(username=username, password=hashed_utf8)

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that the user exists and password is correct. Return user if validl else return False."""

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False

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

