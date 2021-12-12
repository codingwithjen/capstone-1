# Springboard's Capstone-1 Project
### Weather App API

Versions I am currently using and instructions are based off of this<br>

Python --version *3.9.6*<br> - you will need Python installed on a local environment<br>
macOS Monterey *Version 12.0.1*<br>
PostgreSQL *v13*<br>
Check the *requirements.txt* file to see the different packages installed and their versions <br>

# Set Up

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
12. 

---

### Sources:

1. [user_obj.is_authenticated] (https://www.rithmschool.com/courses/intermediate-flask/authentication-with-flask-login)<br>
2. [Unique Index] (https://forum.inductiveautomation.com/t/insert-into-database-only-if-the-entry-doesnt-exist/35122/10)


