from flask import Blueprint, render_template, request, jsonify
import sys
import MySQLdb as mdb1

studentsReportBlueprint = Blueprint("studentsReport", __name__, static_folder="static", template_folder="template")

my_objects = []

@studentsReportBlueprint.route("/administrator/studentsreport", methods=['GET','POST'])
def studentsReport():

    if request.method == 'POST' and 'program' in request.form and 'level' in request.form and 'version' in request.form:

        level = request.form['level']
        programVersionID = request.form['version']
        programCode = request.form['program']

        # the value in the DB is an int
        # request.form['version'] = 20

        print(level+"-"+programVersionID+"-"+programCode)

        failedStudentsRecords = readFailedStudents(level, programVersionID)

        passedStudentsRecords = readPassedStudents(level, programVersionID)

        programVersions = readProgramVersions()

        programs = readPrograms()

        for i in range(len(programVersions)):
            _old = programVersions[i]['pid']
            programVersions[i]['pid'] = str(_old)

        levels = ["A01", "A02", "A03", "A04"]

        print(request.form)

        return render_template("studentsReport.html", levels=levels, programs=programs, programVersions=programVersions,
                               failedStudentsRecords=failedStudentsRecords, passedStudentsRecords=passedStudentsRecords,
                               values=request.form)

    else:
        programVersions = readProgramVersions()

        programs = readPrograms()

        for i in range(len(programVersions)):
            _old = programVersions[i]['pid']
            programVersions[i]['pid'] = str(_old)


        print(programVersions)

        levels = ["A01", "A02", "A03", "A04"]

        values = dict()
        values['level'] = "0"
        values['program'] = "0"
        values['version'] = "0"

        return render_template("studentsReport.html", levels=levels, programs=programs, programVersions=programVersions, values=values)





@studentsReportBlueprint.route("/administrator/studentsreport/generatereport", methods=["POST", "GET"])
def viewStudentsReport():
    if request.method == "POST":

        programCode = request.json['programCode']

        level = "A03"
        programVersionID = "20"

        failedStudentsRecords = readFailedStudents(level, programVersionID)

        passedStudentsRecords = readPassedStudents(level, programVersionID)

        programVersions = readProgramVersions()

        programs = readPrograms()

        levels = ["A01", "A02", "A03", "A04"]

        return jsonify(status="1", message="Program was successfully deleted")



def createCursor():
    try:
        con = mdb1.connect(host='localhost', user='root', password='5Iodine3', database='accm', port=3306)


    except mdb1.Error as e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
        sys.exit(1)

    return con



def readProgramVersions():
    con = createCursor()
    query = f"""SELECT * FROM accm.program;"""

    cursor = con.cursor()
    cursor.execute(query)

    names = [d[0] for d in cursor.description]
    programVersions = [dict(zip(names, row)) for row in cursor.fetchall()]

    con.close()

    return programVersions


def readPrograms():
    con = createCursor()
    query = f"""SELECT * FROM accm.program_offered;"""

    cursor = con.cursor()
    cursor.execute(query)

    names = [d[0] for d in cursor.description]
    programs = [dict(zip(names, row)) for row in cursor.fetchall()]

    con.close()

    return programs


def readFailedStudents(level, programVersionID):
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
                
                WHERE coursemap.level = "{level}" AND grade.letter_grade = "F" AND program.pid="{programVersionID}"
                
                ;    
                
            """

    cursor = con.cursor()
    cursor.execute(query)
    #rows = cursor.fetchall()

    names = [d[0] for d in cursor.description]
    failedStudentsRecords = [dict(zip(names, row)) for row in cursor.fetchall()]

    con.close()

    return failedStudentsRecords


def readPassedStudents(level, programVersion):
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

                WHERE coursemap.level = "{level}" AND grade.letter_grade != "F" AND program.pid="{programVersion}"

                ;    

            """

    cursor = con.cursor()
    cursor.execute(query)
    # rows = cursor.fetchall()

    names = [d[0] for d in cursor.description]
    passedStudentsRecords = [dict(zip(names, row)) for row in cursor.fetchall()]

    con.close()

    return passedStudentsRecords


