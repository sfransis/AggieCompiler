from flask import Blueprint, Flask, redirect, url_for, render_template, request, session, flash

roadmap = Blueprint("roadmap", __name__, static_folder = "static", template_folder = "template")

@roadmap.route("/roadmap")
def roadmapPage():
    return render_template("roadmap.html")