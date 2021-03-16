import os
import csv
import mysql.connector
from configparser import ConfigParser

def inputCSV2DB(pVersion, cTerm, sLevel, fileName):

   print("call uploadGrade2DB in inputCSV", pVersion, cTerm, sLevel, fileName)
   mydb = mysql.connector.connect(host='localhost', user='root', password='root', database='accm')
   print("database connected")

   cursor = mydb.cursor()
   csv_data = csv.reader(open('./Upload/'+fileName, encoding='UTF-8-sig'))
   for row in csv_data:
      print("row ", row)
      if(row == []):
          continue;
      insertQuery = "INSERT INTO ac_grade_input(program_version, course_year, student_level, "+\
                    "term, program_code, program_name, course_level, student_num, student_fname, student_lname, student_email, prof_fname, prof_lname, course_num, course_title, "+\
                    "letter_grade, percent, fcomment, rcomment) VALUES('"+pVersion+"', '"+cTerm+"', '"+sLevel+"', "

      #print(insertQuery+"%s, %s, %s, %s, %s, %s, %s, '', %s, %s, %s, %s, %s, %s, %s, %s)", row)
      #cursor.execute(insertQuery+"%s, %s, %s, %s, %s, %s, %s, '', %s, %s, %s, %s, %s, %s, %s, %s)", row)
      print(
          insertQuery + "'" + row[0] + "', '" + row[1] + "', '" + row[2] + "', '" + row[3] + "', '" + row[4] + "', '" +
          row[5] + "', '" + row[6] + "', '" + "', '" + row[7] + "', '" + row[8] + "', '" + row[9] + "', '" + row[
              10] + "', '" + row[11].strip() + "', '" + row[12].replace(" ", "") + "', '" + row[13] + "', '" + row[
              14] + "')")
      cursor.execute(
          insertQuery + "'" + row[0].strip() + "', '" + row[1].strip() + "', '" + row[2].strip() + "', '" + row[3].strip() + "', '" + row[4].strip() + "', '" +
          row[5].strip() + "', '" + row[6].strip() + "', '" + "', '" + row[7].strip() + "', '" + row[8].strip() + "', '" + row[9].strip() + "', \"" + row[
              10].strip() + "\", '" + row[11].strip() + "', '" + row[12].replace(" ", "") + "', '" + row[13].strip() + "', '" + row[
              14].strip() + "')")

   print("insert program")
   #insert program
   cursor.execute('INSERT INTO program(code, name, program_version) SELECT distinct(program_code), program_name, program_version FROM ac_grade_input as a '+
                   'WHERE NOT EXISTS (SELECT * FROM program WHERE code=a.program_code AND program_version = a.program_version)')

   print("insert course")
   #insert course
   cursor.execute('INSERT INTO course(course_num, title, year) SELECT distinct(course_num), course_title, course_year FROM ac_grade_input as a '+
                  'WHERE NOT EXISTS (SELECT * FROM course WHERE course_num=a.course_num AND year=a.course_year)')

   print("insert coursemap")
   #insert coursemap
   cursor.execute('insert into coursemap(pid, cid, level, term) '+
                  'select program.pid, course.cid, a.course_level, a.term '+
                  'from ac_grade_input as a '+
                  'inner join program '+
                  'on(program.code = a.program_code and program.program_version = a.program_version) '+
                  'inner join course '+
                  'on (course.course_num = a.course_num and course.year = a.course_year) '+
                  'where not exists(select * from coursemap '+
                  'where pid = program.pid and cid = course.cid and course_level=a.course_level and term = a.term) '+
                  'group by program.pid, course.cid')

   print("insert student")
   #insert student
   cursor.execute('insert into student (student_num, fname, lname, level, email) '+
                  'select distinct(student_num), student_fname, student_lname, student_level, student_email '+
                  'from ac_grade_input as a '+
                  'where not exists(select * from student '+
                  'where student_num=a.student_num)')

   print("insert enrollment")
   #insert enrollment
   cursor.execute('insert into enrollment(sid, pid) '+
                  'select student.sid, program.pid '+
                  'from ac_grade_input as a '+
                  'inner join student '+
                     'on(student.student_num = a.student_num and student.level = a.student_level) '+
                  'inner join program '+
                     'on(program.code = a.program_code and program.program_version = a.program_version) '+
                  'where not exists(select * from enrollment '+
                     'where sid = student.sid and pid = program.pid) '+
                  'group by student.sid, program.pid')

   print("insert professor")
   #insert professor
   cursor.execute('insert into professor(fname, lname) '+
                  'select distinct(prof_fname), prof_lname '+
                  'from ac_grade_input as a '+
                  'where not exists(select * from professor '+
                  'where UPPER(fname)  = UPPER(a.prof_fname) and UPPER(lname) = UPPER(a.prof_lname));')

   print("insert teach")
   #insert teach
   cursor.execute('insert into teach(profid, mapid) '+
                  'select professor.profid, coursemap.mapid '+
                  'from ac_grade_input as a '+
                  'inner join professor '+
                  'on(UPPER(professor.fname) = UPPER(a.prof_fname) and UPPER(professor.lname) = UPPER(a.prof_lname)) '+
                  'inner join program '+
                  'on(program.code = a.program_code and program.program_version = a.program_version) '+
                  'inner join course '+
                  'on (course.course_num = a.course_num and course.year = a.course_year) '+
                  'inner join coursemap '+
                  'on(coursemap.pid = program.pid and coursemap.cid=course.cid) '+
                  'where not exists(select * from teach '+
                  'where profid = professor.profid and mapid = coursemap.mapid) '+
                  'group by professor.profid, coursemap.mapid;')

   print("insert grade")
   #insert grade
   cursor.execute('insert into grade(sid, mapid, letter_grade, percent, fcomment, rcomment) '+
                  'select student.sid, coursemap.mapid, a.letter_grade, a.percent, a.fcomment, a.rcomment '+
                  'from ac_grade_input as a '+
                  'inner join student '+
                  'on(student.student_num = a.student_num) '+
                  'inner join program '+
                  'on(program.code = a.program_code and program.program_version = a.program_version) '+
                  'inner join course '+
                  'on (course.course_num = a.course_num and course.year = a.course_year) '+
                  'inner join coursemap '+
                  'on(coursemap.pid = program.pid and coursemap.cid=course.cid) '+
                  'where not exists(select * from grade '+
                  'where sid = student.sid and mapid = coursemap.mapid) '+
                  'group by student.sid, coursemap.mapid;')


   print("insert prerequisite")

   #for each course, insert the prerequisite for 3002X program.
   #rule: parent, prerequisite
   prerequisiteRule=[('CST8250', ['CST8260']),
                     ('CST8253', ['CST8209', 'CST8279']),
                     ('CST8256', ['CST8253', 'CST8260']),
                     ('CST8257', ['CST8260', 'CST8209']),
                     ('CST8258', ['CST8253']),
                     ('ENL8720', ['ENL1813T']),
                     ('CST8259', ['CST8257']),
                     ('CST8265', ['CST8257']),
                     ('CST8267', ['CST8257']),
                     ('CST8268', ['CST8258'])
                     ]
   for rule in prerequisiteRule:
      parent = rule[0]
      prerequisite = rule[1]

      for preCourse in prerequisite:
        print(parent, preCourse)
        query = 'select mapid, course_num from coursemap inner join program using(pid) inner join course using(cid) where program_version="'+pVersion+'" and code="3002X" and course_num="'+parent+'"'
        cursor.execute(query)
        parentCourseMapIDs = cursor.fetchall()
        cursor.execute(
        'select mapid, course_num from coursemap inner join program using(pid) inner join course using(cid) where program_version="'+pVersion+'" and code="3002X" and course_num="'+preCourse+'"')
        prerequisiteMapIDs = cursor.fetchall()
        print(parentCourseMapIDs, prerequisiteMapIDs)

        for c in parentCourseMapIDs:
          for p in prerequisiteMapIDs:
              print("pre: ", c[0], p[0])
              cursor.execute('select count(*) from prerequisite where mapid =' + str(c[0]) + ' and prerequisite=' + str(p[0]) + ' ')
              count = cursor.fetchone()
              if not(count[0]):
                query = 'insert into prerequisite(mapid, prerequisite) values (' + str(c[0]) + ', ' + str(p[0]) + ')'
                cursor.execute(query)

   print("flowchart")
   cursor.execute("delete from flowchart")
   courseSequence = [('CST8260', 1), ('CST8209', 2), ('CST8279', 3), ('MAD9013', 4),('MAT8001C', 5), ('CST8300', 6), ('CST8250', 7), ('CST8253', 8), ('CST8254', 9), ('MAD9010', 10),
                     ('ENL1813T', 11),('CST8256', 13),('CST8257', 14),('CST8258', 15),('ENL8720', 16),('CST8259', 18),('CST8265', 19),('CST8267', 20), ('CST8268', 21)]
   for seq in courseSequence:
       cnum = seq[0]
       seq = seq[1]
       query = "select mapid from coursemap inner join course using(cid) inner join program using(pid) where course_num = '"+cnum+"' and program_version = '"+pVersion +"' and code = '3002X'"
       cursor.execute(query)
       mapIDs = cursor.fetchall()
       for mapID in mapIDs:
           id = mapID[0]
           query = 'insert into flowchart(mapid, sequence) values (' + str(id) + ', ' + str(seq) + ')'
           cursor.execute(query)

   print("insertion done.")

   print("delete ac_grade_input")
   #insert grade
   cursor.execute('delete from ac_grade_input')

   mydb.commit()
   cursor.close()

   print("DONE")

