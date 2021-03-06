from flask import Blueprint, render_template
import sys
import MySQLdb as mdb1

programVersionsBlueprint = Blueprint("programVersions", __name__, static_folder="static", template_folder="template")

@programVersionsBlueprint.route("/administrator/programversions")
def programVersions():

    return render_template("programVersions.html")


