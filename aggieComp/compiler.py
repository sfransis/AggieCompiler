from flask import Blueprint, Flask, redirect, url_for, render_template, request, session, flash, request, jsonify

# My importation libraries 
from flask_socketio import SocketIO, emit

from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess

from flask_codemirror import CodeMirror
from flask_wtf import FlaskForm
from flask_codemirror.fields import CodeMirrorField
from wtforms.fields import SubmitField
from wtforms import TextAreaField



import subprocess
import pycompile

from pathlib import Path


# class MyForm(FlaskForm):
#     source_code = CodeMirrorField(language = "python", 
#                                 config = {'lineNumbers' : 'true', 'tabsize' : 3})
#     submit = SubmitField('Submit')

# mandatory
CODEMIRROR_LANGUAGES = ['python', 'yaml', 'htmlembedded']
WTF_CSRF_ENABLED = True
SECRET_KEY = 'secret'
# optional
CODEMIRROR_THEME = '3024-night'
CODEMIRROR_ADDONS = (
        ('ADDON_DIR','ADDON_NAME'),
)

class MyForm(FlaskForm):
    source_code = CodeMirrorField(language='python', config={'lineNumbers': 'true'})
    submit = SubmitField('Submit')


def showCode():
    form = MyForm()

    if form.validate_on_submit():
        text = form.source_code.data
        code = pycompile.main(text)
        return code

    return "error"

compiler = Blueprint("compiler", __name__, static_folder = "static", template_folder = "template")
# this will create the route of the url
@compiler.route("/compiler", methods = ['POST', "GET"])
def compilerPage():
    form = MyForm()
    result = ""
    if form.validate_on_submit():
        text = form.source_code.data
        result = pycompile.main(text)
        print(result)
    return render_template('compiler.html', form = form, result = result)
    
    
    # if request.method == 'POST':
    #     data = request.form['data']
    #     return render_template('compiler.html', data = data)
    # return render_template('compiler.html')

    
    # code = request.form['code']
    # try:
    #     exec(code)
    #     return jsonify({'output': 'Success'})
    # except Exception as e:
    #     return jsonify({'output': str(e)})


    # editor = MyForm()
    # if editor.validate_on_submit():
    #     text = editor.source_code.data
    # return render_template("compiler.html", form = editor)
    
@compiler.route("/compiler/python", methods=["POST"])
def compile_code():
    code = request.json['code']
    result = subprocess.run(['python', '-c', code], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    error = result.stderr.decode('utf-8')
    return render_template('compiler.html', output=output, error=error)