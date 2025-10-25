#!/usr/bin/env python3

import sqlite3
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns

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

def main():
    conn = sqlite3.connect("applications.db")

    #apps_over_time(conn)
    apps_by_industry_and_status(conn)


if __name__=='__main__':
    main()
