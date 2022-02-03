"""Seed file to generate basic data in DB."""

from app import app
from models import db, User, City

db.drop_all()
db.create_all()