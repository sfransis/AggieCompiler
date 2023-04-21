from flask import Blueprint, Flask, redirect, url_for, render_template, request, session, flash

# My importation libraries 
from flask_socketio import SocketIO, emit

from flask_wtf import FlaskForm
from flask_codemirror.fields import CodeMirrorField
from wtforms.fields import SubmitField


from pathlib import Path


class MyForm(FlaskForm):
    source_code = CodeMirrorField(language = "python", 
                                config = {'lineNumbers' : 'true'})
    submit = SubmitField('Submit')




compiler = Blueprint("compiler", __name__, static_folder = "static", template_folder = "template")
# this will create the route of the url
@compiler.route("/compiler", methods = ["GET", "POST"])
def compilerPage():
    form = MyForm()
    if form.validate_on_submit():
        text = form.source_code.data
    return render_template("compiler.html", form = form)