"""This python file is the main file run that brings together all the
other files to make a webpage. It calls functions from the other python
files and passes information to a html page. It then at the end calls
app.run to actually start running the webpage."""

import os
import random

import flask
from flask import Flask, render_template
import flask_login
from flask_sqlalchemy import SQLAlchemy
from tmdb import get_movie_data
from wiki import get_wiki_link
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
# Point SQLAlchemy to your Heroku database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
# Gets rid of a warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.secret_key = os.getenv('SECRET_KEY')
login_manager = flask_login.LoginManager()
login_manager.init_app(app)


# from models import User

class User(flask_login.UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120))
    
db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id) #returns the User object with that id

#redirect to login page if not signed in
@login_manager.unauthorized_handler
def unauthorized_callback():
    return flask.redirect(flask.url_for("login"))


#Forrest Gump, Cheaper by the Dozen, Deck Dogz
movie_ids = [13, 11007, 26023]


@app.route('/')
@flask_login.login_required
def index():
    """random_id gets a random index of the movie lists, and this
    id is used in the get_movie_data function from TMDB.py in order
    to get movie information and an image url. The title of the movie is
    then used to find a wikipedia article by using the get_wiki_link
    function from WIKI.py. Finally the index.html page is rendered with
    this movie information passed to it to fill out the webpage"""

    
    random_id = random.randint(0, len(movie_ids)-1)
    movie_data = get_movie_data(movie_ids[random_id])
    # movie_data = get_movie_data(3)
    wiki_url = get_wiki_link(movie_data["title"])

    return render_template(
        "index.html",
        movie_title = movie_data["title"],
        tagline = movie_data["tagline"],
        genres = movie_data["genres"],
        genres_length = len(movie_data["genres"]),
        image_url = movie_data["image_url"],
        wiki_url = wiki_url
    )


@app.route('/login')
def login():
    return "<h1>welcome to the login page</h1>"

@app.route('/signup') 
def signup():
    pass


app.run(
    host=os.getenv('IP', '0.0.0.0'),
    port=int(os.getenv('PORT', '8080')),
    debug=True
)
