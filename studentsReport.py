from flask import Blueprint, render_template, request, jsonify
import sys
import MySQLdb as mdb1

studentsReportBlueprint = Blueprint("studentsReport", __name__, static_folder="static", template_folder="template")

@studentsReportBlueprint.route("/administrator/studentsreport")
def studentsReport():
    return render_template("studentsReport.html")



