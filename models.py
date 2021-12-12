"""Database models for Weather Flask Application."""

from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

# Create the Bookmarks Model
class Bookmarks(db.Model):
    """Mapping user bookmarks to cities searched."""

    __tablename__ = 'bookmarks'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="cascade"))
    city_id = db.Column(db.Integer, db, ForeignKey('cities.id', ondelete="cascade"))

# Create the User Model
class User(db.Model, UserMixin):
    """Users in our database."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    cities = db.relationship('City')

    bookmarks = db.relationship('City', secondary="bookmarks")

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

    @classmethod
    def signup(cls, username, pwd):
        """Signup user with hashed password and return user."""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password.`
        
        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password and,
        if it finds such a user, returns that user object.
        
        If it can't find matching user (or if password is incorrect), returns False."""

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
        
        return False


# Create the City Model

class City(db.Model):
    """City Model."""

    __tablename__ = "cities"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="cascade"), nullable=False)
    user = db.relationship('User')


    # def serialize(self):
    #     """Returns a dict representation of city, which we can turn into JSON."""

    #     return {
    #         "id": self.id,
    #         "name": self.name,
    #     }

    # def __repr__(self):
    #     return f"<City {self.id} name={self.name} >"


# DO NOT MODIFY
def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

