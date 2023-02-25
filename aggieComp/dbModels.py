from flask import Flask 
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from run import create_app

app = create_app()

db = SQLAlchemy()
db.init_app(app)

class questionDB(db.Model):
    _id = db.Column("id", db.Integer, primary_key = True) # each obj in our model is gonna have an "id" which is gonna be an int
    userQuestion = db.Column(db.String(100))
    csClass = db.Column(db.String(100))

    # I think these are the things that we for sure need everytime 
    # as in they are alwasy none empty
    def __init__(self, userQuestion, csClass):
        self.userQuestion = userQuestion 
        self.csClass = csClass

# creating a db model
class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key = True) # each obj in our model is gonna have an "id" which is gonna be an int
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    # I think these are the things that we for sure need everytime 
    # as in they are alwasy none empty
    def __init__(self, name, email):
        self.name = name 
        self.email = email