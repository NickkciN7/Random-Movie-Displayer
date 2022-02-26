# pylint: disable=C0103,C0115,E1101,R0903
"""This python file is the main file run that brings together all the
other files to make a webpage. It calls functions from the other python
files and passes information to a html page. It then at the end calls
app.run to actually start running the webpage."""

import os
import random

import flask
from flask import Flask, render_template, session
import flask_login
from flask_login import current_user, login_required
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv, find_dotenv
from tmdb import get_movie_data
from wiki import get_wiki_link


load_dotenv(find_dotenv())

app = Flask(__name__)

app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
# Point SQLAlchemy to your Heroku database
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
# because heroku's DATABASE_URL config variable can't be overwritten
# on their site, change it here
if app.config["SQLALCHEMY_DATABASE_URI"].startswith("postgres://"):
    app.config["SQLALCHEMY_DATABASE_URI"] = app.config[
        "SQLALCHEMY_DATABASE_URI"
    ].replace("postgres://", "postgresql://")
# Gets rid of a warning
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

app.secret_key = os.getenv("SECRET_KEY")
login_manager = flask_login.LoginManager()
login_manager.init_app(app)


# from models import User


class profile(flask_login.UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))


class rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movieid = db.Column(db.Integer)
    userid = db.Column(db.Integer)
    rating = db.Column(db.Integer)


class comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movieid = db.Column(db.Integer)
    userid = db.Column(db.Integer)
    comment = db.Column(db.String(300))


db.create_all()


@login_manager.user_loader
def load_user(user_id):
    """returns the User object with that id"""
    return profile.query.get(user_id)


@login_manager.unauthorized_handler
def unauthorized_callback():
    """redirect to login page if not signed in"""
    return flask.redirect(flask.url_for("login"))


# Forrest Gump, Cheaper by the Dozen, Deck Dogz
movie_ids = [13, 11007, 26023]

# current_movie_id = -1
@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """random_id gets a random index of the movie lists, and this
    id is used in the get_movie_data function from TMDB.py in order
    to get movie information and an image url. The title of the movie is
    then used to find a wikipedia article by using the get_wiki_link
    function from WIKI.py. Finally the index.html page is rendered with
    this movie information passed to it to fill out the webpage"""

    # current_movie_id = 11007
    # user did not just try to post a comment or rate, so pick a random movie
    if not session.get("posted", None) == "true":
        random_id = random.randint(0, len(movie_ids) - 1)
        current_movie_id = movie_ids[random_id]
    else:
        # user just tried to comment or rate, so the current movie id should be the same as before
        current_movie_id = session["movie_id"]
    # reset this session variable so if user reloads page without
    # commenting or rating, a new random movie id is chsoen
    session["posted"] = "false"
    # store movieid in sessions so other routes can access
    # for storing a comment/rating in the database
    session["movie_id"] = current_movie_id
    movie_data = get_movie_data(current_movie_id)
    wiki_url = get_wiki_link(movie_data["title"])

    # get information about comment and pass to html to make comment divs with Jinja
    comment_info = db.session.query(profile.username, rating.rating, comment).filter(
        profile.id == comment.userid,
        comment.userid == rating.userid,
        comment.movieid == current_movie_id,
        comment.movieid == rating.movieid,
    )

    # print(comment_info.column_descriptions)
    # print(comment_info.statement)
    # for row in comment_info:
    #     #row.rating instead of row.rating.rating, probably does not need to specify table
    #      name because in the sqlalchemy query, rating.rating is already specified?
    #     print(str(row.comment.userid) + " " + row.username + " " + str(row.rating) + " " +
    #           str(row.comment.movieid) + " " + row.comment.comment + " ")

    # get user rating
    user_rating_query = rating.query.filter_by(
        userid=current_user.id, movieid=current_movie_id
    ).first()
    user_rating = -1
    session["has_rating"] = "false"  # to prevent user from commenting without rating
    if user_rating_query is not None:
        user_rating = user_rating_query.rating
        session["has_rating"] = "true"

    # get average rating of movie
    all_ratings = rating.query.filter_by(movieid=session.get("movie_id", None))
    # print("count" + str(all_ratings.count()))
    ratings_sum = 0
    average_rating = -1
    if all_ratings.count() != 0:
        for row in all_ratings:
            ratings_sum += row.rating
        average_rating = ratings_sum / all_ratings.count()

    return render_template(
        "index.html",
        movie_title=movie_data["title"],
        tagline=movie_data["tagline"],
        genres=movie_data["genres"],
        genres_length=len(movie_data["genres"]),
        image_url=movie_data["image_url"],
        wiki_url=wiki_url,
        comment_info=comment_info,
        comment_count=comment_info.count(),
        user_rating=user_rating,
        average_rating=average_rating,
    )


@app.route("/rating", methods=["GET", "POST"])
@login_required
def rating_post():
    """Deletes old rating if exists, posts a new rating, then redirect to main page"""

    if flask.request.method == "POST":
        session["posted"] = "true"

        rating_form = flask.request.form["rating"]
        old_rating = rating.query.filter_by(userid=current_user.id).first()
        new_rating = rating(
            movieid=session.get("movie_id", None),
            userid=current_user.id,
            rating=rating_form,
        )
        if old_rating is not None:  # only allow 1 rating per user
            db.session.delete(old_rating)
        db.session.add(new_rating)
        db.session.commit()
        return flask.redirect(flask.url_for("index"))

    return flask.redirect(flask.url_for("index"))


@app.route("/comment", methods=["GET", "POST"])
@login_required
def comment_post():
    """Posts a new comment then redirect to main page. If comment is unchanged from initial text,
    empty, or there is no rating from user yet, a warning is shown and no comment is posted"""

    if flask.request.method == "POST":
        session["posted"] = "true"
        if session.get("has_rating", None) == "false":
            flask.flash("Make Rating Before Commenting.")
            return flask.redirect(flask.url_for("index"))
        comment_form = flask.request.form["comment"]
        if comment_form == "":
            flask.flash("Comment should not be empty.")
            return flask.redirect(flask.url_for("index"))
        if comment_form == "Comment here":
            flask.flash("Comment should change initial text.")
            return flask.redirect(flask.url_for("index"))
        new_comment = comment(
            movieid=session.get("movie_id", None),
            userid=current_user.id,
            comment=comment_form,
        )
        db.session.add(new_comment)
        db.session.commit()
        return flask.redirect(flask.url_for("index"))

    return flask.redirect(flask.url_for("index"))


@app.route("/login", methods=["GET", "POST"])
def login():
    """Checks if username is associated with a profile,
    login that user if there is, then redirect to main page."""

    if flask.request.method == "POST":
        session["posted"] = "false"
        username_form = flask.request.form["username"]
        user_query = profile.query.filter_by(username=username_form).first()
        if user_query is None:
            flask.flash("Username Not Found")
        else:
            flask_login.login_user(user_query)
            # flask.flash("you signed in!")
            return flask.redirect(flask.url_for("index"))

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Creates new profile if the username is not taken yet,
    then logs in the user, then redirects to the main page"""

    if flask.request.method == "POST":
        session["posted"] = "false"
        username_form = flask.request.form["username"]
        user_query = profile.query.filter_by(username=username_form).first()
        if user_query is None:
            # user name not taken so make new profile
            new_profile = profile(username=username_form)
            db.session.add(new_profile)
            db.session.commit()
            flask_login.login_user(new_profile)
            return flask.redirect(flask.url_for("index"))
        flask.flash("Username Already Taken")

    return render_template("signup.html")


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    """Logs user out, then redirects to login page"""
    flask_login.logout_user()
    flask.flash("Successfully Logged Out")
    return flask.redirect(flask.url_for("login"))


app.run(
    host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", "8080")), debug=True
)
