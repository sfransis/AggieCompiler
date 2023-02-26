from flask import Blueprint, render_template, session, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from run import create_app
from dbModels import *

# creating a db model

qANDa = Blueprint("qANDa", __name__, static_folder = "static", template_folder = "template")

@qANDa.route("/postQuestion", methods = ["POST", "GET"])
def pstQst(): 
    if request.method == "POST":
        if request.form['submit-button'] == "Change Class":
            return redirect(url_for("qANDa.showClasses"))
        elif request.form['submit-button'] == "Post Other Question":
            return redirect(url_for("qANDa.showClasses"))
        elif request.form['submit-button'] == "Post":
            session.permanent = True
            questionPost = request.form["userQuestion"]
            csClass = session["questionClass"]
            question = questionDB(questionPost, csClass) # creating a new entry in the db model or "table"
            db.session.add(question) # adding this user model to the db
            db.session.commit()
            flash("Post successful!...")

    return render_template("qANDa.html")

@qANDa.route("/showingClassOptions", methods = ["POST", "GET"])
def showClasses():
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

@qANDa.route("/viewQuestions")
def viewQ():
    return render_template("viewQuestions.html", htmlQuestion = questionDB.query.all())