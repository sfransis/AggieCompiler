from flask import Blueprint, Flask, redirect, url_for, render_template, request, session, flash

# My importation libraries 
from PyQt6 import * 
from PyQt6.QtWidgets import * 
from PyQt6.QtCore import * 
from PyQt6.QtGui import * 
from PyQt6.Qsci import * 

from PyQt6 import QtCore, QtGui, QtWidgets

from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QMainWindow, QApplication


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