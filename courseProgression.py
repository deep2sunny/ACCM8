from flask import Blueprint, render_template, request, session, redirect, url_for
import sys
import MySQLdb as mdb1
import copy
import configparser
import os

courseProgressionBlueprint = Blueprint("courseProgression", __name__, static_folder="static", template_folder="template")


# http://localhost:5000/administrator/courseprogression
@courseProgressionBlueprint.route("/administrator/courseprogression", methods=['GET','POST'])
def courseProgression():


    # check if user is logged in
    if 'loggedin' in session:

        # check if user is coordinator or secretary
        if session['category'] == "coordinator" or session['category'] == "secretary":

            parameters = request.form.to_dict()
            _list = list(parameters.keys())

            buttonType = checkButtonType(parameters)

            allCoreCourses = createCoreCourseDataDict()

            largestSize = 0

            for course in allCoreCourses:
                if len(course['prerequisites']) > largestSize:
                    largestSize = len(course['prerequisites'])

            prerequisite_col = ['prerequisite_1', 'prerequisite_2', 'prerequisite_3', 'prerequisite_4',
                            'prerequisite_5']

            # user adds new course progression
            if request.method == 'POST' and buttonType == "addBtn":


                prerequisite_name = ['prereqCode1', 'prereqCode2', 'prereqCode3', 'prereqCode4', 'prereqCode5']

                sequence = parameters['sequence'].upper().strip()

                courseCode = parameters['courseCode'].upper().strip()

                prerequisites = []

                if not RepresentsInt(sequence):
                    message = "The sequence number " + sequence + " must be a valid integer"
                    return render_template("courseProgression.html", allCoreCourses=allCoreCourses, largestSize=largestSize,
                                           message=message, success=False, failure=True, values=request.form)

                for col in prerequisite_name:
                    if parameters[col].upper().strip():
                        prerequisites.append(parameters[col].upper().strip())


                if checkCoreCourseExistence(courseCode) == False:
                    message = "The course code " + courseCode + " provided isn't a core course"
                    return render_template("courseProgression.html", allCoreCourses=allCoreCourses, largestSize=largestSize,
                                           message=message, success=False, failure=True, values=request.form)

                if checkCoreCourseFlowchart(courseCode) == True:
                    message = "The course code " + courseCode + " is already in the sequence"
                    return render_template("courseProgression.html", allCoreCourses=allCoreCourses,
                                           largestSize=largestSize,
                                           message=message, success=False, failure=True, values=request.form)


                CoreCourseCheckPass = False

                # check if the prerequisites are core courses
                for prereq in prerequisites:
                    if prereq:

                        if checkCoreCourseExistence(prereq) == False:
                            message = "The prerequisite " + prereq + " course code provided doesn't exist"
                            return render_template("courseProgression.html", allCoreCourses=allCoreCourses,
                                                   largestSize=largestSize,
                                                   message=message, success=False, failure=True, values=request.form)
                        else:
                            CoreCourseCheckPass = True

                if CoreCourseCheckPass is True:
                    # check if prerequisites are already in the sequence
                    for prereq in prerequisites:
                        if prereq:
                            if checkCoreCourseFlowchart(prereq) == False:
                                message = "The prerequisite code " + prereq + " needs to first be added in the sequence"
                                return render_template("courseProgression.html", allCoreCourses=allCoreCourses,
                                                       largestSize=largestSize,
                                                       message=message, success=False, failure=True, values=request.form)



                addIntoFlowchart(courseCode, sequence)


                for prereq in prerequisites:
                    if prereq:
                        addIntoPrerequisite(courseCode, prereq)


                allCoreCourses = createCoreCourseDataDict()

                largestSize = 0

                for course in allCoreCourses:
                    if len(course['prerequisites']) > largestSize:
                        largestSize = len(course['prerequisites'])

                message = "The course progression was added successfully"
                return render_template("courseProgression.html", allCoreCourses=allCoreCourses,
                                       largestSize=largestSize,
                                       message=message, success=True, failure=False, values=dict())

            # user confirms edit to course progression
            if request.method == 'POST' and "confirmEditBtn" in parameters:

                courseCode = parameters['courseCode'].upper().strip()
                oldCourseCode = parameters['oldCourseCode'].upper().strip()

                oldPrerequisites = []

                oldCourse = dict()

                for course in allCoreCourses:
                    if course['core_course_num'] == oldCourseCode:
                        oldCourse = copy.deepcopy(course)

                for i in range(len(oldCourse['prerequisites'])):
                    oldPrerequisites.append(oldCourse['prerequisites'][i])

                prerequisites = []

                for col in prerequisite_col:
                    if parameters[col].upper().strip():
                        prerequisites.append(parameters[col].upper().strip())

                if checkCoreCourseExistence(courseCode) == False:
                    message = "The course code " + courseCode + " provided isn't a core course"
                    return render_template("courseProgression.html", allCoreCourses=allCoreCourses, largestSize=largestSize,
                                           message=message, success=False, failure=True, values=request.form, updatedCourse=courseCode, rowClass="errorRow")

                if checkCoreCourseFlowchart(courseCode) == True and courseCode != oldCourseCode:
                    message = "The course code " + courseCode + " is already in the sequence"
                    return render_template("courseProgression.html", allCoreCourses=allCoreCourses,
                                           largestSize=largestSize,
                                           message=message, success=False, failure=True, values=request.form, updatedCourse=courseCode, rowClass="errorRow")


                if checkIfPrerequisite(courseCode) == True:
                    message = "This course code " + courseCode + " cannot be edited as it's used as a prerequisite for another course"
                    return render_template("courseProgression.html", allCoreCourses=allCoreCourses,
                                           largestSize=largestSize,
                                           message=message, success=False, failure=True, values=dict(), updatedCourse=courseCode, rowClass="errorRow")

                # check if the prerequisites are core courses
                for prereq in prerequisites:
                    if prereq:

                        if checkCoreCourseExistence(prereq) == False:
                            message = "The prerequisite " + prereq + " isn't a valid core course code. Please re-check the course code."
                            return render_template("courseProgression.html", allCoreCourses=allCoreCourses,
                                                   largestSize=largestSize,
                                                   message=message, success=False, failure=True, values=request.form, updatedCourse=courseCode, rowClass="errorRow")


                # Delete all existing prerequisites for the course
                if len(oldPrerequisites) > 0:
                    for prereq in oldPrerequisites:
                        if prereq:
                            deletePrerequisite(courseCode, prereq)

                # Add new set of prerequisites for the course
                if len(prerequisites) > 0:
                    for prereq in prerequisites:
                        if prereq:
                            addIntoPrerequisite(courseCode, prereq)

                allCoreCourses = createCoreCourseDataDict()

                largestSize = 0

                for course in allCoreCourses:
                    if len(course['prerequisites']) > largestSize:
                        largestSize = len(course['prerequisites'])


                message = "The course progression was successfully updated"
                return render_template("courseProgression.html", allCoreCourses=allCoreCourses,
                                       largestSize=largestSize,
                                       message=message, success=True, failure=False, values=dict(), updatedCourse=courseCode, rowClass="updatedRow")

            # user confirms deletion of course progression
            if request.method == 'POST' and "confirmDeleteBtn" in parameters:


                courseCode = parameters['courseDeleteInput'].upper().strip()

                if checkIfPrerequisite(courseCode) == True:
                    message = "This course code " + courseCode + " cannot be edited as it's used as a prerequisite for another course"
                    return render_template("courseProgression.html", allCoreCourses=allCoreCourses,
                                           largestSize=largestSize,
                                           message=message, success=False, failure=True, values=dict(), updatedCourse=courseCode, rowClass="errorRow")

                prerequisites = []

                for col in prerequisite_col:
                    if parameters[col].upper().strip():
                        prerequisites.append(parameters[col].upper().strip())


                _sequenceNumber = findCourseSequenceNumber(courseCode)


                if len(prerequisites) > 0:
                    for prereq in prerequisites:
                        if prereq:
                            deleteFlowchart(courseCode)
                            deletePrerequisite(courseCode, prereq)
                else:
                    deleteFlowchart(courseCode)


                allCoreCourses = createCoreCourseDataDict()

                largestSize = 0

                for course in allCoreCourses:
                    if len(course['prerequisites']) > largestSize:
                        largestSize = len(course['prerequisites'])


                message = "The course progression was successfully deleted"
                return render_template("courseProgression.html", allCoreCourses=allCoreCourses,
                                       largestSize=largestSize,
                                       message=message, success=True, failure=False, values=dict())



            return render_template("courseProgression.html", allCoreCourses=allCoreCourses, largestSize=largestSize, message="", success=False, failure=False, values=dict())

        else:
            return redirect(url_for('home'))

    else:
        return redirect(url_for('login'))


def checkButtonType(dict):
    allKeys = list(dict.keys())

    for key in allKeys:

        if "deleteBtn" in key:
            return "deleteBtn"
        if "saveBtn" in key:
            return "saveBtn"
        if "addBtn" in key:
            return "addBtn"

    return ""


def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

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



# Creates a dictionary containing course, sequence and prerequisite information
def createCoreCourseDataDict():
    # >>> Setup MySQL Connection
    con = createConnection()
    cursor = con.cursor()

    # >>> fetch all core courses
    query = f"""SELECT * FROM core_course_flowchart 
                left join core_course using (core_course_num)
                order by sequence
                ;"""
    cursor.execute(query)
    rows = cursor.fetchall()

    # Write all query rows into dictionary with column headers
    names = [d[0] for d in cursor.description]
    allCoreCourses = [dict(zip(names, row)) for row in rows]

    for course in allCoreCourses:
        # Create new columns

        course['prerequisites'] = []


        # fetch prerequisites for the course
        query = f"""
                SELECT * FROM core_course_prerequisites                
                where core_course_num = '{course['core_course_num']}'
                ;
                """
        cursor.execute(query)
        rows = cursor.fetchall()

        # Write all query rows into dictionary with column headers
        names = [d[0] for d in cursor.description]
        coursePrerequisites = [dict(zip(names, row)) for row in rows]

        prerequisites = []

        if len(coursePrerequisites) > 0:
            # go through the dictionary of queried prerequisites
            for singlePrerequisite in coursePrerequisites:
                prerequisites.append(singlePrerequisite['prerequisite_num'])

        for index in range(0,5):
            if 0 <= index < len(prerequisites):
                course['prerequisites'].append(prerequisites[index])

    cursor.close()
    con.close()

    return allCoreCourses



def checkCoreCourseExistence(courseCode):

    # >>> Setup MySQL Connection
    con = createConnection()


    query = f"""

                    SELECT count(*) FROM core_course
                    where core_course_num = '{courseCode}';

                """

    cursor = con.cursor()
    cursor.execute(query)
    rowCount = cursor.fetchone()
    count = rowCount[0]

    cursor.close()
    con.close()

    if count > 0:
        return True

    return False


def checkCoreCourseFlowchart(courseCode):
    # >>> Setup MySQL Connection
    con = createConnection()

    query = f"""

                        SELECT count(*) FROM core_course_flowchart
                        where core_course_num = '{courseCode}';

                    """

    cursor = con.cursor()
    cursor.execute(query)
    rowCount = cursor.fetchone()
    count = rowCount[0]
    cursor.close()
    con.close()

    if count > 0:
        return True

    return False


def addIntoFlowchart(courseCode, sequence):
    # >>> Setup MySQL Connection
    con = createConnection()

    query = f"""

            insert into core_course_flowchart(core_course_num, sequence) values('{courseCode}', {sequence})

            """

    cursor = con.cursor()
    cursor.execute(query)
    con.commit()
    cursor.close()
    con.close()



def addIntoPrerequisite(courseCode, prereqCode):
    # >>> Setup MySQL Connection
    con = createConnection()

    query = f"""

            insert into core_course_prerequisites(core_course_num, prerequisite_num)
            values ('{courseCode}','{prereqCode}')
            ;

            """

    cursor = con.cursor()
    cursor.execute(query)
    con.commit()
    cursor.close()
    con.close()



def checkIfPrerequisite(courseCode):
    con = createConnection()
    query = f"""
                    SELECT count(*) FROM core_course_prerequisites WHERE prerequisite_num='{courseCode}';
                """

    cursor = con.cursor()
    cursor.execute(query)
    rowCount = cursor.fetchone()
    count = rowCount[0]
    cursor.close()
    con.close()

    if count > 0:
        return True

    return False


def deletePrerequisite(courseCode,prerequisite):
    con = createConnection()

    query = f""" 
            DELETE FROM core_course_prerequisites 
            WHERE core_course_num='{courseCode}' 
            AND prerequisite_num='{prerequisite}'
            """
    cursor = con.cursor()
    cursor.execute(query)
    con.commit()
    cursor.close()
    con.close()


def deleteFlowchart(courseCode):
    con = createConnection()

    query = f""" 
                DELETE FROM core_course_flowchart 
                WHERE core_course_num='{courseCode}' 
                """
    cursor = con.cursor()
    cursor.execute(query)
    con.commit()
    cursor.close()
    con.close()

def findCourseSequenceNumber(courseCode):
    con = createConnection()
    query = f"""
                SELECT sequence FROM core_course_flowchart
                WHERE core_course_num = "{courseCode}"
                ;
            """

    cursor = con.cursor()
    cursor.execute(query)
    row = cursor.fetchone()
    sequence = row[0]
    cursor.close()
    con.close()

    return sequence

def checkIfSequenceExists(sequence):
    con = createConnection()
    query = f"""
                        SELECT count(*) FROM core_course_flowchart WHERE sequence='{sequence}';
                    """

    cursor = con.cursor()
    cursor.execute(query)
    rowCount = cursor.fetchone()
    count = rowCount[0]
    cursor.close()
    con.close()

    if count > 0:
        return True

    return False



def updatePrerequisite(courseCode, prerequisite):
    con = createConnection()

    query = f"""
                UPDATE core_course_prerequisites
                SET prerequisite_num = '{prerequisite}' 
                WHERE core_course_num = '{courseCode}';
            """

    cursor = con.cursor()
    cursor.execute(query)
    con.commit()
    cursor.close()
    con.close()


def deletePrerequisites(courseCode):
    con = createConnection()

    query = f"""
                DELETE FROM core_course_prerequisites
                WHERE core_course_num = '{courseCode}';
            """

    cursor = con.cursor()
    cursor.execute(query)
    con.commit()
    cursor.close()
    con.close()

