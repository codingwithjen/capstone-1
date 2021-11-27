# from unittest import TestCase

# from app import app
# from models import db,  

# # Use test database and don't clutter tests with SQL
# app.config['SQLALCHEMY_DATABASE_URL'] = 'postgresql:///weather_test'
# app.config['SQLALCHEMY_ECHO'] = False

# # Make Flask errors be real erros, rather than HTML pages with error info
# # app.config['TESTING'] = True

# db.drop_all()
# db.create_all()

# class TestCase(TestCase):
#     """Tests..."""

#     def setUp(self):
#         """Make demo data."""

#         City.query.delete()
#         db.session.commit()

#         city = City.(name="TestCake", calories=10)
#         db.session.add(dessert)
#         db.session.commit()

#         self.city_id = city.id

#     def tearDown(self):
#         """Clean up fouled transactions."""

#         db.session.rollback()

#     def test_all_cities(self):