#ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
#anaconda-project 0.10.1 requires ruamel-yaml, which is not installed.
#cookiecutter 1.7.2 requires Jinja2<3.0.0, but you have jinja2 3.1.2 which is incompatible.
#cookiecutter 1.7.2 requires MarkupSafe<2.0.0, but you have markupsafe 2.1.2 which is incompatible.

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

from compiler import compiler
from roadmap import roadmap
from qANDa import qANDa

from dbModels import * # needed so that db and app can be used in this routes file

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

# lets you see all of the users and their hashed passwords as long as they have registered 
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
    if form.validate_on_submit(): # v_on_sub check if it is a post request and if it is valid, returns true if active request
        hashed_password = bcrypt.generate_password_hash(form.password.data) # getting the users entered password and encrypting it

        # creating a new entry in the users db
        new_user = users(username = form.username.data, password = hashed_password)
        db.session.add(new_user)
        db.session.commit()

        # will just take the user to login page after they create and account
        flash("Your account has been created...")
    return render_template("registerUser.html", form = form)

if __name__ == "__main__":
    db.create_all() # creates all of the db NOTE that if you want to make a change to the db, you need to replace create_all with drop_all so that current dbs are deleted and then change it back so that the changes are made
    #db.session.query(Comment).delete()
    app.run(debug = True) #means that we won't have to rerun the server