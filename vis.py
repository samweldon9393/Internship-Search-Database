#!/usr/bin/env python3

import sys
import sqlite3
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
from enum import Enum

class Vis(Enum):
    apps_over_time = 1
    apps_by_industry_and_status = 2
    app_outcomes = 3

def apps_over_time(conn):
    df = pd.read_sql_query("SELECT application_date, status FROM applications", conn)
    df['application_date'] = pd.to_datetime(df['application_date'])
    df['day'] = df['application_date'].dt.to_period('D')
    apps_per_month = df.groupby(['day', 'status']).size().unstack(fill_value=0)

    apps_per_month.plot(kind='area', stacked=True, figsize=(10,6))
    plt.title("Applications by Status Over Time")
    plt.xlabel("Month")
    plt.ylabel("Number of Applications")
    plt.show()

def apps_by_industry_and_status(conn):
    df = pd.read_sql_query("""
        SELECT c.industry, a.status, COUNT(*) as num_apps
        FROM applications a 
        JOIN companies c 
            ON a.company_name = c.company_name 
        GROUP BY c.industry, a.status;
        """, conn)

    p = df.pivot(index="industry", columns="status", values="num_apps")
    sns.heatmap(p, annot=True)
    plt.title("Applications by Industry and Status")
    plt.show()

def app_outcomes(conn):
    df = pd.read_sql_query("""
        SELECT status
        FROM applications 
        """, conn)
    sns.countplot(x='status', data=df, order=df['status'].value_counts().index)
    plt.title("Application Outcomes")
    plt.xlabel("Status")
    plt.ylabel("Count")
    plt.show()


def main():
    conn = sqlite3.connect("applications.db")


    print("1: Applications Over Time")
    print("2: Applications by Industry and Status Heat Map")
    print("3: Application Outcomes")
    vis = input("Which visualization to view? Enter: ")
    try:
        vis = int(vis)
    except:
        print("Invalid input (must be integer)")
        sys.exit(1)

    match vis:
        case Vis.apps_over_time.value:
            apps_over_time(conn)
        case Vis.apps_by_industry_and_status.value:
            apps_by_industry_and_status(conn)
        case Vis.app_outcomes.value:
            app_outcomes(conn)
        case _:
            print("Invalid input (must be 1-3)")
            sys.exit(2)


if __name__=='__main__':
    main()
