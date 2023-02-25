from flask import Blueprint, render_template, session, request, flash
from flask_sqlalchemy import SQLAlchemy
from run import create_app
from dbModels import *

# creating a db model

qANDa = Blueprint("qANDa", __name__, static_folder = "static", template_folder = "template")

@qANDa.route("/postQuestion", methods = ["POST", "GET"])
def pstQst(): 
    if request.method == "POST":
        session.permanent = True
        questionPost = request.form["userQuestion"]
        question = questionDB(questionPost, "cs172") # creating a new entry in the db model or "table"
        db.session.add(question) # adding this user model to the db
        db.session.commit()
        flash("Post successful!...")
    return render_template("qANDa.html")

@qANDa.route("/viewQuestions")
def viewQ():
    return render_template("viewQuestions.html", htmlQuestion = questionDB.query.all())