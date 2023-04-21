# Creator:      Fransisco Sanchez
# Last Updated: Feb 27
# Purpose:      this file is just used to create the app and db objects in a place tht can be accessed by all other files 
#               just incase they need to be used 

from flask import Flask 
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

from flask_codemirror import CodeMirror
from flask_wtf import FlaskForm
from flask_codemirror.fields import CodeMirrorField
from wtforms.fields import SubmitField


SECRET_KEY = 'secret!'
CODEMIRROR_LANGUAGES = ['python', 'html', 'java', 'c++','c']
WTF_CSRF_ENABLED = True

CODEMIRROR_THEME = '3024-day'
CODEMIRROR_ADDONS = ( 
            ('display', 'placeholder'),
)

app = Flask(__name__)
app.config.from_object(__name__)
codemirror = CodeMirror(app)

app.app_context().push() # there was an error that was saying "working outside of application context" and it was fixed by adding this line...idk what it does

#session is encypted in the server which is why we need the secret key 
# and if we don't then we will get some problem
#app.secret_key = "hello"

# this is being used so that the user can actually get out of the browser and not be
# logged out imediately. They can come back, say two days later, and not have to log back in. 
app.permanent_session_lifetime = timedelta(days = 5) # you can use minutes, and days 

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'thisisthesecretkey'
# creating a db object

db = SQLAlchemy(app)
