from flask import Blueprint, render_template

programVersionsBlueprint = Blueprint("programVersions", __name__, static_folder="static", template_folder="template")

@programVersionsBlueprint.route("/administrator/programversions")
def programVersions():
    return render_template("programVersions.html")

