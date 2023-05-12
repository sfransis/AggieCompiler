from flask import Flask, Blueprint, render_template, session, request, flash, redirect, url_for
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
from dbModels import *

qANDa = Blueprint("qANDa", __name__, static_folder = "static", template_folder = "template")

# route that will allow uesers to post a question
@qANDa.route("/postQuestion", methods = ["POST", "GET"])
def pstQst(): 
    # check if a user is logged in and if they are they can post but if they're not they can't post questions
    if current_user.is_authenticated:
        if request.method == "POST":
            session.permanent = True
            # checking what class is currently selected by the user 
            if request.form['class-options'] == "CS-1":
                session["questionClass"] =  "CS-1"
            elif request.form['class-options'] == "CS-2":
                session["questionClass"] = "CS-2"
            elif request.form['class-options'] == "CS-3":
                session["questionClass"] = "CS-3"
            elif request.form['class-options'] == "CS-4":
                session["questionClass"] = "CS-4" 
            elif request.form['class-options'] == "General":
                session["questionClass"] = "General" 

            # changes the page depending on whether the user selects post, change class, or post other question buttons
            # There has been a change to how the questions are made which means there doesn't need to be the options to go back to "showclass"
            # I will keep them here however just incase something happens in the future
            #if request.form['submit-button'] == "Change Class":
            #   return redirect(url_for("qANDa.showClasses"))
            #elif request.form['submit-button'] == "Post Other Question":
            #    return redirect(url_for("qANDa.showClasses"))
            
            # commits the question with all of the needed information when the user presses the post button
            if request.form['submit-button'] == "Post":
                questionPost = request.form['userQuestion'] # gets the info from the question box
                csClass = session['questionClass'] # sets this info based on the users selected class
                question = Questions(questionPost, csClass, current_user.username) # creating a new entry in the db model or "table"
                db.session.add(question) # adding this question model to the db
                db.session.commit()
                flash("Post successful!...")
    else:
        flash("You have to be logged in to post a question...")
        return redirect(url_for("login"))
    return render_template("qANDa.html")

# allows the user to post a comment underneath a specific post and add it to the db for questions
# the comment isn't added to other post
# needs to have the post id which is passed through the html form in viewQuestions.html
@qANDa.route("createComment/<post_id>/<csClass>", methods = ["POST"])
def createComment(post_id, csClass):
    if current_user.is_authenticated:
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
        # when you post a comment you're going to be redirected to the question group where the question you just commented under was
        if csClass == "General":
            return redirect(url_for("qANDa.viewQ"))
        elif csClass == "CS-1":
            return redirect(url_for("qANDa.viewCS1"))
        elif csClass == "CS-2":
            return redirect(url_for("qANDa.viewCS2"))
        elif csClass == "CS-3":
            return redirect(url_for("qANDa.viewCS3"))
        elif csClass == "CS-4":
            return redirect(url_for("qANDa.viewCS4"))
        else:
            return redirect(url_for("qANDa.viewQ"))
    else:
            flash("You have to be logged in to post a comment...")
            return redirect(url_for("login"))
    
# allows the user that posted a post to delete and when a post is deleted, all comments associated with it are also deleted
# getting sent here is dependent on the html if 
@qANDa.route("/deletePost/<post_id>/<csClass>", methods = ["POST"])
def deletePost(post_id, csClass):
    post = Questions.query.filter_by(_id = post_id).delete()
    db.session.commit()
    question = Comment.query.filter_by(post_id = post_id).delete()
    db.session.commit()
    # when you post a comment you're going to be redirected to the question group where the question you just commented under was
    if csClass == "General":
        return redirect(url_for("qANDa.viewQ"))
    elif csClass == "CS-1":
        return redirect(url_for("qANDa.viewCS1"))
    elif csClass == "CS-2":
        return redirect(url_for("qANDa.viewCS2"))
    elif csClass == "CS-3":
        return redirect(url_for("qANDa.viewCS3"))
    elif csClass == "CS-4":
        return redirect(url_for("qANDa.viewCS4"))
    else:
        return redirect(url_for("qANDa.viewQ"))

# deletes a single comment in a post if the deleter is also the comment poster
# this is the same as the del post where it is called from html
@qANDa.route("/deleteComment/<post_id>/<csClass>", methods = ["POST"])
def deleteComment(post_id, csClass):
    post = Comment.query.filter_by(id = post_id).delete()
    db.session.commit()
    # when you post a comment you're going to be redirected to the question group where the question you just commented under was
    if csClass == "General":
        return redirect(url_for("qANDa.viewQ"))
    elif csClass == "CS-1":
        return redirect(url_for("qANDa.viewCS1"))
    elif csClass == "CS-2":
        return redirect(url_for("qANDa.viewCS2"))
    elif csClass == "CS-3":
        return redirect(url_for("qANDa.viewCS3"))
    elif csClass == "CS-4":
        return redirect(url_for("qANDa.viewCS4"))
    else:
        return redirect(url_for("qANDa.viewQ"))
    
# allows the admin to delete comments that were reported. Option only shows up when a user is admin
@qANDa.route("/deleteReportedComment/<post_id>", methods = ["POST"])
def deleteReportedComment(post_id):
    post = reportedComment.query.filter_by(id = post_id).delete()
    delete = Comment.query.filter_by(id = post_id).first()
    db.session.delete(delete)
    db.session.commit()
    return redirect(url_for("qANDa.viewReportedComments"))

# allows the admin to delete questions that were reported. Option only shows up when a user is admin
@qANDa.route("/deleteReportedPost/<post_id>", methods = ["POST"])
def deleteReportedPost(post_id):
    post = reportedQuestions.query.filter_by(_id = post_id).delete()
    delete = Questions.query.filter_by(_id = post_id).first()
    db.session.delete(delete)
    db.session.commit()
    return redirect(url_for("qANDa.viewReportedQuestions"))

# allows the ueser to report a comment. All users can report comments
@qANDa.route("/reportComment/<post_id>/<csClass>", methods = ["POST"])
def reportComment(post_id, csClass):
    post = Comment.query.filter_by(id = post_id).first()
    report = reportedComment(content = post.content, posterUsername = post.posterUsername, post_id = post.post_id)
    db.session.add(report)
    db.session.commit()
    
    if csClass == "General":
        return redirect(url_for("qANDa.viewQ"))
    elif csClass == "CS-1":
        return redirect(url_for("qANDa.viewCS1"))
    elif csClass == "CS-2":
        return redirect(url_for("qANDa.viewCS2"))
    elif csClass == "CS-3":
        return redirect(url_for("qANDa.viewCS3"))
    elif csClass == "CS-4":
        return redirect(url_for("qANDa.viewCS4"))
    else:
        return redirect(url_for("qANDa.viewQ"))

# allows the ueser to report a question/post. All users can report comments
@qANDa.route("/reportPost/<post_id>/<csClass>", methods = ["POST"])
def reportPost(post_id, csClass):
    post = Questions.query.filter_by(_id = post_id).first()
    report = reportedQuestions(userQuestion = post.userQuestion, posterName = post.posterName, csClass = post.csClass)
    db.session.add(report)
    db.session.commit()
    
    if csClass == "General":
        return redirect(url_for("qANDa.viewQ"))
    elif csClass == "CS-1":
        return redirect(url_for("qANDa.viewCS1"))
    elif csClass == "CS-2":
        return redirect(url_for("qANDa.viewCS2"))
    elif csClass == "CS-3":
        return redirect(url_for("qANDa.viewCS3"))
    elif csClass == "CS-4":
        return redirect(url_for("qANDa.viewCS4"))
    else:
        return redirect(url_for("qANDa.viewQ"))
    
# allows the admin to remove report from a comment
@qANDa.route("/postReportedComment/<post_id>", methods = ["POST", "GET"])
def pstReportedComm(post_id): 
    # check if a user is logged in and if they are they can post but if they're not they can't post questions
    if request.method == "POST":
        reportedComm = reportedComment.query.filter_by(id = post_id).first()
        
        db.session.delete(reportedComm)
        db.session.commit()
    return redirect(url_for("qANDa.viewReportedComments"))

# allows the admin to remove report from a question/post
@qANDa.route("/postReportedPost/<post_id>", methods = ["POST", "GET"])
def pstReportedPost(post_id): 
    # check if a user is logged in and if they are they can post but if they're not they can't post questions
    if request.method == "POST":
        reportedComm = reportedQuestions.query.filter_by(_id = post_id).first()
        
        db.session.delete(reportedComm)
        db.session.commit()
    return redirect(url_for("qANDa.viewReportedQuestions"))

@qANDa.route("/adminRemoveReportComment/<post_id>", methods = ["POST", "GET"])
def adminRemoveReportComment(post_id): 
    reportedComm = reportedComment.query.filter_by(id = post_id).first()
    db.session.delete(reportedComm)
    db.session.commit()
    return redirect(url_for("qANDa.viewReportedComments"))

@qANDa.route("/adminDeleteReportedComment/<post_id>", methods = ["POST", "GET"])
def adminDeleteReportedComment(post_id):
    comment = reportedComment.query.filter_by(id = post_id).first()
    db.session.delete(comment)
    delete = Comment.query.filter_by(id = post_id).first()
    db.session.delete(delete)
    db.session.commit()
    return redirect(url_for("qANDa.viewReportedComments"))

@qANDa.route("/adminRemoveReportOnPost/<post_id>", methods = ["POST", "GET"])
def adminRemoveReportOnPost(post_id): 
    reportedQst = reportedQuestions.query.filter_by(_id = post_id).first()  
    db.session.delete(reportedQst)
    db.session.commit()
    return redirect(url_for("qANDa.viewReportedQuestions"))

@qANDa.route("/adminDeleteReportedPost/<post_id>", methods = ["POST", "GET"])
def adminDeleteReportedPost(post_id):
    post = reportedQuestions.query.filter_by(_id = post_id).first()
    db.session.delete(post)
    delete = Questions.query.filter_by(_id = post_id).first()
    db.session.delete(delete)
    db.session.commit()
    return redirect(url_for("qANDa.viewReportedQuestions"))

@qANDa.route("/viewReportedComments")
def viewReportedComments():
    return render_template("viewReportedComments.html", repoComm = reportedComment.query.all())

@qANDa.route("/viewReportedQuestions")
def viewReportedQuestions():
    return render_template("viewReportedQst.html", repoQst = reportedQuestions.query.all())


# just lets user view all post organized by class
@qANDa.route("/viewQuestions", methods = ["POST", "GET"])
def viewQ():
    q = Questions.query.filter_by(csClass = "General")
    if current_user.is_authenticated:
        if q.count() == 0:
                return render_template("emptyClass.html")
        else:
            return render_template("viewQuestions.html", htmlQuestion = q, htmlResponses = Comment.query.all(), currentUser = current_user.username)
    else:
        if q.count() == 0:
            return render_template("emptyClass.html")
        return render_template("viewQuestions.html", htmlQuestion = q, htmlResponses = Comment.query.all(), currentUser = "notSignedIn")

@qANDa.route("/viewCS-1", methods = ["POST", "GET"])
def viewCS1():
    q = Questions.query.filter_by(csClass = "CS-1")
    if current_user.is_authenticated:
        if q.count() == 0:
                return render_template("emptyClass.html")
        else:
            return render_template("viewQuestions.html", htmlQuestion = q, htmlResponses = Comment.query.all(), currentUser = current_user.username)
    else:
        if q.count() == 0:
            return render_template("emptyClass.html")
        return render_template("viewQuestions.html", htmlQuestion = q, htmlResponses = Comment.query.all(), currentUser = "notSignedIn")
    
@qANDa.route("/viewCS-2", methods = ["POST", "GET"])
def viewCS2():
    q = Questions.query.filter_by(csClass = "CS-2")
    if current_user.is_authenticated:
        if q.count() == 0:
                return render_template("emptyClass.html")
        else:
            return render_template("viewQuestions.html", htmlQuestion = q, htmlResponses = Comment.query.all(), currentUser = current_user.username)
    else:
        if q.count() == 0:
            return render_template("emptyClass.html")
        return render_template("viewQuestions.html", htmlQuestion = q, htmlResponses = Comment.query.all(), currentUser = "notSignedIn")

@qANDa.route("/viewCS-3", methods = ["POST", "GET"])
def viewCS3():
    q = Questions.query.filter_by(csClass = "CS-3")
    if current_user.is_authenticated:
        if q.count() == 0:
                return render_template("emptyClass.html")
        else:
            return render_template("viewQuestions.html", htmlQuestion = q, htmlResponses = Comment.query.all(), currentUser = current_user.username)
    else:
        if q.count() == 0:
            return render_template("emptyClass.html")
        return render_template("viewQuestions.html", htmlQuestion = q, htmlResponses = Comment.query.all(), currentUser = "notSignedIn")

@qANDa.route("/viewCS-4", methods = ["POST", "GET"])
def viewCS4():
    q = Questions.query.filter_by(csClass = "CS-4")
    if current_user.is_authenticated:
        if q.count() == 0:
                return render_template("emptyClass.html")
        else:
            return render_template("viewQuestions.html", htmlQuestion = q, htmlResponses = Comment.query.all(), currentUser = current_user.username)
    else:
        if q.count() == 0:
            return render_template("emptyClass.html")
        return render_template("viewQuestions.html", htmlQuestion = q, htmlResponses = Comment.query.all(), currentUser = "notSignedIn")
    
@qANDa.route("/viewAccountPost", methods = ["POST", "GET"])
def viewAccountPost():
    q = Questions.query.filter_by(posterName = current_user.username )
    if current_user.is_authenticated:
        if q.count() == 0:
                return render_template("emptyClass.html")
        else:
            return render_template("viewAccountPost.html", htmlQuestion = q, htmlResponses = Comment.query.all(), currentUser = current_user.username)
    else:
        if q.count() == 0:
            return render_template("emptyClass.html")
        return render_template("viewAccountPost.html", htmlQuestion = q, htmlResponses = Comment.query.all(), currentUser = "notSignedIn")
