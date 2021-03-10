from flask import Blueprint, render_template

courseProgressionBlueprint = Blueprint("courseProgression", __name__, static_folder="static", template_folder="template")

@courseProgressionBlueprint.route("/administrator/courseprogression")
def courses():
    return render_template("courseProgression.html")

