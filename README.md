To see the page I made for this current milestone click the "SEE ALL POSTS" button near the Welcome message in the top right corner of the screen after getting the website running.
# Heroku URL
https://project1-dominickdileo.herokuapp.com/
(current milestone not deployed)
# Commit History
    I copied my milestone1 folder locally to work on milestone2 there, deleted the .git folder in the new directory, and re-initialized with git init. This was then pushed to 
    this remote repository. So there are no commits from milestone 1 here. Mr. Martin said this is ok on discord here https://discord.com/channels/928733838715289640/942873026083561513/945494866329227264
    Here is a link to milestone 1: https://github.com/csc4350-sp22/project1-ddileo2
# Detailing How This Project Works
## General
    This project is a webpage that makes use of the Flask framework to run. Everytime the page is refreshed it will display a different 
    random movie's information, a picture, and a wikipedia article link for the movie. The user can post comments and make ratings. These will appear on the main screen,
    and the user can go to a page where all comments and ratings they've made for all movies are shown.
## APIS
    I make use of APIs from The Movie Database(TMDB) and Wikipedia(Wiki). For TMDB, I used the Movies section of the 
    API to search for a movie based on movie_id. Using the poster_path info from the previous get request and getting 
    the base_url from another get request using the Configuration section of the API, I was able to get an image URL 
    for the movie as well. For Wiki, I made use of the action query and the list search query parameters as well as 
    the movie title received from TMDB before to get movie article information. Using the pageid from the get request
    of Wiki, and using the action query, info prop, and url inprop query parameters, I was actually able to get the 
    article URL. The TMDB API needs an API key, which is placed in a .env file and imported into the environment 
    variables and then used in the python files.
## React
    The page that shows all comments and ratings the user made uses React. This helps make better separation of
    html into components amongst other benefits. I talk more about installation and using it below.
## Explaining Each File
### App.js
    This is the file with javscript and jsx code. It is what the index.html page is made from after typing npm run build.
    There are 4 components. The main parent component(CommentsAndRatingsPage), the Movie component, the Comment component, and the 
    Rating component. A fetch request in the CommentsAndRatingsPage gets a json from the returnalluserposts route talked about in the
    project1.py description. map is used to create as many Movie components as there are movies rated/commented on by user.
    The rating information is then passed down to the Rating component in each Movie component, and map is used again to 
    create as many Comment components as there are comments by the user for that movie. States are used to keep the UI updated and 
    functions tied to buttons are used to change the state as well as update the database through fetch POST requests. Comments in 
    the code for App.js will provide more specific explanations for different parts.
### App.css
    I mainly just copied the css from the styles.css in the static folder so I could use the code with React and keep the
    look of the website more consistent.
### Other react related files
    There are many files and folders such as all the others files in the src folder except App.js and App.css that I did 
    not touch. When you create a react app, they will be made for you.
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

    5 additional routes now: rating, comment, login, signup, and logout

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




    For milestone3:
    Added routes to handle the back end for the React page:
    6 additional routes now: commentsandratings, returnalluserposts, returnusername, ratingreact, commentupdatereact, and commentdeletereact

    commentsandratings:
        Renders React generated html page: index.html.
    returnalluserposts:
        Returns a json formatted list of all the comments and ratings
        for every movie the current user has commented on or rated.
    returnusername:
        Returns the username so the welcome div can display the proper name.
    ratingreact:
        Will update the rating in the database made by the current user for a
        specific movie matching the movieid passed in the POST request.
    commentupdatereact:
        Will update the specific comment in the database matching
        the comment id passed in the POST request.
    commentdeletereact:
        Will delete the specific comment in the database matching
        the comment id passed in the POST request.


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
    From the setup repository posted by Mr. Martin https://github.com/csc4350-sp22/setup-and-demos/blob/main/csc-4350-setup.md:
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

    If you would like to put on Heroku(Current milestone is not deployed on heroku):
    sudo curl https://cli-assets.heroku.com/install.sh | sh # install Heroku


    For react related things look in the setup repo linked above. 

#### Mac
    From the setup repository posted by Mr. Martin https://github.com/csc4350-sp22/setup-and-demos/blob/main/csc-4350-setup.md:
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

    If you would like to put on Heroku(Current milestone is not deployed on heroku):
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)  # install Homebrew
    brew tap heroku/brew && brew install heroku  # install Heroku CLI


    For react related things look in the setup repo linked above. 

### Running After Installs
    You must have a .env file as described above. 
    for the DATABASE_URL in the .env file:
    To use a heroku database type 
    "heroku addons:create heroku-postgresql:hobby-dev"
    then "heroku config" to see your database url. 
    this goes in your .env file, but replace the text "postgres" with "postgresql"

    After cloning this repository, run `npm ci` in that directory to pull in all the node packages you need.(this 
    repository does not have all the necessary React related files as is). After this, type `npm run build`, which 
    makes the index.html file and builds React related things. Finally type `python3 project1.py` to start the web app. 
    Then click on the link provided in the terminal to see the website in your browser. To see the page I made for
    this current milestone click the "SEE ALL POSTS" button near the Welcome message in the top right corner 
    of the screen.

    (CURRENT MILESTONE IS NOT DEPLOYED ON HEROKU)

# Technical Issues I Encounterd
1. I was having trouble combining the starter code provided with my milestone 2 code. I wasn't sure what exactly I was supposed 
to change about my old code. I manually copied the content from my homework 7 code, since that uses the same starter code. I had to
make it so my old styles.css and the starter code's "static/react/" folder were both in the same single "static" folder. I had 
an idea about how to use blueprint and after talking to some guy in the office hours(I can't remember his name), he said the way 
I was thinking is what he did. So I just added a few lines from the starter code and kept most of my old code the same. Here is a 
discord post I made describing it in more detail: https://discord.com/channels/928733838715289640/946909452760657961/950841488550555708
2. I was not sure how to properly make the json containing all posts on the backend to send to the react page. I went to John's office hours 
and he wrote some code/pseudocode that helped me create good data. The code basically makes a list where each index contains a dictionary that 
corresponds to one movie the user rated/commented on. Each dictionary contains the keys movieid, title, rating, and comments. comments is a list of dictionaries. 
And each dictionary contains a comment id and the actual comment.
3. Part of my code makes a state in a child component out of the props passed down by its parent. This caused unexpected issues. The code I wrote that used those states
would produce errors saying something like the state variable was undefined. After some research I learned there can be some delay when setting a state from
props. I ended up using useEffect. An example for updating a state containing the rating is shown below. Whenever the props.rating was changed(based on whats in []), 
the state for rating would be changed with setRating. This way, even with a delay, eventually this code would properly update the state.
    ```
    useEffect(() => {
        setRating(props.rating);
    }, [props.rating]);
    ```
# What was the hardest part of the project for you, across all milestones? What is the most useful thing you learned, across all milestones?
I'd say the hardest part of the project was in this current milestone. Getting all the parent components to work with the children components was hard for me.
As I said in technical issue 2, getting the proper data format was tricky. Then actually parsing it correctly on the React side and putting it into states then 
passing that information down to children components was difficult. I had very little experience with React before this semester, so it took some time and practice 
to get more used to React's way of using html and components. Another part of the project I thought was pretty hard was using flask login. I wasn't sure how to 
get it working and I felt like the documentation wasn't super helpful. But now that I got it working it doesn't seem to bad.

The most useful thing I learned for this project was probably getting better at using python in general. I don't have much experience with python and I've heard 
it's really popular so it's nice to get more experience. I already had experience making a website that modified a database, though not with flask or sqlalchemy, 
so I appreciate that I learned that too, but not as much as just python in general. React is also pretty useful, if I decide to make websites in the future outside 
of class or school, I might consider using React.