from flask import Blueprint, render_template, request, session, redirect, url_for
import sys
import MySQLdb as mdb1
from flask_mysqldb import MySQL
from app import app

courseProgressionBlueprint = Blueprint("courseProgression", __name__, static_folder="static", template_folder="template")


def checkButtonType(dict):
    allKeys = list(dict.keys())

    for key in allKeys:

        if "deleteBtn" in key:
            return "deleteBtn"
        if "editBtn" in key:
            return "editBtn"
        if "addBtn" in key:
            return "addBtn"

    return ""

@courseProgressionBlueprint.route("/administrator/courseprogression", methods=['GET','POST'])
def courseProgression():

    global con

    x=5

    # check if user is logged in
    #if 'loggedin' in session:
    if x == 5:

        con = createConnection()

        parameters = request.form.to_dict()
        _list = list(parameters.keys())

        buttonType = checkButtonType(parameters)

        allCoreCourses = createCoreCourseDataDict()

        largestSize = 0

        for course in allCoreCourses:
            if len(course['prerequisites']) > largestSize:
                largestSize = len(course['prerequisites'])



        if request.method == 'POST' and buttonType == "addBtn":

            print("clicked add button")

            sequence = parameters['sequence'].upper()
            courseCode = parameters['courseCode'].upper()
            prereqCode1 = parameters['prereqCode1'].upper()
            prereqCode2 = parameters['prereqCode2'].upper()
            prereqCode3 = parameters['prereqCode3'].upper()
            prereqCode4 = parameters['prereqCode4'].upper()
            prereqCode5 = parameters['prereqCode5'].upper()

            prerequisite_col = ['prereqCode1', 'prereqCode2', 'prereqCode3', 'prereqCode4', 'prereqCode5']

            prerequisites = []

            for col in prerequisite_col:
                if parameters[col].upper():
                    prerequisites.append(parameters[col].upper())

            print(parameters)

            if checkCoreCourseExistence(courseCode) == False:
                message = "The course code provided isn't a core course"
                return render_template("courseProgression.html", allCoreCourses=allCoreCourses, largestSize=largestSize,
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


        if request.method == 'POST' and buttonType == "editBtn":
            print("clicked edit button")
            print(parameters)


        if request.method == 'POST' and buttonType == "deleteBtn":

            print(parameters)
            print("clicked delete button")

            prerequisite_col = ['prerequisite_1','prerequisite_2','prerequisite_3','prerequisite_4','prerequisite_5']

            courseCode = parameters['courseCode'].upper()



            prerequisites = []

            for col in prerequisite_col:
                if parameters[col].upper():
                    prerequisites.append(parameters[col].upper())


            print(prerequisites)

            if findCourseSequenceNumber(courseCode) < len(allCoreCourses):
                message = "This progression cannot be deleted as it comes before other progressions and would affect the display of flowcharts"
                return render_template("courseProgression.html", allCoreCourses=allCoreCourses,
                                   largestSize=largestSize,
                                   message=message, success=False, failure=True, values=dict())

            if checkIfPrerequisite(courseCode) == True:
                message = "This progression cannot be deleted as it's used as a prerequisite for another course"
                return render_template("courseProgression.html", allCoreCourses=allCoreCourses,
                                       largestSize=largestSize,
                                       message=message, success=False, failure=True, values=dict())

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


def createConnection():
    mysql = MySQL(app)

    try:
        con = mdb1.connect(host=mysql.app.config['MYSQL_HOST'],
                           user=mysql.app.config['MYSQL_USER'],
                           password=mysql.app.config['MYSQL_PASSWORD'],
                           #database=mysql.app.config['MYSQL_DB'],
                           database="accm_test",
                           port=mysql.app.config['MYSQL_PORT'])


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

    return allCoreCourses



def checkCoreCourseExistence(courseCode):

    global con

    query = f"""

                    SELECT count(*) FROM core_course
                    where core_course_num = '{courseCode}';

                """

    cursor = con.cursor()
    cursor.execute(query)
    rowCount = cursor.fetchone()
    count = rowCount[0]

    if count > 0:
        return True

    return False


def checkCoreCourseFlowchart(courseCode):
    global con
    query = f"""

                        SELECT count(*) FROM core_course_flowchart
                        where core_course_num = '{courseCode}';

                    """

    cursor = con.cursor()
    cursor.execute(query)
    rowCount = cursor.fetchone()
    count = rowCount[0]


    if count > 0:
        return True

    return False


def addIntoFlowchart(courseCode, sequence):
    global con
    query = f"""

            insert into core_course_flowchart(core_course_num, sequence) values('{courseCode}', {sequence})

            """

    cursor = con.cursor()
    cursor.execute(query)
    con.commit()



def addIntoPrerequisite(order, courseCode, prereqCode):
    global con
    query = f"""

            insert into core_course_prerequisites(`order`, core_course_num, prerequisite_num)
            values ({order}, '{courseCode}','{prereqCode}')
            ;

            """

    cursor = con.cursor()
    cursor.execute(query)
    con.commit()



def getSequenceNumber():
    global con
    query = f"""
                SELECT count(*) FROM core_course_flowchart;
            """

    cursor = con.cursor()
    cursor.execute(query)
    rowCount = cursor.fetchone()
    count = rowCount[0]


    return count + 1


def getOrderNumber():
    global con
    query = f"""
                SELECT count(*) FROM core_course_prerequisites;
            """

    cursor = con.cursor()
    cursor.execute(query)
    rowCount = cursor.fetchone()
    count = rowCount[0]


    return count + 1


def checkIfPrerequisite(courseCode):
    global con
    query = f"""
                    SELECT count(*) FROM core_course_prerequisites WHERE prerequisite_num='{courseCode}';
                """

    cursor = con.cursor()
    cursor.execute(query)
    rowCount = cursor.fetchone()
    count = rowCount[0]

    if count > 0:
        return True

    return False


def deletePrerequisite(courseCode,prerequisite):
    global con

    query = f""" 
            DELETE FROM core_course_prerequisites 
            WHERE core_course_num='{courseCode}' 
            AND prerequisite_num='{prerequisite}'
            """
    cursor = con.cursor()
    cursor.execute(query)
    con.commit()


def deleteFlowchart(courseCode):
    global con

    query = f""" 
                DELETE FROM core_course_flowchart 
                WHERE core_course_num='{courseCode}' 
                """
    cursor = con.cursor()
    cursor.execute(query)
    con.commit()

def findCourseSequenceNumber(courseCode):
    global con
    query = f"""
                SELECT sequence FROM accm_test.core_course_flowchart
                WHERE core_course_num = "{courseCode}"
                ;
            """

    cursor = con.cursor()
    cursor.execute(query)
    row = cursor.fetchone()
    sequence = row[0]

    return sequence