#ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
#anaconda-project 0.10.1 requires ruamel-yaml, which is not installed.
#cookiecutter 1.7.2 requires Jinja2<3.0.0, but you have jinja2 3.1.2 which is incompatible.
#cookiecutter 1.7.2 requires MarkupSafe<2.0.0, but you have markupsafe 2.1.2 which is incompatible.

# sessions are temp. as in all the data that is there and being used is "deleted" when the user leaves the web page
# these can be used to get some info form a db and makes it so that you don't have to keep rereading from the db
from flask import Flask, redirect, url_for, render_template, request, session, flash, Blueprint

from datetime import timedelta

from flask_sqlalchemy import SQLAlchemy

from compiler import compiler
from roadmap import roadmap
from qANDa import qANDa

from run import create_app

from dbModels import *
#app = create_app()
app.register_blueprint(qANDa, url_prefix = "")
app.register_blueprint(compiler, url_prefix = "")
app.register_blueprint(roadmap, url_prefix = "")

# get is not secure 
# post is secure

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/view")
def view():
    return render_template("view.html", values = users.query.all())

@app.route("/login", methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"] # you have to use the nm specifically since this is what is being used for the login.html

        #session data is being set up 
        session["user"] = user

        # check if the user already exist and if they don't then create them 
        found_user = users.query.filter_by(name = user).first() # finds all the users that have the name typed in by the user in the login page
        # how to delete 1 entry: users.query.delete() where you can still use the filter by shit. you can also just use users.delete()
        if found_user: 
            session["email"] = found_user.email
        else:
            usr = users(user, "") # creating a new entry in the db model or "table"
            db.session.add(usr) # adding this user model to the db
            db.session.commit()

        flash("login succesful!")
        return redirect(url_for("user"))
    # this else is just for when the user is already logged in but tries to go to the login page 
    # through the url. Which wouldn't make sense since they're already logged in. So they're redirected to the 
    # user page which just looks like they're staying in the same spot and nothing happens
    else: 
        if "user" in session:
            flash("already logged in!")
            return redirect(url_for("user"))
        return render_template("login.html")

@app.route("/user", methods = ["POST", "GET"])
def user():
    email = None
    # getting session data
    # if is making sure that there is actually some data in the session for the user
    if "user" in session:
        user = session["user"]
        # this if is getting the email if the user hasn't already put it in the session
        if request.method == "POST":
            email = request.form["email"] # think this is getting the email from the submit button form
            session["email"] = email # setting the current sessions info for emal to the email that was put in by the user
            found_user = users.query.filter_by(name = user).first()
            found_user.email = email # changing the users email in the db
            db.session.commit() # i think this makes it so that users email is rememberd through out the session
            flash("Email was saved!")
        # else runs to check if the email is already in the session
        else: 
            if "email" in session:
                email = session["email"]
        return render_template("user.html", email = email)
    else:
        flash("you are not logged in!")
        return redirect(url_for("login"))

# this will delete session info if the usr logsout or something similar
@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash("Yu have been logged out...", "info") # second param is the category
    session.pop("user", None) 
    session.pop("email", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    db.create_all()
    app.run(debug = True) #means that we won't have to rerun the server