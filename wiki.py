"""File is used to find the wikipedia article of a movie given the
movie title."""

import requests


# BASE_URL = 'https://www.mediawiki.org/w/api.php'
BASE_URL = "https://en.wikipedia.org/w/api.php"


def get_wiki_link(title):
    """Function looks for wikipedia article based on movie title passed
    in the main project1.py file. After finding the pageid from the
    first get request, another get request makes use of this pageid
    to find the actual url. Finally this url is returned."""

    # in order to get page id
    params = {
        "action": "query",
        "list": "search",
        "srsearch": title,
        "srlimit": "1",
        "format": "json",
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()
    page_id = data["query"]["search"][0]["pageid"]

    # get url
    params = {
        "action": "query",
        "prop": "info",
        "inprop": "url",
        "pageids": page_id,
        "format": "json",
    }

    response = requests.get(BASE_URL, params=params)
    prop_data = response.json()
    return prop_data["query"]["pages"][str(page_id)]["fullurl"]
