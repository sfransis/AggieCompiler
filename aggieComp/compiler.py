from flask import Blueprint, Flask, redirect, url_for, render_template, request, session, flash

# My importation libraries 
from flask_socketio import SocketIO, emit

from pathlib import Path


beta = Flask(__name__)
beta.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(beta)

compiler = Blueprint("compiler", __name__, static_folder = "static", template_folder = "template")
# this will create the route of the url
@compiler.route("/compiler")
def compilerPage():
    return render_template("compiler.html")