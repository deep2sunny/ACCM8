from flask import Blueprint, render_template

coursesBlueprint = Blueprint("courses", __name__, static_folder="static", template_folder="template")

@coursesBlueprint.route("/administrator/courses")
def courses():
    return render_template("courses.html")


