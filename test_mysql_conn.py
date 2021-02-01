import sys
import MySQLdb as mdb1
import mysql.connector as mdb2


def test_mysqldb_conn_1():

    try:
        con = mdb1.connect(host='localhost', user='root', password='5Iodine3', database='accm', port=3306)
        cur = con.cursor()
        cur.execute("SELECT * FROM course")

        rows = cur.fetchall()

        print("\n\n ***** Printing number of rows in Table course using MySQL DB Connection 1 *****")

        print(len(rows))

        print("\n")

    except mdb1.Error as e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
        sys.exit(1)



def test_mysqldb_conn_2():

    try:
        con = mdb2.connect(host='localhost', user='root', password='5Iodine3', database='accm', port=3306)
        cursor = con.cursor()

        cursor.execute("SELECT * FROM course")

        rows = cursor.fetchall()

        print("\n ***** Printing number of rows Table course using MySQL DB Connection 2 *****")

        print(len(rows))

        print("\n")

    except mdb2.Error as e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
        sys.exit(1)



test_mysqldb_conn_1()

test_mysqldb_conn_2()


