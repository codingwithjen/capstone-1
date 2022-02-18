"""Seed file to generate basic data in DB."""

from app import db
from csv import DictReader
from models import Bookmark, User, City

# Create all tables
db.drop_all()
db.create_all()

# Seed database with cities data from CSV files
# with open('generator/cities.csv') as cities:
#     db.session.bulk_insert_mappings(City, DictReader(cities))

# us_cities.csv db from https://github.com/kelvins/US-Cities-Database, revised to fit my schemas

# Make a user
# u1 = User.signup(username="ollythecorgi", email="itsollythecorgi@gmail.com", password="test_user")
# u2 = User.signup(username="test_user1234", email="testuser1@testuser1.com", password="test_user1234")

# db.session.add_all([u1, u2])
# db.session.commit()

# Make bookmarks list
# bookmarks_list1 = Bookmark(city_id=28091, user_id=1)
# bookmarks_list2 = Bookmark(city_id=1, user_id=2)
# # 1st is Seattle, and the 2nd is Adak - The first city that popped up for Alaska

# db.session.add_all([bookmarks_list1, bookmarks_list2])
# db.session.commit()