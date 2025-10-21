#!/usr/bin/env python3

import sqlite3

def main():
    conn = sqlite3.connect('applications.db')
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM applications;")
    cnt = cursor.fetchone()
    print(cnt[0])
    conn.commit()

if __name__=='__main__':
    main()
