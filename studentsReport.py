from flask import Blueprint, render_template, request, session, redirect, url_for
import sys
import MySQLdb as mdb1
import configparser
import os

studentsReportBlueprint = Blueprint("studentsReport", __name__, static_folder="static", template_folder="template")


# http://localhost:5000/administrator/studentsreport
@studentsReportBlueprint.route("/administrator/studentsreport", methods=['GET','POST'])
def studentsReport():

    # check if user is logged in
    if 'loggedin' in session:

        # check if user is coordinator or secretary
        if session['category'] == "coordinator" or session['category'] == "secretary":

            levels = ["A01", "A02", "A03", "A04"]

            # re-load page when View Report button is clicked
            if request.method == 'POST' and 'level' in request.form:

                level = request.form['level']

                showMessage = False

                failedStudentsRecords = readFailedStudents(level)

                passedStudentsRecords = readPassedStudents(level)

                if len(failedStudentsRecords) == 0 and len(passedStudentsRecords) == 0 and level != "0":
                    showMessage = True

                return render_template("studentsReport.html", levels=levels,
                                       failedStudentsRecords=failedStudentsRecords, passedStudentsRecords=passedStudentsRecords,
                                       values=request.form, showMessage=showMessage, currentLevel=level)


            # this is to handle the POST request when "back to student report" button on viewFlowchart page is clicked
            elif request.method == 'POST' and 'levelReport' in request.form:

                level = request.form['levelReport']

                failedStudentsRecords = readFailedStudents(level)

                passedStudentsRecords = readPassedStudents(level)

                showMessage = False

                if len(failedStudentsRecords) == 0 and len(passedStudentsRecords) == 0:
                    showMessage = True

                values = dict()
                values['level'] = level



                return render_template("studentsReport.html", levels=levels,
                                       failedStudentsRecords=failedStudentsRecords, passedStudentsRecords=passedStudentsRecords,
                                       values=values, showMessage=showMessage, currentLevel=level)

            # Load page for the first time
            else:

                values = dict()
                values['level'] = ""



                return render_template("studentsReport.html", levels=levels, values=values, showMessage=False)

        else:
            return redirect(url_for('home'))

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



def readFailedStudents(level):
    con = createConnection()
    cursor = con.cursor()
    query = f"""
    
                SELECT 
                distinct student.student_num, student.sid, student.fname, student.lname, program.pid,
                program.program_version,coursemap.`level`,
                coursemap.mapid
                FROM student
                INNER JOIN grade ON student.sid = grade.sid
                INNER JOIN coursemap ON grade.mapid = coursemap.mapid
                INNER JOIN course ON coursemap.cid = course.cid
                INNER JOIN program ON coursemap.pid = program.pid
                INNER JOIN prerequisite ON coursemap.mapid = prerequisite.prerequisite
                WHERE coursemap.level = "{level}" AND grade.letter_grade = "F"                 
                ;    
                
            """

    cursor.execute(query)
    rows = cursor.fetchall()

    names = [d[0] for d in cursor.description]
    failedStudentsRecords = [dict(zip(names, row)) for row in rows]

    con.close()

    return failedStudentsRecords


def readPassedStudents(level):
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

                WHERE coursemap.level = "{level}" AND grade.letter_grade != "F" 
                

                ;    

            """

    cursor.execute(query)
    rows = cursor.fetchall()

    names = [d[0] for d in cursor.description]
    passedStudentsRecords = [dict(zip(names, row)) for row in rows]

    con.close()
    return passedStudentsRecords


