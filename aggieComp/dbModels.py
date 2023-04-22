from flask import Flask 
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from run import *
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

class Questions(db.Model, UserMixin):
    _id = db.Column("id", db.Integer, primary_key = True) # each obj in our model is gonna have an "id" which is gonna be an int
    userQuestion = db.Column(db.String(100))
    csClass = db.Column(db.String(100))
    posterName = db.Column(db.String(100))

    comments = db.relationship('Comment', backref = 'questions')

    # I think these are the things that we for sure need everytime 
    # as in they are alwasy none empty
    # This is needed for some reasons that i don't know since the videos are from different people
    # so there isn't a way for me to knwo exactly what is going on unless i look at documentation which is probs a good idea
    def __init__(self, userQuestion, csClass, posterName):
        self.userQuestion = userQuestion 
        self.csClass = csClass
        self.posterName = posterName

class reportedQuestions(db.Model, UserMixin):
    _id = db.Column("id", db.Integer, primary_key = True) # each obj in our model is gonna have an "id" which is gonna be an int
    userQuestion = db.Column(db.String(100))
    csClass = db.Column(db.String(100))
    posterName = db.Column(db.String(100))

    # I think these are the things that we for sure need everytime 
    # as in they are alwasy none empty
    # This is needed for some reasons that i don't know since the videos are from different people
    # so there isn't a way for me to knwo exactly what is going on unless i look at documentation which is probs a good idea
    def __init__(self, userQuestion, csClass, posterName):
        self.userQuestion = userQuestion 
        self.csClass = csClass
        self.posterName = posterName

class Comment(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.Text)
    posterUsername = db.Column(db.String(100))
    post_id = db.Column(db.Integer, db.ForeignKey('questions.id'))

    def __init__(self, content, post_id, posterUsername):
        self.content = content 
        self.post_id = post_id
        self.posterUsername = posterUsername

class reportedComment(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.Text)
    posterUsername = db.Column(db.String(100))
    post_id = db.Column(db.Integer, db.ForeignKey('questions.id'))

    def __init__(self, content, post_id, posterUsername):
        self.content = content 
        self.post_id = post_id
        self.posterUsername = posterUsername

# creating a db model
class users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True) # each obj in our model is gonna have an "id" which is gonna be an int
    username = db.Column(db.String(100), unique = True, nullable = False) #the nullable and unique things might not have been added since they were added after the db was already created
    password = db.Column(db.String(100), nullable = False)
    isAdmin = db.Column(db.String(100))
    email = db.Column(db.String(100), unique = True, nullable = False)

class registerForm(FlaskForm):
    username = StringField(validators = [InputRequired(), Length(min = 4, max = 20)], render_kw = {"placeholder": "Email"})
    password = PasswordField(validators = [InputRequired(), Length(min = 4, max = 20)], render_kw = {"placeholder": "Password"}) #using passwordField makesit so that when the user enters their shit it's black dots instead of letters
    submit = SubmitField("Register") # Just the button to register and has the word "Register" on it 

    # the length for these passwords and stuff in the db are differnt from the form since the max a password can be is 20 but in the encryption it can be much larger 

    def validate_username(self, username):
        existing_user_username = users.query.filter_by(username = username.data).first() # looks to see if the username already exist in the db and then raises some kind of problem if it does
        if existing_user_username:
            raise ValidationError("That username is already in use. Please chose a different one.")
        
class loginForm(FlaskForm):
    username = StringField(validators = [InputRequired(), Length(min = 4, max = 20)], render_kw = {"placeholder": "Username"})
    password = PasswordField(validators = [InputRequired(), Length(min = 4, max = 20)], render_kw = {"placeholder": "Password"}) #using passwordField makesit so that when the user enters their shit it's black dots instead of letters
    submit = SubmitField("Login") # Just the button to register and has the word "Login" on it 

class deleteAccForm(FlaskForm):
    username = StringField(validators = [InputRequired(), Length(min = 1, max = 20)], render_kw = {"placeholder": "Username"})
    password = PasswordField(validators = [InputRequired(), Length(min = 4, max = 20)], render_kw = {"placeholder": "Password"}) #using passwordField makesit so that when the user enters their shit it's black dots instead of letters
    submit = SubmitField("Delete") # Just the button to register and has the word "Login" on it 
