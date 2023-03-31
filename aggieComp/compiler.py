from flask import Blueprint, Flask, redirect, url_for, render_template, request, session, flash

# My importation libraries 
from PyQt6 import * 
from PyQt6.QtWidgets import * 
from PyQt6.QtCore import * 
from PyQt6.QtGui import * 
from PyQt6.Qsci import * 

from pathlib import Path

import sys 
import os

from PyQt6 import QtCore, QtGui, QtWidgets






compiler = Blueprint("compiler", __name__, static_folder = "static", template_folder = "template")

# this will create the route of the url 
@compiler.route("/compiler")
def compilerPage():
    
    return render_template("compiler.html")