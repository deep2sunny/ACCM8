from flask import Blueprint, render_template, request, session, redirect, url_for
import sys
import MySQLdb as mdb1
import copy
import configparser
import os

courseProgressionBlueprint = Blueprint("courseProgression", __name__, static_folder="static", template_folder="template")


@courseProgressionBlueprint.route("/administrator/courseprogression", methods=['GET','POST'])
def courseProgression():

    x=5

    # check if user is logged in
    if 'loggedin' in session:
    #if x == 5:

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

        if request.method == 'POST' and buttonType == "addBtn":

            print("clicked add button")

            sequence = parameters['sequence'].upper()
            courseCode = parameters['courseCode'].upper()
            prereqCode1 = parameters['prereqCode1'].upper()
            prereqCode2 = parameters['prereqCode2'].upper()
            prereqCode3 = parameters['prereqCode3'].upper()
            prereqCode4 = parameters['prereqCode4'].upper()
            prereqCode5 = parameters['prereqCode5'].upper()

            prerequisite_name = ['prereqCode1', 'prereqCode2', 'prereqCode3', 'prereqCode4', 'prereqCode5']

            prerequisites = []

            if not RepresentsInt(sequence):
                message = "The sequence number must be a valid integer"
                return render_template("courseProgression.html", allCoreCourses=allCoreCourses, largestSize=largestSize,
                                       message=message, success=False, failure=True, values=request.form)

            for col in prerequisite_name:
                if parameters[col].upper():
                    prerequisites.append(parameters[col].upper())

            print(parameters)

            if checkIfSequenceExists(sequence):
                message = "The sequence number is already taken, please use a different number"
                return render_template("courseProgression.html", allCoreCourses=allCoreCourses, largestSize=largestSize,
                                       message=message, success=False, failure=True, values=request.form)

            highestSequence = findHighestSequence()
            sequence_int = int(sequence)

            if sequence_int <= highestSequence:
                message = "The sequence number provided must be greater than the existing course progression sequences"
                return render_template("courseProgression.html", allCoreCourses=allCoreCourses, largestSize=largestSize,
                                       message=message, success=False, failure=True, values=request.form)

            if checkCoreCourseExistence(courseCode) == False:
                message = "The course code provided isn't a core course"
                return render_template("courseProgression.html", allCoreCourses=allCoreCourses, largestSize=largestSize,
                                       message=message, success=False, failure=True, values=request.form)

            if checkCoreCourseFlowchart(courseCode) == True:
                message = "The course code is already in the sequence"
                return render_template("courseProgression.html", allCoreCourses=allCoreCourses,
                                       largestSize=largestSize,
                                       message=message, success=False, failure=True, values=request.form)

            prerequisites = [prereqCode1, prereqCode2, prereqCode3, prereqCode4, prereqCode5]

            CoreCourseCheckPass = False

            # check if the prerequisites are core courses
            for prereq in prerequisites:
                if prereq:

                    if checkCoreCourseExistence(prereq) == False:
                        message = "The prerequisite course code provided doesn't exist"
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
                            message = "The prerequisite code needs to first be added in the sequence"
                            return render_template("courseProgression.html", allCoreCourses=allCoreCourses,
                                                   largestSize=largestSize,
                                                   message=message, success=False, failure=True, values=request.form)


            print("** next sequence" + str(sequence))

            addIntoFlowchart(courseCode, sequence)
            print("** added course code into flowchart")


            for prereq in prerequisites:
                if prereq:
                    nextOrder = getOrderNumber()
                    addIntoPrerequisite(nextOrder,courseCode, prereq)

            print("** added course code into prerequisites")

            allCoreCourses = createCoreCourseDataDict()

            largestSize = 0

            for course in allCoreCourses:
                if len(course['prerequisites']) > largestSize:
                    largestSize = len(course['prerequisites'])

            message = "The course sequence was added successfully"
            return render_template("courseProgression.html", allCoreCourses=allCoreCourses,
                                   largestSize=largestSize,
                                   message=message, success=True, failure=False, values=dict())


        if request.method == 'POST' and buttonType == "saveBtn":
            print("clicked save button")
            print(parameters)

            courseCode = parameters['courseCode'].upper()
            oldCourseCode = parameters['oldCourseCode'].upper()

            oldPrerequisites = []

            oldCourse = dict()

            for course in allCoreCourses:
                if course['core_course_num'] == oldCourseCode:
                    oldCourse = copy.deepcopy(course)

            for i in range(len(oldCourse['prerequisites'])):
                oldPrerequisites.append(oldCourse['prerequisites'][i])

            prerequisites = []
            print(prerequisites)

            highestSequence = findHighestSequence()

            for col in prerequisite_col:
                if parameters[col].upper():
                    prerequisites.append(parameters[col].upper())

            if checkCoreCourseExistence(courseCode) == False:
                message = "The course code provided isn't a core course"
                return render_template("courseProgression.html", allCoreCourses=allCoreCourses, largestSize=largestSize,
                                       message=message, success=False, failure=True, values=request.form, updatedCourse=courseCode, rowClass="errorRow")

            if checkCoreCourseFlowchart(courseCode) == True and courseCode != oldCourseCode:
                message = "The course code is already in the sequence"
                return render_template("courseProgression.html", allCoreCourses=allCoreCourses,
                                       largestSize=largestSize,
                                       message=message, success=False, failure=True, values=request.form, updatedCourse=courseCode, rowClass="errorRow")

            if findCourseSequenceNumber(courseCode) < highestSequence and courseCode != oldCourseCode:
                message = "The course code cannot be edited as it comes before other progressions and would affect the display of flowcharts"
                return render_template("courseProgression.html", allCoreCourses=allCoreCourses,
                                   largestSize=largestSize,
                                   message=message, success=False, failure=True, values=dict(), updatedCourse=courseCode, rowClass="errorRow")

            if checkIfPrerequisite(courseCode) == True:
                message = "This course code cannot be edited as it's used as a prerequisite for another course"
                return render_template("courseProgression.html", allCoreCourses=allCoreCourses,
                                       largestSize=largestSize,
                                       message=message, success=False, failure=True, values=dict(), updatedCourse=courseCode, rowClass="errorRow")

            # check if the prerequisites are core courses
            for prereq in prerequisites:
                if prereq:

                    if checkCoreCourseExistence(prereq) == False:
                        message = "The prerequisite course code provided isn't a core course"
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
                        nextOrder = getOrderNumber()
                        addIntoPrerequisite(nextOrder, courseCode, prereq)

            allCoreCourses = createCoreCourseDataDict()

            message = "The progression was successfully updated"
            return render_template("courseProgression.html", allCoreCourses=allCoreCourses,
                                   largestSize=largestSize,
                                   message=message, success=True, failure=False, values=dict(), updatedCourse=courseCode, rowClass="updatedRow")




        if request.method == 'POST' and buttonType == "deleteBtn":

            print(parameters)
            print("clicked delete button")

            courseCode = parameters['courseCode'].upper()

            prerequisites = []

            for col in prerequisite_col:
                if parameters[col].upper():
                    prerequisites.append(parameters[col].upper())


            print(prerequisites)

            _sequenceNumber = findCourseSequenceNumber(courseCode)

            highestSequence = findHighestSequence()

            if _sequenceNumber < highestSequence:
                message = "This progression cannot be deleted as it comes before other progressions and would affect the display of flowcharts"
                return render_template("courseProgression.html", allCoreCourses=allCoreCourses,
                                   largestSize=largestSize,
                                   message=message, success=False, failure=True, values=dict(), updatedCourse=courseCode, rowClass="errorRow")

            if checkIfPrerequisite(courseCode) == True:
                message = "This progression cannot be deleted as it's used as a prerequisite for another course"
                return render_template("courseProgression.html", allCoreCourses=allCoreCourses,
                                       largestSize=largestSize,
                                       message=message, success=False, failure=True, values=dict(), updatedCourse=courseCode, rowClass="errorRow")

            print(len(prerequisites))

            if len(prerequisites) > 0:
                for prereq in prerequisites:
                    if prereq:
                        deleteFlowchart(courseCode)
                        deletePrerequisite(courseCode, prereq)
            else:
                deleteFlowchart(courseCode)


            allCoreCourses = createCoreCourseDataDict()

            message = "The progression was successfully deleted"
            return render_template("courseProgression.html", allCoreCourses=allCoreCourses,
                                   largestSize=largestSize,
                                   message=message, success=True, failure=False, values=dict())

        return render_template("courseProgression.html", allCoreCourses=allCoreCourses, largestSize=largestSize, message="", success=False, failure=False, values=dict())

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



def addIntoPrerequisite(order, courseCode, prereqCode):
    # >>> Setup MySQL Connection
    con = createConnection()

    query = f"""

            insert into core_course_prerequisites(`order`, core_course_num, prerequisite_num)
            values ({order}, '{courseCode}','{prereqCode}')
            ;

            """

    cursor = con.cursor()
    cursor.execute(query)
    con.commit()
    cursor.close()
    con.close()


def getSequenceNumber():
    con = createConnection()
    query = f"""
                SELECT count(*) FROM core_course_flowchart;
            """

    cursor = con.cursor()
    cursor.execute(query)
    rowCount = cursor.fetchone()
    count = rowCount[0]
    cursor.close()
    con.close()

    return count + 1


def getOrderNumber():
    con = createConnection()
    query = f"""
                SELECT count(*) FROM core_course_prerequisites;
            """

    cursor = con.cursor()
    cursor.execute(query)
    rowCount = cursor.fetchone()
    count = rowCount[0]
    cursor.close()
    con.close()


    return count + 1


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

def findHighestSequence():
    con = createConnection()
    query = f"""
                    SELECT sequence FROM core_course_flowchart
                    order by sequence desc
                    limit 1
                    ;
                """

    cursor = con.cursor()
    cursor.execute(query)
    row = cursor.fetchone()
    cursor.close()
    con.close()

    if row is None:
        return 0

    return row[0]


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

