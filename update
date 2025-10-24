#!/usr/bin/env python3

import sys
import sqlite3
from datetime import date


def main():
    if len(sys.argv) != 3:
        print("Usage: ./update <company_name> <status>")
        sys.exit(1)

    company = sys.argv[1]
    status = sys.argv[2]
    
    today = date.today()
    date_str = f"{today.month}-{today.day}-{today.year}"

    conn = sqlite3.connect('applications.db')
    cursor = conn.cursor()

    cmpy = [company]
    cursor.execute("""
    SELECT count(*) FROM applications WHERE company_name = ?
    """, cmpy)
    count = int(cursor.fetchone()[0])

    if count == 1:
        data = [status, company]
        cursor.execute("""
        UPDATE applications SET status = ? WHERE company_name = ?
        """, data)

        data[0] = date_str
        cursor.execute("""
        UPDATE applications SET status_date = ? WHERE company_name = ?
        """, data)

    else:
        cursor.execute("""
        SELECT application_id, company_name, position_title, department_or_team
        FROM applications 
        WHERE company_name = ?
        """, cmpy)

        rows = cursor.fetchall()

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
        UPDATE applications SET status_date = ? WHERE company_name = ?
        """, data)

    conn.commit()

if __name__=="__main__":
    main()
