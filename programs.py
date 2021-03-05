from flask import Blueprint, render_template, request, jsonify
import sys
import MySQLdb as mdb1

programsBlueprint = Blueprint("programs", __name__, static_folder="static", template_folder="template")


@programsBlueprint.route("/administrator/programs")
def programs():

    rows = readAllProgramsOffered()
    codes, names= seperateProgramData(rows)

    return render_template("programs.html",codes=codes, names=names)



@programsBlueprint.route("/administrator/programs/createProgram", methods=["POST", "GET"])
def createProgram():

    if request.method == "POST":

        programCode = request.form["programCode"]
        programName = request.form["programName"]

        if checkIfProgramOfferedExists(programCode):
            return jsonify(status="0", message="The specified program already exists")

        createProgramOfferingQuery(programCode, programName)

        return jsonify(status="1", message="Successfully added new program")


@programsBlueprint.route("/administrator/programs/deleteProgram", methods=["POST", "GET"])
def deleteProgram():
    if request.method == "POST":

        programCode = request.json['programCode']

        programVersionsExist = checkIfProgramVersionsExistQuery(programCode)

        if programVersionsExist:
            return jsonify(status="0", message="The Program has other data associated with it, it cannot be removed on this page")

        deleteProgramOfferedQuery(programCode)

        return jsonify(status="1", message="Program was successfully deleted")


@programsBlueprint.route("/administrator/programs/updateProgram", methods=["POST", "GET"])
def updateProgram():
    if request.method == "POST":

        programCode = request.json['programCode']
        programName = request.json['programName']
        oldProgramCode = request.json['oldProgramCode']

        programVersionsExist = checkIfProgramVersionsExistQuery(oldProgramCode)

        if programVersionsExist:
            return jsonify(status="0", message="The Program has multiple year versions, it's information cannot be updated at this point")

        updateProgramInfoQuery(programCode, programName)

        return jsonify(status="1", message="Program was successfully updated")





def createCursor():
    try:
        con = mdb1.connect(host='localhost', user='root', password='5Iodine3', database='accm', port=3306)


    except mdb1.Error as e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
        sys.exit(1)

    return con


def seperateProgramData(rows):
    codes = []
    names = []

    for i in range(len(rows)):
        codes.append(rows[i][0])
        names.append(rows[i][1])

    return codes, names



def createProgramOfferingQuery(programCode, programName):

    con = createCursor()
    cursor = con.cursor()
    query = f"""INSERT INTO program_offered(program_code, program_name) 
            VALUES('{programCode}','{programName}');"""

    cursor.execute(query)
    con.commit()
    con.close()


def updateProgramInfoQuery(programCode, programName):
    con = createCursor()
    query = f""" 
            UPDATE program_offered 
            SET program_code = '{programCode}', program_name = '{programName}'
            WHERE program_code = '{programCode}';
            """
    cursor = con.cursor()
    cursor.execute(query)
    con.commit()
    con.close()


def deleteProgramOfferedQuery(programCode):
    con = createCursor()
    query = f"DELETE FROM program_offered WHERE program_code = '{programCode}' ;"
    cursor = con.cursor()
    cursor.execute(query)
    con.commit()
    con.close()


def readAllProgramsOffered():
    con = createCursor()
    query = f"SELECT * FROM program_offered;"
    cursor = con.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    con.close()
    return rows


def checkIfProgramVersionsExistQuery(programCode):
    con = createCursor()
    query = f"SELECT COUNT(*) FROM program WHERE code = '{programCode}';"
    cursor = con.cursor()
    cursor.execute(query)
    rowCount = cursor.fetchone()
    count = rowCount[0]
    con.close()

    if count > 0:
        return True

    return False



def checkIfProgramOfferedExists(programCode):

    con = createCursor()
    query = f"SELECT COUNT(*) FROM program_offered WHERE program_code='{programCode}';"
    cursor = con.cursor()
    cursor.execute(query)
    rowCount = cursor.fetchone()
    count = rowCount[0]
    con.close()


    if count == 1:
        return True

    return False


