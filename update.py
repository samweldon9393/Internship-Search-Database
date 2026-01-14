#!/usr/bin/env python3

import sys
import sqlite3
import getopt
from datetime import date

def usage(errno):
    print("Usage: ./update -c \"<company_name>\" -s \"<status>\"")
    sys.exit(errno)

def main():

    if len(sys.argv) < 2:
        usage(1)

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc:s:")
    except getopt.GetoptError as err:
        print(err)
        usage(2)

    company_list = None
    status       = None
    for o, a in opts:
        if o == "-h":
            usage(0)
        elif o == "-c":
            company_list = a 
        elif o == "-s":
            status = a
        else:
            assert False, "unhandled option"


    company = "%"
    for c in company_list:
        company += c 
        company += "%"

    today = date.today()
    date_str = f"{today.month}-{today.day}-{today.year}"

    conn = sqlite3.connect('applications.db')
    cursor = conn.cursor()

    cmpy = [company]
    print(cmpy)
    cursor.execute("""
    SELECT count(*) FROM applications WHERE company_name like ?
    """, cmpy)
    count = int(cursor.fetchone()[0])

    if count == 1:
        data = [status, company]
        cursor.execute("""
        UPDATE applications SET status = ? WHERE company_name like ?
        """, data)

        data[0] = date_str
        cursor.execute("""
        UPDATE applications SET status_date = ? WHERE company_name like ?
        """, data)

    else:
        cursor.execute("""
        SELECT application_id, company_name, position_title, department_or_team
        FROM applications 
        WHERE company_name like ?
        """, cmpy)

        rows = cursor.fetchall()

        app_id = 0
        for i in rows:
            is_job = input(f"{i}\nIs this the role you want to update? (y/n): ")
            if is_job == 'y':
                app_id = i[0]
                break

        data = [status, app_id]
        cursor.execute("""
        UPDATE applications SET status = ? WHERE application_id = ?
        """, data)

        data[0] = date_str
        cursor.execute("""
        UPDATE applications SET status_date = ? WHERE company_name like ?
        """, data)

    resp_date(cursor, company, date_str)

    conn.commit()

def resp_date(cursor, company, date_str):
    data = [company]
    cursor.execute("""
    SELECT 1 FROM applications WHERE company_name LIKE ? AND response_date is not null
    """, data)

    if cursor:
        row = cursor.fetchone()
        if not row:
            data = [date_str, company]
            cursor.execute("""
            UPDATE applications SET response_date = ? WHERE company_name like ?
            """, data)



if __name__=="__main__":
    main()
