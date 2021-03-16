from flask import Blueprint, render_template, request, session, redirect, url_for
import sys
import MySQLdb as mdb1
import configparser
import os

studentsReportBlueprint = Blueprint("studentsReport", __name__, static_folder="static", template_folder="template")


# http://localhost:5000/administrator/studentsreport
@studentsReportBlueprint.route("/administrator/studentsreport", methods=['GET','POST'])
def studentsReport():
    x = 5

    # check if user is logged in
    if 'loggedin' in session:
    # if x == 5:
        levels = ["A01", "A02", "A03", "A04"]
        programPid = "20"

        # re-load page when View Report button is clicked
        if request.method == 'POST' and 'level' in request.form:

            level = request.form['level']

            showMessage = False

            failedStudentsRecords = readFailedStudents(level, programPid)

            passedStudentsRecords = readPassedStudents(level, programPid)

            if len(failedStudentsRecords) == 0 and len(passedStudentsRecords) == 0 and level != "0":
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

    else:
        return redirect(url_for('login'))



def createConnection():

    config = configparser.ConfigParser()
    config.read(os.path.dirname(os.path.abspath(__file__)) + '/static/mysql-config.ini')


    try:
        con = mdb1.connect(
                            host=config['DEFAULT']['MYSQL_HOST'],
                            user=config['DEFAULT']['MYSQL_USER'],
                            password=config['DEFAULT']['MYSQL_PASSWORD'],
                            database=config['DEFAULT']['MYSQL_DB'],
                            port=int(config['DEFAULT']['MYSQL_PORT']),
                           )

    except mdb1.Error as e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
        sys.exit(1)

    return con



def readFailedStudents(level, programPid):
    con = createConnection()
    cursor = con.cursor()
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

    cursor.execute(query)
    rows = cursor.fetchall()

    names = [d[0] for d in cursor.description]
    failedStudentsRecords = [dict(zip(names, row)) for row in rows]

    con.close()

    return failedStudentsRecords


def readPassedStudents(level, programPid):
    con = createConnection()
    cursor = con.cursor()

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

    cursor.execute(query)
    rows = cursor.fetchall()

    names = [d[0] for d in cursor.description]
    passedStudentsRecords = [dict(zip(names, row)) for row in rows]

    con.close()
    return passedStudentsRecords


def getProgramCode(programVersionId):
    con = createConnection()
    cursor = con.cursor()
    query = f"""

                    SELECT program.code, program.name, program.program_version
                    
                    FROM accm.program

                    where program.pid="{programVersionId}"
                    
                    ;

                    ;    

                """


    cursor.execute(query)
    rows = cursor.fetchall()
    programCode = rows[0][0]
    programName = rows[0][1]
    programVersionYear = rows[0][2]

    con.close()

    return programCode, programName, programVersionYear
