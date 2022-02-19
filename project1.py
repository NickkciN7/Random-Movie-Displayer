"""This python file is the main file run that brings together all the
other files to make a webpage. It calls functions from the other python
files and passes information to a html page. It then at the end calls
app.run to actually start running the webpage."""

import os
import random

from flask import Flask, render_template
import flask_login
# from flask_sqlalchemy import SQLAlchemy
from tmdb import get_movie_data
from wiki import get_wiki_link
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# db = SQLAlchemy(app)

# app.secret_key = os.getenv('SECRET_KEY')
# login_manager = flask_login.LoginManager()
# login_manager.init_app(app)


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     username = db.Column(db.String(120))

#     def is_active(self):
#         return True

#     def is_authenticated(self):
#         return True

#     def is_anonymous(self):
#         return False

#     def get_id(self):
#         try:
#             return str(self.id)
#         except AttributeError:
#             raise NotImplementedError('No `id` attribute - override `get_id`')


# class User(flask_login.UserMixin):
#     def get_id(self):
#         return super().get_id()
    

# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)

class UserPosts(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    userid = db.Column(db.Integer)
    comment = db.Column(db.String(300), nullable=True)
    rating = db.Column(db.Integer, nullable=True)


#Forrest Gump, Cheaper by the Dozen, Deck Dogz
movie_ids = [13, 11007, 26023]


@app.route('/')
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

app.run(
    host=os.getenv('IP', '0.0.0.0'),
    port=int(os.getenv('PORT', '8080')),
    debug=True
)
