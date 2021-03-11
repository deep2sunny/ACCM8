from flask import Blueprint, render_template, request, jsonify, current_app
import sys
import MySQLdb as mdb1
from flask_mysqldb import MySQL
from app import app

studentsReportBlueprint = Blueprint("studentsReport", __name__, static_folder="static", template_folder="template")


# http://localhost:5000/administrator/studentsreport
@studentsReportBlueprint.route("/administrator/studentsreport", methods=['GET','POST'])
def studentsReport():

    levels = ["A01", "A02", "A03", "A04"]
    programPid = "20"

    # re-load page when View Report button is clicked
    if request.method == 'POST' and 'level' in request.form:

        level = request.form['level']

        failedStudentsRecords = readFailedStudents(level, programPid)

        passedStudentsRecords = readPassedStudents(level, programPid)

        showMessage = False

        if len(failedStudentsRecords) == 0 and len(passedStudentsRecords) == 0:
            showMessage = True

        return render_template("studentsReport.html", levels=levels,
                               failedStudentsRecords=failedStudentsRecords, passedStudentsRecords=passedStudentsRecords,
                               values=request.form, showMessage=showMessage)


    # this is to hand the POST request when "back to student report" button on viewFlowchart page is clicked
    elif request.method == 'POST' and 'levelReport' in request.form:

        level = request.form['levelReport']

        failedStudentsRecords = readFailedStudents(level, programPid)

        passedStudentsRecords = readPassedStudents(level, programPid)

        showMessage = False

        if len(failedStudentsRecords) == 0 and len(passedStudentsRecords) == 0:
            showMessage = True

        values = dict()
        values['level'] = level

        return render_template("studentsReport.html", levels=levels,
                               failedStudentsRecords=failedStudentsRecords, passedStudentsRecords=passedStudentsRecords,
                               values=values, showMessage=showMessage)

    # Load page for the first time
    else:

        values = dict()
        values['level'] = "0"

        return render_template("studentsReport.html", levels=levels, values=values, showMessage=False)



def createCursor():
    mysql = MySQL(app)

    try:
        con = mdb1.connect(host=mysql.app.config['MYSQL_HOST'],
                           user=mysql.app.config['MYSQL_USER'],
                           password=mysql.app.config['MYSQL_PASSWORD'],
                           database=mysql.app.config['MYSQL_DB'],
                           port=mysql.app.config['MYSQL_PORT'])


    except mdb1.Error as e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
        sys.exit(1)

    return con



def readFailedStudents(level, programPid):

    con = createCursor()
    query = f"""
    
                SELECT 
                distinct student.student_num, student.sid, student.fname, student.lname, program.pid,
                program.program_version,coursemap.level
                FROM student
                INNER JOIN grade ON student.sid = grade.sid
                INNER JOIN coursemap ON grade.mapid = coursemap.mapid
                INNER JOIN course ON coursemap.cid = course.cid
                INNER JOIN program ON coursemap.pid = program.pid
                
                WHERE coursemap.level = "{level}" AND grade.letter_grade = "F" AND program.pid="{programPid}"
                
                
                ;    
                
            """


    cursor = con.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()

    names = [d[0] for d in cursor.description]
    failedStudentsRecords = [dict(zip(names, row)) for row in rows]

    con.close()

    return failedStudentsRecords


def readPassedStudents(level, programPid):
    con = createCursor()
    query = f"""

                SELECT 
                distinct student.student_num, student.sid, student.fname, student.lname, program.pid,
                program.program_version,coursemap.level
                FROM student
                INNER JOIN grade ON student.sid = grade.sid
                INNER JOIN coursemap ON grade.mapid = coursemap.mapid
                INNER JOIN course ON coursemap.cid = course.cid
                INNER JOIN program ON coursemap.pid = program.pid

                WHERE coursemap.level = "{level}" AND grade.letter_grade != "F" AND program.pid="{programPid}"
                

                ;    

            """

    cursor = con.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()

    names = [d[0] for d in cursor.description]
    passedStudentsRecords = [dict(zip(names, row)) for row in rows]

    con.close()

    return passedStudentsRecords


def getProgramCode(programVersionId):
    con = createCursor()
    query = f"""

                    SELECT program.code, program.name, program.program_version
                    
                    FROM accm.program

                    where program.pid="{programVersionId}"
                    
                    ;

                    ;    

                """

    cursor = con.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    programCode = rows[0][0]
    programName = rows[0][1]
    programVersionYear = rows[0][2]

    return programCode, programName, programVersionYear
