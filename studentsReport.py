from flask import Blueprint, render_template, request, jsonify
import sys
import MySQLdb as mdb1

studentsReportBlueprint = Blueprint("studentsReport", __name__, static_folder="static", template_folder="template")

my_objects = []

# http://localhost:5000/administrator/studentsreport
@studentsReportBlueprint.route("/administrator/studentsreport", methods=['GET','POST'])
def studentsReport():

    # re-load page when View Report button is clicked
    if request.method == 'POST' and 'program' in request.form and 'level' in request.form and 'version' in request.form:

        level = request.form['level']
        programVersion = request.form['version']
        programCode = request.form['program']


        failedStudentsRecords = readFailedStudents(level, programVersion, programCode)

        passedStudentsRecords = readPassedStudents(level, programVersion, programCode)

        programVersions = readProgramVersions()

        programs = readPrograms()

        for i in range(len(programVersions)):
            _old = programVersions[i]['pid']
            programVersions[i]['pid'] = str(_old)

        levels = ["A01", "A02", "A03", "A04"]

        showMessage = False


        if len(failedStudentsRecords) == 0 and len(passedStudentsRecords) == 0:
            showMessage = True

        return render_template("studentsReport.html", levels=levels, programs=programs, programVersions=programVersions,
                               failedStudentsRecords=failedStudentsRecords, passedStudentsRecords=passedStudentsRecords,
                               values=request.form, showMessage=showMessage)

    # this is to hand the POST request when "back to student report" button on viewFlowchart page is clicked
    elif request.method == 'POST' and 'programReport' in request.form and 'levelReport' in request.form and 'versionReport' in request.form:

        level = request.form['levelReport']
        programVersion = request.form['versionReport']
        programVersionPid = request.form['programReport']

        programCode, programName, programVersionYear = getProgramCode(programVersionPid)

        failedStudentsRecords = readFailedStudents(level, programVersion, programCode)

        passedStudentsRecords = readPassedStudents(level, programVersion, programCode)

        programVersions = readProgramVersions()

        programs = readPrograms()

        for i in range(len(programVersions)):
            _old = programVersions[i]['pid']
            programVersions[i]['pid'] = str(_old)

        levels = ["A01", "A02", "A03", "A04"]

        showMessage = False

        if len(failedStudentsRecords) == 0 and len(passedStudentsRecords) == 0:
            showMessage = True

        values = dict()
        values['level'] = level
        values['program'] = programCode
        values['version'] = programVersionYear

        return render_template("studentsReport.html", levels=levels, programs=programs, programVersions=programVersions,
                               failedStudentsRecords=failedStudentsRecords, passedStudentsRecords=passedStudentsRecords,
                               values=values, showMessage=showMessage)

    # Load page for the first time
    else:
        programVersions = readProgramVersions()

        programs = readPrograms()

        for i in range(len(programVersions)):
            _old = programVersions[i]['pid']
            programVersions[i]['pid'] = str(_old)



        levels = ["A01", "A02", "A03", "A04"]

        values = dict()
        values['level'] = "0"
        values['program'] = "0"
        values['version'] = "0"

        return render_template("studentsReport.html", levels=levels, programs=programs, programVersions=programVersions, values=values, showMessage=False)





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


def readFailedStudents(level, programVersion, programCode):
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
                
                WHERE coursemap.level = "{level}" AND grade.letter_grade = "F" AND program.program_version="{programVersion}"
                AND program.code="{programCode}" 
                
                ;    
                
            """

    cursor = con.cursor()
    cursor.execute(query)
    #rows = cursor.fetchall()

    names = [d[0] for d in cursor.description]
    failedStudentsRecords = [dict(zip(names, row)) for row in cursor.fetchall()]

    con.close()

    return failedStudentsRecords


def readPassedStudents(level, programVersion, programCode):
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

                WHERE coursemap.level = "{level}" AND grade.letter_grade != "F" AND program.program_version="{programVersion}"
                AND program.code="{programCode}" 

                ;    

            """

    cursor = con.cursor()
    cursor.execute(query)
    # rows = cursor.fetchall()

    names = [d[0] for d in cursor.description]
    passedStudentsRecords = [dict(zip(names, row)) for row in cursor.fetchall()]

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
