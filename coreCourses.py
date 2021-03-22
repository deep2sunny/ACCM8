from flask import Blueprint, render_template, request, session, redirect, url_for
import sys
import MySQLdb as mdb1
import configparser
import os

coreCoursesBlueprint = Blueprint("coreCourses", __name__, static_folder="static", template_folder="template")

# http://localhost:5000/administrator/corecourses
@coreCoursesBlueprint.route("/administrator/corecourses", methods=['GET','POST'])
def coreCourses():

    # check if user is logged in
    if 'loggedin' in session:

        # check if user is coordinator or secretary
        if session['category'] == "coordinator" or session['category'] == "secretary":

            parameters = request.form.to_dict()

            allCoreCourses = readCourses()

            if request.method == 'POST' and "addBtn" in parameters:
                courseCode = parameters['courseCode'].upper()
                courseTitle = parameters['courseTitle']


                if checkCoreCourseExistence(courseCode) == True:
                    message = "The course code " + courseCode + " already exists"
                    return render_template("coreCourses.html", allCoreCourses=allCoreCourses,message=message, success=False, failure=True)

                addCourse(courseCode, courseTitle)
                allCoreCourses = readCourses()

                message = "The course was added successfully"
                return render_template("coreCourses.html", allCoreCourses=allCoreCourses, message=message, success=True, failure=False)

            # user confirms course deletion
            if request.method == 'POST' and "confirmDeleteBtn" in parameters:
                courseCode = parameters['courseDeleteInput'].upper()

                if checkCoreCourseFlowchart(courseCode) == True or checkCoreCoursePrerequisite(courseCode) == True:
                    message = "The course code " + courseCode + " cannot be deleted as it has other data associated with it"
                    return render_template("coreCourses.html", allCoreCourses=allCoreCourses, message=message, success=False,
                                           failure=True)

                deleteCourse(courseCode)
                allCoreCourses = readCourses()

                message = "The course was deleted successfully"
                return render_template("coreCourses.html", allCoreCourses=allCoreCourses, message=message, success=True, failure=False)

            # user confirms course edit
            if request.method == 'POST' and "confirmEditBtn" in parameters:
                oldCourseCode = parameters['oldCourseCode']
                courseCode = parameters['editCourseCodeInput'].upper()
                courseTitle = parameters['editCourseTitleInput']
                updateCourse(oldCourseCode, courseCode, courseTitle)
                allCoreCourses = readCourses()
                message = "The course information was successfully updated"
                return render_template("coreCourses.html", allCoreCourses=allCoreCourses, message=message, success=True,
                                       failure=False)




            return render_template("coreCourses.html", allCoreCourses=allCoreCourses, success=False, failure=False)

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


def readCourses():

    con = createConnection()

    cursor = con.cursor()

    # >>> fetch all core courses
    query = f"""SELECT * FROM core_course;"""
    cursor.execute(query)
    rows = cursor.fetchall()

    # Write all query rows into dictionary with column headers
    names = [d[0] for d in cursor.description]
    allCoreCourses = [dict(zip(names, row)) for row in rows]

    return allCoreCourses


def addCourse(courseCode, courseTitle):
    con = createConnection()
    cursor = con.cursor()

    # >>> fetch all core courses
    query = f"""INSERT INTO core_course(core_course_num, title) VALUES('{courseCode}','{courseTitle}');"""
    cursor.execute(query)
    con.commit()


def deleteCourse(courseCode):
    con = createConnection()

    cursor = con.cursor()

    # >>> fetch all core courses
    query = f"""DELETE FROM core_course
                WHERE core_course_num = '{courseCode}';"""
    cursor.execute(query)
    con.commit()


def updateCourse(oldCourseCode, courseCode, courseTitle):
    con = createConnection()

    cursor = con.cursor()

    query = f"""UPDATE core_course
            SET core_course_num = '{courseCode}', title = '{courseTitle}'
            WHERE core_course_num = '{oldCourseCode}';"""

    cursor.execute(query)
    con.commit()


def checkCoreCourseExistence(courseCode):
    con = createConnection()

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


def checkCoreCoursePrerequisite(courseCode):
    con = createConnection()
    query = f"""
                    SELECT count(*) FROM core_course_prerequisites WHERE core_course_num='{courseCode}';
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