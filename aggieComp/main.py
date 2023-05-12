# sessions are temp. as in all the data that is there and being used is "deleted" when the user leaves the web page
# these can be used to get some info form a db and makes it so that you don't have to keep rereading from the db
from flask import Flask, redirect, url_for, render_template, request, session, flash, Blueprint

from datetime import timedelta

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

from flask_wtf import FlaskForm
from flask_codemirror.fields import CodeMirrorField
from wtforms.fields import SubmitField


from compiler import compiler
from compiler import * 
from roadmap import roadmap
from qANDa import qANDa

from dbModels import * # needed so that db and app can be used in this routes file

import re
import sys 

login_manager = LoginManager() # allow app and flask login to work together
login_manager.init_app(app)
login_manager.login_view = "login"

# blueprints that need to be used from other files 
app.register_blueprint(qANDa, url_prefix = "")
app.register_blueprint(compiler, url_prefix = "")
app.register_blueprint(roadmap, url_prefix = "")

# obj that allows user passwords to be encrypted
bcrypt = Bcrypt(app)

# get is not secure 
# post is secure

@login_manager.user_loader # used to reload user object from the session
def load_user(user_id):
    return users.query.get(int(user_id))

# routes for the home page
@app.route("/home")
@app.route("/")
def home():
    return render_template("home.html")

# lets you see all of the users if you are admin and delete the user or make that user your viewing into an admin
@app.route("/view")
def view():
    return render_template("view.html", values = users.query.all())

# login page route where user can go to be logged in 
@app.route("/login", methods = ["POST", "GET"])
def login():
    form = loginForm() # using form that was created in dbModels so that user info can be collected
    if form.validate_on_submit():
        user = users.query.filter_by(username = form.username.data).first() # looking for an entry in the users db that has the same username that was enterd by ther person trying to login
        # if a user with the usernmae that was entered is found in the db then this stuff happens
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data): # comparing passwored enterd to password saved in ther users db
                login_user(user) # some funciton from flask_login that logs in the user...don't know much else about it
                flash("You have been logged in...") # test template to make sure that login worked <! --- need to change this to an actual page that will be used --- !>
            else:
                flash("Incorret Password...try again...")
        else:
            flash("There is not account with that name")
                
    return render_template("login.html", form = form)
    # there are two things that were here. One that flashes "logged in" when you add the  username and shit to the query 
    # the other is checking the sessions to see if the user is already logged in

# this will delete session info if the usr logsout or something similar
@app.route("/logout")
def logout():
    logout_user() # another function from flask_login library
    flash("You have been logged out...", "info") # second param is the category
    return redirect(url_for("login"))

# lets the user create a new account which they can use to login
@app.route("/register", methods = ["POST", "GET"])
def register():
    form = registerForm() # using the form that was created in dbModels which just has the boxes to submit user info
    admin = "False"
    if form.validate_on_submit(): # v_on_sub check if it is a post request and if it is valid, returns true if active request

        validEmail =  (re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', form.username.data)) # regex for an email and compares if the user info is a valid email

        # if the user enter email was valid then you do this stuff
        if validEmail:
            createdUserName = form.username.data.partition('@')[0] # getting the info up until the @ sign in the email. Ex: input = email@.com -> createdUserName = email

            userExist = users.query.filter_by(username = createdUserName).first() # quick query looking for a user with the username entered

            if userExist:
                flash("that user already exist")
            else:
                # no matter what, user with sfransis@nmsu.edu will be an admin
                if form.username.data == "sfransis@nmsu.edu":
                    admin = "True"
                hashed_password = bcrypt.generate_password_hash(form.password.data) # getting the users entered password and encrypting it

                # creating a new entry in the users db
                new_user = users(username = createdUserName, password = hashed_password, isAdmin = admin, email = form.username.data)
                db.session.add(new_user)
                db.session.commit()

                # will just take the user to login page after they create and account
                flash("Your account has been created...")
        else:
            flash("That is not a valid email")
        
    return render_template("registerUser.html", form = form)

@app.route("/deleteAccount", methods = ["POST", "GET"])
def deleteAccount():
    form = deleteAccForm()
    if form.validate_on_submit():
        # only allows the user to delete their own account if they're logged in with the account they wish to delete
        if form.username.data == current_user.username:
            regUser = users.query.filter_by(username = form.username.data).first() # looking for an entry in the users db that has the same username that was enterd by ther person trying to login
            if regUser:
                isSamePass = bcrypt.check_password_hash(regUser.password, form.password.data) # comparing entered password to the password in the database
                # if the two passwords are the same then if goes through
                if isSamePass:
                    flash("Account has been deleted...")
                    db.session.delete(regUser)
                    db.session.commit()
                    return redirect(url_for("login"))
                else:
                    flash("Password is incorrect...")
            else:
                flash("There is no user with that name...")
        else:
            flash("You can't delete other peoples data...")
    return render_template("deleteAcc.html", form = form)

# allows the admin to delete account in the admin page. Page only shows up for an admin
@app.route("/adminDeleteAccount/<givenUsername>", methods = ["POST", "GET"])
def adminDeleteAccount(givenUsername):
    regUser = users.query.filter_by(username = givenUsername).first()
    db.session.delete(regUser)
    db.session.commit()
    return render_template("view.html", values = users.query.all())

# allows the admin to make other users admin in the admin page. Page only shows up for an admin
@app.route("/makeUserAdmin/<givenUsername>", methods = ["POST", "GET"])
def makeUserAdmin(givenUsername):
    #setattr(user, 'no_of_logins', user.no_of_logins + 1)
    regUser = users.query.filter_by(username = givenUsername).first()
    setattr(regUser, 'isAdmin', "True")
    db.session.commit()
    return render_template("view.html", values = users.query.all())

if __name__ == "__main__":
    db.create_all() # creates all of the db NOTE that if you want to make a change to the db, you need to replace create_all with drop_all so that current dbs are deleted and then change it back so that the changes are made
    #db.session.query(Comment).delete()
    app.run(debug = True) #means that we won't have to rerun the server