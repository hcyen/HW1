## HW 1
## SI 364 W18
## 1000 points
# to run it, go to the command line and cd to the directory the code resides in
# python SI364W18_HW1.py runserver

import os
import urllib
#import urlparse
import re
import datetime
import json
import urllib.request, urllib.parse, urllib.error
from urllib.request import Request, urlopen
import ssl
import requests
#from flask import request #https://stackoverflow.com/questions/41487473/nameerror-name-request-is-not-defined
#for problem 3: NameError: name 'request' is not defined

#from flask import Response
from flask import Flask, request, Response, redirect

import hashlib
#################################

## List below here, in a comment/comments, the people you worked with on this assignment AND any resources you used to find code (50 point deduction for not doing so). If none, write "None".
## None


## [PROBLEM 1] - 150 points
## Below is code for one of the simplest possible Flask applications. Edit the code so that once you run this application locally and go to the URL 'http://localhost:5000/class', you see a page that says "Welcome to SI 364!"
import flask
#from flask import Flask
app = Flask(__name__)
app.debug = True

@app.route('/')
def hello_to_you():
    return 'Hello!'
#http://pymbook.readthedocs.io/en/latest/flask.html
#need to create a directory - templates and create a welcome.html within the templates directory.
@app.route('/class')
def welcome():
    return flask.render_template('welcome.html')




## [PROBLEM 2] - 250 points
## Edit the code chunk above again so that if you go to the URL
## 'http://localhost:5000/movie/<name-of-movie-here-one-word>' you see a big dictionary of data on the page.
## For example, if you go to the URL 'http://localhost:5000/movie/ratatouille', you should see something
## like the data shown in the included file sample_ratatouille_data.txt, which contains data about the animated movie Ratatouille.
## However, if you go to the url http://localhost:5000/movie/titanic, you should get different data,
## and if you go to the url
##'http://localhost:5000/movie/dsagdsgskfsl' for example, you should see data on the page that looks like this:
#first_flask_app_solution.py 
# {
#  "resultCount":0,
#  "results": []
# }


## You should use the iTunes Search API to get that data.
## Docs for that API are here: https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/
## Of course, you'll also need the requests library and knowledge of how to make a request to a REST API for data.

## Run the app locally (repeatedly) and try these URLs out!

@app.route('/movie/<anytitlesearch>')
def get_itunes_data(anytitlesearch):
	# Get specifics of how to write this from knowledge about REST APIs in Python -- see textbook -- and iTunes API documentation
    baseurl = "https://itunes.apple.com/search"
    params_diction = {}
    params_diction["term"] = anytitlesearch
    resp = requests.get(baseurl,params=params_diction)
    text = resp.text
    python_obj = json.loads(text)
    album_titles = []
    for item in python_obj["results"]:
        if 'collectionName' in item: #if the key exists in the dictionary
            album_titles.append(item["collectionName"])
            #album_titles.append(item["trackName"])
            # This turns out where you find the album name in the nested data
    all_titles = "<br>".join(album_titles) # join by the <br> tag, which means 'line break' in html
    # return str(album_titles)
    return all_titles
    #return a string -- must return a string to render on the page




## [PROBLEM 3] - 250 points

## Edit the above Flask application code so that if you run the application locally
## and got to the URL http://localhost:5000/question, you see a form that asks you to
## enter your favorite number.
## Once you enter a number and submit it to the form, you should then see a web page that says
## "Double your favorite number is <number>".
## For example, if you enter 2 into the form, you should then see a page that says
## "Double your favorite number is 4". Careful about types in your Python code!
## You can assume a user will always enter a number only.
@app.route('/question')
##http://interactivepython.org/runestone/static/webfundamentals/Frameworks/frameworkintro.html#forms-processing
def question_form():
    if 'favoritenumber' in request.args:
        return sendPage(request.args['favoritenumber'])
    else:
        return sendForm()

def sendForm():
    return '''
    <html>
      <body>
          <form method='get'>
              <label for="mynumber">Enter Your Favorite Number</label>
              <input id="mynumber" type="text" name="favoritenumber" value="2" />
              <input type="submit">
          </form>
      </body>
    </html>
    '''

def sendPage(number):
    return '''
    <html>
      <body>
        <h1>Double your favorite number is <p id="demo"></p> </h1>
        <script>
        
            var z = {0} * 2;
            document.getElementById("demo").innerHTML = z;
        </script>
      </body>
    </html>
    '''.format(number)

## [PROBLEM 4] - 350 points
#@app.route('/problem4form')
#https://stackoverflow.com/questions/11556958/sending-data-from-html-form-to-a-python-script-in-flask
#https://www.tutorialspoint.com/flask/flask_wtf.htm
#https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms-legacy
#@app.route('/problem4form')

## Come up with your own interactive data exchange that you want to see happen dynamically
## in the Flask application, and build it into the above code for a Flask application,
## following a few requirements.

## You should create a form that appears at the route: http://localhost:5000/problem4form

## Submitting the form should result in your seeing the results of the form on the same page.

## What you do for this problem should:
# - not be an exact repeat of something you did in class
# - must include an HTML form with checkboxes and text entry
# - should, on submission of data to the HTML form,
# show new data that depends upon the data entered into the submission form and is readable by humans (
# more readable than e.g. the data you got in Problem 2 of this HW).
# The new data should be gathered via API request or BeautifulSoup.

# You should feel free to be creative and do something fun for you --
# And use this opportunity to make sure you understand these steps:
# if you think going slowly and carefully writing out steps for a simpler data transaction,
# like Problem 1, will help build your understanding, you should definitely try that!

# You can assume that a user will give you the type of input/response you expect in your form;
# you do not need to handle errors or user confusion.
#(e.g. if your form asks for a name, you can assume a user will type a reasonable name;
# if your form asks for a number, you can assume a user will type a reasonable number;
# if your form asks the user to select a checkbox, you can assume they will do that.)

# Points will be assigned for each specification in the problem.
@app.route('/problem4form',methods=["GET","POST"])
def form4():
    formstring = """<br><br>
    <form action="" method='POST'>
    
    <input type="checkbox" name="searchfrom" value="itune"> Search from itune<br>
    <input type="text" name="moviename"> Enter a movie name: <br>
    
    <input type="submit" value="Submit">
    """ ## HINT: In there ^ is where you need to add a little bit to the code...
    if request.method == "POST":
        searchfrom = request.form['searchfrom']
        print(searchfrom)
        if searchfrom:
            movietext = request.form['moviename']
            movielist = get_itunes_data(movietext)
            return '''
            <html>
              <body>
                <h1>Movie list <p id="demo"></p> </h1>
                <script>
            
                
                document.getElementById("demo").innerHTML = "''' + movielist + '''";
                </script>
          </body>
        </html>
        '''
            
            
        
        #pass
        # Add more code here so that when someone enters a phrase, you see their data (somehow) AND the form!
    else:
        return formstring
#http://opentechschool.github.io/python-flask/core/form-submission.html
#def signup():
#    email = request.form['email']
#   print("The email address is '" + email + "'")

#if __name__ == '__main__':
#    app.run()
if __name__ == "__main__":
    app.run(use_reloader=True, debug=True) # Nice trick -- see details in lecture notes
