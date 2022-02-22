# Heroku URL
https://project1-dominickdileo.herokuapp.com/

# Detailing How This Project Works
## General
    This project is a webpage that makes use of the Flask framework to run. Everytime the page is refreshed it will display a different 
    random movie's information, a picuture, and a wikipedia article link for the movie.
## APIS
    I make use of APIs from The Movie Database(TMDB) and Wikipedia(Wiki). For TMDB, I used the Movies section of the 
    API to search for a movie based on movie_id. Using the poster_path info from the previous get request and getting 
    the base_url from another get request using the Configuration section of the API, I was able to get an image URL 
    for the movie as well. For Wiki, I made use of the action query and the list search query parameters as well as 
    the movie title received from TMDB before to get movie article information. Using the pageid from the get request
    of Wiki, and using the action query, info prop, and url inprop query parameters, I was actually able to get the 
    article URL. The TMDB API needs an API key, which is placed in a .env file and imported into the environment 
    variables and then used in the python files.
## Explaining Each File
### project1.py
    This is the main file that is run with python3. It randomly chooses a movie id from a hardcoded list of movie 
    ids by making use of the Random libray. This file imports functions from tmdb.py and wiki.py. It passes the 
    movie id to the function from tmdb.py in order to get information about the movie and an image url, with the 
    API talked about above. Next project1.py passes the movie title received from the previous imported function 
    into the imported function from wiki.py. This function returns a wikipedia article. After getting all this info, 
    project1.py renders the index.html and passes all this information talked about above to it. At the end of this 
    file, app.run() is called to finally start running the web app making use of the Flask framework. In app.run 
    the os library is used to get an environment variables IP and PORT(which are provided by heroku automaticlly if 
    hosted there), and if those env variables are not there, it will just choose default values.
### tmdb.py
    This file makes use of the API talked about above to return an image url and information about a movie given a 
    movie id. The requests library is used to make Get requests. Functions from the dotenv library are imported in
    order to load the api key from the .env file into the environment variables. The os library is used to load 
    this api key environment variable and use it in the python file to pass it in the get request. The json library
    is used to debug and make it easier to read the json data recieved.
### wiki.py
    This file makes use of the API talked about above to return a wikipedia article given a movie title. 
    The only library used in the file is the requests library in order to make a get request for the Wiki API. No 
    api key was needed.
### index.html
    This file must be in the templates directory. This file contains a center div that is filled with the 
    information passed to it from project1.py. This information is placed in the rendered html page dynamically using 
    Jinja coding in the index.html file
### style.css
    This file must be in the static directory. This file beautifies the rendered webpage.
### .env
    Though this file is not here on the repository, you will need to make a .env file locally containing the line 
        export TMDB_KEY = "<your api key>"
### .gitignore
    This file is used to disallow the local .env file from being pushed to a remote repository. It also prevents 
    pycache files from being pushed.
### Procfile
    This file tells heroku what python file(project1.py) to run initially and that it is a website.
### requirements.txt
    This file tells heroku what to install in order to make the webpage work properly.
### README.md 
    This is just all the text you see here.
## How To Get Website Running
### Installs
#### Windows
    From the setup repository posted by Mr. Martin:
    sudo apt-get update  # update your installer so the Pip installation works
    sudo apt install python3-pip  # install pip, which manages python packages
    pip3 install flask
    pip3 install requests
    pip3 install python-dotenv

    If you would like to put on Heroku:
    sudo curl https://cli-assets.heroku.com/install.sh | sh # install Heroku

#### Mac
    From the setup repository posted by Mr. Martin:
    python3 -m ensurepip --upgrade  # install pip, which manages python packages
    pip3 install flask
    pip3 install requests
    pip3 install python-dotenv

    If you would like to put on Heroku:
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)  # install Homebrew
    brew tap heroku/brew && brew install heroku  # install Heroku CLI

### Running After Installs
    To run locally, type python3 project1.py to start the web app. Then click on the link provided in the terminal
    to see the website in your browser. You must have a .env file as described above.

    To put on Heroku, you must type "heroku login -i" to login. Then "heroku create" to make an app. Then "git push heroku main" to push your files onto heroku. You must put you api key in the settings -> config of your app on heroku's website since the .env file is not pushed. After this, just go on the url for your app and it should work.

# Technical Issues I Encounterd
1. circular import when trying to import models.py

# Current Problems and Improvements I Would Make
## Problem
    The center div containing all the content widens to fit the content. So if the tagline is really long, then the center div will expand a lot. I want to make the center div have a max width so regardless of the tagline length, the div looks the same. The tagline should instead wrap to the next line.
## Improvements I Would Make
    Right now there are only 3 hardcoded movie ids that are randomly displayed. 
    I would like to add more, or make it so a random movie id is chosen from amongst all of the ids on TMDB. 
    
    Recommend a random movie based on a genre given by the user.

    Another Add a small snippet of information from the wikipedia article too, so 
    that there is a brief description of the movie.