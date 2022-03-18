#  Weather Flask Search

**Live Demo/Deployed Web App:** <https://flask-weather-app-1.herokuapp.com/>
**External API Used:** <https://openweathermap.org/api>

## Description
A weather forecasting web application that allows users to see the conditions, forecast, temperature, and other related metrics based on the user's desired location, as well as a number of other cities. Users can create an account to bookmark cities at their leisure, and can continue tracking those cities via a dashboard. The web app performs an API call to a third-party resource to acquire weather data on each city searched, and the web applicaiton stores user information and bookmarks on our database.

## Features
- jQuery Ajax used to fetch current weather conditions, along with a five-day weather forecast for the particular city searched by the user, without the need of redirecting user to a new page with results; faster response, no need for page to reload
- Functionality to bookmark and remove cities built using **CRUD operation**
- Usage of **Flask-SQLAlchemy** to build Database to store user information, and to keep track of the user's dashboard, which contains bookmarked cities with current weather data information fetched from the external API
- Usage of **Flask-Bcrypt** for user Authorization and Authentication, and password security
    - Login and registration handled on server-side with the use of Flask and WTForms
    - Can bookmark cities to easily access them via their dashboard, once the user is logged in
    - An account is not required to search weather data
- Usage of {{ mustache }} templating, along with Jinja templating
- Flask sessions used to keep track of users, whether registered or anon-user
- **Deployment with Heroku, and adding a Postgres Database**


## Features in Development
- Ability to reset password if the user forgot crendentials
- Ability to delete the user's account
- Ability to include an autocomplete search bar with all US cities
    - Only US cities, due to just wanting to use OpenWeatherMap API and having a csv file of us_cities imported into *seed.py* file


## Set Up
First, Git Clone the Repo in Command Line (Instructions for Mac Users):
1. COMMAND + SPACE BAR and type in search "terminal"
2. In the Terminal window, choose the location you want the directory located in
3. cd to your desired location, and *git clone https://github.com/codingwithjen/capstone-1.git*
4. Create a venv file: `python3 -m venv venv`
5. Activate the virtual environment before installing any libraries via pip `source venv/bin/activate`
6. Once activated, `pip install -r requirements.txt`
7. Sign up via OpenWeather for an API key - I have hidden this in my *.gitignore* file and via *dotenv*
8. Once all the packages are installed, `export FLASK_ENV=development` and then ENTER (can set this once per terminal)
9. Once you hit ENTER, type in `flask run`
9.1 Or you can create a .env file in your root directory. That's where I put my API key and I hid it in my *.gitignore* :)
10. Use your local server URL on a browser (I use Chrome) http://localhost:5000/.
11. To end the live server, on the Terminal window, enter CONTROL + C
12. Since I used an **npm** package, you can install that package by adding this into your root project directory `npm install axios`


## Screenshots
Homepage below:
![Homepage of Weather Flask Search](/static/img/Homepage.png "Homepage of Weather Flask Search")
Dashboard if you are a registered user:
![Dashboard of Weather Flask Serach](/static/img/Dashboard.png "Dashboard of Weather Flask Search")

## Tech Stack

### Languages:
- HTML5
- CSS
- Python3
- JavaScript
- SQL
    - PostgreSQL

### Libaries/Tools:
- Flask
- jQuery AJAX
- Bootstrap
- Bcrypt
- SQLAlchemy
- Flask-DebugToolbar
- WTForms
- Jinja
- requests
- npm
    - {{ mustache }}

### Versions Used
- Python --version 3.9.6
- PostgreSQL v13
- All else found in requirements.txt, runtime.txt, Profile
---
### Sources:

1. [user_obj.is_authenticated] (https://www.rithmschool.com/courses/intermediate-flask/authentication-with-flask-login)<br>
2. [Unique Index] (https://forum.inductiveautomation.com/t/insert-into-database-only-if-the-entry-doesnt-exist/35122/10)<br>
3. [mustache.js] (https://www.npmjs.com/package/mustache)
4. [cdnjs.cloudflare.com] (https://cdnjs.cloudflare.com/)
5. [Google Hosted Libraries] (https://developers.google.com/speed/libraries)

