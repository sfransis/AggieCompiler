from flask import Flask 
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

def create_app():
    app = Flask(__name__)
    app.app_context().push() # there was an error that was saying "working outside of application context" and it was fixed by adding this line...idk what it does

    #session is encypted in the server which is why we need the secret key 
    # and if we don't then we will get some problem
    app.secret_key = "hello"

    # this is being used so that the user can actually get out of the browser and not be
    # logged out imediately. They can come back, say two days later, and not have to log back in. 
    app.permanent_session_lifetime = timedelta(days = 5) # you can use minutes, and days 

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # creating a db object

    return app