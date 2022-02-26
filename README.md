# Heroku URL
https://project1-dominickdileo.herokuapp.com/
# Commit History
    I copied my milestone1 folder locally to work on milestone2 there, deleted the .git folder in the new directory, and re-initialized with git init. This was then pushed to 
    this remote repository. So there are no commits from milestone 1 here. Mr. Martin said this is ok on discord here https://discord.com/channels/928733838715289640/942873026083561513/945494866329227264
    Here is a link to milestone 1: https://github.com/csc4350-sp22/project1-ddileo2
# Detailing How This Project Works
## General
    This project is a webpage that makes use of the Flask framework to run. Everytime the page is refreshed it will display a different 
    random movie's information, a picture, and a wikipedia article link for the movie.
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

    For milestone2:
    The flask_login library is used to login a user, with sessions.
    The flask_sqlalchemy is used to write in python and communicate with a database

    5 addition routes now: rating, comment, login, signup, and logout
    main page the / route:
        Now does a bunch of querys with sqlalchemy, such as getting all the comments and ratings for a particualar movie and passes that information to the index.html to populate information on the webpage.
    rating:
        Deletes old rating if exists, posts a new rating, then redirect to main
        page. Uses the sqlaclchemy library to interact with the database
    comment:
        Posts a new comment then redirect to main page. If comment is unchanged from 
        initial text, empty, or there is no rating from user yet, a warning is shown 
        and no comment is posted
    login:  
        Checks if username is associated with a profile,
        login that user if there is, then redirect to main page.
    signup:
        Creates new profile if the username is not taken yet,
        then logs in the user, then redirects to the main page
    logout:
        Logs user out, then redirects to login page
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

    milestone2:
        Now allows user to post comments or ratings. Uses jinja to create comment divs and show ratings. There is also a small div in the top right corner with a welcome message and a button to log out. 
### login.html
    Center div like main page and similar styling. Single input box and submit button. This form's action is the /login route talked about above
### signup.html
    Center div like main page and similar styling. Single input box and submit button. This form's action is the /signup route talked about above

### style.css
    This file must be in the static directory. This file beautifies the rendered webpage.
### .env
    Though this file is not here on the repository, you will need to make a .env file locally containing the line 
        export TMDB_KEY = "<your api key>"
        export SECRET_KEY="<your made up secret key>"
        export DATABASE_URL="<your database url>"
            see Running After Installs section to see how to get a database url
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
    sudo apt install postgresql
    sudo service postgresql start
    sudo -u postgres psql  # just testing that psql is installed. You should get an interactive prompt. Quit by entering "\q"
    pip3 install psycopg2-binary
    pip3 install Flask-SQLAlchemy==2.1
    If you would like to put on Heroku:
    sudo curl https://cli-assets.heroku.com/install.sh | sh # install Heroku

#### Mac
    From the setup repository posted by Mr. Martin:
    python3 -m ensurepip --upgrade  # install pip, which manages python packages
    pip3 install flask
    pip3 install requests
    pip3 install python-dotenv
    brew install postgresql
    brew services start postgresql
    psql -h localhost  # this is just to test out that postgresql is installed okay - type "\q" to quit
    # if the above command gives you an error like "database <user> does not exist," try the workaround in this link: https://stackoverflow.com/questions/17633422/psql-fatal-database-user-does-not-exist
    pip3 install psycopg2-binary
    pip3 install Flask-SQLAlchemy==2.1

    If you would like to put on Heroku:
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)  # install Homebrew
    brew tap heroku/brew && brew install heroku  # install Heroku CLI

### Running After Installs
    You must have a .env file as described above. 
    for the DATABASE_URL in the .env file:
    To use a heroku database type 
    "heroku addons:create heroku-postgresql:hobby-dev"
    then "heroku config" to see your database url. 
    this goes in your .env file, but replace the text "postgres" with "postgresql"

    To run locally, type python3 project1.py to start the web app. Then click on the link provided in the terminal
    to see the website in your browser. 

    To put on Heroku, you must type "heroku login -i" to login. Then "heroku create" to make an app. Then "git push heroku main" to push your files onto heroku. You must put you api key in the settings -> config of your app on heroku's website since the .env file is not pushed. After this, just go on the url for your app and it should work. 

# Technical Issues I Encounterd
1. I tried to put all the database table classes in a separate python file called models.py. But I would get 
circular import errors when trying to import into project1.py since the models.py file also imported from project1.py. In the end my project does not use this models.py file and just has the 
classes in the main project1.py file. Mr. Martin said this is ok too.
2. I did not understand what the user class was supposed to be for flask login. I tried to just have it inherit from UserMixin like the documentation said, but according to the teacher,
it was actually supposed to inherit from db.model and is a table for the database too. So after not making progress for a while I finally got it all working when he told me that. Another thing I did not understand was what the user_loader callback did in the documentation. It did return User.get(user_id), so I was trying to add a .get function to my user class before the 
teacher explained what the user class is. Based on what he said and the other example link for flask login provided in the milestone2 instructions. I finally understood that this line return User.get(user_id) actually queries the database for the user with user_id as its id. So I did not need to add a .get function
3. I called a table user which is reserved keyword. So whenever I tried to run psql queries from the terminal after typing heroku pg:psql, I would run into issues. I asked about it
on discord and Mr. Martin and a student replied telling me its a reserved keyword. So I dropped the table from the database and changed the name to profile instead, which is not reserved.


# How did your experience working on this milestone differ from what you pictured while working through the planning process? What was unexpectedly hard? Was anything unexpectedly easy?
    I did not expect this project to take so long. I put in a decent amount of time and did not procrastinate a lot, but still am finishing up the day its due. The flask login part took 
    longer than I thought. As I talked about in the techincal issues section above, I was confused about what the User class was supposed to do or how it would relate to the database. But 
    as I said above, after a while I understood it better and finally got it all working. I wouldn't say anything was unexpectedly easy in this project.

# Current Problems and Improvements I Would Make
## Problem
    The center div containing all the content widens to fit the content. So if the tagline is really long, then the center div will expand a lot. I want to make the center div have a max width so regardless of the tagline length, the div looks the same. The tagline should instead wrap to the next line.
    The user can not make a comment without rating. This is to avoid an issue with how I retrieve information from the database. The query I use will not return a comment unless there is a 
    rating. So I could do some more complicated coding to allow for this, but for now it works, a user just needs to rate too.
## Improvements I Would Make
    Right now there are only 3 hardcoded movie ids that are randomly displayed. 
    I would like to add more, or make it so a random movie id is chosen from amongst all of the ids on TMDB. 
    
    Recommend a random movie based on a genre given by the user.

    Another Add a small snippet of information from the wikipedia article too, so 
    that there is a brief description of the movie.

# Stretch features
    I'm not sure if this counts, but my code gets the average of all ratings for the movie and shows the average rating on the website.