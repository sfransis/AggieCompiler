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
                question = Questions(questionPost, csClass, current_user.username) # creating a new entry in the db model or "table"
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

# allows the user to post a comment underneath a specific post and add it to the db for questions
# the comment isn't added to other post
# needs to have the post id which is passed through the html form in viewQuestions.html
@qANDa.route("createComment/<post_id>", methods = ["POST"])
def createComment(post_id):
    text = request.form.get('userResponse') # just another from that holds the users reponse in the web page
    if not text:
        flash("comment can't be empty")
    else:
        post = Questions.query.filter_by(_id = post_id) # find questions that have the needed post id
        # a post was found with the needed post id
        if post:
            response = Comment(content = text, posterUsername = current_user.username, post_id = post_id) # setting var to a row in the db table with the given info
            db.session.add(response) # adding this question model to the db
            db.session.commit()
        else:
            flash("Post does not exist...")
    return redirect(url_for("qANDa.viewQ"))

# just lets user view all post <! --- Changes later so that the post are organized by class rather than having them all in one place --- !>
@qANDa.route("/viewQuestions", methods = ["POST", "GET"])
def viewQ():
    return render_template("viewQuestions.html", htmlQuestion = Questions.query.all(), htmlResponses = Comment.query.all(), currentUser = current_user.username)

# allows the user that posted a post to delete and when a post is deleted, all comments associated with it are also deleted
@qANDa.route("/deletePost/<post_id>", methods = ["POST"])
def deletePost(post_id):
    post = Questions.query.filter_by(_id = post_id).delete()
    db.session.commit()
    question = Comment.query.filter_by(post_id = post_id).delete()
    db.session.commit()
    return redirect(url_for("qANDa.viewQ"))

# deletes a single comment in a post if the deleter is also the comment poster
@qANDa.route("/deleteComment/<post_id>", methods = ["POST"])
def deleteComment(post_id):
    post = Comment.query.filter_by(id = post_id).delete()
    db.session.commit()
    return redirect(url_for("qANDa.viewQ"))

