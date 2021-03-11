from flask import Blueprint, render_template, request
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

    parameters = request.form.to_dict()
    _list = list(parameters.keys())

    buttonType = checkButtonType(parameters)

    allCoreCourses = createCoreCourseDataDict()

    largestSize = 0

    for course in allCoreCourses:
        if len(course['prerequisites']) > largestSize:
            largestSize = len(course['prerequisites'])

    if request.method == 'POST' and buttonType == "deleteBtn":
        print("clicked delete button")
        print(parameters)

    if request.method == 'POST' and buttonType == "editBtn":
        print("clicked edit button")
        print(parameters)

    if request.method == 'POST' and buttonType == "addBtn":
        print("clicked add button")
        print(parameters)

    return render_template("courseProgression.html", allCoreCourses=allCoreCourses, largestSize=largestSize, message="", success=False, failure=False)



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



# Creates a dictionary containing course, sequence and prerequisite information
def createCoreCourseDataDict():
    # >>> Setup MySQL Connection
    con = createCursor()
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
        course['prerequisite_1'] = ""
        course['prerequisite_2'] = ""
        course['prerequisite_3'] = ""
        course['prerequisite_4'] = ""
        course['prerequisite_5'] = ""
        course['prerequisites'] = []

        prerequisiteColumns = ['prerequisite_1','prerequisite_2','prerequisite_3','prerequisite_4','prerequisite_5']

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