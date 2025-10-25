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
    event_companies = 5

def applications(cursor, date):
    cursor.execute("SELECT count(*) FROM applications;")
    app_id = int(cursor.fetchone()[0]) + 1
    company_name = input("Enter company name: ")
    position = input("Enter position title: ")
    department = input("Enter department or team: ")
    location = input("Enter location: ")
    app_date = date 
    salary = float(input("Enter salary (float): "))
    status = "Applied"
    status_date = date 
    posting_url = input("Enter job posting url: ")
    where_applied = input("Enter where applied: ")
    resume = input("Enter resume version: ")
    referral = input("Enter referral name: ")
    if referral == "":
        referral = None
    interview_date = None 
    follow_up_date = None 
    offer_details = None 
    notes = input("Enter notes: ")
    if notes == "":
        notes = None
    last_updated = date 
    start_date = input("Enter start date: ")
    if start_date == "":
        start_date = "06-01-2025"
    end_date = input("Enter end date: ")
    if end_date == "":
        end_date = "08-01-2025"
    job_board = input("Enter job board: ")

    data = [ app_id, company_name, position, department, location, app_date,
            salary, status, start_date, posting_url, where_applied, resume,
            referral, interview_date, follow_up_date, offer_details, notes,
            last_updated, start_date, end_date, job_board ]
    assert len(data) == 21, "Data invalid"

    cursor.execute("""
    INSERT INTO applications VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, data)


def companies(cursor, date):
    company_name = input("Enter company name: ")
    if company_name == "":
        print("Company name cannot be null")
    industry = input("Enter industry: ")
    headquarters = input("Enter headquarters location: ")
    size = input("Enter size (small, medium, large): ")
    website = input("Enter website url: ")
    careers_page = input("Enter careers page url: ")
    contact_email = input("Enter contact email: ")
    contact_person = input("Enter contact person name: ")
    notes = input("Enter notes: ")
    is_target_str = input("Is target? (y/n): ")
    is_target = False
    if is_target_str == "y":
        is_target = True
    last_updated = date

    data = [ company_name, industry, headquarters, size, website, careers_page,
            contact_email, contact_person, notes, is_target, last_updated ]
    assert len(data) == 11, "Data invalid"

    cursor.execute("""
    INSERT INTO companies VALUES(?,?,?,?,?,?,?,?,?,?,?)
    """, data)

def contacts(cursor, date):
    contact_name = input("Enter contact name: ")
    if contact_name == "":
        print("Contact name cannot be null")
        sys.exit(1)
    company_name = input("Enter company name: ")
    linkedin= input("Enter LinkedIn: ")
    email = input("Enter email: ")
    phone_number = input("Enter phone_number: ")
    if phone_number != "":
        try:
            phone_number = int(phone_number)
        except:
            print("Invalid phone number")
            sys.exit(1)
    last_contacted = input("Enter last contacted date (\'DD-MM-YYYY\' or t for today): ")
    if last_contacted == "t":
        last_contacted = date 
    where_met = input("Where did we meet?: ")

    data = [ contact_name, company_name, linkedin, email, phone_number,
            last_contacted, where_met ]
    assert len(data) == 7, "Data invalid"

    cursor.execute("""
    INSERT INTO contacts VALUES(?,?,?,?,?,?,?)
    """, data)


def events(cursor, date):
    cursor.execute("SELECT count(*) FROM events;")
    event_id = int(cursor.fetchone()[0]) + 1

    event_name = input("Enter event name: ")
    if event_name == "":
        print("Event name cannot be null")
        sys.exit(1)

    event_date = input("Enter event date (\'DD-MM-YYYY\' or t for today): ")
    if event_date == "t":
        event_date = date 

    notes = input("Enter notes: ")
    contact_person = input("Enter contact person name: ")
    website = input("Enter event website url: ")

    data = [ event_id, event_name, event_date, notes, contact_person, website ]
    assert len(data) == 6, "Data invalid"

    cursor.execute("""
    INSERT INTO events VALUES(?,?,?,?,?,?)
    """, data)

def event_companies(cursor):
    keyword = "%" + input("Keyword search on event name: ") + "%"
    cursor.execute("SELECT event_id, event_name FROM events WHERE event_name LIKE ?", [keyword])

    event_id = -1
    for row in cursor:
        print(f"Matches: {row[1]}")
        response = input("Is this the event? (y/n): ")
        if response == "y":
            event_id = row[0]

    if event_id == -1:
        print("No match")
        sys.exit(1)

    print("Enter companies, they must be from this list: ")
    cursor.execute("SELECT company_name FROM companies;")
    companies_in_db = set([row[0] for row in cursor])
    print(companies_in_db)

    companies = []
    company_name = ""
    while company_name != "D":
        company_name = input("Enter company name (D when done): ")
        if company_name not in companies_in_db and company_name != "D":
            print("Not in database")
        else:
            companies.append(company_name)

    for company in companies:
        values = [event_id, company]
        cursor.execute("INSERT INTO event_companies VALUES (?, ?)",
                       values)


def main():
    print("1: applications")
    print("2: companies")
    print("3: contacts")
    print("4: events")
    print("5: event_companies")
    table = input("Insert into which table? Enter: ")
    try:
        table = int(table)
    except:
        print("Invalid input (must be integer)")
        sys.exit(1)

    conn = sqlite3.connect('applications.db')
    cursor = conn.cursor()

    today = date.today()
    date_str = f"{today.month}-{today.day}-{today.year}"

    match table:
        case Table.applications.value:
            applications(cursor, date_str)
        case Table.companies.value:
            companies(cursor, date_str)
        case Table.contacts.value:
            contacts(cursor, date_str)
        case Table.events.value:
            events(cursor, date_str)
        case Table.event_companies.value:
            event_companies(cursor)
        case _:
            print("Invalid input (must be 1-4)")
            sys.exit(2)
    
    conn.commit()

if __name__=="__main__":
    main()
