#!/usr/bin/env python3

import sys
import sqlite3
from datetime import date
from enum import Enum

class Table(Enum):
    applications = 1
    companies = 2
    contacts = 3 
    events = 4

def applications():
    pass

def companies():
    pass

def contacts():
    pass

def events():
    pass

def main():
    print("1: applications")
    print("2: companies")
    print("3: contacts")
    print("4: events")
    table = input("Insert into which table? Enter:")
    try:
        table = int(table)
    except:
        print("Invalid input")
        sys.exit(1)

    conn = sqlite3.connect('applications.db')
    cursor = conn.cursor()

    today = date.today()
    date_str = f"\'{today.month}-{today.day}-{today.year}\'"

    match table:
        case 1:
            application(cursor)
        case 2:
            companies(cursor)
        case 3:
            contacts(cursor)
        case 4:
            events(cursor)
        case _:
            print("Invalid input")
            sys.exit(2)

if __name__=="__main__":
    main()
