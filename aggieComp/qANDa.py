from flask import Blueprint, render_template, session, request, flash
from flask_sqlalchemy import SQLAlchemy

qANDa = Blueprint("qANDa", __name__, static_folder = "static", template_folder = "template")

@qANDa.route("/postQuestion", methods = ["POST", "GET"])
def pstQst(): 
    if request.method == "POST":
        session.permanent = True
        question = request.form["userQuestion"]
        session["question"] = question
        flash("Post successful!...")
    return render_template("qANDa.html")

@qANDa.route("/viewQuestions")
def viewQ():
    return render_template("viewQuestions.html", userQuestions = session["question"])