from flask import Blueprint, Flask, redirect, url_for, render_template, request, session, flash

compiler = Blueprint("compiler", __name__, static_folder = "static", template_folder = "template")

@compiler.route("/compiler")
def compilerPage():
    return render_template("compiler.html")