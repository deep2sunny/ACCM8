from flask import Blueprint, render_template


adminBlueprint = Blueprint("administrator", __name__, static_folder="static", template_folder="template")

@adminBlueprint.route("/administrator")
def administrator():
    return render_template("administrator.html")




