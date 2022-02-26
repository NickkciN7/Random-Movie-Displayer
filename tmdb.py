"""This file is used to find the movie information and an image url using
The Movie Database's APIs"""

import os

# import json
import requests
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())  # This is to load your API keys from .env

BASE_URL = "https://api.themoviedb.org/3/"


def get_movie_data(movie_id):
    """Finds movie info based on the movieid passed from the main project1.py file.
    And it makes anothe rget request to get an image url. At the end all this information
    is returned"""

    # append current random movie id to end of base url
    base_url_movie = BASE_URL + "movie/" + str(movie_id)

    params = {"api_key": os.getenv("TMDB_KEY"), "language": "en-US"}

    response = requests.get(base_url_movie, params=params)
    data = response.json()
    # print(json.dumps(data, indent = 3))
    genre_list = []  # will return this list of just the genre names
    for genre in data["genres"]:
        genre_list.append(genre["name"])

    # for finding image url
    base_url_configuration = (
        BASE_URL + "configuration"
    )  # don't have forward slash at end

    params = {"api_key": os.getenv("TMDB_KEY")}

    response = requests.get(base_url_configuration, params=params)
    config = response.json()

    img_url = config["images"]["base_url"] + "w400" + data["poster_path"]

    return {
        "title": data["title"],
        "tagline": data["tagline"],
        "genres": genre_list,
        "image_url": img_url,
    }
