"""Seed file to generate basic data in DB."""

from app import db

db.drop_all()
db.create_all()

