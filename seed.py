"""Seed file to generate basic data in DB."""

from app import app
# from csv import DictReader
# from models import User, City

# Create all tables
db.drop_all()
db.create_all()

# Seed database with cities data from CSV files
# with open('generator/cities.csv') as cities:
#     db.session.bulk_insert_mappings(City, DictReader(cities))

# us_cities.csv db from https://github.com/kelvins/US-Cities-Database, revised to fit my schemas
# db.session.commit()

