import csv
import mysql.connector
import os
from pathlib import Path
import shutil
import datetime


def inputCSV2DB(fileName):
    mydb = mysql.connector.connect(host='localhost', user='root', password='', database='accm')
    cursor = mydb.cursor()
    success_records_count = 0
    error_records_count = 0
    destination_path = ''

    with open('./Upload/' + fileName, encoding='UTF-8-sig') as csv_file:
        csv_data = csv.DictReader(csv_file)

        with open('./Upload/csvErrors.csv', 'w') as error_file:

            error_file_created = False
            field_names = csv_data.fieldnames
            csv_writer = csv.DictWriter(error_file, fieldnames=field_names)
            csv_writer.writeheader()

            for row in csv_data:

                if not row:
                    continue

                pVersion = 'IAWD'
                insertQuery = "INSERT INTO ac_grade_input(program_version, course_year, student_level, " \
                              "term, program_code, program_name, course_level, student_num, student_fname, " \
                              "student_lname, student_email, prof_fname, prof_lname, course_num, course_title," \
                              " letter_grade, percent, fcomment, rcomment) VALUES("

                try:
                    cursor.execute(
                        insertQuery + "'"
                        + pVersion + "', '"
                        + row['Term'].strip() + "', '"
                        + "', '"
                        + row['Term'].strip() + "', '"
                        + row['Program Code'].strip() + "', '"
                        + row['Program Name'].strip() + "', '"
                        + row['Level'].strip() + "', '"
                        + row['Student Number'].strip() + "', '"
                        + row['Student First Name'].strip().replace("'", "") + "', '"
                        + row['Student Last Name'].strip().replace("'", "") + "', '"
                        + "', '"
                        + row['Faculty First Name'].strip() + "', '"
                        + row['Faculty Last Name'].strip() + "', '"
                        + row['Course Number'].strip() + "', \""
                        + row['Course Title'].strip().replace("'", "") + "\", '"
                        + row['Letter Grade'].strip() + "', '"
                        + row['%'].replace(" ", "") + "', '"
                        + row['Faculty Comment'].strip() + "', '"
                        + row['Reviewer Comment'].strip() + "')")


                    if cursor.rowcount:
                        success_records_count += cursor.rowcount

                except Exception as e:
                    csv_writer.writerow(row)
                    error_file_created = True
                    error_records_count += 1

        print("CSV Records Count = {}".format(success_records_count))

        if error_file_created:
            date_time = datetime.datetime.now().strftime("%d-%b-%Y %I_%M_%S %p")
            destination_path = os.path.join(str(Path.home()), "Desktop\\CSV Errors " + date_time + " .csv")
            shutil.move('./Upload/csvErrors.csv', destination_path)
            print("CSV Error Records Count = {}".format(error_records_count))
        else:
            print('No errors were found in the csv file upload')
            print("Deleting error file from application")
            os.remove('./Upload/csvErrors.csv')

        # insert program
        print("Inserting data into program table")
        cursor.execute(
            'INSERT INTO program(code, name, program_version) '
            'SELECT distinct(program_code), program_name, program_version '
            'FROM ac_grade_input as a WHERE NOT EXISTS '
            '(SELECT * FROM program WHERE code = a.program_code AND program_version = a.program_version)')

        # insert course
        print("Inserting data into course table")
        cursor.execute('SELECT distinct(course_num), course_title FROM ac_grade_input as a '
                       'WHERE NOT EXISTS (SELECT * FROM course WHERE course_num = a.course_num )')
        new_courses = cursor.fetchall()
        print("New Courses Record Count = {}".format(cursor.rowcount))

        cursor.execute('SELECT * FROM core_course')
        core_courses = cursor.fetchall()

        for new_course in new_courses:
            print("New Course: {}".format(new_course))
            core = False
            core_course_code = ''
            core_course_description = ''
            for core_course in core_courses:
                if new_course[0] == core_course[0]:
                    core = True
                    core_course_code = core_course[0]
                    core_course_description = core_course[1]
                    break
            if core:
                cursor.execute("INSERT INTO course(course_num, title, core_course) "
                               "VALUES('" + core_course_code + "', '" + core_course_description + "', True)")
            else:
                cursor.execute("INSERT INTO course(course_num, title, core_course) "
                               "VALUES('" + new_course[0] + "', '" + new_course[1] + "', False)")

        # insert coursemap
        print("Inserting data into coursemap table")
        cursor.execute('INSERT INTO coursemap(pid, cid, level, term) '
                       'SELECT program.pid, course.cid, a.course_level, a.term '
                       'FROM ac_grade_input as a '
                       'INNER JOIN program '
                       'on(program.code = a.program_code and program.program_version = a.program_version) '
                       'INNER JOIN course '
                       'on (course.course_num = a.course_num) '
                       'WHERE NOT EXISTS (SELECT * FROM coursemap '
                       'WHERE pid=program.pid and cid = course.cid and course_level=a.course_level and term=a.term)'
                       'GROUP BY program.pid, course.cid')

        # insert student
        print("Inserting data into student table")
        cursor.execute('INSERT INTO student (student_num, fname, lname, level, email) '
                       'SELECT DISTINCT(student_num), student_fname, student_lname, student_level, student_email '
                       'from ac_grade_input as a '
                       'WHERE NOT EXISTS (SELECT * from student WHERE student_num = a.student_num)')
        cursor.execute('SELECT count(DISTINCT student_num) from ac_grade_input')
        new_students = cursor.fetchone()
        result = new_students[0]
        students_count = int(result)
        print("Students Count: {}".format(students_count))

        # insert enrollment
        print("Inserting data into enrollment table")
        cursor.execute('INSERT INTO enrollment(sid, pid) '
                       'SELECT student.sid, program.pid '
                       'FROM ac_grade_input as a '
                       'INNER JOIN student '
                       'on(student.student_num = a.student_num and student.level = a.student_level) '
                       'INNER JOIN program '
                       'on(program.code = a.program_code and program.program_version = a.program_version) '
                       'WHERE NOT EXISTS(SELECT * from enrollment '
                       'WHERE sid = student.sid and pid = program.pid) '
                       'GROUP BY student.sid, program.pid')

        # insert professor
        print("Inserting data into professor table")
        cursor.execute('INSERT INTO professor(fname, lname) '
                       'SELECT DISTINCT(prof_fname), prof_lname '
                       'FROM ac_grade_input as a '
                       'WHERE NOT EXISTS(select * from professor '
                       'WHERE UPPER(fname) = UPPER(a.prof_fname) and UPPER(lname) = UPPER(a.prof_lname))')

        # insert teach
        print("Inserting data into teach table")
        cursor.execute('INSERT INTO teach(profid, mapid) '
                       'SELECT professor.profid, coursemap.mapid '
                       'FROM ac_grade_input as a '
                       'INNER JOIN professor '
                       'on(UPPER(professor.fname) = UPPER(a.prof_fname) '
                       'and UPPER(professor.lname) = UPPER(a.prof_lname)) '
                       'INNER JOIN program '
                       'on(program.code = a.program_code and program.program_version = a.program_version) '
                       'INNER JOIN course '
                       'on (course.course_num = a.course_num) '
                       'INNER JOIN coursemap '
                       'on(coursemap.pid = program.pid and coursemap.cid=course.cid) '
                       'WHERE NOT EXISTS(SELECT * from teach '
                       'WHERE profid = professor.profid and mapid = coursemap.mapid) '
                       'GROUP BY professor.profid, coursemap.mapid')

        # insert grade
        print("Inserting data into grade table")
        cursor.execute('INSERT INTO grade(sid, mapid, letter_grade, percent, fcomment, rcomment) '
                       'SELECT student.sid, coursemap.mapid, a.letter_grade, a.percent, a.fcomment, a.rcomment '
                       'FROM ac_grade_input as a '
                       'INNER JOIN student '
                       'on(student.student_num = a.student_num) '
                       'INNER JOIN program '
                       'on(program.code = a.program_code and program.program_version = a.program_version) '
                       'INNER JOIN course '
                       'on (course.course_num = a.course_num) '
                       'INNER JOIN coursemap '
                       'on(coursemap.pid = program.pid and coursemap.cid=course.cid) '
                       'WHERE NOT EXISTS(SELECT * from grade '
                       'WHERE sid = student.sid and mapid = coursemap.mapid) '
                       'GROUP BY student.sid, coursemap.mapid')

        # insert prerequisite
        print("Inserting data into prerequisite table")
        cursor.execute('SELECT DISTINCT(core_course_num) FROM core_course_prerequisites ORDER BY core_course_num')
        courses = cursor.fetchall()

        cursor.execute('SELECT core_course_num, prerequisite_num '
                       'FROM core_course_prerequisites '
                       'ORDER BY core_course_num, prerequisite_num')
        courses_and_prerequisites = cursor.fetchall()

        prerequisite_rule = []

        for course in courses:
            prerequisite_list = []
            for courses in courses_and_prerequisites:
                if course[0] == courses[0]:
                    prerequisite_list.append(courses[1])
            add_list_into_tuple = (prerequisite_list,)
            prerequisite_tuple = course + add_list_into_tuple
            prerequisite_rule.append(prerequisite_tuple)

        # for each course, insert the prerequisite for 3002X program.
        # rule: parent, prerequisite
        for rule in prerequisite_rule:
            parent = rule[0]
            prerequisite = rule[1]

            for preCourse in prerequisite:
                cursor.execute('SELECT mapid, course_num from coursemap '
                               'INNER JOIN program using(pid) '
                               'INNER JOIN course using(cid) '
                               'WHERE program_version="'+pVersion+'" and code="3002X" and course_num="'+parent+'"')
                parentCourseMapIDs = cursor.fetchall()
                cursor.execute('SELECT mapid, course_num from coursemap '
                               'INNER JOIN program using(pid) '
                               'INNER JOIN course using(cid) '
                               'WHERE program_version="'+pVersion+'" and code="3002X" and course_num="'+preCourse+'"')
                prerequisiteMapIDs = cursor.fetchall()

                for c in parentCourseMapIDs:
                    for p in prerequisiteMapIDs:
                        print("pre: ", c[0], p[0], c[1], p[1])
                        cursor.execute('SELECT count(*) from prerequisite '
                                       'WHERE mapid =' + str(c[0]) + ' and prerequisite=' + str(p[0]) + ' ')
                        count = cursor.fetchone()
                        if not (count[0]):
                            cursor.execute('INSERT INTO prerequisite(mapid, prerequisite) '
                                           'VALUES (' + str(c[0]) + ', ' + str(p[0]) + ')')

        # insert flowchart
        print("Inserting data into flowchart table")
        cursor.execute("delete from flowchart")

        cursor.execute('SELECT * FROM core_course_flowchart ORDER BY sequence')
        courseSequence = cursor.fetchall()

        for seq in courseSequence:
            cnum = seq[0]
            seq = seq[1]
            cursor.execute("SELECT mapid FROM coursemap "
                           "INNER JOIN course using(cid) "
                           "INNER JOIN program using(pid) "
                           "where course_num = '"+cnum+"' and program_version = '"+pVersion+"' and code = '3002X'")
            mapIDs = cursor.fetchall()
            for mapID in mapIDs:
                id = mapID[0]
                query = 'INSERT INTO  flowchart(mapid, sequence) VALUES (' + str(id) + ', ' + str(seq) + ')'
                cursor.execute(query)

        print("Completed populating all the tables")

        print("Deleting records from table ac_grade_input")
        cursor.execute('delete from ac_grade_input')

        mydb.commit()
        cursor.close()

    print("Deleting uploaded CSV file from application")
    os.remove('./Upload/' + fileName)

    print("DONE")

    return success_records_count, students_count, error_records_count, destination_path
