from flask import Blueprint, Flask, redirect, url_for, render_template, request, session, flash

# My importation libraries 
from flask_socketio import SocketIO, emit

from flask_wtf import FlaskForm
from flask_codemirror.fields import CodeMirrorField
from wtforms.fields import SubmitField



from pathlib import Path


# class MyForm(FlaskForm):
#     source_code = CodeMirrorField(language = "python", 
#                                 config = {'lineNumbers' : 'true', 'tabsize' : 3})
#     submit = SubmitField('Submit')




compiler = Blueprint("compiler", __name__, static_folder = "static", template_folder = "template")
# this will create the route of the url
@compiler.route("/compiler", methods = ['GET', 'POST'])
def compilerPage():
    if request.method == 'POST':
        data = request.form['data']
        return render_template('compiler.html', data = data)
    return render_template('compiler.html')
    # editor = MyForm()
    # if editor.validate_on_submit():
    #     text = editor.source_code.data
    # return render_template("compiler.html", form = editor)