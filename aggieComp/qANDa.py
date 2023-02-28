from flask import Blueprint, render_template, session, request, flash, redirect, url_for
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
from dbModels import *

# creating a db model

qANDa = Blueprint("qANDa", __name__, static_folder = "static", template_folder = "template")

@qANDa.route("/postQuestion", methods = ["POST", "GET"])
def pstQst(): 
    # check if a user is logged in and if they are they can post but if they're not they can't post questions
    if current_user.is_authenticated:
        if request.method == "POST":
            # changes the page depending on whether the user selects post, change class, or post other question buttons
            if request.form['submit-button'] == "Change Class":
                return redirect(url_for("qANDa.showClasses"))
            elif request.form['submit-button'] == "Post Other Question":
                return redirect(url_for("qANDa.showClasses"))
            elif request.form['submit-button'] == "Post":
                session.permanent = True
                questionPost = request.form["userQuestion"] # gets the info from the question box
                csClass = session["questionClass"] # sets this info based on the users selected class
                question = questionDB(questionPost, csClass, current_user.username) # creating a new entry in the db model or "table"
                db.session.add(question) # adding this question model to the db
                db.session.commit()
                flash("Post successful!...")
    else:
        flash("You have to be logged in to post a question...")
        return redirect(url_for("qANDa.showClasses"))
    return render_template("qANDa.html")

@qANDa.route("/showingClassOptions", methods = ["POST", "GET"])
def showClasses():
    # sets the sessions class to whatever class the user clicks on so that 
    # this info can be used later
    if request.method == "POST":
        session.permanent = True
        if request.form['submit-button'] == "CS-1":
            session["questionClass"] =  "CS-1"
            return redirect(url_for("qANDa.pstQst"))
        elif request.form['submit-button'] == "CS-2":
            session["questionClass"] = "CS-2"
            return redirect(url_for("qANDa.pstQst"))
        elif request.form['submit-button'] == "CS-3":
            session["questionClass"] = "CS-3"
            return redirect(url_for("qANDa.pstQst"))
        elif request.form['submit-button'] == "CS-4":
            session["questionClass"] = "CS-4" 
            return redirect(url_for("qANDa.pstQst"))
        elif request.form['submit-button'] == "General":
            session["questionClass"] = "General" 
            return redirect(url_for("qANDa.pstQst"))
    else:
        return render_template("showClasses.html")

# just lets user view all post <! --- Changes later so that the post are organized by class rather than having them all in one place --- !>
@qANDa.route("/viewQuestions")
def viewQ():
    return render_template("viewQuestions.html", htmlQuestion = questionDB.query.all())