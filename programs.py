from flask import Blueprint, render_template

programsBlueprint = Blueprint("programs", __name__, static_folder="static", template_folder="template")

@programsBlueprint.route("/administrator/programs")
def programs():
    return render_template("programs.html")